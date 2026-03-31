# PicoRV32 Assembler — Web Tabanlı Görsel Assembler (RV32I)

Bu projede, kullanıcıların assembly kodlarını tarayıcı üzerinden yazıp anında makine koduna (binary/hex) dönüştürebildiği web tabanlı bir assembler geliştirilmektedir.

Sistem, klasik assembler mantığını (opcode table, symbol table, parser) backend tarafında çalıştırırken, frontend tarafında kullanıcıya görsel ve etkileşimli bir deneyim sunar. Kullanıcı assembly kodunu yazdığı anda sistem komutları analiz eder, hataları anlık olarak gösterir ve her komutun makine koduna nasıl dönüştüğünü detaylı biçimde sunar.

Proje sadece kod çeviren bir assembler değil; aynı zamanda assembly öğrenimini kolaylaştıran, hata analizini görselleştiren ve sistem programlama kavramlarını somutlaştıran interaktif bir araç olarak tasarlanmaktadır.

## Amaç

- RV32I komut alt kümesi desteği ve iki geçişli (two-pass) assembler yapısı
- Pseudo-komut desteği (`li`, `mv`, `j` vb.) ve `.macro` / `.endmacro` ile makro sistemi
- Syntax ve semantic hata kontrolü (geçersiz register, tanımsız etiket, immediate taşması vb.)
- Instruction breakdown görselleştirmesi, label adres eşlemeleri ve satır bazlı hata işaretleme
- Web arayüz üzerinden kod girişi, çıktı gösterimi ve hata görselleştirmesi

---

## 1. Aşama — Assembler Core

Projenin ilk aşamasında temel assembler bileşenleri geliştirilmektedir.

### Problemin Analizi
> _Güncellenecek._

### Literatür Araştırması
> _Güncellenecek._

### Assembler Mimarisi
> _Güncellenecek._

### Kullanılan Veri Yapıları
> _Güncellenecek._

### Opcode Table Tasarımı
> _Güncellenecek._

### Symbol Table Tasarımı
> _Güncellenecek._

### Assembler Algoritması
> _Güncellenecek._

### Akış Diyagramı
> _Güncellenecek._

### Desteklenen Direktifler
```
.data   .text   .word   .byte   .org   .end
```

### Desteklenen Komut Formatları

| Format | Açıklama | Örnek |
|--------|----------|-------|
| R-type | Register işlemleri | `add`, `sub`, `and`, `or` |
| I-type | Immediate işlemleri | `addi`, `lw`, `jalr` |
| S-type | Store işlemleri | `sw`, `sb` |
| B-type | Branch işlemleri | `beq`, `bne`, `blt` |
| U-type | Upper immediate | `lui`, `auipc` |
| J-type | Jump | `jal` |

### Test Senaryoları ve Sonuçlar
> _Güncellenecek._

### Algoritma Karmaşıklığı Analizi
> _Güncellenecek._

---

Bu proje SUBÜ Sistem Programlama dersi kapsamında geliştirilmektedir.