# AYAS OS Resmi APT Deposudur

Bu depo, AYAS OS için GitHub Pages üzerinden sunulan Debian/Ubuntu APT paket deposudur.

## Özellikler
- Kolay ve hızlı kurulum
- Sürüm kontrol desteği
- Güvenli APT altyapısı

## 1. APT Kaynağı Ekleme
Debian/Ubuntu tabanlı sisteminize bu depoyu eklemek için terminalinizde şu komutları sırasıyla çalıştırın:
```bash
echo 'deb [arch=amd64 trusted=yes] https://AYASCELL.github.io/ayasos-repo/ trixie main' | sudo tee /etc/apt/sources.list.d/ayasos.list
sudo apt update
```

## 2. Paket Kurma
Depoyu ekledikten sonra uygulamalarımızı kolayca indirebilirsiniz:
```bash
sudo apt install ayasfetch
sudo apt install ayascell-browser
```

## 3. Belirli Bir Sürümü Kurma
Eğer uygulamanın eski veya belirli bir sürümünü kurmak isterseniz:
```bash
sudo apt install ayasfetch=1.0.0
```

## 4. Paket Kaldırma
Kurduğunuz bir paketi kaldırmak için:
```bash
sudo apt remove ayascell-browser
```

## 5. Lisans ve Kullanım Koşulları / License and Terms of Use (ÖNEMLİ/IMPORTANT)
Bu proje **AYASCELL LİSANSI** ile korunmaktadır. 
Bu projeyi veya paketlerini kullanan, kopyalayan veya üzerine inşa eden geliştiriciler aşağıdaki kurallara uymak **zorundadır**:
1. Orijinal geliştiricinin AYASCELL olduğu açıkça belirtilmeli ve proje/profil açıklamalarında **"Powered by AYASCELL"** ibaresi bulunmalıdır.
2. Paket ve proje adları ("ayasfetch", "Ayascell-Browser" vb.) birebir kullanılamaz; değiştirilerek özgün isimler verilmelidir.
3. Proje hiçbir şekilde zararlı, yasa dışı veya yanıltıcı amaçlarla kullanılamaz.
4. Geliştiriciler projeyi kullanırken tüm riski üstlenirler; AYASCELL olası veri veya donanım kayıplarından sorumlu tutulamaz.

---

This project is protected by the **AYASCELL LICENSE**.
Developers who use, copy, or build upon this project or its packages **must** comply with the following rules:
1. It must be clearly stated that the original developer is AYASCELL, and the phrase **"Powered by AYASCELL"** must be included in the project/profile descriptions.
2. Package and project names (e.g., "ayasfetch", "Ayascell-Browser") cannot be used exactly as they are; they must be changed to unique names.
3. The project cannot be used for malicious, illegal, or deceptive purposes in any way.
4. Developers assume all risk when using the project; AYASCELL cannot be held liable for possible data or hardware losses.

Tüm şartları okumak için / To read all the terms, see the [LICENSE](LICENSE) file.
