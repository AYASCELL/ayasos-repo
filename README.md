# AYAS OS APT Repository

Bu depo, AYAS OS için GitHub Pages üzerinden sunulan basit bir Debian/Ubuntu APT paket deposudur.

## Özellikler
- Birden fazla uygulama ve birden fazla sürüm desteği
- GitHub Actions ile otomatik build/deploy
- .deb paketlerini pool altına yerleştirip Debian APT metaveri üretir
- Büyük paketler için GitHub Pages kullanımında dosya boyutu kısıtları göz önünde bulundurulmalıdır

## Kullanım
1. Paket dosyalarını examples/ klasörüne koyun.
2. apps.json dosyasında paket adları, sürümleri ve dosya yollarını ekleyin.
3. Değişiklikleri gönderin; GitHub Actions otomatik olarak public/ klasörünü oluşturur.

## APT ayarı
```bash
sudo tee /etc/apt/sources.list.d/ayasos.list > /dev/null <<'EOF2'
deb [arch=amd64] https://<kullanici-adiniz>.github.io/<repo-adiniz> ./
EOF2
sudo apt update
```

## Yerel test
```bash
chmod +x scripts/build_repo.sh
./scripts/build_repo.sh
```
