#!/usr/bin/env python3
import gzip
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "apps.json"
OUTPUT = ROOT / "public"


def fail(msg: str) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(1)


def ensure_tools() -> None:
    for tool in ["dpkg-scanpackages", "apt-ftparchive"]:
        if shutil.which(tool) is None:
            fail(f"Required tool not found: {tool}")


def load_manifest() -> dict:
    if not MANIFEST.exists():
        fail(f"Manifest not found: {MANIFEST}")
    with MANIFEST.open("r", encoding="utf-8") as fh:
        return json.load(fh)


import urllib.request

def copy_package(pkg: dict, pool_root: Path) -> Path:
    safe_name = re.sub(r"[^A-Za-z0-9.+-]+", "-", pkg["name"])
    safe_version = re.sub(r"[^A-Za-z0-9.+-]+", "-", str(pkg["version"]))
    dest_dir = pool_root / safe_name / safe_version
    dest_dir.mkdir(parents=True, exist_ok=True)

    if "url" in pkg:
        url = pkg["url"]
        filename = url.split("/")[-1]
        dest_path = dest_dir / filename
        print(f"Downloading package from URL: {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp, open(dest_path, "wb") as out:
            shutil.copyfileobj(resp, out)
        return dest_path

    source = (ROOT / pkg["file"]).resolve()
    if not source.exists():
        fail(f"Package file not found: {source}")

    dest_path = dest_dir / source.name
    shutil.copy2(source, dest_path)
    return dest_path


def write_override_file(manifest: dict, output_dir: Path) -> None:
    seen: set[str] = set()
    lines: list[str] = []
    for pkg in manifest.get("packages", []):
        name = pkg["name"]
        if name in seen:
            continue
        seen.add(name)
        lines.append(f"{name} optional utils")
    (output_dir / "override").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def sign_release(output_dir: Path, release_file: Path) -> None:
    if shutil.which("gpg") is None:
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        env = os.environ.copy()
        env["GNUPGHOME"] = tmpdir
        key_id = "AYAS OS Repo <ayascellsoftware@gmail.com>"
        subprocess.run(
            ["gpg", "--batch", "--yes", "--pinentry-mode", "loopback", "--passphrase", "", "--quick-generate-key", key_id, "ed25519", "sign", "0"],
            check=True,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["gpg", "--batch", "--yes", "--armor", "--output", str(release_file.with_suffix(release_file.suffix + ".gpg")), "--detach-sign", str(release_file)],
            check=True,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["gpg", "--batch", "--yes", "--clearsign", "--output", str(release_file.parent / "InRelease"), str(release_file)],
            check=True,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["gpg", "--batch", "--armor", "--export", key_id],
            check=True,
            env=env,
            stdout=(output_dir / "RepoKey.asc").open("w", encoding="utf-8"),
            stderr=subprocess.DEVNULL,
        )


def write_index_html(manifest: dict, output_dir: Path, pkg_links: list[tuple[str, str, str]]) -> None:
    rows = "".join(
        f"<tr><td>{html.escape(pkg_name)}</td><td>{html.escape(version)}</td><td><a href=\"{html.escape(link)}\">{html.escape(link)}</a></td></tr>"
        for pkg_name, version, link in pkg_links
    )
    suite = manifest.get("suite", "trixie")
    components = manifest.get("components", ["main"])
    owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "AYASCELL")
    repo_name = os.environ.get("GITHUB_REPOSITORY_NAME", "ayasos-repo")
    repo_uri = f"https://{owner}.github.io/{repo_name}/"
    trusted = manifest.get("trusted", True)
    options = "arch=amd64"
    if trusted:
        options = f"{options} trusted=yes"
    apt_source = f"deb [{options}] {repo_uri} {suite} {' '.join(components)}"
    html_content = f"""<!doctype html>
<html lang=\"tr\">
<head>
  <meta charset=\"utf-8\">
  <title>{html.escape(manifest.get('label', 'AYAS OS APT Repo'))}</title>
  <style>body{{font-family:Arial,sans-serif;max-width:900px;margin:2rem auto;line-height:1.6}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #ddd;padding:0.6rem;text-align:left}}th{{background:#f5f5f5}}</style>
</head>
<body>
  <h1>{html.escape(manifest.get('label', 'AYAS OS APT Repo'))}</h1>
  <p>Bu depo, AYAS OS için Debian tabanlı .deb paketlerini GitHub Pages üzerinden sunar.</p>
  <p>APT ayarı:</p>
  <pre>{html.escape(apt_source)}</pre>
  <table>
    <thead><tr><th>Paket</th><th>Sürüm</th><th>Dosya</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</body>
</html>
"""
    (output_dir / "index.html").write_text(html_content, encoding="utf-8")


def generate_repo(manifest: dict) -> None:
    ensure_tools()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / ".nojekyll").write_text("", encoding="utf-8")
    write_override_file(manifest, OUTPUT)

    suite = manifest.get("suite", "trixie")
    components = manifest.get("components", ["main"])
    architectures = manifest.get("architectures", ["amd64"])
    pool_root = OUTPUT / "pool" / "main"
    pool_root.mkdir(parents=True, exist_ok=True)

    pkg_links: list[tuple[str, str, str]] = []
    for pkg in manifest.get("packages", []):
        copied = copy_package(pkg, pool_root)
        rel = copied.relative_to(OUTPUT).as_posix()
        pkg_links.append((pkg["name"], pkg["version"], rel))

    for component in components:
        for arch in architectures:
            packages_dir = OUTPUT / "dists" / suite / component / f"binary-{arch}"
            packages_dir.mkdir(parents=True, exist_ok=True)
            packages_file = packages_dir / "Packages"
            gz_path = packages_dir / "Packages.gz"
            with packages_file.open("w", encoding="utf-8") as fh:
                subprocess.run(
                    ["dpkg-scanpackages", "--multiversion", "pool/main", "override", "./"],
                    check=True,
                    cwd=OUTPUT,
                    stdout=fh,
                )
            with packages_file.open("rb") as src, gzip.open(gz_path, "wb") as dst:
                shutil.copyfileobj(src, dst)

    release_file = OUTPUT / "dists" / suite / "Release"
    release_file.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "apt-ftparchive",
        "-o", "APT::FTPArchive::Release::Origin=AYAS OS",
        "-o", f"APT::FTPArchive::Release::Label={manifest.get('label', 'AYAS OS APT Repo')}",
        "-o", f"APT::FTPArchive::Release::Suite={suite}",
        "-o", f"APT::FTPArchive::Release::Codename={manifest.get('codename', suite)}",
        "-o", f"APT::FTPArchive::Release::Components={','.join(components)}",
        "-o", f"APT::FTPArchive::Release::Architectures={','.join(architectures)}",
        "-o", f"APT::FTPArchive::Release::Description={manifest.get('description', 'AYAS OS package repository')}",
        "release",
        str(OUTPUT / "dists" / suite),
    ]
    with release_file.open("w", encoding="utf-8") as fh:
        subprocess.run(cmd, check=True, cwd=OUTPUT, stdout=fh)

    sign_release(OUTPUT, release_file)
    write_index_html(manifest, OUTPUT, pkg_links)


if __name__ == "__main__":
    manifest = load_manifest()
    generate_repo(manifest)
    print(f"APT repository generated at {OUTPUT}")
