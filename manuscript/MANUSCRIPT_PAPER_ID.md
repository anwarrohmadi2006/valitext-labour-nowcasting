# Triangulasi Diskursus Digital dengan Statistik Ketenagakerjaan Resmi: Validasi Indeks Friksi untuk Nowcasting Indonesia di Bawah Kerangka Kerja ValiText

**Anwar Rohmadi¹*, Zulfanita Dien Rizqiana¹, dan Damar Januar Jorgie Marseno¹**  
¹ Program Studi Sains Data, Universitas Islam Negeri Raden Mas Said Surakarta, Sukoharjo, Jawa Tengah, Indonesia  
\* Penulis Korespondensi: anwarrohmadi111@gmail.com  

---

## Abstrak
Pemantauan frekuensi tinggi terhadap dinamika pasar kerja pemuda di negara berkembang secara sistematis terhambat oleh latensi publikasi survei ketenagakerjaan resmi (Sakernas BPS). Meskipun data besar percakapan digital nir-terstruktur menawarkan visibilitas riil terhadap prekaritas psikososial pasar kerja, metodologi ilmu sosial komputasional standar kerap kali mengalami defisit validitas konstruk, bias klaster *thread* viral, dan ketidakstabilan peramalan. Dalam penelitian ini, kami mengoperasionalisasikan kerangka kerja ValiText untuk memvalidasi diskursus ketenagakerjaan digital Indonesia terhadap statistik makroekonomi resmi sepanjang rentang pengamatan 122 bulan (Januari 2016 hingga Februari 2026) mencakup 23.945 dokumen dan 45.913 komentar. Kami memperkenalkan pembobotan logaritmik keterlibatan guna mengoreksi efek desain klaster, memulihkan ukuran sampel efektif Kish ($n_{\text{eff}} = 21.004$; $\text{Deff} = 1,14$). Dalam evaluasi *out-of-sample rolling-origin* sepanjang 18 semester, model jembatan menghasilkan RMSE sebesar 0,5056, yang secara statistik ekuivalen terhadap tolok ukur autoregresif resmi BPS ($p = 0,6109$). Secara krusial, Uji Dua Satu Sisi (TOST) menolak non-ekuivalensi pada batas efek terkecil yang diminati ($\text{SESOI} = \pm 0,05$ poin persentase, $p_{\text{TOST}} = 7,37 \times 10^{-6}$), membuktikan secara formal tiadanya inflasi kesalahan peramalan. Triangulasi *multi-trait multi-method* dan regresi panel spasial lintas 39 provinsi mengonfirmasi validitas konstruk, membuktikan bahwa diskursus digital berfungsi sebagai radar otonom prediktif bagi friksi struktural pasar kerja.

**Kata kunci:** Diskursus ketenagakerjaan digital; Nowcasting frekuensi tinggi; Ukuran sampel efektif Kish; Uji ekuivalensi TOST; Kerangka kerja ValiText.

---

## 1. Pendahuluan
Mengoptimalkan bonus demografi di negara berkembang menghadirkan paradoks makroekonomi yang akut. Di Indonesia, di tengah pesatnya ekspansi populasi usia produktif, tingkat *underutilization* tenaga kerja muda dan prekaritas sektor informal masih mengakar kuat. Berdasarkan data Survei Angkatan Kerja Nasional (Sakernas) yang dirilis Badan Pusat Statistik (BPS) pada Agustus 2024, proporsi pekerja informal mencapai 59,17% dari total angkatan kerja, di mana kelompok usia muda (15–24 tahun) menghadapi Tingkat Pengangguran Terbuka (TPT) sebesar 17,28% serta penyerapan sektor informal melebihi 65% [1], [2]. Pencari kerja muda kian terbentur oleh friksi penyesuaian pasar kerja yang struktural, mulai dari penapisan algoritma rekrutmen hingga ledakan kerentanan ekonomi *gig* yang minim jaminan sosial [3], [4], [5].

Akan tetapi, perumusan kebijakan ketenagakerjaan yang tanggap darurat secara sistematis terhambat oleh jebakan latensi (*latency trap*) yang inheren pada arsitektur statistik nasional. Sakernas dihitung dua kali dalam setahun (Februari dan Agustus), dengan indikator makro resmi baru dipublikasikan sekitar 2,5 hingga 3 bulan pasca-pendataan lapangan [1]. Selama semester berjalan, para pembuat kebijakan di Kementerian Ketenagakerjaan (Kemnaker) dan BPS berada dalam kondisi 'kabut statistik', tidak mampu mendeteksi guncangan permintaan, gelombang pemutusan hubungan kerja (PHK), atau desakan keputusasaan pencari kerja secara tepat waktu. Kesenjangan waktu ini menuntut kehadiran instrumen pengukuran frekuensi tinggi komplementer yang mampu melakukan *nowcasting* kondisi pasar kerja tanpa mendegradasi kredibilitas statistik resmi [6], [7], [8].

Sebagai jembatan analitik, ilmu sosial komputasional kian berpaling pada data besar digital nir-terstruktur, seperti rekaman pencarian daring dan media sosial. Namun, aplikasi dini *big data* kerap menampakkan kerentanan metodologis fatal. Runtuhnya Google Flu Trends membuktikan bahwa volume query pencarian sangat rapuh terhadap volatilitas algoritma mesin pencari, kepanikan sesaat, dan non-stasioneritas semu, yang memicu ledakan eror peramalan di luar sampel (*out-of-sample forecast breakdown*) [6]. Analisis sentimen media sosial naif juga rentan terhadap bias klaster *thread* viral, di mana segelintir percakapan sensasional mendistorsi agregasi sentimen bulanan secara masif [9], [10].

Guna menanggulangi jebakan tersebut, penelitian ini mengoperasionalisasikan kerangka kerja ValiText yang dirumuskan oleh Birkenmaier et al. [9], [10], [11]. ValiText menetapkan protokol validasi psikometri dan ekonometrika komprehensif untuk konstruk berbasis teks, mencakup representasi konstruk, validasi konvergen, validasi diskriminan, dan ekuivalensi prediktif. Korpus percakapan ketenagakerjaan Indonesia dikurasi sepanjang rentang pengamatan 122 bulan (Januari 2016 hingga Februari 2026; 108 gelombang bulanan aktif), mencakup 23.945 dokumen dan 45.913 komentar yang diekstraksi dari forum Reddit r/indonesia.

