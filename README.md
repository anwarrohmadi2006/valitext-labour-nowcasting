# Triangulating Digital Discourse with Official Labour Statistics: Validating Friction Indices for Indonesian Nowcasting under the ValiText Framework

**Anwar Rohmadi¹, Zulfanita Dien Rizqiana¹, Damar Januar Jorgie Marseno¹**  
¹ Data Science Study Program, Universitas Islam Negeri Raden Mas Said Surakarta, Sukoharjo, Central Java, Indonesia  
Corresponding author: [anwarrohmadi111@gmail.com](mailto:anwarrohmadi111@gmail.com)

---

## Overview

This repository contains the data, econometric scripts, and documentation for the paper *"Triangulating Digital Discourse with Official Labour Statistics: Validating Friction Indices for Indonesian Nowcasting under the ValiText Framework"*, prepared for the **Joint International Conference 2026 (2nd IFLP & 4th ICDSOS)**.

### Summary of Empirical Findings
- **Corpus & Observation Window:** 122-month observation window (January 2016 – February 2026; 108 active monthly waves), $N = 23,945$ labour-filtered thread submissions and $45,913$ nested comments from `r/indonesia`.
- **Kish Design-Effect Adjustment:** Logarithmic engagement weighting $w_i = 1 + \ln(1 + C_i)$ reduces thread-clustering design effects from $\text{Deff} = 2.82$ to $\text{Deff} = 1.14$, yielding an effective sample size of $n_{\text{eff}} = 21,004$.
- **Rolling-Origin Out-of-Sample Nowcasting (18 Semesters, 2017S1–2025S2):**
  - Random Walk (Baseline): $\text{RMSE} = 0.4655$, $\text{MAE} = 0.3096$
  - Official BPS Autoregressive $\text{AR}(1)$: $\text{RMSE} = 0.5017$, $\text{MAE} = 0.4047$
  - ValiText Bridge Model (Kish Weighted): $\text{RMSE} = 0.5056$, $\text{MAE} = 0.4077$ (Diebold-Mariano HLN $p = 0.6109$, Clark-West $p = 0.6762$)
- **Statistical Equivalence (TOST):** Within pre-registered smallest effect sizes of interest ($\text{SESOI} = \pm 0.05$ percentage points), $t_1 = +7.0225$, $t_2 = -5.9859$, $p_{\text{TOST}} = 7.37 \times 10^{-6}$, 90% CI $[-0.0094, +0.0174]$.
- **Provincial Spatial Panel Regressions (39 Provinces, 2021–2025, $N = 183$):** Fixed-effects estimation with Driscoll-Kraay standard errors:
  - Log Regional GDP per Capita ($\ln \text{PDRB}$): $r = -0.6339$ ($t = -9.754, p = 1.49 \times 10^{-17}$)
  - Mean Years of Schooling ($\text{RLS}$): $r = -0.5566$ ($t = -8.041, p = 4.36 \times 10^{-13}$)
  - Household Internet Penetration ($\text{Internet}$): $r = -0.5420$ ($t = -7.746, p = 2.28 \times 10^{-12}$)

---

## Repository Structure

