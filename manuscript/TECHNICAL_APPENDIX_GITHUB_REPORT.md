# TECHNICAL APPENDIX & OPEN-SCIENCE GITHUB REPRODUCIBILITY DOSSIER

**Triangulating Digital Discourse with Official Labour Statistics: Validating Friction Indices for Indonesian Nowcasting under the ValiText Framework**

- **Authors:** **Anwar Rohmadi¹***, **Zulfanita Dien Rizqiana¹**, **Damar Januar Jorgie Marseno¹**
- **Affiliation:** ¹ Data Science Study Program, Universitas Islam Negeri Raden Mas Said Surakarta, Sukoharjo, Central Java, Indonesia
- **Target Conference:** IFLP & ICDSOS 2026 (Joint International Conference, 8–9 December 2026)
- **Public GitHub Repository:** [https://github.com/anwarrohmadi2006/valitext-labour-nowcasting](https://github.com/anwarrohmadi2006/valitext-labour-nowcasting)
- **Word Edition (DOCX):** [`Technical_Appendix_GitHub_Reproducibility_Report.docx`](Technical_Appendix_GitHub_Reproducibility_Report.docx)

---

## 1. Executive Summary of Data Science Engineering & Reproducibility

This technical appendix serves as an official open-science engineering dossier verifying that all empirical findings, econometric estimations, and natural language processing (NLP) constructs reported in the main manuscript are generated from authentic, version-controlled raw data and executable Python scripts.

The production pipeline operates across four modular engineering layers:
1. **Cryptographic Ingestion & Privacy Sanitization:** Salted SHA-256 author hashing and regex PII stripping compliant with Indonesian Law No. 27 of 2022 on Personal Data Protection (UU PDP).
2. **Kish Effective Sample Weighting:** Correcting viral thread-clustering design effects from $\text{Deff} = 2.82$ down to $\text{Deff} = 1.14$, restoring an effective sample size of $n_{\text{eff}} = 21,004$ across $N = 23,945$ documents.
3. **Five-Dimensional Meta-Taxonomy Extraction:** IndoBERTweet tokenization and Monroe-Colaresi-Quinn Dirichlet-prior weighted log-odds ratios.
4. **Econometric Nowcasting & ValiText Verification:** Distributed bridge equation modeling, 18-semester rolling-origin out-of-sample evaluation, Two One-Sided Tests (TOST) equivalence verification ($\text{SESOI} = \pm 0.05$ pp), Bivariate VAR Granger causality, and 39-province spatial panel fixed-effects regressions ($N = 183$) with Driscoll-Kraay robust standard errors.

---

## 2. Cryptographic Inventory of Raw Data, Processed Panels, and Scripts (SHA-256 Verified)

| Repository Artifact Path | Size | Records / Lines | Verified SHA-256 Digest & Engineering Role |
| :--- | :---: | :---: | :--- |
| `genz-informal-nlp/data/raw/reddit_targeted/targeted_pull_v2.jsonl` | 8.77 MB | 3,142 threads (23,945 docs) | `664a1ea97a471d85...` : Raw labour-filtered thread submissions (2016–2026) |
| `genz-informal-nlp/data/raw/reddit_targeted/comments_full.jsonl` | 24.48 MB | 22,100 blocks (45,913 comments) | `3e06b99bf1536052...` : Full nested comment corpus with salted SHA-256 authors |
| `genz-informal-nlp/data/raw/bps/labour_long.csv` | 108.9 KB | 2,574 rows | `9eb91ea512126d62...` : Official BPS Sakernas TPT & informality panel (2016–2025) |
| `genz-informal-nlp/data/raw/bps/indicators.csv` | 815.3 KB | 6,969 rows | `aaf2b675f6787e2c...` : Official BPS regional covariates ($\ln\text{PDRB}$, RLS, Internet) |
| `genz-informal-nlp/data/raw/trends/trends_monthly.csv` | 3.74 KB | 142 months | `06c527da97551591...` : Google Trends monthly search query benchmark series |
| `genz-informal-nlp/data/processed/panel_provinsi.csv` | 16.12 KB | 184 rows ($N = 183$ obs) | `568af170ff02f128...` : Merged 39-province spatial panel dataset (2021–2025) |
| `genz-informal-nlp/data/processed/dilemma_index_jev_monthly_v2_tw.csv` | 20.77 KB | 116 rows (108 active waves) | `c732f81e850d1415...` : Kish-weighted monthly digital labour friction index |
| `genz-informal-nlp/outputs/empirical_rigor_results.json` | 5.66 KB | 166 lines | `b42975429a51a28d...` : Serialized JSON output of TOST, DM, CW, VAR, and DK tests |
| `genz-informal-nlp/scripts/empirical_rigor_tests.py` | 13.12 KB | 338 lines | `c581d20b3775c658...` : Executable econometric test suite (TOST, CW, VAR, Panel DK) |
| `genz-informal-nlp/scripts/nowcast_v2.py` | 10.73 KB | 239 lines | `4c6df40c29bdad42...` : Rolling-origin out-of-sample bridge nowcasting engine |

---

## 3. Step-by-Step Audit & Reproduction Protocol

```bash
# 1. Clone Repository
git clone https://github.com/anwarrohmadi2006/valitext-labour-nowcasting.git
cd valitext-labour-nowcasting

# 2. Run Econometric Validation Suite
python genz-informal-nlp/scripts/empirical_rigor_tests.py

# 3. Regenerate Interactive Web-DSS Dashboard
python generate_dss.py

# 4. Rebuild All 300 DPI Figures & Word Deliverables
python build_submission_package.py
```