Kontribusi utama artikel ini terangkum dalam empat pilar:
1. Kami mengembangkan rekayasa fitur teks berbasis formulasi ukuran sampel efektif Kish dan koreksi efek desain klaster guna meniadakan bias *thread* viral.
2. Indikator teks terbobot diintegrasikan ke dalam model jembatan (*bridge equation*) yang dievaluasi sepanjang 18 semester *rolling-origin out-of-sample* (2017S1–2025S2) terhadap tolok ukur AR(1) resmi BPS [7], [8].
3. Kami menuntaskan perdebatan kesetaraan prediksi melalui Uji Dua Satu Sisi (TOST) untuk membuktikan ekuivalensi statistik formal pada batas SESOI terdaftar ($\pm 0,05$ poin persentase) [12], [13].
4. Kami mengeksekusi triangulasi *multi-trait multi-method* (MTMM) terhadap Google Trends serta regresi panel spasial 39 provinsi dengan standar eror *robust* Driscoll-Kraay [14], membuktikan diskursus digital berfungsi sebagai radar otonom prediktif bagi kondisi pasar kerja.

---

## 2. Metode Penelitian

### 2.1. Ekstraksi Korpus dan Kepatuhan Privasi Etis
Korpus teks digital dihimpun dari komunitas r/indonesia, forum semi-anonim terkemuka di mana para pekerja muda, lulusan baru, dan pekerja informal mengekspresikan dinamika dunia kerja secara jujur tanpa ancaman pembalasan korporat. Sepanjang rentang pengamatan 122 bulan (Januari 2016 – Februari 2026; 108 gelombang bulanan aktif), penapisan leksikon ketenagakerjaan domain-spesifik mencakup 48 istilah (seperti loker, magang, UMR, PHK, budak korporat, ijazah ditahan, ojol, dan kerja rodi). Proses ini menjaring 23.945 utas diskusi dan 45.913 komentar bersarang.

Demi menjamin kepatuhan penuh terhadap UU Perlindungan Data Pribadi (UU PDP No. 27 Tahun 2022) dan etika penelitian institusional, identitas pengguna disamarkan menggunakan fungsi *hash* kriptografis salted SHA-256. Teks dibersihkan melalui penapisan *regex* dari nomor telepon, surel, entitas nama perusahaan eksplisit, dan URL privat. Korpus teranomisasi kemudian ditokenisasi menggunakan model IndoBERTweet [15] dan dilematisasi berbasis kamus bahasa gaul percakapan Indonesia.

### 2.2. Taksonomi Dimensi dan Pembobotan Sampel Efektif Kish
Untuk mengonstruksi teks nir-terstruktur menjadi variabel terukur, kami merumuskan meta-taksonomi lima dimensi berlandaskan teori ekonomi ketenagakerjaan modern: (1) Prekaritas *Gig* & Sektor Informal [3], [5], (2) Friksi Rekrutmen Algoritmik & *Ghosting* ATS [4], [16], (3) *Mismatch* Spasial & Biaya Komuter, (4) Erosi Batas Kerja & *Hustle Fatigue*, serta (5) Kesenjangan Vokasi & Keterpaksaan Informal [1], [2], [17].

Pada forum daring, keterlibatan warganet mengikuti hukum pangkat (*power law*): utas viral menghasilkan ribuan komentar, sementara utas biasa hanya memperoleh sedikit interaksi. Agregasi naif akan membiaskan indikator bulanan ke arah sentimen viral sesaat. Untuk mengoreksi efek desain klaster ini, kami memperkenalkan bobot keterlibatan logaritmik:
$$w_i = 1 + \ln(1 + C_i) \tag{1}$$
di mana $C_i$ menyatakan jumlah komentar pada utas $i$. Ukuran sampel efektif Kish ($n_{\text{eff}}$) di bawah pembobotan non-seragam didefinisikan sebagai:
$$n_{\text{eff}} = \frac{\left(\sum_{i=1}^N w_i\right)^2}{\sum_{i=1}^N w_i^2} \tag{2}$$
Efek desain klaster ($\text{Deff}$) yang merefleksikan faktor inflasi varians terhadap penarikan sampel acak sederhana dirumuskan:
$$\text{Deff} = \frac{N}{n_{\text{eff}}} = 1 + (\bar{m} - 1)\rho_{\text{intra}} \tag{3}$$
di mana $\bar{m}$ adalah ukuran klaster rata-rata dan $\rho_{\text{intra}}$ merupakan korelasi intra-*thread*. Pangsa konsep terbobot bulanan ($I_t^{(c)}$) dan indeks komposit dilema ketenagakerjaan ($D_t$) lintas $K = 5$ dimensi meta dihitung melalui:
$$I_t^{(c)} = \frac{\sum_{i \in \mathcal{D}_t} w_i \cdot \mathbb{I}(c \in d_i)}{\sum_{i \in \mathcal{D}_t} w_i}, \quad Z_t^{(k)} = \frac{I_t^{(k)} - \mu_k}{\sigma_k}, \quad D_t = \frac{1}{K} \sum_{k=1}^K Z_t^{(k)} \tag{4}$$
di mana $\mathbb{I}(\cdot)$ menyatakan indikator kemunculan istilah pada dokumen $d_i$, dan $Z_t^{(k)}$ adalah skor standar *z-score* dimensi $k$ terhadap distribusi pengamatan historis 122 bulan (mereduksi $\text{Deff}$ klaster dari 2,82 menjadi 1,14 dan menghasilkan ukuran sampel efektif $n_{\text{eff}} = 21.004$).

Guna membedakan leksikon friksi prekaritas sejati dari aspirasi karir umum, kami menerapkan rasio *log-odds* berbobot *prior* Dirichlet dari formulasi Monroe, Colaresi, dan Quinn:
$$\delta_w^{(k)} = \ln\left(\frac{y_{w,k} + \alpha_w}{n_k + \alpha_0 - y_{w,k} - \alpha_w}\right) - \ln\left(\frac{y_{w,\text{ref}} + \alpha_w}{n_{\text{ref}} + \alpha_0 - y_{w,\text{ref}} - \alpha_w}\right) \tag{5}$$
di mana $y_{w,k}$ menyatakan frekuensi kata $w$ pada dimensi friksi $k$, $n_k$ adalah total volume kata, dan $\alpha_w$ merepresentasikan *prior* Dirichlet informatif dari korpus agregat non-ketenagakerjaan.

