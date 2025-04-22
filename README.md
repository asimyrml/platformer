# Platformer Game

Bu proje, **Python** ve **Pygame Zero (pgzrun)** kullanılarak geliştirilmiş 2D bir platform oyunudur. Oyuncu olarak platformlar üzerinde zıplayarak altınları toplamalı, düşmanlardan kaçmalı ve bölümü başarıyla tamamlamalısınız.

## 🎮 Özellikler

- 🎲 Rastgele oluşturulan platform yapısı
- 🪙 Toplanabilir altınlar
- 👾 Yapay zekalı düşmanlar
- ⚔️ Saldırı mekaniği (yakın mesafede)
- 🔊 Müzik ve ses efektleri
- 📜 Oyun sonu ve menü ekranları
- 🕹️ Basit ama eğlenceli kontroller

## 🧰 Gereksinimler
- Python 3.7 veya üstü
- Pygame Zero (pgzero)

Kurmak için:
```bash
pip install pgzero
```

## 🚀 Oyunu Çalıştırma
```bash
pgzrun game.py
```

## 🎮 Kontroller

| Tuş      | İşlev                                     |
|----------|--------------------------------------------|
| ← / →    | Oyuncuyu sola/sağa hareket ettirir         |
| SPACE    | Zıplama                                    |
| X        | Saldırı (yakındaysa düşmanı yok eder)      |
| H        | "Nasıl Oynanır" ekranını gösterir          |


## 🏆 Amaç
Oyundaki tüm altınları toplarsanız bölümü kazanırsınız. Saldırmadan bir düşmana temas ederseniz oyun biter.
```nash
project/
├── game.py          # Ana oyun dosyası
├── README.md        # Bu dosya
├── images/          # Sprite'lar (adventurer, coin, enemy vs.)
├── sounds/          # Ses dosyaları (bgm, jump, attack, etc.)
```

## 🔧 Geliştirme İpuçları
- Platformlar rastgele oluşturulur, her oynanış farklı olur.
- Platformlar arasında zigzag bir yapı izlenir.
- Oyuncu ekran dışına çıkamaz.
- Düşman ve coin doğum noktaları akıllıca hesaplanır.