```text
valitext-labour-nowcasting/
├── code/
│   ├── empirical_rigor_tests.py     # Econometric test suite (TOST, DM, Clark-West, VAR, Panel DK)
│   ├── nowcast_v2.py                # 18-semester rolling-origin bridge nowcasting model
│   ├── jev_index_validation.py      # ValiText construct & convergent/discriminant validation
│   ├── convergent_validation.py     # Multi-Trait Multi-Method (MTMM) triangulation
│   ├── generate_clean_figures.py    # Script to generate all 8 manuscript figures (300 DPI)
│   ├── generate_dss.py              # Script to build the standalone Web-DSS dashboard
│   └── src/genz_informal/           # Core Python modules for text preprocessing and panel estimation
├── data/
│   ├── raw/
│   │   ├── targeted_pull_v2.jsonl   # Salted SHA-256 Reddit labour threads (8.77 MB, N = 23,945 docs)
│   │   ├── comments_full.jsonl      # Salted SHA-256 nested comments (24.48 MB, 45,913 comments)
│   │   ├── bps_labour_long.csv      # Official BPS Sakernas open unemployment & informality series
│   │   ├── bps_indicators.csv       # Official BPS regional macroeconomic indicators
│   │   └── gtrends_monthly.csv      # Google Trends monthly search volume series
│   └── processed/
│       ├── panel_provinsi.csv       # Merged 39-province panel dataset (2021–2025, N = 183)
│       ├── dilemma_index_jev_monthly_v2_tw.csv  # Monthly Kish-weighted labour friction index
│       └── topic_keywords.json      # Five-dimensional taxonomy dictionary
├── figures/                         # Publication figures (300 DPI PNG)
├── manuscript/
│   ├── Manuscript_IFLP_ICDSOS_2026_Labor_Nowcast.docx            # Main Manuscript (DOCX)
│   ├── Technical_Appendix_GitHub_Reproducibility_Report.docx     # Technical Appendix (DOCX)
│   ├── MANUSCRIPT_PAPER.md                                       # Main Manuscript (Markdown)
│   └── TECHNICAL_APPENDIX_GITHUB_REPORT.md                       # Technical Appendix (Markdown)
└── outputs/
    ├── empirical_rigor_results.json # Summary statistics and test outputs
    ├── convergent_validation.json   # MTMM correlation and RMSE comparison
    └── dss_dashboard.html           # Interactive Web Decision Support System (DSS)
```

---

## Dataset & Script Checksums (SHA-256)

| File Path | Size | Scope | SHA-256 (First 16 Hex) | Description |
| :--- | :---: | :---: | :---: | :--- |
| `data/raw/targeted_pull_v2.jsonl` | 8.77 MB | 23,945 docs | `664a1ea97a471d85` | Anonymized Reddit submissions (2016–2026) |
| `data/raw/comments_full.jsonl` | 24.48 MB | 45,913 comments | `3e06b99bf1536052` | Anonymized nested comments ($n_{\text{eff}} = 21,004$) |
| `data/raw/bps_labour_long.csv` | 108.9 KB | 2,574 rows | `9eb91ea512126d62` | BPS Sakernas TPT & informality series |
| `data/raw/bps_indicators.csv` | 815.3 KB | 6,969 rows | `aaf2b675f6787e2c` | BPS regional covariates ($\ln\text{PDRB}$, RLS, Internet) |
| `data/processed/panel_provinsi.csv` | 16.12 KB | 183 obs | `568af170ff02f128` | 39-province panel dataset (2021–2025) |
| `data/processed/dilemma_index_jev_monthly_v2_tw.csv` | 20.77 KB | 108 waves | `c732f81e850d1415` | Monthly Kish-weighted friction index ($D_t$) |
| `code/empirical_rigor_tests.py` | 13.12 KB | 338 lines | `c581d20b3775c658` | TOST, DM, Clark-West, VAR, and Panel DK tests |
| `code/nowcast_v2.py` | 10.73 KB | 239 lines | `4c6df40c29bdad42` | Rolling-origin bridge nowcasting evaluation |

---

## Usage

```bash
git clone https://github.com/anwarrohmadi2006/valitext-labour-nowcasting.git
cd valitext-labour-nowcasting

pip install numpy pandas scipy statsmodels matplotlib python-docx lxml

# Run econometric tests and regenerate figures
python code/empirical_rigor_tests.py
python code/generate_clean_figures.py
```

---

## Citation

```bibtex
@inproceedings{rohmadi2026triangulating,
  author    = {Rohmadi, Anwar and Rizqiana, Zulfanita Dien and Marseno, Damar Januar Jorgie},
  title     = {Triangulating Digital Discourse with Official Labour Statistics: Validating Friction Indices for Indonesian Nowcasting under the ValiText Framework},
  booktitle = {Proceedings of the Joint International Conference: The 2nd Indonesia Forum on Labour and Productivity (IFLP) and The 4th International Conference on Data Science and Official Statistics (ICDSOS)},
  year      = {2026}
}
```