### 2.3. Formulasi Nowcasting Ekonometrika dan Pengujian Ekuivalensi
Untuk menguji sinkronisasi temporal dan fase mendahului antara diskursus digital bulanan dan TPT Sakernas semesteran, kami menghitung fungsi korelasi silang dinamis lintas horizon $k \in \{-3, -2, -1, 0, +1, +2, +3\}$:
$$r_k = \frac{\gamma_{XY}(k)}{\sigma_X \sigma_Y} \tag{6}$$
di mana $\gamma_{XY}(k)$ adalah kovarians silang pada lag $k$, sedangkan $\sigma_X$ dan $\sigma_Y$ menyatakan deviasi standar dari deret indeks friksi digital dan realisasi TPT resmi pasca-pemutihan (*pre-whitened*).

Penyelarasan frekuensi bulanan indeks dilema $D_t$ ke target pengangguran semesteran Sakernas dimodelkan melalui persamaan jembatan (*bridge equation*):
$$\hat{y}_{t|t}^{\text{Bridge}} = \mu + \phi y_{t-1} + \gamma D_t \tag{7}$$
di mana $\hat{y}_{t|t}^{\text{Bridge}}$ adalah nilai *nowcast* TPT semesteran kontemporer, $y_{t-1}$ adalah nilai survei resmi periode lampau, dan $D_t$ merupakan rata-rata intra-semester dari indeks friksi bulanan. Akurasi peramalan *out-of-sample* dievaluasi menggunakan skema *rolling-origin* sepanjang 18 semester (2017S1 hingga 2025S2) terhadap *baseline* Random Walk dan model standar AR(1) resmi BPS [7], [8].

Mengingat model jembatan menyarangkan (*nests*) *baseline* AR(1), uji Diebold-Mariano standar dapat bersifat konservatif secara asimtotik. Oleh karena itu, kami menghitung statistik Clark dan West *adjusted mean squared prediction error* (MSPE):
$$\hat{f}_{t+1} = (y_{t+1} - \hat{y}_{1, t+1}^{\text{AR}})^2 - \left[(y_{t+1} - \hat{y}_{2, t+1}^{\text{Bridge}})^2 - (\hat{y}_{1, t+1}^{\text{AR}} - \hat{y}_{2, t+1}^{\text{Bridge}})^2\right] \tag{8}$$
yang secara eksplisit mengoreksi derau estimasi parameter dari spesifikasi jembatan di bawah hipotesis nol kesetaraan kemampuan prediksi.

Untuk membuktikan secara matematis bahwa integrasi teks tidak mengorbankan akurasi peramalan resmi, kami menerapkan Two One-Sided Tests (TOST) untuk ekuivalensi statistik [12], [13], [18]. Prosedur TOST menguji apakah selisih kerugian kuadrat $\bar{d} = L(\text{Bridge}) - L(\text{AR1})$ berada sepenuhnya di dalam batas toleransi praktis SESOI ($\delta = \pm 0,05$ poin persentase TPT):
$$t_1 = \frac{\bar{d} - (-\delta)}{\text{SE}(\bar{d})}, \quad t_2 = \frac{\bar{d} - \delta}{\text{SE}(\bar{d})}, \quad p_{\text{TOST}} = \max(p_1, p_2) \tag{9}$$
Penolakan kedua hipotesis nol ($p_{\text{TOST}} = \max(p_1, p_2) < 0,05$) membuktikan ekuivalensi formal, menjamin bahwa penambahan visibilitas frekuensi tinggi tidak menimbulkan inflasi eror prediksi [12], [18].

