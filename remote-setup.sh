#!/bin/bash

# Kullanıcıya soru sorulmasını engelleyerek tam otomatik kurulum sağlar
export DEBIAN_FRONTEND=noninteractive

echo "AYAS OS Uzaktan Kurulum Yöneticisi Başladı..."

# ---------------------------------------------------------
# 1. ESKİ VEYA İPTAL EDİLEN REPOLARI TEMİZLEME BÖLÜMÜ
# ---------------------------------------------------------
# Eğer ileride bir repoyu kaldırmak istersen buradaki yorum satırlarını kaldırıp yollarını yazabilirsin
# rm -f /etc/apt/sources.list.d/eski-repo.list
# rm -f /usr/share/keyrings/eski-repo.gpg

# ---------------------------------------------------------
# 2. YENİ REPO EKLEME BÖLÜMÜ
# ---------------------------------------------------------
# AYAS OS ana reposunu ekliyoruz
echo 'deb [arch=amd64 trusted=yes] https://AYASCELL.github.io/ayasos-repo/ trixie main' > /etc/apt/sources.list.d/ayasos.list

# Farklı bir repo eklemek istersen komutunu bu satırın altına ekleyebilirsin

# ---------------------------------------------------------
# 3. SİSTEMİ GÜNCELLEME
# ---------------------------------------------------------
# Repolar eklendikten veya silindikten sonra paket listesini yeniliyoruz
apt-get update -y

# ---------------------------------------------------------
# 4. PROGRAM KURULUM VE KALDIRMA BÖLÜMÜ
# ---------------------------------------------------------
# Kurulmasını istediğin paketleri buraya yazıyorsun
apt-get install -y ayasfetch ayascell-browser

# Eğer ileride kullanıcılardan silinmesini istediğin paketler olursa:
# apt-get purge -y istenmeyen-paket
# apt-get autoremove -y

# ---------------------------------------------------------
# 5. EKSTRA İŞLEMLER VE OPTİMİZASYONLAR
# ---------------------------------------------------------
# Örnek: Yalnızca süresi geçmiş (eski sürüm) indirmeleri temizler, önbelleği korur
apt-get autoclean

echo "Tüm işlemler başarıyla tamamlandı!"
