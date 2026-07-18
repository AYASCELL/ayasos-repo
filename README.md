# AYAS OS APT Repository

Bu depo, AYAS OS için GitHub Pages üzerinden sunulan basit bir Debian/Ubuntu APT paket deposudur.

## Özellikler
- Birden fazla uygulama desteği
- Birden fazla sürüm desteği
- GitHub Actions ile otomatik build/deploy
- .deb paketlerini APT deposu yapısına dönüştürür
- GitHub Pages üzerinden yayınlanır

## 1. Depoyu GitHub’a yükleme
```bash
cd /workspaces/ayasos-repo
git init
git add .
git commit -m "Initial apt repo setup"
git branch -M main
git remote add origin https://github.com/<kullanici-adiniz>/<repo-adiniz>.git
git push -u origin main
```

## 2. GitHub Pages ayarı
1. GitHub repo sayfasında Settings açın.
2. Sol menüden Pages seçin.
3. Source bölümünde GitHub Actions seçin.
4. Actions sekmesinden workflow’un çalışmasını bekleyin.

Yayın adresi genelde şu formdadır:
```text
https://<kullanici-adiniz>.github.io/<repo-adiniz>/
```

## 3. APT kaynağı ekleme
Debian/Ubuntu sistemine bu depoyu eklemek için:
```bash
printf 'deb [arch=amd64] https://<kullanici-adiniz>.github.io/<repo-adiniz>/ bookworm main\n' | sudo tee /etc/apt/sources.list.d/ayasos.list
sudo apt update
```

## 4. Paket kurma
Örnek paket kurmak için:
```bash
sudo apt install ayas-app
sudo apt install ayas-tools
sudo apt install ayas-ui
```

## 5. Belirli sürüm kurma
Belirli sürümü kurmak için:
```bash
sudo apt install ayas-app=1.1.0
sudo apt install ayas-tools=1.0.0
sudo apt install ayas-ui=1.1.0
```

## 6. Yeni paket ekleme
Yeni bir paket eklemek için:
1. Yeni paket klasörü oluşturun, örneğin `examples/myapp-1.0.0/`.
2. `DEBIAN/control` dosyası oluşturun.
3. Paket içeriğini `usr/` altına koyun.
4. `.deb` dosyasını oluşturun:
```bash
dpkg-deb --build examples/myapp-1.0.0 examples/myapp_1.0.0_amd64.deb
```
5. `apps.json` dosyasına paket bilgisi ekleyin:
```json
{
  "name": "myapp",
  "version": "1.0.0",
  "file": "examples/myapp_1.0.0_amd64.deb"
}
```
6. Build’i tekrar çalıştırın:
```bash
./scripts/build_repo.sh
```

## 7. Yeni sürüm ekleme
Aynı paket için yeni sürüm eklemek için:
1. Yeni klasör oluşturun, örneğin `examples/myapp-1.1.0/`.
2. Yeni `.deb` üretin.
3. `apps.json` içine yeni bir kayıt ekleyin.
4. Repo yeniden build edilir.

## 8. Sürüm numaraları neden önemlidir?
Deb paketlerinde sürüm numarası çok önemlidir. Çünkü APT, aynı paketin farklı sürümlerini ayırt etmek için bunu kullanır.

- `DEBIAN/control` dosyasındaki `Version:` değeri, `.deb` paketinin kendi sürümüdür.
- `apps.json` dosyasındaki `version` değeri, APT deposundaki kayıt için kullanılır.
- İki değer birbirinin aynı olmalıdır.

Örnek:
```text
DEBIAN/control -> Version: 1.1.0
apps.json      -> "version": "1.1.0"
```

Eğer sürüm numarası tutarsız olursa:
- paket bulunmayabilir
- belirli sürüm kurulumu çalışmayabilir
- güncelleme akışı bozulabilir

## 9. Yerel test
```bash
chmod +x scripts/build_repo.sh
./scripts/build_repo.sh
```

## 10. Sorun giderme
Eğer workflow hata verirse:
- Actions sekmesinden hatayı kontrol edin.
- `./scripts/build_repo.sh` komutunu yerelde çalıştırın.
- Hata mesajını düzeltip tekrar push edin.