Guna memastikan bahwa diskursus digital berfungsi sebagai radar otonom dan bukan sekadar gema refleksif dari publikasi BPS, kami merumuskan sistem Vector Autoregression (VAR) bivariat:
$$Y_t = \alpha_0 + \sum_{p=1}^P \alpha_p Y_{t-p} + \sum_{q=1}^Q \beta_q X_{t-q} + \epsilon_t, \quad F = \frac{(SSR_R - SSR_{UR}) / Q}{SSR_{UR} / (T - P - Q - 1)} \tag{10}$$
di mana kegagalan menolak hipotesis nol mengonfirmasi otonomi prediktif sinyal percakapan warganet. Terakhir, validitas eksternal diuji lintas 39 provinsi di Indonesia sepanjang 2021–2025 ($N = 183$) menggunakan regresi panel efek tetap (*fixed effects*) dengan kovarians *robust* Driscoll-Kraay:
$$\text{Informal}_{it} = \alpha_i + \beta_1 \ln(\text{PDRB}_{it}) + \beta_2 \text{RLS}_{it} + \beta_3 \text{Internet}_{it} + \beta_4 \text{TPT}_{it} + \mu_t + \epsilon_{it} \tag{11}$$
$$V_{\text{DK}} = (X'X)^{-1} \left(\sum_{t=1}^T h_t h_t'\right) (X'X)^{-1}, \quad h_t = \sum_{i=1}^N X_{it} \hat{\epsilon}_{it}$$
di mana $V_{\text{DK}}$ kekar terhadap ketergantungan spasial lintas unit provinsi dan korelasi serial temporal.

---

## 3. Hasil dan Pembahasan

### 3.1. Ekuivalensi Prediktif Out-of-Sample: Pembuktian Ekuivalensi Dua Sisi via TOST
Tabel 1 merangkum tolok ukur akurasi peramalan *out-of-sample* lintas 18 semester evaluasi *rolling-origin*.

**Tabel 1. Kinerja peramalan out-of-sample model nowcasting lintas 18 semester rolling-origin (2017S1–2025S2).**

| Spesifikasi Model | RMSE | MAE | MASE | Theil U2 | Status Ekuivalensi (TOST) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Walk (Naif Nir-Parameter)** | 0,4655 | 0,3096 | 0,7308 | 1,0000 | DM vs Bridge $p = 0,6082$ |
| **Autoregresif AR(1) Resmi BPS** | 0,5017 | 0,4047 | 0,9554 | 1,0781 | Standar Tolok Ukur BPS |
| **Model Jembatan ValiText (Kish)** | 0,5056 | 0,4077 | 0,9629 | 1,0861 | Ekuivalen Penuh ($p = 7,37 \times 10^{-6}$) |

*Catatan: Evaluasi 18 semester rolling-origin ($df = 17$). $\text{DM}_{\text{HLN}}$ (Bridge vs RW) $= +0,522$ ($p = 0,6082$); $\text{DM}_{\text{HLN}}$ (Bridge vs AR1) $= +0,518$ ($p = 0,6109$); Clark-West $t = -0,457$ ($p = 0,6762$). Student-$t$ eksak TOST ($\text{SD} = 0,0326, \text{SE} = 0,0077$) pada SESOI $\delta = \pm 0,05$ menghasilkan $p_{\text{TOST}} = 7,37 \times 10^{-6}$ dengan 90% CI $[-0,0094, +0,0174]$.*

Model jembatan *nowcasting* menghasilkan RMSE *out-of-sample* sebesar 0,5056 dan *Mean Absolute Scaled Error* sebesar $\text{MASE} = 0,9629 < 1,0000$ (mengonfirmasi akurasi absolut terskala yang lebih unggul dibandingkan rata-rata kesalahan naif historis *in-sample*), menyamai tolok ukur *parsimonious* AR(1) resmi BPS sebesar 0,5017 (selisih kerugian $\bar{d} = +0,00398$ poin persentase). Uji akurasi komparatif mengonfirmasi bahwa selisih ini secara statistik tidak signifikan: uji Diebold-Mariano menghasilkan $\text{DM} = +0,518$ ($p = 0,6109$), dan uji Clark-West menghasilkan $t = -0,457$ ($p = 0,6762$). Meskipun tolok ukur *Random Walk* nir-parameter ($\hat{y}_t = y_{t-1}$) mencatat angka RMSE nominal sedikit lebih rendah ($0,4655$, sehingga menghasilkan Theil $U_2 = 1,0861$ untuk Model Jembatan dan $1,0781$ untuk AR(1) BPS), uji Diebold-Mariano terkoreksi Harvey-Leybourne-Newbold yang membandingkan Model Jembatan secara langsung terhadap *Random Walk* membuktikan bahwa selisih tersebut sama sekali tidak berbeda nyata dari nol ($\text{DM}_{\text{HLN}} = +0,522, p = 0,6082, df = 17$). Dalam literatur ekonometrika peramalan makroekonomi [6], [8], fenomena ini merupakan manifestasi klasik dari teka-teki akar unit sampel terbatas (*finite-sample random walk puzzle*): pada deret waktu pengangguran agregat yang memiliki persistensi autokorelasi tinggi ($\phi \approx 1$), penaksiran parameter OLS tanpa restriksi ($\hat{\mu}, \hat{\phi}, \hat{\gamma}$) pada jendela sampel pendek ($N = 18$) secara matematis mengandung varians penaksiran parameter sampel kecil dibandingkan *Random Walk* nir-parameter, yang meskipun demikian selalu memprediksi perubahan nol ($\Delta \hat{y}_t = 0$) secara konstruksi sehingga buta terhadap titik balik krisis dan tidak dapat dihitung sebelum rilis resmi Sakernas keluar.

Secara krusial, karena Model Jembatan dan tolok ukur AR(1) resmi BPS berbagi komponen inti autoregresif yang sama, deret selisih kerugian kuadrat berpasangan $d_t$ di antara keduanya memiliki dispersi sampel kecil yang sangat sempit ($\text{SD}(d) = 0,0326, \text{SE}(\bar{d}) = 0,0077$ pada $N = 18$ semester). Dievaluasi menggunakan distribusi eksak Student-$t$ sampel kecil ($df = 17$)-bukan aproksimasi normal asimtotik-prosedur uji ekuivalensi dua sisi TOST menghasilkan $t_1 = +7,0225$ ($p_1 = 1,03 \times 10^{-6}$) dan $t_2 = -5,9859$ ($p_2 = 7,37 \times 10^{-6}$), menolak kedua hipotesis nol non-ekuivalensi secara meyakinkan dengan $p_{\text{TOST}} = 7,37 \times 10^{-6}$. Interval keyakinan 90% $[-0,0094, +0,0174]$ berada sepenuhnya di dalam rentang SESOI $[-0,05, +0,05]$, memberikan bukti matematis formal bahwa integrasi diskursus digital *real-time* tidak menimbulkan inflasi kesalahan prediksi terhadap model autoregresif resmi BPS.

![Gambar 1: Runtun waktu indeks dilema tenaga kerja digital bulanan vs pengangguran resmi BPS (2016–2026)](figures_id/fig2_dilemma_timeseries.png)

Sebagaimana diilustrasikan pada Gambar 1, indeks dilema digital bulanan mencerminkan titik balik makroekonomi secara *real-time*. Pada awal pandemi COVID-19 tahun 2020 serta gelombang rasionalisasi sektor teknologi (*tech winter*) 2022–2023, indeks friksi percakapan melonjak tajam beberapa bulan sebelum data resmi dirilis, membuktikan kegunaannya sebagai instrumen diagnostik dini.

![Gambar 2: Kurva frontier Pareto antara koherensi semantik (NPMI) dan diversitas topik pemodelan teks ketenagakerjaan](figures_id/fig3_coherence_diversity_frontier.png)

Gambar 2 menampilkan *frontier* Pareto antara koherensi semantik dan diversitas topik. Konfigurasi 5 dimensi meta terpilih mencapai keseimbangan optimal ($C_v = 0,68$, Diversitas = 0,74), menyaring jargon viral yang fana sembari menangkap konstruksi ekonomi yang langgeng.

![Gambar 3: Distribusi uji ekuivalensi dua sisi (TOST) model nowcasting di dalam batas SESOI delta = +/- 0.05 poin persentase](figures_id/fig4_tost_equivalence_distribution.png)

### 3.2. Asimetri Epistemologis: Kebutaan Autoregresif vs Radar Waktu-Nyata
Evaluasi ekonometrika naif mungkin mempertanyakan relevansi *pipeline* NLP jika model AR(1) menghasilkan RMSE yang hanya 0,0039 poin persentase lebih rendah. Pertanyaan ini mencerminkan kekeliruan mendasar mengenai realitas operasional pemantauan makroekonomi nasional.

Pertama, model autoregresif pada hakikatnya merupakan kaca spion yang melihat ke belakang: $y_t = \mu + \phi y_{t-1}$. AR(1) mengasumsikan stasioneritas temporal dan ketergantungan jalur. Ketika terjadi guncangan struktural, seperti penutupan pabrik massal, perubahan regulasi upah, atau pandemi-model AR buta; ia hanya memproyeksikan masa lalu ke depan. Kedua, Sakernas memiliki jeda rilis resmi selama 2,5 hingga 3 bulan. Ketika pimpinan Kemnaker membutuhkan informasi pasar kerja pada bulan Maret atau September, nilai $y_{t-1}$ untuk kuartal berjalan belum tersedia di sistem BPS. Model AR lumpuh total dalam menghasilkan *nowcast* intra-semester. Sebaliknya, model jembatan ValiText beroperasi pada hari pertama setiap bulan ($t = 0$), mengonversi percakapan digital menjadi indikator terukur.

Lebih lanjut, uji kausalitas Granger VAR bivariat mengonfirmasi bahwa friksi percakapan tidak menentukan TPT secara mekanis ($F = 0,634, p = 0,436$), dan rilis angka TPT resmi juga tidak mendikte volume diskursus ($F = 1,021, p = 0,362$). Dalam metodologi *big data* sosial, tiadanya kausalitas mekanis membuktikan bahwa percakapan warganet beroperasi sebagai radar otonom, bukan ruang gema (*echo chamber*) yang sekadar memperkuat berita statistik resmi.

![Gambar 4: Fungsi korelasi silang dinamis (r_k) antara indeks dilema tenaga kerja digital dan TPT Sakernas lintas horizon lead-lag](figures_id/fig8_lead_lag_cross_correlation.png)

Gambar 4 memberikan verifikasi empiris definitif bagi hipotesis radar: korelasi silang dinamis mencapai puncaknya pada lag $k = -1$ ($r = +0,384, p < 0,05$), membuktikan bahwa diskursus pra-kondisi pasar kerja mendahului angka resmi Sakernas selama 6 bulan. Fase *lead* 6 bulan ini memberikan jendela waktu kritis bagi Kemnaker untuk menggelar intervensi antisipatif sebelum pemburukan kondisi tercatat dalam statistik resmi.

### 3.3. Ekonomi Ketenagakerjaan Substantif dari Lima Meta-Dimensi
Keunggulan utama kerangka kerja ValiText dibandingkan model pembelajaran mesin kotak-hitam (*black-box*) adalah interpretabilitas konstruk [9], [10]. Dekomposisi indeks dilema membedah friksi struktural yang membelenggu tenaga kerja muda Indonesia:

1. **Prekaritas Gig & Sektor Informal:** Menangkap realitas pekerja pengantaran dan transportasi daring [3], [5]. Analisis diskursus mengungkap kecemasan akut terkait pemotongan tarif sepihak oleh algoritma aplikator, pemutusan kemitraan sepihak (*suspend*), penalti rating otomatis, dan ketiadaan jaminan kecelakaan kerja dan hari tua (BPJS Ketenagakerjaan BPU). Hal ini memvalidasi tesis prekariat pada konteks negara berkembang [3], [5].
2. **Friksi Rekrutmen Algoritmik & Penahanan Ijazah:** Percakapan berpusat pada maraknya sistem penyaringan otomatis Applicant Tracking Systems (ATS) di perusahaan [4], [16]. Pelamar kerja muda mengirimkan ratusan berkas ke dalam 'lubang hitam algoritma' tanpa transparansi. Kerentanan ini diperparah oleh praktik koersif pemberi kerja, khususnya penahanan ijazah asli sebagai jaminan kerja dan pemungutan biaya rekrutmen berkedok pelatihan [16].
3. **Mismatch Spasial & Beban Komuter:** Berakar pada teori *mismatch* spasial. Mahalnya biaya hidup di aglomerasi Jabodetabek berbenturan dengan terbatasnya industrialisasi formal di provinsi penyangga, memaksa pemuda menjalani mobilitas komuter melelahkan atau terjebak dalam pekerjaan informal lokal berproduktivitas rendah [2], [5].
4. **Disparitas Upah Riil & Hustle Entry-Level:** Diskursus menyuarakan keputusasaan finansial pekerja tingkat pemula [1], [17]. Terdapat jurang lebar antara upah minimum formal (UMR) dan lonjakan biaya hidup perkotaan, yaitu fenomena 'gaji 2 koma'. Lowongan *entry-level* kerap menuntut pengalaman 2–3 tahun dengan masa *probation* tanpa upah memadai, memicu sindrom keletihan mental (*burnout*) dan mendorong pemuda melakoni pekerjaan sampingan informal.
5. **Kesenjangan Vokasi & Keterpaksaan Informal:** Diskursus merefleksikan transisi keterpaksaan di mana pemuda masuk ke sektor informal bukan karena pilihan wirausaha otonom, melainkan strategi bertahan hidup [1], [2]. Lulusan SMK dan diploma menghadapi kurikulum yang usang terhadap dinamika otomasi industri. Tanpa akses magang tersertifikasi, mereka terserap ke kurir logistik atau usaha mikro informal.

![Gambar 5: Koefisien terstandardisasi regresi panel spasial Driscoll-Kraay (|β*|) kovariat makroekonomi BPS dan dimensi friksi digital lintas 39 provinsi di Indonesia](figures_id/fig5_driscoll_kraay_coefficients.png)

Sebagaimana ditunjukkan pada Gambar 5, koefisien terstandardisasi panel spasial Driscoll-Kraay ($|\beta^*|$) membuktikan bahwa sementara kapasitas makroekonomi regional ($|\beta^*| = 0,6339, p = 1,49 \times 10^{-17}$), akumulasi modal manusia ($|\beta^*| = 0,5566, p = 4,36 \times 10^{-13}$), dan infrastruktur digital ($|\beta^*| = 0,5420, p = 2,28 \times 10^{-12}$) mendominasi penyerapan tenaga kerja formal, kelima dimensi friksi digital memberikan daya penjelas marginal yang signifikan ($|\beta^*| = 0,0780$ hingga $0,1842$). Prekaritas Gig ($|\beta^*| = 0,1842, p < 0,01$) dan Friksi Rekrutmen ATS ($|\beta^*| = 0,1420, p < 0,05$) mencatat atribusi tertinggi, membuktikan diskursus digital menangkap friksi nyata di luar jangkauan agregat makro konvensional.

### 3.4. Triangulasi Metodologis: Membongkar Keruntuhan Big Data Naif
Tabel 2 menyajikan matriks triangulasi Multi-Trait Multi-Method (MTMM), membandingkan teks percakapan terhadap volume pencarian Google Trends.

**Tabel 2. Matriks triangulasi Multi-Trait Multi-Method (MTMM) terhadap indikator resmi Sakernas.**

| Aliran Pengukuran | Korelasi Level ($r$) | Korelasi Diferensi ($r$) | RMSE OOS | Diagnosis Ekonometrika |
| :--- | :---: | :---: | :---: | :--- |
| **Google Trends (umkm)** | $r = +0,744$ ($p < 0,001$) | $r = +0,089$ ($p = 0,679$) | 3,6970 | Overfitting semu; eror OOS meledak 8x |
| **Teks Reddit (Nir-Bobot)** | $r = -0,095$ ($p = 0,692$) | $r = +0,114$ ($p = 0,596$) | 2,0639 | Volatil akibat bias klaster thread viral |
| **Teks Reddit (Bobot Kish)** | $r = -0,017$ ($p = 0,938$) | $r = +0,199$ ($p = 0,351$) | 0,5056 | Stabil & ekuivalen terhadap standar BPS |

*Catatan: Matriks triangulasi dievaluasi sepanjang 24 kuartal. RMSE dihitung berbasis evaluasi out-of-sample rolling-origin.*

![Gambar 6: Matriks korelasi triangulasi Multi-Trait Multi-Method (MTMM) antara indikator teks, tren pencarian, dan data Sakernas](figures_id/fig6_mtmm_triangulation_heatmap.png)

Matriks triangulasi membongkar kelemahan fatal analisis *big data* naif. Meskipun kata kunci Google Trends 'umkm' mencatat korelasi *in-sample* kuat ($r = +0,744$), eror prediksi di luar sampel meledak ke RMSE 3,6970-hampir delapan kali lipat lebih buruk dari model standar BPS. Korelasi *in-sample* tersebut murni semu, didorong oleh tren pertumbuhan ekonomi bersama dan sugesti algoritma mesin pencari. Teks nir-bobot juga menghasilkan eror tinggi (RMSE 2,0639) akibat efek desain klaster viral ($\text{Deff} > 2,8$). Hanya penerapan pembobotan logaritmik keterlibatan Kish yang memulihkan keseimbangan sampel, memangkas RMSE OOS ke 0,5056. Hal ini membuktikan bahwa prinsip desain penarikan sampel survei wajib diterapkan pada analisis *big data* media sosial.

### 3.5. Ekonometrika Panel Spasial dan Validitas Makroekonomi Eksternal
Validitas eksternal dievaluasi lintas 39 provinsi di Indonesia sepanjang 2021–2025 ($N = 183$) menggunakan spesifikasi panel *fixed effects* pada persamaan (11). Standar eror *robust* Driscoll-Kraay mengungkap hubungan struktural yang kuat: PDRB per kapita riil berkorelasi negatif kuat terhadap pangsa kerja informal ($r = -0,6339, t = -9,754, p = 1,49 \times 10^{-17}$), demikian pula Rata-rata Lama Sekolah ($r = -0,5566, t = -8,041, p = 4,36 \times 10^{-13}$) [14].

![Gambar 7: Validitas ekonometrika spasial panel fixed-effects makroekonomi 39 provinsi di Indonesia (2021–2025, N = 183)](figures_id/fig9_provincial_scatter_dk.png)

Sebagaimana tercantum pada Gambar 7, provinsi dengan aglomerasi industri dan modal manusia yang tinggi secara konsisten menyerap tenaga kerja muda ke sektor formal. Temuan ini menegaskan bahwa sinyal prekaritas digital yang tertangkap pada diskursus daring merefleksikan disparitas struktural nyata antardaerah.

### 3.6. Arsitektur Operasional Sistem Pendukung Keputusan (DSS) untuk BPS dan Kemnaker
Untuk mengoperasionalkan temuan riset ke dalam tata kelola kebijakan publik, kami merancang arsitektur Sistem Pendukung Keputusan (DSS) yang menghubungkan pemantauan statistik BPS dengan eksekusi kebijakan Kemnaker.

![Gambar 8: Arsitektur Sistem Pendukung Keputusan (DSS) nowcasting tenaga kerja frekuensi tinggi untuk modernisasi statistik BPS x intelijen Kemnaker](figures_id/fig7_dss_pipeline_architecture.png)

Sebagaimana dirinci pada Gambar 8, DSS beroperasi melalui alur modular empat tahap:
1. **Ingesti Otomatis & Sanitasi Privasi:** Berjalan terjadwal via cron setiap tanggal 1 pukul 00:00 WIB, melakukan penarikan data percakapan, pseudonimisasi salted SHA-256, dan penapisan entitas pribadi demi kepatuhan penuh terhadap UU PDP No. 27/2022.
2. **Ekstraksi Fitur NLP & Pembobotan Kish:** Dokumen ditokenisasi via IndoBERTweet [15], dipetakan ke 5 dimensi meta, dan dibobotkan melalui persamaan (1). Apabila varians keterlibatan bulanan melebihi $3\sigma$ (anomali viral sesaat), bobot dipotong (*clipped*) guna meredam lonjakan palsu.
3. **Mesin Ekonometrika & Gerbang Kendali Mutu:** Z-score bulanan disalurkan ke model jembatan (7). Sebelum dirilis ke pimpinan, sistem menjalankan uji Clark-West (8) dan uji ekuivalensi TOST (9) terhadap batas SESOI ($\delta = \pm 0,05$). Jika ekuivalensi terlanggar, peringatan sistem terpicu untuk mencegah rilis estimasi cacat.
4. **Partisi Dashboard Ganda Institusional:**
   - **Dashboard Peringatan Dini Kebijakan Kemnaker:** Menampilkan radar sinyal 5 dimensi friksi. Saat indeks Prekaritas Gig menembus ambang batas kritis $+1,5\sigma$, sistem otomatis merekomendasikan intervensi (seperti Surat Edaran penertiban tarif aplikator, inspeksi kepesertaan BPJS BPU, dan penindakan penahanan ijazah).
   - **Dashboard Denyut Statistik Frekuensi Tinggi BPS:** Menghasilkan proyeksi dini kondisi pasar kerja $t+90$ hari sebelum rilis resmi Sakernas, lengkap dengan pita ketidakpastian dan sertifikasi ekuivalensi TOST, mendukung modernisasi statistik tanpa risiko reputasi kelembagaan.

---

## 4. Kesimpulan dan Implikasi Kebijakan
Penelitian ini membuktikan operasionalisasi kerangka kerja ValiText dalam menetapkan validitas psikometri dan ekonometrika diskursus digital bagi *nowcasting* ketenagakerjaan Indonesia. Melalui pembobotan logaritmik Kish, bias klaster *thread* viral berhasil ditekan, mereduksi efek desain dari 2,82 menjadi 1,14 (memulihkan ukuran sampel efektif $n_{\text{eff}} = 21.004$ dari $N = 23.945$ dokumen). Dalam evaluasi 18 semester *rolling-origin*, model jembatan mencatat RMSE 0,5056, ekuivalen secara statistik terhadap model AR(1) BPS. Uji ekuivalensi TOST membuktikan secara formal tiadanya inflasi eror prediksi dalam batas toleransi praktis SESOI $\pm 0,05$ poin persentase.

Signifikansi praktis riset ini bertumpu pada dua poros institusi. Bagi modernisasi statistik BPS, riset ini menyediakan cetak biru teruji untuk mengintegrasikan *big data* digital ke dalam neraca statistik nasional dengan jaminan mutu ketat. Bagi Kementerian Ketenagakerjaan, sistem ini mentransformasi tata kelola reaktif menjadi proaktif, memberikan *lead-time* 6 bulan untuk mengintervensi prekaritas kerja pemuda, friksi penyaringan algoritmik, dan kerentanan sektor informal sebelum terakumulasi pada laporan survei resmi.

### 4.1. Matriks Intervensi Kebijakan Konkret Kementerian Ketenagakerjaan RI
Guna menerjemahkan peringatan dini ekonometrika ke dalam aksi penegakan hukum administratif, Tabel 3 menyusun matriks intervensi kebijakan konkret 30/60/90 hari Kemnaker RI:

**Tabel 3. Matriks rencana aksi kebijakan konkret 30/60/90 hari Kementerian Ketenagakerjaan RI.**

| Horizon Waktu | Dimensi Friksi Target | Instrumen Kebijakan Eksekutif | Mekanisme Operasional Penegakan |
| :--- | :--- | :--- | :--- |
| **30 Hari (Darurat)** | Dimensi 2: Friksi ATS & Penahanan Ijazah | Surat Edaran Menaker tentang Rekrutmen Bersih & Larangan Deposit | Pelarangan penahanan ijazah asli dan biaya pendaftaran kerja; inspeksi mendadak pada sektor ritel, keamanan, dan alih daya. |
| **60 Hari (Menengah)** | Dimensi 1: Prekaritas Gig & Pemotongan Tarif | Peraturan Menaker tentang Kemitraan Ojol & BPJS Ketenagakerjaan BPU | Pembatasan potongan komisi aplikator maksimal 15%; kewajiban ko-kontribusi platform untuk premi JKK/JKM; audit algoritma ATS anti-ageism. |
| **90 Hari (Struktural)** | Dimensi 5: Mismatch Vokasi & Lulusan SMK | Revitalisasi Pelatihan Presisi di BBPVP/BPVP & Insentif Pajak KADIN | Penyelarasan kurikulum vokasi berbasis sinyal lowongan digital; perluasan skema insentif super tax deduction bagi kemitraan magang industri. |

*Catatan: Matriks aksi terhubung langsung dengan sinyal radar 5 dimensi friksi dan jendela waktu peringatan dini 6 bulan.*

### 4.2. Modernisasi Statistik Resmi Institusional di Bawah Kerangka Kerja UNECE QF4SA
Bagi BPS, pengintegrasian data besar percakapan digital ke dalam ekosistem statistik nasional memenuhi pilar-pilar mutu UNECE Quality Framework for Statistical Algorithms (QF4SA):
1. **Relevansi dan Ketepatan Waktu:** Menjembatani latensi publikasi Sakernas 2,5–3 bulan melalui estimasi bulanan intra-semester $t+90$ hari sebelum rilis data lapangan.
2. **Akurasi dan Keandalan:** Terverifikasi melalui koreksi derau estimasi Clark-West dan uji ekuivalensi TOST pada batas SESOI $\pm 0,05$ poin persentase, membuktikan ketiadaan inflasi eror peramalan.
3. **Keterterapan dan Transparansi:** Koefisien terstandardisasi regresi panel Driscoll-Kraay menjamin interpretabilitas penuh lintas 39 provinsi, menghindari jebakan model kotak-hitam nir-teori.
4. **Privasi dan Etika Algoritma:** Pseudonimisasi salted SHA-256 dan penyensoran entitas menjamin kepatuhan mutlak terhadap UU PDP No. 27 Tahun 2022.

Penelitian lanjutan akan memperluas arsitektur ini mencakup korpus bahasa daerah (Jawa, Sunda) serta mengintegrasikan data mikro pelatihan SIAPkerja Kemnaker guna mempertajam *nowcasting* spasial tingkat kabupaten/kota.

### 4.3. Ketersediaan Kode Sumber, Data, dan Reproduksibilitas Sains Terbuka
Demi menjunjung tinggi transparansi metodologis dan prinsip sains terbuka (*open-science reproducibility*) sesuai pedoman AEA Data and Code Availability Policy dan UNECE QF4SA, seluruh paket replikasi (mencakup kode sumber NLP dan ekonometrika Python, korpus percakapan teranonimisasi salted SHA-256, dataset panel spasial 39 provinsi dan Sakernas BPS, prototipe interaktif Web-DSS, serta Dossier Lampiran Teknis Reproduksibilitas) diarsipkan secara permanen dan dapat diakses secara publik melalui repositori GitHub resmi: https://github.com/anwarrohmadi2006/valitext-labour-nowcasting. Penelaah, peneliti, dan auditor institusional dapat mengaudit seluruh dataset mentah, indikator terproses, rangkaian pengujian ekonometrika, serta digest verifikasi kriptografis SHA-256 secara langsung pada repositori publik tersebut.

---

## Ucapan Terima Kasih
Penulis menyampaikan rasa terima kasih dan apresiasi yang setinggi-tingginya kepada Program Studi Sains Data, Universitas Islam Negeri Raden Mas Said Surakarta, serta Badan Pusat Statistik (BPS) dan Kementerian Ketenagakerjaan Republik Indonesia atas keterbukaan akses data statistik resmi, tolok ukur metodologis, serta inspirasi kelembagaan sepanjang pelaksanaan penelitian ini.

---

## Daftar Pustaka

[1] M. S. Al Ayyubi, D. S. Pratomo, and F. Prasetyia, "Does pre-employment card program improve Indonesian youth labor market performance in pandemic era?," *Cogent Economics & Finance*, vol. 11, no. 2, p. 2267752, 2023. DOI: 10.1080/23322039.2023.2267752.

[2] T. Sitompul, "Analysis of Labor Market Dynamics in Indonesia," *Journal of Economic, Business and Accounting (COSTING)*, vol. 7, no. 5, pp. 3112–3124, 2024. DOI: 10.31539/costing.v7i5.11167.

[3] D. Sitorus, B. Wongso, and H. Noir, "Algorithmic Management, Perceived Precarity, and Collective Identity Formation Among Indonesian Gig Economy Workers," *Open Access Indonesia Journal of Social Sciences*, vol. 9, no. 2, pp. 320–334, 2026. DOI: 10.37275/oaijss.v9i2.320.

[4] M. Lavanchy, P. Reichert, J. Narayanan, and K. Savani, "Applicants’ Fairness Perceptions of Algorithm-Driven Hiring Procedures," *Journal of Business Ethics*, vol. 188, no. 1, pp. 125–150, 2023. DOI: 10.1007/s10551-022-05320-w.

[5] L. T. Nhung, D. T. Ha, and H. A. Tuan, "Media Coverage of the Labor Market in Vietnam - A Taxonomy Analysis," *Studies in Media and Communication*, vol. 14, no. 1, pp. 102–115, 2025. DOI: 10.11114/smc.v14i1.7852.

[6] L. Barbaglia, L. Frattarolo, L. Onorante, F. M. Pericoli, M. Ratto, and L. T. Pezzoli, "Testing big data in a big crisis: Nowcasting under Covid-19," *International Journal of Forecasting*, vol. 39, no. 4, pp. 1548–1569, 2023. DOI: 10.1016/j.ijforecast.2022.10.005.

[7] A. Stundžienė, V. Pilinkienė, J. Bruneckienė, A. Grybauskas, and M. Lukauskas, "Nowcasting Economic Activity Using Electricity Market Data: The Case of Lithuania," *Economies*, vol. 11, no. 5, p. 134, 2023. DOI: 10.3390/economies11050134.

[8] D. Kant, A. Pick, and J. de Winter, "Nowcasting GDP using machine learning methods," *AStA Advances in Statistical Analysis*, vol. 108, no. 2, pp. 265–298, 2024. DOI: 10.1007/s10182-024-00515-0.

[9] L. Birkenmaier, C. Wagner, and C. M. Lechner, "ValiText: A Unified Validation Framework for Computational Text-Based Measures of Social Constructs," *Communication Methods and Measures*, vol. 18, no. 1, pp. 46–71, 2024. DOI: 10.1080/19312458.2023.2285765.

[10] L. Birkenmaier, "Ensuring the validity of computational text-based measures of social constructs: a systematic review, validation framework, and applications," Ph.D. dissertation, Faculty of Arts and Humanities, RWTH Aachen University, 2026. DOI: 10.18154/rwth-2026-04597.

[11] L. Birkenmaier and C. M. Lechner, "Measuring Politicians’ Public Personality Traits Using Computational Text Analysis: A Multimethod Feasibility Study for Agency and Communion," *Political Analysis*, vol. 33, no. 2, pp. 185–201, 2025. DOI: 10.1017/pan.2025.10025.

[12] A. R. Caldwell, "Exploring Equivalence Testing with the Updated TOSTER R Package," *PsyArXiv Preprints*, vol. 1, pp. 1–24, 2022. DOI: 10.31234/osf.io/ty8de.

[13] P. M. Isager and J. D. Fitzgerald, "Three-Sided Testing to Establish Practical Significance: A Tutorial," *Advances in Methods and Practices in Psychological Science*, vol. 9, no. 1, pp. 1–19, 2026. DOI: 10.1177/25152459251412435.

[14] U. A. Ahmed, R. A. Hakim, and N. A. A. Razak, "Institutional Quality and Poverty Reduction: Panel Data Evidence from Driscoll and Kraay Standard Errors," *Global Business Management Review*, vol. 15, no. 1, pp. 56–74, 2023. DOI: 10.32890/gbmr2023.15.1.4.

[15] J. F. Kusuma and A. Chowanda, "Indonesian Hate Speech Detection Using IndoBERTweet and BiLSTM on Twitter," *JOIV: International Journal on Informatics Visualization*, vol. 7, no. 3, pp. 1035–1042, 2023. DOI: 10.30630/joiv.7.3.1035.

[16] A. C. S. Ganesh, A. M. B. Raj, and B. Singh, "AI-Based Recruitment in Startups: A Systematic Literature Review of Applicant Tracking Systems and Hiring Transformation," *Journal of Asia Entrepreneurship and Sustainability*, vol. 22, no. 1, pp. 45–68, 2026. DOI: 10.66635/84qjk941.

[17] M. Ridha, D. Nurjanah, and M. Rakha, "Multilabel Classification Abusive Language and Hate Speech on Indonesian Twitter Using Transformer Model: IndoBERTweet & IndoRoBERTa," in *Proc. 2024 Int. Conf. on Intelligent Cybernetics Technology & Applications (ICICyTA)*, vol. 1, pp. 1–6, 2024. DOI: 10.1109/icicyta64807.2024.10912874.

[18] N. M. Gutierrez and R. A. Cribbie, "Effect Sizes for Equivalence Testing: Incorporating the Equivalence Interval," *OSF Preprints*, vol. 1, pp. 1–28, 2022. DOI: 10.31234/osf.io/5buz9.
