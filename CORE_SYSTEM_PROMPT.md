# CORE v3.5 - Sistem Prompt Dokümantasyonu

> **Cut Optimization & Reporting Engine**  
> Mobilya üretimi için Excel kesim listesi analiz ve optimizasyon yazılımı

---

## 📋 İÇİNDEKİLER

1. [Genel Bakış](#1-genel-bakış)
2. [Mimari Yapı](#2-mimari-yapı)
3. [Veri Modeli](#3-veri-modeli)
4. [Parça Tipi Tespiti](#4-parça-tipi-tespiti)
5. [Excel Sütun Mapping](#5-excel-sütun-mapping)
6. [Kalınlık Sistemi](#6-kalınlık-sistemi)
7. [API Referansı](#7-api-referansı)
8. [Frontend State Yönetimi](#8-frontend-state-yönetimi)
9. [UI Bileşenleri](#9-ui-bileşenleri)
10. [İş Akışları](#10-iş-akışları)
11. [Dosya Yapısı](#11-dosya-yapısı)
12. [Formüller ve Hesaplamalar](#12-formüller-ve-hesaplamalar)
13. [Ayarlar Sistemi](#13-ayarlar-sistemi)
14. [Hata Yönetimi](#14-hata-yönetimi)

---

## 1. GENEL BAKIŞ

### 1.1 Uygulama Amacı
CORE, mobilya üretim tesislerinde kullanılan Excel kesim listelerini analiz eder ve optimize edilmiş çıktı üretir. Parçaları otomatik olarak sınıflandırır, malzeme kalınlıklarını yönetir ve yan yana tablolu Excel çıktısı oluşturur.

### 1.2 Teknoloji Stack
```
Backend:  Python 3.x + PyWebview
Frontend: HTML5 + CSS3 + Vanilla JavaScript
Database: SQLite (history) + JSON (settings, materials)
Excel:    pandas + openpyxl
```

### 1.3 Temel Özellikler
- Excel/CSV dosya analizi
- Otomatik parça tipi tespiti (YAN, ALT-ÜST, RAF, ARKALIK, vb.)
- Malzeme kalınlık hafızası (öğrenme sistemi)
- Kanallı/Kanalsız parça yönetimi
- Manuel düzenleme + öğrenme
- Yan yana tablolu Excel çıktısı (Gövde | İnce)
- İş geçmişi ve birleştirme
- Çoklu dil desteği (TR/EN)
- Koyu/Açık tema

---

## 2. MİMARİ YAPI

### 2.1 Backend Sınıfları

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                              │
├─────────────────────────────────────────────────────────────┤
│  Config              │ Uygulama yapılandırması              │
│  DatabaseManager     │ SQLite işlemleri (history, stats)    │
│  JsonDataManager     │ JSON dosya yönetimi                  │
│  UserManager         │ Kullanıcı kimlik doğrulama           │
│  ExcelAnalyzer       │ Excel analiz ve parça tespiti        │
│  Api                 │ Frontend-Backend iletişim köprüsü    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Sınıf Detayları

#### Config
```python
class Config:
    APP_NAME = "CORE"
    APP_VERSION = "3.5"
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 900
    
    @staticmethod
    def get_data_dir() -> Path:
        # Windows: %LOCALAPPDATA%\CORE\data
        # Linux:   ~/.core/data
        
    @staticmethod
    def get_db_path() -> Path:
        return Config.get_data_dir() / "core.db"
    
    @staticmethod
    def get_json_path(name: str) -> Path:
        return Config.get_data_dir() / f"core_{name}.json"
```

#### DatabaseManager
```python
class DatabaseManager:
    """SQLite veritabanı yönetimi"""
    
    # Tablolar:
    # - history: İş geçmişi (job_no, date, file_name, body_data, thin_data, ...)
    # - stats: İstatistikler (total_jobs, total_parts)
    
    def add_history(job: Dict) -> bool
    def delete_history(job_ids: List[int]) -> Dict
    def get_history(limit: int = 100) -> List[Dict]
    def get_stats() -> Dict
```

#### JsonDataManager
```python
class JsonDataManager:
    """JSON dosya yönetimi"""
    
    # Dosyalar:
    # - core_settings.json: Uygulama ayarları
    # - core_materials.json: Malzeme kalınlık hafızası
    # - core_learned_parts.json: Öğrenilmiş parça tipleri
    
    def get_settings() -> Dict
    def save_settings(settings: Dict) -> bool
    def get_materials() -> Dict  # {"MAL_KODU": 18, ...}
    def save_material(code: str, thickness: int) -> bool
    def get_learned_parts() -> Dict  # {"720x580_LAM": "YAN", ...}
    def save_learned_part(key: str, part_type: str) -> bool
```

#### ExcelAnalyzer
```python
class ExcelAnalyzer:
    """Excel analiz motoru"""
    
    def check_file(file_path: str) -> Dict
        # Dosyayı kontrol et, bilinmeyen malzemeleri bul
        
    def analyze_only(file_path: str, custom_depths: Dict) -> Dict
        # Analiz et, sonuçları döndür (kaydetme)
        
    def analyze_and_export(file_path: str, output_path: str, custom_depths: Dict) -> Dict
        # Analiz et ve Excel'e kaydet
```

#### Api
```python
class Api:
    """Frontend-Backend köprüsü - PyWebview expose edilir"""
    
    # Kullanım: window.pywebview.api.method_name(args)
    
    # Dosya İşlemleri
    def select_file() -> Dict
    def check_file(file_path: str) -> Dict
    def check_all_files() -> Dict
    def analyze_file(file_index: int) -> Dict
    def analyze_and_export(file_path: str) -> Dict
    def analyze_all_files() -> Dict
    def export_edited_results(body: List, thin: List, job_no: str) -> Dict
    
    # Ayarlar
    def get_settings() -> Dict
    def save_settings(settings: Dict) -> Dict
    def reset_settings() -> Dict
    
    # Malzemeler
    def get_materials() -> Dict
    def save_material(code: str, thickness: int) -> Dict
    def delete_material(code: str) -> Dict
    def clear_materials() -> Dict
    
    # Geçmiş
    def get_history() -> List[Dict]
    def delete_history(job_ids: List[int]) -> Dict
    def get_stats() -> Dict
    
    # Öğrenme
    def save_learned_parts(rules: List[Dict]) -> Dict
    
    # Kullanıcı
    def login(username: str, password: str) -> Dict
    def logout() -> Dict
```

---

## 3. VERİ MODELİ

### 3.1 History Tablosu (SQLite)
```sql
CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_no TEXT,                    -- İş numarası (Info16'dan)
    date TEXT,                      -- Tarih (YYYY-MM-DD HH:MM)
    file_name TEXT,                 -- Kaynak dosya adı
    file_path TEXT,                 -- Kaynak dosya yolu
    output_path TEXT,               -- Çıktı Excel yolu
    total_parts INTEGER,            -- Toplam parça sayısı
    material_count INTEGER,         -- Malzeme çeşidi
    type_count INTEGER,             -- Parça tipi çeşidi
    body_data TEXT,                 -- JSON: Gövde parçaları
    thin_data TEXT,                 -- JSON: İnce parçaları
    created_at TIMESTAMP
);
```

### 3.2 Materials JSON
```json
{
    "LAM BEYAZ 18MM": 18,
    "MDF LAK BEYAZ": 18,
    "SUNTA 8MM ARK": 8,
    "YONGA 16MM": 16
}
```

### 3.3 Learned Parts JSON
```json
{
    "720x580_LAM BEYAZ": "YAN",
    "564x579_MDF LAK": "ALT-ÜST",
    "683x563_SUNTA": "ARKALIK (İÇERDE)"
}
```

### 3.4 Settings JSON
```json
{
    "standart_yukseklik": 720,
    "standart_derinlik": 580,
    "ust_dolap_yukseklik": 720,
    "ust_dolap_derinlik": 330,
    "boy_dolap_yukseklik": 2100,
    "boy_dolap_derinlik": 580,
    "yan_dusumu": 36,
    "raf_genislik_dusumu": 37,
    "raf_derinlik_alt_dolap": 50,
    "raf_derinlik_ust_dolap": 40,
    "sabit_derinlik_dusumu": 23,
    "arkalik_dusumu": 18,
    "arkalik_icerde_dusumu": 37,
    "tolerans": 5,
    "arkalik_max_kalinlik": 8,
    "govde_kalinlik": 18,
    "cekmece_yan_kalinlik": 16,
    "arkalik_kalinlik": 8
}
```

---

## 4. PARÇA TİPİ TESPİTİ

### 4.1 Tespit Algoritması Akışı

```
┌─────────────────────────────────────────────────────────────┐
│                  determine_part_type()                       │
├─────────────────────────────────────────────────────────────┤
│ 1. Malzeme kalınlığını veritabanından al (db_kalinlik)      │
│ 2. Öğrenilmiş parça kontrolü (learned_parts)                │
│ 3. Malzeme kalınlığı ≤ 8mm ise → İnce parça tipleri         │
│ 4. Özel modül ayarları varsa → Özel hesaplama               │
│ 5. Standart ölçü kontrolü (YAN, ALT-ÜST, vb.)              │
│ 6. Modül genişliğine göre hesaplama                         │
│ 7. Hiçbiri uymazsa → DİĞER                                  │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Parça Tipleri ve Formülleri

| Parça Tipi | BOY Formülü | EN Formülü | Açıklama |
|------------|-------------|------------|----------|
| **YAN** | Yükseklik | Derinlik | 720x580, 720x330, 2100x580 |
| **ALT-ÜST** | Genişlik - 36 | Derinlik - 1 | Alt ve üst paneller |
| **SABİT** | Genişlik - 36 | Derinlik - 23 | Sabit raflar |
| **RAF** | Genişlik - 37 | Derinlik - 50 | Alt dolap rafı |
| **RAF (ÜST)** | Genişlik - 37 | Derinlik - 40 | Üst dolap rafı |
| **ARKALIK** | Yükseklik - 18 | Genişlik - 18 | Normal arkalık |
| **ARKALIK (İÇERDE)** | Yükseklik - 37 | Genişlik - 37 | Tesisat arkalığı |
| **KAYIT/KUŞAK** | Değişken | 80-140mm | Destek parçaları |
| **ÇEKMECE YANI** | Değişken | Değişken | 16mm çekmece yanları |
| **DİĞER** | - | - | Sınıflandırılamayan |

### 4.3 Standart Ölçüler

```python
# Alt Dolap
ALT_DOLAP_YUKSEKLIK = 720   # mm
ALT_DOLAP_DERINLIK = 580    # mm

# Üst Dolap
UST_DOLAP_YUKSEKLIK = 720   # mm
UST_DOLAP_DERINLIK = 330    # mm

# Boy Dolap
BOY_DOLAP_YUKSEKLIK = 2100  # mm
BOY_DOLAP_DERINLIK = 580    # mm

# Tolerans
TOLERANS = 5  # mm (±5mm kabul edilir)
```

### 4.4 Örnek Hesaplamalar

```
Modül: 600mm genişlik, Alt dolap

YAN:      720 x 580
ALT-ÜST:  (600-36) x (580-1) = 564 x 579
SABİT:    (600-36) x (580-23) = 564 x 557
RAF:      (600-37) x (580-50) = 563 x 530
ARKALIK:  (720-18) x (600-18) = 702 x 582
ARK.İÇ:   (720-37) x (600-37) = 683 x 563
```

### 4.5 Tespit Kodu Örneği

```python
def determine_part_type_with_module(row) -> tuple:
    """
    Returns: (parça_tipi, kalınlık, boy, en, kanalli)
    
    KRİTİK: Kalınlık HER ZAMAN malzemenin kalınlığı (db_kalinlik)!
    """
    olcu1, olcu2 = row['OLCU1'], row['OLCU2']
    malzeme = row['MALZEME']
    db_kalinlik = materials_db.get(malzeme, GOVDE_KALINLIK)
    
    boy = max(olcu1, olcu2)
    en = min(olcu1, olcu2)
    kanalli = check_kanalli(row)
    
    # 1. Öğrenilmiş parça kontrolü
    learned_key = f"{boy}x{en}_{malzeme}"
    if learned_key in learned_parts:
        return learned_parts[learned_key], db_kalinlik, boy, en, kanalli
    
    # 2. Malzeme 8mm veya altı ise → Arkalık
    if db_kalinlik <= 8:
        return 'ARKALIK', db_kalinlik, boy, en, kanalli
    
    # 3. Standart YAN kontrolü
    if abs(boy - 720) <= TOLERANS and abs(en - 580) <= TOLERANS:
        return 'YAN', db_kalinlik, boy, en, kanalli
    
    # 4. ALT-ÜST kontrolü (EN ≈ 579)
    if abs(en - 579) <= TOLERANS:
        return 'ALT-ÜST', db_kalinlik, boy, en, kanalli
    
    # ... diğer kontroller
    
    return 'DİĞER', db_kalinlik, boy, en, kanalli
```

---

## 5. EXCEL SÜTUN MAPPING

### 5.1 Beklenen Excel Formatı

```
┌────────┬────────┬────────┬────────┬────────┬────────┬────────┐
│ POZ    │ Modül  │ Adet   │ Uzunluk│ Genişl.│ Kanallı│Malzeme │
│ Info4  │ Info5  │ Sipariş│ (BOY)  │ (EN)   │ Info1  │        │
├────────┼────────┼────────┼────────┼────────┼────────┼────────┤
│ A-01   │Alt 60cm│ 2      │ 720    │ 580    │SAĞ_13+9│LAM BYZ │
│ A-02   │Alt 60cm│ 2      │ 564    │ 579    │SOL_13+9│LAM BYZ │
│ A-03   │Alt 60cm│ 4      │ 702    │ 582    │        │ARK 8MM │
└────────┴────────┴────────┴────────┴────────┴────────┴────────┘
```

### 5.2 Sütun Mapping Algoritması

```python
def _get_column_mapping(df) -> Dict:
    mapping = {}
    
    for col in df.columns:
        col_lower = str(col).lower().strip()
        
        # POZ (Info4)
        if 'Info4' in str(col) or col_lower == 'poz':
            mapping['poz'] = col
        
        # Modül (Info5)
        if 'Info5' in str(col) or 'modül' in col_lower:
            mapping['modul'] = col
        
        # Adet/Sipariş
        if col_lower in ['adet', 'sipariş', 'qty']:
            mapping['adet'] = col
        
        # Ölçü 1 (Uzunluk/BOY)
        if col_lower in ['uzunluk', 'boy', 'ölçü 1']:
            mapping['olcu1'] = col
        
        # Ölçü 2 (Genişlik/EN)
        if col_lower in ['genişlik', 'en', 'ölçü 2']:
            mapping['olcu2'] = col
        
        # Kanallı (Info1)
        if 'Info1' in str(col) or col_lower == 'kanallı':
            mapping['kanalli'] = col
        
        # Malzeme
        if 'malzeme' in col_lower:
            mapping['malzeme'] = col
        
        # İş Numarası (Info16)
        if 'Info16' in str(col):
            mapping['info16'] = col
    
    return mapping
```

### 5.3 Kanallı Tespit Formatları

```python
def check_kanalli(row) -> bool:
    kanalli_val = str(row.get(kanalli_col, '')).upper().strip()
    
    # Doğrudan değerler
    if kanalli_val in ['TRUE', 'EVET', 'YES', '1', 'VAR']:
        return True
    
    # Format: SOL_5+5, SAĞ_10+10
    if re.search(r'(SOL|SAĞ|SAG)_\d+\+\d+', kanalli_val):
        return True
    
    return False
```

---

## 6. KALINLIK SİSTEMİ

### 6.1 Temel Kural

> **KRİTİK:** Parça tipi ne olursa olsun, kalınlık HER ZAMAN malzemenin veritabanındaki kalınlığından alınır!

```python
# YANLIŞ ❌
if part_type == 'ARKALIK':
    return part_type, 8, boy, en  # Sabit 8mm

# DOĞRU ✅
db_kalinlik = materials_db.get(malzeme, 18)
return part_type, db_kalinlik, boy, en  # Malzemenin gerçek kalınlığı
```

### 6.2 Tablo Ayrımı

```python
ARKALIK_KALINLIK = 8  # Eşik değer

# Gövde tablosu: Kalınlık > 8mm
body_df = summary[summary['KALINLIK'] > ARKALIK_KALINLIK]

# İnce tablosu: Kalınlık ≤ 8mm  
thin_df = summary[summary['KALINLIK'] <= ARKALIK_KALINLIK]
```

### 6.3 Varsayılan Kalınlıklar

```python
GOVDE_KALINLIK = 18         # Gövde parçaları
CEKMECE_YAN_KALINLIK = 16   # Çekmece yanları
ARKALIK_KALINLIK = 8        # Arkalıklar
```

---

## 7. API REFERANSI

### 7.1 Dosya İşlemleri

```javascript
// Dosya seçme
const result = await api('select_file');
// Returns: { success, files: [{name, path, job_no, unknown_materials}] }

// Dosya kontrol
const check = await api('check_file', filePath);
// Returns: { success, materials, unknown, row_count, job_no }

// Tüm dosyaları kontrol
const checkAll = await api('check_all_files');
// Returns: { success, unknown: [], total_rows, file_count }

// Analiz (sonuç göster)
const analysis = await api('analyze_file', fileIndex);
// Returns: { success, job_no, total_parts, body: [], thin: [] }

// Hızlı analiz (direkt kaydet)
const quick = await api('analyze_and_export', filePath);
// Returns: { success, job_no, total_parts, output_path }

// Düzenlenmiş sonuçları kaydet
const save = await api('export_edited_results', bodyData, thinData, jobNo);
// Returns: { success, output_path }
```

### 7.2 Malzeme Yönetimi

```javascript
// Malzemeleri getir
const materials = await api('get_materials');
// Returns: { "MAL_KODU": 18, ... }

// Malzeme kaydet
const result = await api('save_material', 'LAM BEYAZ', 18);
// Returns: { success }

// Malzeme sil
const result = await api('delete_material', 'LAM BEYAZ');
// Returns: { success }

// Tüm malzemeleri temizle
const result = await api('clear_materials');
// Returns: { success }
```

### 7.3 Geçmiş Yönetimi

```javascript
// Geçmişi getir
const history = await api('get_history');
// Returns: [{ id, job_no, date, file_name, stats, results }, ...]

// İş sil
const result = await api('delete_history', [jobId]);
// Returns: { success, deleted }

// İstatistikler
const stats = await api('get_stats');
// Returns: { jobs, parts, today, materials }
```

### 7.4 Öğrenme Sistemi

```javascript
// Öğrenilen kuralları kaydet
const rules = [
    { boy: 720, en: 580, malzeme: 'LAM', partType: 'YAN' },
    { boy: 564, en: 579, malzeme: 'LAM', partType: 'ALT-ÜST' }
];
const result = await api('save_learned_parts', rules);
// Returns: { success, saved_count }
```

---

## 8. FRONTEND STATE YÖNETİMİ

### 8.1 Global State

```javascript
const state = {
    // Kullanıcı
    user: null,
    isAdmin: false,
    
    // Tema ve Dil
    theme: 'light',
    language: 'tr',
    
    // Dosyalar
    files: [],                    // Seçili dosyalar
    currentFileIndex: 0,
    
    // Analiz Sonuçları
    currentResults: {
        body: [],                 // Gövde parçaları
        thin: [],                 // İnce parçalar
        job_no: null
    },
    
    // Düzenleme
    editedParts: new Map(),       // Değiştirilen parça tipleri
    
    // Geçmiş
    history: [],
    selectedJobs: new Set(),
    
    // Malzemeler
    materials: {},
    unknownMaterials: [],
    currentMaterialIndex: 0,
    
    // Ayarlar
    settings: {},
    
    // Özel Modüller
    customModules: {},
    
    // UI State
    afterMaterialsAction: null    // 'analyze' | 'quickAnalyze'
};
```

### 8.2 State Güncelleme Akışı

```
Dosya Seç → state.files güncelle → UI güncelle
    ↓
Analiz Et → Bilinmeyen malzeme? → Malzeme Dialog
    ↓                                   ↓
state.currentResults güncelle    state.unknownMaterials
    ↓                                   ↓
Sonuçlar Modal aç              Kalınlık seç → save_material
    ↓
Düzenleme → state.editedParts.set(key, value)
    ↓
Kaydet → save_learned_parts → export_edited_results
    ↓
state.history güncelle → UI güncelle
```

---

## 9. UI BİLEŞENLERİ

### 9.1 Sayfalar

```
┌───────────────────────────────────────────────────────────────┐
│ HEADER: Logo | Ana Sayfa | Geçmiş | Malzemeler | 🌙 | TR | 👤│
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  page-dashboard    │ Ana sayfa, dosya yükleme, istatistikler  │
│  page-history      │ İş geçmişi listesi                       │
│  page-materials    │ Malzeme kalınlık yönetimi                │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### 9.2 Modallar

```javascript
// Modal açma/kapama
openModal('modal-id');
closeModal('modal-id');
closeAllModals();

// Modallar:
// - modal-settings    : Ayarlar
// - modal-results     : Analiz sonuçları (düzenlenebilir)
// - modal-material    : Yeni malzeme kalınlık seçimi
// - modal-confirm     : Onay penceresi
// - modal-job-detail  : İş detayı
// - modal-user        : Kullanıcı yönetimi
// - modal-module-depth: Özel modül ayarları
```

### 9.3 Onay Penceresi (showConfirm)

```javascript
// Kullanım
const confirmed = await showConfirm(
    'İşi silmek istediğinize emin misiniz?',
    'İşi Sil',
    'danger'  // 'warning' | 'danger' | 'info' | 'success'
);

if (confirmed) {
    // İşlemi yap
}
```

### 9.4 Toast Bildirimleri

```javascript
showToast('success', 'Başarılı', 'İşlem tamamlandı!');
showToast('error', 'Hata', 'Bir sorun oluştu!');
showToast('warning', 'Uyarı', 'Dikkat edilmesi gereken durum');
showToast('info', 'Bilgi', 'Bilgilendirme mesajı');
```

### 9.5 Buton Stilleri

```css
/* Renk Paleti (Logo bazlı) */
--logo-dark: #1f315d;
--logo-mid: #223961;
--logo-light: #2d4a7c;

/* Buton Tipleri */
.btn-primary   → Koyu mavi, hover: invert (beyaz bg, mavi text)
.btn-success   → Yeşil, hover: invert
.btn-danger    → Kırmızı, hover: invert
.btn-warning   → Turuncu, hover: invert
.btn-secondary → Outline, hover: dolu
.btn-ghost     → Şeffaf, hover: hafif bg
```

### 9.6 Kanallı Toggle

```html
<span class="kanalli-toggle active" onclick="toggleKanalli(this)">K</span>
```

```css
.kanalli-toggle {
    /* Kanalsız: Gri */
    background: transparent;
    color: var(--text-muted);
    border: 2px solid var(--text-muted);
}

.kanalli-toggle.active {
    /* Kanallı: Turuncu */
    background: var(--warning);
    color: white;
    border-color: var(--warning);
}
```

---

## 10. İŞ AKIŞLARI

### 10.1 Normal Analiz Akışı

```
1. Dosya Seç/Sürükle
   ↓
2. [Özel Modül] (opsiyonel) → Modül boyutları ayarla
   ↓
3. [Analiz Et] butonuna tıkla
   ↓
4. check_all_files() → Bilinmeyen malzeme var mı?
   ↓
   ├─ Var → Malzeme Dialog açılır
   │        ↓
   │        Her malzeme için kalınlık seç (8/16/18mm)
   │        ↓
   │        save_material() → Hafızaya kaydet
   │        ↓
   └─ Yok → Devam
   ↓
5. analyze_file() → Sonuçları getir
   ↓
6. Sonuçlar Modal açılır
   ↓
7. Manuel düzenleme (opsiyonel)
   - Parça tipi değiştir (dropdown)
   - Kanallı toggle (K butonu)
   ↓
8. [Kaydet ve Excel Oluştur]
   ↓
9. save_learned_parts() → Değişiklikleri öğren
   ↓
10. export_edited_results() → Excel oluştur
    ↓
11. Excel otomatik açılır
```

### 10.2 Hızlı Analiz Akışı

```
1. Dosya Seç/Sürükle
   ↓
2. [Hızlı Analiz] butonuna tıkla (yeşil)
   ↓
3. check_all_files() → Bilinmeyen malzeme var mı?
   ↓
   ├─ Var → Malzeme Dialog
   └─ Yok → Devam
   ↓
4. analyze_and_export() → Direkt Excel oluştur
   ↓
5. Kayıt yeri seç (Save Dialog)
   ↓
6. Excel kaydedilir ve açılır
   
NOT: Sonuçlar Modal AÇILMAZ, düzenleme yapılamaz
```

### 10.3 Malzeme Öğrenme Akışı

```
Yeni Malzeme Bulundu:
"LAM BEYAZ 18MM" → Kalınlık seç: [8mm] [16mm] [18mm]
                           ↓
                   save_material("LAM BEYAZ 18MM", 18)
                           ↓
                   core_materials.json güncellenir
                           ↓
                   Sonraki analizlerde otomatik 18mm kullanılır
```

### 10.4 Parça Tipi Öğrenme Akışı

```
Sonuçlar Modal'da:
564x579 LAM → ALT-ÜST olarak görünüyor
         ↓
Kullanıcı değiştirdi: ALT-ÜST → SABİT
         ↓
state.editedParts.set("564x579_LAM", {partType: "SABİT", ...})
         ↓
Kaydet tıklandığında:
save_learned_parts([{boy:564, en:579, malzeme:"LAM", partType:"SABİT"}])
         ↓
core_learned_parts.json: {"564x579_LAM": "SABİT"}
         ↓
Sonraki analizlerde 564x579 LAM → otomatik SABİT
```

---

## 11. DOSYA YAPISI

### 11.1 Proje Dosyaları

```
CORE/
├── main.py              # Python backend (2472 satır)
├── index.html           # Frontend (4693 satır, tek dosya)
├── build.py             # PyInstaller build script
├── requirements.txt     # Python bağımlılıkları
├── CORE_LOGO.png        # Uygulama logosu
├── CORE_Installer.nsi   # NSIS installer script
└── LICENSE.txt          # Lisans
```

### 11.2 Veri Dosyaları (Runtime)

```
Windows: %LOCALAPPDATA%\CORE\data\
Linux:   ~/.core/data/

├── core.db              # SQLite veritabanı
├── core_settings.json   # Ayarlar
├── core_materials.json  # Malzeme kalınlıkları
├── core_learned_parts.json  # Öğrenilmiş parçalar
└── core_users.json      # Kullanıcılar
```

### 11.3 Build Çıktısı

```
dist/
└── CORE/
    ├── CORE.exe         # Ana uygulama
    ├── index.html       # Frontend
    ├── CORE_LOGO.png    # Logo
    └── _internal/       # Python runtime
```

---

## 12. FORMÜLLER VE HESAPLAMALAR

### 12.1 Parça Ölçü Formülleri

```python
# Modül Genişliği: Excel'den "Alt dolap 60 cm" → 600mm
def get_modul_genislik(modul_adi: str) -> int:
    match = re.search(r'(\d+)\s*cm', modul_adi.lower())
    return int(match.group(1)) * 10 if match else None

# YAN
boy = YUKSEKLIK  # 720 veya 2100
en = DERINLIK    # 580 veya 330

# ALT-ÜST
boy = MODUL_GENISLIK - 36
en = DERINLIK - 1

# SABİT
boy = MODUL_GENISLIK - 36
en = DERINLIK - 23

# RAF (Alt Dolap)
boy = MODUL_GENISLIK - 37
en = DERINLIK - 50

# RAF (Üst Dolap)
boy = MODUL_GENISLIK - 37
en = DERINLIK - 40

# ARKALIK
boy = YUKSEKLIK - 18
en = MODUL_GENISLIK - 18

# ARKALIK (İÇERDE)
boy = YUKSEKLIK - 37
en = MODUL_GENISLIK - 37
```

### 12.2 Tersine Hesaplama (Ölçüden Modül)

```python
# ALT-ÜST'ten modül genişliği bul
# boy = modul - 36 → modul = boy + 36
modul_genislik = boy + 36

# RAF'tan modül genişliği bul
# boy = modul - 37 → modul = boy + 37
modul_genislik = boy + 37
```

### 12.3 Tolerans Kontrolü

```python
TOLERANS = 5  # mm

def check_match(actual, expected) -> bool:
    return abs(actual - expected) <= TOLERANS

# Örnek: 718mm ≈ 720mm (fark 2mm < 5mm tolerans)
check_match(718, 720)  # True
```

---

## 13. AYARLAR SİSTEMİ

### 13.1 Varsayılan Ayarlar

```python
default_settings = {
    # Dolap Ölçüleri
    "standart_yukseklik": 720,
    "standart_derinlik": 580,
    "ust_dolap_yukseklik": 720,
    "ust_dolap_derinlik": 330,
    "boy_dolap_yukseklik": 2100,
    "boy_dolap_derinlik": 580,
    
    # Düşüm Değerleri
    "yan_dusumu": 36,
    "raf_genislik_dusumu": 37,
    "raf_derinlik_alt_dolap": 50,
    "raf_derinlik_ust_dolap": 40,
    "sabit_derinlik_dusumu": 23,
    "arkalik_dusumu": 18,
    "arkalik_icerde_dusumu": 37,
    
    # Kalınlıklar
    "govde_kalinlik": 18,
    "cekmece_yan_kalinlik": 16,
    "arkalik_kalinlik": 8,
    "arkalik_max_kalinlik": 8,
    
    # Diğer
    "tolerans": 5,
    "kanalli_ayir": True
}
```

### 13.2 Ayarlar UI

```
Ayarlar Modal:
├── Genel Tab
│   ├── Standart Yükseklik: [720] mm
│   ├── Standart Derinlik: [580] mm
│   └── Tolerans: [5] mm
├── Üst Dolap Tab
│   ├── Yükseklik: [720] mm
│   └── Derinlik: [330] mm
├── Boy Dolap Tab
│   ├── Yükseklik: [2100] mm
│   └── Derinlik: [580] mm
├── Yedekleme Tab
│   ├── [Yedek Al] → JSON indir
│   └── [Yedek Yükle] → JSON yükle
└── Hakkında Tab
    └── CORE v3.5 bilgileri
```

---

## 14. HATA YÖNETİMİ

### 14.1 Backend Hata Yapısı

```python
# Başarılı yanıt
return {'success': True, 'data': ...}

# Hata yanıtı
return {'success': False, 'error': 'Hata mesajı'}

# Try-Catch pattern
try:
    result = do_something()
    return {'success': True, 'result': result}
except Exception as e:
    import traceback
    traceback.print_exc()
    return {'success': False, 'error': str(e)}
```

### 14.2 Frontend Hata Yakalama

```javascript
async function doSomething() {
    try {
        const result = await api('method_name', args);
        
        if (result.success) {
            showToast('success', 'Başarılı', 'İşlem tamamlandı');
        } else {
            showToast('error', 'Hata', result.error || 'Bilinmeyen hata');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('error', 'Hata', 'Bağlantı hatası!');
    }
}
```

### 14.3 Yaygın Hatalar ve Çözümleri

| Hata | Neden | Çözüm |
|------|-------|-------|
| "pandas kütüphanesi yüklü değil" | Eksik bağımlılık | `pip install pandas` |
| "Excel formatı tanınamadı" | Yanlış sütun isimleri | Sütun mapping kontrolü |
| "Dosya seçilmedi" | Kullanıcı iptal etti | Normal akış, hata değil |
| "Kayıt yeri seçilmedi" | Kullanıcı iptal etti | Normal akış, hata değil |
| "API metodu bulunamadı" | Api sınıfında eksik metod | Metodu ekle |

---

## 15. EXCEL ÇIKTI FORMATI

### 15.1 Yan Yana Tablo Yapısı

```
┌─────────────────────────────────────┬─────────────────────────────────────┐
│         GÖVDE PARÇALAR              │      İNCE PARÇALAR (ARKALIK)        │
├─────────────────────────────────────┼─────────────────────────────────────┤
│KALINLIK│MALZEME│BOY│EN│TİP    │ADET │KALINLIK│MALZEME│BOY│EN│TİP    │ADET │
├────────┼───────┼───┼──┼───────┼─────┼────────┼───────┼───┼──┼───────┼─────┤
│ 18     │LAM BYZ│720│580│YAN   │ 4   │ 8      │ARK 8MM│702│582│ARKALIK│ 4   │
│ 18     │LAM BYZ│564│579│ALT-ÜST│ 4   │ 8      │ARK 8MM│702│482│ARKALIK│ 2   │
│ 18     │LAM BYZ│563│530│RAF   │ 8   │        │       │   │   │       │     │
└────────┴───────┴───┴──┴───────┴─────┴────────┴───────┴───┴──┴───────┴─────┘
```

### 15.2 Kanallı Gösterimi

```
Excel'de parça tipi sütununda:
- Kanalsız: "ALT-ÜST"
- Kanallı:  "ALT-ÜST (K)"
```

### 15.3 Sıralama

```python
# Gövde: Malzeme → Kalınlık → Parça Tipi → Boy
body_df.sort_values(by=['MALZEME', 'KALINLIK', 'PARÇA TİPİ', 'BOY'])

# İnce: Malzeme → Parça Tipi → Boy
thin_df.sort_values(by=['MALZEME', 'PARÇA TİPİ', 'BOY'])
```

---

## 16. DEBUG VE GELİŞTİRME

### 16.1 Debug Modu

```python
# main.py sonunda
if __name__ == '__main__':
    debug = True  # False yaparak DevTools kapatılır
    
    window = webview.create_window(
        Config.APP_TITLE,
        str(Config.get_html_path()),
        js_api=api,
        width=Config.WINDOW_WIDTH,
        height=Config.WINDOW_HEIGHT
    )
    
    webview.start(debug=debug)  # debug=True → DevTools açık
```

### 16.2 Console Logları

```javascript
// Frontend'de
console.log('State:', state);
console.log('API result:', result);

// Backend'de
print(f"Column mapping: {mapping}")
print(f"Materials DB: {materials_db}")
```

### 16.3 Build Komutu

```bash
# PyInstaller ile build
python build.py

# Manuel build
pyinstaller --onedir --windowed --name CORE \
    --add-data "index.html;." \
    --add-data "CORE_LOGO.png;." \
    --icon=CORE_LOGO.ico \
    main.py
```

---

## 📝 HIZLI REFERANS

### Sık Kullanılan API Çağrıları

```javascript
await api('select_file')                              // Dosya seç
await api('analyze_file', 0)                          // Analiz et
await api('export_edited_results', body, thin, jobNo) // Kaydet
await api('save_material', 'MALZEME', 18)             // Malzeme ekle
await api('delete_history', [id])                     // İş sil
await api('get_stats')                                // İstatistikler
```

### Parça Tipi Formülleri (Özet)

```
YAN:           Yükseklik x Derinlik
ALT-ÜST:       (Genişlik-36) x (Derinlik-1)
SABİT:         (Genişlik-36) x (Derinlik-23)
RAF:           (Genişlik-37) x (Derinlik-50)
RAF (ÜST):     (Genişlik-37) x (Derinlik-40)
ARKALIK:       (Yükseklik-18) x (Genişlik-18)
ARKALIK İÇERDE:(Yükseklik-37) x (Genişlik-37)
```

### Standart Değerler

```
Alt Dolap:  720 x 580mm
Üst Dolap:  720 x 330mm
Boy Dolap:  2100 x 580mm
Tolerans:   ±5mm
```

---

**Son Güncelleme:** v3.5  
**Geliştirici Notu:** Bu dokümantasyon CORE v3.5 için tersine mühendislik ile oluşturulmuştur.
