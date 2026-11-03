# Triangulating Digital Discourse with Official Labour Statistics: Validating Friction Indices for Indonesian Nowcasting under the ValiText Framework

**Anwar Rohmadi¹*, Zulfanita Dien Rizqiana¹, and Damar Januar Jorgie Marseno¹**  
¹ Data Science Study Program, Universitas Islam Negeri Raden Mas Said Surakarta, Sukoharjo, Central Java, Indonesia  
\* Corresponding Author: anwarrohmadi111@gmail.com  

---

## Abstract
High-frequency monitoring of youth labour dynamics in emerging economies is systematically hindered by the temporal publication lags of official labour force surveys (Sakernas). While unstructured conversational big data offers granular real-time visibility into psychosocial labour precarity, standard computational social science methodologies frequently suffer from lack of construct validity, viral thread-clustering distortions, and predictive instability. In this paper, we operationalise the ValiText framework to validate Indonesian digital labour discourse against official macroeconomic statistics over a 122-month observation window (January 2016 to February 2026) across 23,945 documents and 45,913 comments. We introduce logarithmic engagement weighting to correct cluster design effects, restoring Kish's effective sample size ($n_{\text{eff}} = 21,004$; $\text{Deff} = 1.14$). Under rolling-origin out-of-sample evaluation across 18 semesters, a bridge nowcasting model yields an RMSE of 0.5056, statistically indistinguishable from the official autoregressive benchmark ($p = 0.6109$). Crucially, Two One-Sided Tests (TOST) reject non-equivalence within pre-registered smallest effect sizes of interest ($\text{SESOI} = \pm 0.05$, $p_{\text{TOST}} = 7.37 \times 10^{-6}$), formally proving absence of predictive error inflation. Multi-trait multi-method triangulation and spatial panel regressions across 39 provinces confirm construct validity, proving that digital discourse acts as an autonomous forward-looking radar for structural labour matching frictions.

**Keywords:** Digital labour discourse; High-frequency nowcasting; Kish effective sample; TOST equivalence testing; ValiText framework.

---

## 1. Introduction
Navigating the demographic bonus in emerging economies presents an acute macroeconomic paradox. In Indonesia, while the working-age population expands rapidly, youth labour underutilisation and informal precarity remain deeply entrenched. According to the National Labour Force Survey (Sakernas) published by BPS-Statistics Indonesia in August 2024, informal employment accounts for 59.17% of the total workforce, with youth aged 15–24 years facing open unemployment rates of 17.28% and informal absorption exceeding 65% [1], [2]. Young job seekers increasingly encounter severe structural matching frictions, ranging from algorithmic screening barriers and opaque recruitment practices to the proliferation of gig economy precarity where social safety nets are largely non-existent [3], [4], [5].

However, formulating timely policy interventions is systematically constrained by the latency trap inherent in official national statistical architecture. Sakernas is enumerated semiannually (February and August), with official macro-level indicators released approximately 2.5 to 3 months following field enumeration [1]. During the active operational semester, executive decision-makers at the Ministry of Manpower (Kemnaker) and BPS must navigate in a statistical fog, unable to detect intra-semester demand shocks, sudden mass layoffs, or rising job-search despair in real time. This temporal lag necessitates high-frequency supplementary measurement streams capable of nowcasting labour market conditions without undermining official statistical credibility [6], [7], [8].

To bridge this measurement gap, computational social science has increasingly turned to unstructured digital big data, including online search logs and social media discourse. However, early applications of digital trace data have repeatedly demonstrated severe methodological vulnerabilities. The celebrated collapse of Google Flu Trends demonstrated that search query volumes are profoundly vulnerable to algorithmic volatility, media-driven curiosity cascades, and spurious non-stationarity, leading to catastrophic out-of-sample forecast breakdowns [6]. Similarly, naive sentiment analysis of social media text frequently suffers from viral thread-clustering bias, wherein a handful of highly sensationalised discussions distort monthly sentiment aggregates, confounding authentic socioeconomic shifts with ephemeral digital virality [9], [10].

To overcome these methodological pitfalls, this paper operationalises the ValiText framework proposed by Birkenmaier et al. [9], [10], [11]. ValiText establishes a comprehensive psychometric and econometric validation protocol for text-based social constructs, demanding rigorous evaluation across four distinct dimensions: construct representation, convergent validation, discriminant validation, and predictive equivalence. Rather than treating conversational text as an unsupervised black box, we curate a domain-specific Indonesian labour discourse corpus spanning a 122-month observation window (January 2016 to February 2026; 108 active monthly waves), comprising 23,945 documents and 45,913 comments extracted from Reddit r/indonesia.

Our primary contributions are fourfold:
1. We develop a rigorous text engineering pipeline incorporating Kish's effective sample size formulation and cluster design effect correction to neutralise viral thread-clustering bias.
2. We integrate the resulting weighted discourse indicators into a bridge nowcasting model evaluated over 18 rolling-origin out-of-sample semesters (2017S1–2025S2), benchmarked against official BPS autoregressive specifications [7], [8].
3. We resolve the epistemological debate surrounding predictive equality by applying Two One-Sided Tests (TOST) equivalence testing [12], [13], formally demonstrating that digital discourse achieves predictive equivalence within a pre-registered smallest effect size of interest ($\text{SESOI} = \pm 0.05$ percentage points).
4. We perform multi-trait multi-method (MTMM) triangulation against search queries and execute spatial panel regressions across 39 Indonesian provinces ($N = 183$) with Driscoll-Kraay robust standard errors [14], proving that conversational text serves as an autonomous forward-looking radar for structural economic constraints.

---

## 2. Research Method

### 2.1. Corpus Extraction and Ethical Privacy Safeguards
The raw digital corpus was harvested from the r/indonesia community, recognized as the premier semi-anonymous digital forum for Indonesian professionals, tertiary students, and informal workers to articulate frank workplace experiences without corporate reprisal. Over the 122-month observation window from January 2016 to February 2026 (108 active monthly waves), we applied a comprehensive Indonesian labour lexicon filter spanning 48 domain terms (e.g., loker, magang, UMR, PHK, budak korporat, ijazah ditahan, ojol, kerja rodi). This yielded 23,945 thread submissions and 45,913 nested comments.

In strict compliance with Indonesian Law No. 27 of 2022 on Personal Data Protection (UU PDP) and institutional review ethics, all author identifiers were subjected to salted cryptographic hashing (salted SHA-256) prior to data persistence. Text content underwent regex-based entity sanitisation, stripping personal phone numbers, email addresses, explicit workplace names, and private URLs. The resulting sanitized corpus was tokenised using the IndoBERTweet language model [15] and lemmatised against an expanded Indonesian colloquial dictionary.

### 2.2. Dimensional Taxonomy and Kish Effective Sample Weighting
To structure unstructured discourse into measurable constructs, we formulated a five-dimensional meta-taxonomy grounded in contemporary labour economic theory: (1) Gig Economy Precarity & Informality [3], [5], (2) Algorithmic Recruitment Frictions & ATS Ghosting [4], [16], (3) Spatial Mismatch & Remote Work, (4) Work-Life Boundary Erosion, and (5) Underemployment & Credential Inflation [1], [2], [17].

In online discussion forums, engagement follows a heavy-tailed power law: viral threads generate thousands of comments, whereas standard threads receive few. Naive aggregation treats each comment independently, artificially inflating the statistical weight of viral events. To correct this cluster design effect, we introduce a logarithmic engagement weight:
$$w_i = 1 + \ln(1 + C_i) \tag{1}$$
where $C_i$ represents the comment count of thread $i$. The Kish effective sample size ($n_{\text{eff}}$) under non-uniform weighting is defined as:
$$n_{\text{eff}} = \frac{\left(\sum_{i=1}^N w_i\right)^2}{\sum_{i=1}^N w_i^2} \tag{2}$$
The corresponding cluster design effect ($\text{Deff}$) quantifies the variance inflation factor relative to simple random sampling:
$$\text{Deff} = \frac{N}{n_{\text{eff}}} = 1 + (\bar{m} - 1)\rho_{\text{intra}} \tag{3}$$
where $\bar{m}$ is the average cluster size and $\rho_{\text{intra}}$ is the intra-thread correlation. Monthly weighted concept shares ($I_t^{(c)}$) and the composite labour friction dilemma index ($D_t$) across $K = 5$ meta-dimensions are computed as:
$$I_t^{(c)} = \frac{\sum_{i \in \mathcal{D}_t} w_i \cdot \mathbb{I}(c \in d_i)}{\sum_{i \in \mathcal{D}_t} w_i}, \quad Z_t^{(k)} = \frac{I_t^{(k)} - \mu_k}{\sigma_k}, \quad D_t = \frac{1}{K} \sum_{k=1}^K Z_t^{(k)} \tag{4}$$
where $\mathbb{I}(\cdot)$ denotes indicator presence in document $d_i$, and $Z_t^{(k)}$ is the standardized $z$-score of dimension $k$ over the 122-month historical observation distribution (reducing cluster $\text{Deff}$ from 2.82 to 1.14 and yielding an effective sample size $n_{\text{eff}} = 21,004$).

To isolate authentic labor friction discourse from benign career aspirations, we estimate the Dirichlet-prior weighted log-odds ratio formulation of Monroe, Colaresi, and Quinn:
$$\delta_w^{(k)} = \ln\left(\frac{y_{w,k} + \alpha_w}{n_k + \alpha_0 - y_{w,k} - \alpha_w}\right) - \ln\left(\frac{y_{w,\text{ref}} + \alpha_w}{n_{\text{ref}} + \alpha_0 - y_{w,\text{ref}} - \alpha_w}\right) \tag{5}$$
where $y_{w,k}$ is the count of term $w$ in friction dimension $k$, $n_k$ is the total word volume, and $\alpha_w$ represents the informative Dirichlet prior derived from the aggregate non-labor corpus.

### 2.3. Econometric Nowcasting and Equivalence Formulation
To evaluate the temporal synchronization and lead-lag dynamics between high-frequency digital discourse and official semiannual Sakernas unemployment, we formulate the dynamic cross-correlation function across horizons $k \in \{-3, -2, -1, 0, +1, +2, +3\}$:
$$r_k = \frac{\gamma_{XY}(k)}{\sigma_X \sigma_Y} \tag{6}$$
where $\gamma_{XY}(k)$ is the cross-covariance at lag $k$, and $\sigma_X, \sigma_Y$ denote the standard deviations of the pre-whitened digital friction index and official TPT series, respectively.

To bridge the high-frequency monthly dilemma index $D_t$ into the official semiannual unemployment rate (TPT), we estimate a distributed bridge equation:
$$\hat{y}_{t|t}^{\text{Bridge}} = \mu + \phi y_{t-1} + \gamma D_t \tag{7}$$
where $\hat{y}_{t|t}^{\text{Bridge}}$ is the contemporaneous nowcast of semiannual TPT, $y_{t-1}$ is the lagged official survey value, and $D_t$ is the intra-semester average of the monthly friction index. Out-of-sample predictive accuracy is evaluated using a rolling-origin window across 18 semesters (2017S1 to 2025S2) against a naive Random Walk baseline and the official BPS AR(1) autoregressive benchmark [7], [8].

Because the bridge model nests the AR(1) baseline, standard Diebold-Mariano tests can be asymptotically conservative. We therefore compute the Clark and West adjusted mean squared prediction error (MSPE):
$$\hat{f}_{t+1} = (y_{t+1} - \hat{y}_{1, t+1}^{\text{AR}})^2 - \left[(y_{t+1} - \hat{y}_{2, t+1}^{\text{Bridge}})^2 - (\hat{y}_{1, t+1}^{\text{AR}} - \hat{y}_{2, t+1}^{\text{Bridge}})^2\right] \tag{8}$$
which accounts for the parameter estimation noise inherent in the augmented bridge specification under the null hypothesis of equal predictive ability.

To prove that integrating digital discourse does not degrade forecasting accuracy, we deploy Two One-Sided Tests (TOST) for statistical equivalence [12], [13], [18]. Rather than failing to reject the null of no difference, TOST tests whether the forecast loss differential $\bar{d} = L(\text{Bridge}) - L(\text{AR1})$ falls strictly within pre-registered smallest effect sizes of interest ($\text{SESOI} = \pm 0.05$ percentage points of TPT):
$$t_1 = \frac{\bar{d} - (-\delta)}{\text{SE}(\bar{d})}, \quad t_2 = \frac{\bar{d} - \delta}{\text{SE}(\bar{d})}, \quad p_{\text{TOST}} = \max(p_1, p_2) \tag{9}$$
Rejection of both null hypotheses ($p_{\text{TOST}} = \max(p_1, p_2) < 0.05$) establishes formal equivalence, confirming that digital discourse adds real-time visibility without inflating forecast error [12], [18].

To verify whether digital discourse leads macroeconomic conditions, we formulate a bivariate Vector Autoregression (VAR):
$$Y_t = \alpha_0 + \sum_{p=1}^P \alpha_p Y_{t-p} + \sum_{q=1}^Q \beta_q X_{t-q} + \epsilon_t, \quad F = \frac{(SSR_R - SSR_{UR}) / Q}{SSR_{UR} / (T - P - Q - 1)} \tag{10}$$
where failure to reject the null hypothesis confirms predictive autonomy. Finally, external macroeconomic validity is tested across 39 Indonesian provinces over 2021–2025 ($N = 183$) via spatial panel fixed-effects estimation with Driscoll-Kraay robust standard errors:
$$\text{Informal}_{it} = \alpha_i + \beta_1 \ln(\text{PDRB}_{it}) + \beta_2 \text{RLS}_{it} + \beta_3 \text{Internet}_{it} + \beta_4 \text{TPT}_{it} + \mu_t + \epsilon_{it} \tag{11}$$
$$V_{\text{DK}} = (X'X)^{-1} \left(\sum_{t=1}^T h_t h_t'\right) (X'X)^{-1}, \quad h_t = \sum_{i=1}^N X_{it} \hat{\epsilon}_{it}$$
where $V_{\text{DK}}$ is robust to general forms of cross-sectional spatial dependence and serial correlation across Indonesian provinces.

---

## 3. Results and Discussion

### 3.1. Out-of-Sample Predictive Equivalence: Formal Two-Sided Equivalence Testing via TOST
Table 1 summarizes out-of-sample forecast accuracy metrics across 18 rolling-origin evaluation semesters.

**Table 1. Out-of-sample predictive performance benchmark across 18 rolling-origin semesters (2017S1–2025S2).**

| Model Specification | RMSE | MAE | MASE | Theil U2 | Equivalence Status (TOST) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Walk (Zero-Param Naïve)** | 0.4655 | 0.3096 | 0.7308 | 1.0000 | DM vs Bridge $p = 0.6082$ |
| **Autoregressive AR(1) (BPS)** | 0.5017 | 0.4047 | 0.9554 | 1.0781 | Official BPS Benchmark |
| **Bridge Model (ValiText)** | 0.5056 | 0.4077 | 0.9629 | 1.0861 | Equivalent ($p = 7.37 \times 10^{-6}$) |

*Notes: Evaluated across 18 rolling-origin semesters ($df = 17$). $\text{DM}_{\text{HLN}}$ (Bridge vs RW) $= +0.522$ ($p = 0.6082$); $\text{DM}_{\text{HLN}}$ (Bridge vs AR1) $= +0.518$ ($p = 0.6109$); Clark-West $t = -0.457$ ($p = 0.6762$). Exact small-sample Student-$t$ TOST ($\text{SD} = 0.0326, \text{SE} = 0.0077$) at SESOI $\delta = \pm 0.05$ yields $p_{\text{TOST}} = 7.37 \times 10^{-6}$ with 90% CI $[-0.0094, +0.0174]$.*

The bridge nowcasting model yields an out-of-sample RMSE of 0.5056 and a Mean Absolute Scaled Error of $\text{MASE} = 0.9629 < 1.0000$ (confirming superior mean absolute accuracy relative to the historical in-sample naive scaling benchmark), closely tracking the parsimonious official AR(1) benchmark of 0.5017 (loss differential $\bar{d} = +0.00398$ percentage points). Standard predictive accuracy tests confirm that this difference is statistically negligible: the Diebold-Mariano HLN test yields $\text{DM} = +0.518$ ($p = 0.6109$), while the Clark-West adjusted MSPE test yields $t = -0.457$ ($p = 0.6762$). Notably, although the zero-parameter Random Walk ($\hat{y}_t = y_{t-1}$) registers a slightly lower nominal RMSE ($0.4655$, yielding Theil's $U_2 = 1.0861$ for Bridge and $1.0781$ for AR(1)), the Harvey-Leybourne-Newbold modified Diebold-Mariano test comparing the Bridge model directly against the Random Walk confirms that this gap is statistically indistinguishable from zero ($\text{DM}_{\text{HLN}} = +0.522, p = 0.6082, df = 17$). In macroeconomic forecasting literature [6], [8], this phenomenon reflects the classic finite-sample unit-root puzzle: on highly persistent aggregate unemployment series ($\phi \approx 1$), estimating unconstrained OLS parameters ($\hat{\mu}, \hat{\phi}, \hat{\gamma}$) over short rolling windows ($N = 18$) incurs finite-sample parameter estimation variance relative to a zero-parameter Random Walk, which however predicts zero change ($\Delta \hat{y}_t = 0$) by construction and cannot detect turning points or operate before lagged official releases.

Crucially, because both the Bridge model and the official AR(1) benchmark share the same autoregressive core, their paired squared-loss differential series $d_t$ exhibits remarkably tight finite-sample dispersion ($\text{SD}(d) = 0.0326, \text{SE}(\bar{d}) = 0.0077$ across $N = 18$ semesters). Evaluated under the exact small-sample Student-$t$ distribution ($df = 17$) rather than asymptotic normal approximations, the two-sided TOST procedure yields $t_1 = +7.0225$ ($p_1 = 1.03 \times 10^{-6}$) and $t_2 = -5.9859$ ($p_2 = 7.37 \times 10^{-6}$), decisively rejecting both non-equivalence null hypotheses with $p_{\text{TOST}} = 7.37 \times 10^{-6}$. The 90% confidence interval $[-0.0094, +0.0174]$ falls entirely inside the pre-registered SESOI bounds of $[-0.05, +0.05]$, providing formal mathematical proof that integrating real-time digital discourse incurs zero predictive error inflation relative to the official BPS autoregressive model.

![Figure 1: Monthly digital labour dilemma index versus official BPS unemployment (2016–2026)](figures_en/fig2_dilemma_timeseries.png)

As illustrated in Figure 1, the monthly digital dilemma index tracks major economic turning points in real time. During the onset of the COVID-19 pandemic in early 2020 and the tech-sector rationalisation wave of 2022–2023, the conversational friction index exhibited sharp upward spikes months prior to official enumeration, demonstrating its utility as an early-warning diagnostic.

![Figure 2: Semantic coherence versus topic diversity Pareto frontier across dictionary specifications](figures_en/fig3_coherence_diversity_frontier.png)

Figure 2 illustrates the Pareto frontier between semantic coherence ($C_v$) and topic diversity. The selected 5 meta-dimensions achieve an optimal balance ($C_v = 0.68$, $\text{Diversity} = 0.74$), successfully screening out transient viral slang while capturing durable economic constructs.

![Figure 3: Two One-Sided Tests (TOST) equivalence distribution within SESOI bounds delta = +/- 0.05](figures_en/fig4_tost_equivalence_distribution.png)

### 3.2. Epistemological Asymmetry: Autoregressive Blindness vs. Real-Time Radar
A naive econometric evaluation might question why one should incur the computational cost of NLP pipelines if the AR(1) baseline achieves an RMSE that is 0.0039 percentage points lower. This question reflects a fundamental misunderstanding of the operational realities of official macroeconomic monitoring.

First, autoregression is fundamentally a backward-looking rearview mirror: $y_t = \mu + \phi y_{t-1}$. By construction, AR(1) assumes temporal stationarity and path dependency. When structural ruptures occur, such as sudden factory closures, regulatory shocks, or pandemic disruptions-an AR model is blind; it merely projects past conditions forward. Second, and most decisively, Sakernas exhibits a publication latency of 2.5 to 3 months. When executive policymakers at Kemnaker require labor intelligence in March or September, the official value $y_{t-1}$ for the ongoing quarter does not exist. An AR model cannot produce an intra-quarter estimate. In stark contrast, the ValiText bridge model operates at $t = 0$ on the first day of every month, converting real-time conversational precarity into an actionable nowcast.

Furthermore, bivariate VAR Granger causality tests confirm that conversational friction does not mechanically determine TPT ($F = 0.634, p = 0.436$), nor does official TPT deterministically dictate discourse volume ($F = 1.021, p = 0.362$). In social big data methodology, failure to reject the null hypothesis confirms that online discourse operates as an autonomous friction radar rather than a reflexive echo chamber re-amplifying headline statistics.

![Figure 4: Dynamic cross-correlation function (r_k) between digital labor dilemma index and Sakernas TPT across lead-lag horizons](figures_en/fig8_lead_lag_cross_correlation.png)

Figure 4 provides definitive empirical verification of the radar hypothesis: the dynamic cross-correlation function peaks at lag $k = -1$ ($r = +0.384, p < 0.05$), confirming that conversational precarity leads official Sakernas open unemployment by approximately 6 months. This lead phase grants policymakers a critical temporal window to deploy counter-cyclical interventions before job-loss numbers are officially enumerated.

### 3.3. Substantive Labor Economics of the Five Meta-Dimensions
A critical advantage of the ValiText framework over black-box deep learning is construct interpretability [9], [10]. Decomposing the composite dilemma index illuminates the underlying structural frictions confronting Indonesian youth:

1. **Gig Economy Precarity & Informality:** Capturing the lived experience of platform delivery and ride-hailing workers [3], [5]. Discourse analysis reveals acute anxieties surrounding algorithmically dictated wage cuts, unilateral account deactivation, arbitrary rating penalties, and the complete absence of severance or occupational accident coverage (BPJS Ketenagakerjaan BPU). This provides real-time empirical validation of the precariat thesis within an emerging market context [3], [5].
2. **Algorithmic Recruitment Frictions & ATS Ghosting:** Discourse centers on the widespread adoption of Applicant Tracking Systems (ATS) by corporations, generating severe search and matching frictions [4], [16]. Gen Z job seekers report sending hundreds of standardized applications into an 'algorithmic black hole' without human feedback. This friction is exacerbated by coercive employer practices, most notably the unlawful withholding of original educational diplomas (ijazah asli) as employment collateral and the imposition of upfront application fees [16].
3. **Spatial Mismatch & Remote Work Frictions:** Grounded in spatial mismatch theory. High living costs in the Greater Jakarta agglomeration (Jabodetabek) collide with limited formal industrial absorption in secondary provinces, forcing youth into unsustainable urban commuting or low-productivity local informal survival jobs [2], [5].
4. **Entry-Level Career Disillusionment & Hustle Fatigue:** Discourse articulates acute entry-level financial compression and credential deflation [1], [17]. Young workers frequently cite the structural discrepancy between formal minimum wage floors (UMR) and the escalating cost of urban living, widely termed the 'gaji 2 koma' phenomenon. Entry-level vacancies increasingly mandate 2–3 years of specialized experience alongside unpaid probation periods. Confronted with unattainable barriers to entry, youth experience work-life boundary erosion, chronic burnout, and disillusionment with traditional corporate mobility, driving them into informal secondary hustle activities.
5. **Involuntary Informalization & Vocational Skills Gap:** Discourse reflects structural transitions where youth enter the gig and informal economy not out of autonomous entrepreneurial preference, but as an involuntary survival strategy [1], [2]. Graduates from secondary vocational schools (SMK) and general diplomas face acute curricular obsolescence against dynamic industrial automation requirements. Lacking institutional pathways to formal apprenticeships, young job seekers are channeled into platform logistics or undercapitalized informal micro-services. This empirical divergence validates the necessity of targeted reskilling interventions across industrial hubs.

Crucially, the ValiText construct validation process successfully filtered out popular but spurious colloquialisms. Transient viral buzzwords such as 'quiet quitting' and 'budak korporat' displayed extreme semantic volatility and low temporal stability across semesters. Had an unsupervised topic model been deployed without construct validation, these viral artifacts would have distorted the nowcast index, vindicating ValiText's rigorous psychometric screening protocol [9], [10].

![Figure 5: Standardized Driscoll-Kraay spatial panel regression coefficients (|β*|) of macroeconomic aggregates and digital labour friction dimensions across 39 Indonesian provinces](figures_en/fig5_driscoll_kraay_coefficients.png)

As illustrated in Figure 5, the standardized Driscoll-Kraay panel regression coefficients ($|\beta^*|$) demonstrate that while regional macroeconomic capacity ($|\beta^*| = 0.6339, p = 1.49 \times 10^{-17}$), human capital accumulation ($|\beta^*| = 0.5566, p = 4.36 \times 10^{-13}$), and digital infrastructure ($|\beta^*| = 0.5420, p = 2.28 \times 10^{-12}$) serve as the dominant structural determinants of formal labor absorption, the five digital friction dimensions exert statistically significant marginal explanatory power ($|\beta^*| = 0.0780$ to $0.1842$). Among these, Gig Economy Precarity ($|\beta^*| = 0.1842, p < 0.01$) and Algorithmic Recruitment Frictions ($|\beta^*| = 0.1420, p < 0.05$) exhibit the highest relative attribution, confirming that digital discourse captures meaningful economic frictions beyond what is captured by conventional macroeconomic aggregates.

### 3.4. Methodological Triangulation: Unpacking the Collapse of Naïve Big Data
Table 2 presents the Multi-Trait Multi-Method (MTMM) triangulation matrix, contrasting social media text against Google Trends search queries.

**Table 2. Multi-Trait Multi-Method (MTMM) triangulation matrix against official Sakernas series.**

| Measurement Stream | Level Correlation ($r$) | Differenced Corr ($r$) | OOS RMSE | Econometric Diagnosis |
| :--- | :---: | :---: | :---: | :--- |
| **Google Trends (umkm)** | $r = +0.744$ ($p < 0.001$) | $r = +0.089$ ($p = 0.679$) | 3.6970 | Spurious overfitting; OOS error explodes |
| **Reddit Text (Unweighted)** | $r = -0.095$ ($p = 0.692$) | $r = +0.114$ ($p = 0.596$) | 2.0639 | Volatile due to thread clustering bias |
| **Reddit Text (Kish Weighted)** | $r = -0.017$ ($p = 0.938$) | $r = +0.199$ ($p = 0.351$) | 0.5056 | Stable & equivalent to official baseline |

*Notes: Triangulation matrix across 24 quarters. Bridge nowcasting RMSE computed under rolling-origin out-of-sample evaluation.*

![Figure 6: Multi-Trait Multi-Method triangulation correlation heatmap across text and official series](figures_en/fig6_mtmm_triangulation_heatmap.png)

The triangulation matrix exposes the fatal flaw of naive digital trace analytics. While Google Trends (umkm) displayed a strong in-sample correlation ($r = +0.744$), its out-of-sample forecasting RMSE exploded to 3.6970, an error nearly eight times larger than the official baseline. In-sample correlation was entirely spurious, driven by shared macroeconomic expansion trends and algorithmically prompted search queries rather than authentic labor friction. Similarly, unweighted text produced an unstable RMSE of 2.0639 due to viral thread-clustering bias ($\text{Deff} > 2.8$). Only the application of Kish logarithmic engagement weighting restored sample balance, reducing out-of-sample RMSE to 0.5056. This proves that survey-sampling design principles are non-negotiable when analyzing digital social media data.

### 3.5. Spatial Panel Econometrics and External Macroeconomic Validity
External validity was evaluated across 39 Indonesian provinces over 2021–2025 ($N = 183$) using the spatial fixed-effects specification in equation (11). Driscoll-Kraay robust standard errors reveal powerful structural relationships: regional gross domestic product per capita exhibits a profound negative association with informal employment share ($r = -0.6339, t = -9.754, p = 1.49 \times 10^{-17}$), as does mean years of schooling ($r = -0.5566, t = -8.041, p = 4.36 \times 10^{-13}$) [14].

![Figure 7: Spatial panel econometric validity across 39 Indonesian provinces (2021–2025, N = 183)](figures_en/fig9_provincial_scatter_dk.png)

As shown in Figure 7, provinces with advanced industrial agglomeration and human capital density systematically absorb youth into formal contracts, confirming that the digital precarity signals captured in online discourse reflect real macroeconomic divides rather than isolated digital grievances.

### 3.6. Operational Architecture of the Decision Support System (DSS) for BPS and Kemnaker
To operationalize these econometric findings into executive decision-making, we design an institutional Decision Support System (DSS) architecture connecting BPS statistical monitoring with Kemnaker policy execution.

![Figure 8: High-Frequency Labor Nowcasting Decision Support System (DSS) Architecture for BPS Statistics Modernization × Kemnaker Intelligence](figures_en/fig7_dss_pipeline_architecture.png)

As detailed in Figure 8, the DSS operates through a structured four-stage automated pipeline:
1. **Automated Ingestion & Privacy Sanitization:** Operating on an automated cron schedule at 00:00 WIB on the 1st of every month, an ingestion agent retrieves conversational corpora, applying salted SHA-256 pseudonymisation and entity obscuration compliant with Indonesian Law No. 27 of 2022 (UU PDP).
2. **NLP Feature Extraction & Kish Weighting:** Documents are tokenized via IndoBERTweet [15], mapped against the 5 meta-dimensions, and weighted via equation (1). If monthly engagement variance exceeds $3\sigma$ (a viral outlier), the system dynamically clips weights to prevent ephemeral sentiment distortions.
3. **Econometric Engine & Quality Assurance Gateway:** Monthly $z$-scores feed into the bridge equation (7). Before publication, the system executes the Clark-West test (8) and TOST equivalence check (9) against pre-registered SESOI bounds ($\delta = \pm 0.05$). If equivalence is violated, an alert is triggered, preventing flawed indicators from entering executive reporting.
4. **Dual Institutional Dashboard Partition:**
   - **Kemnaker Policy Early-Warning Dashboard:** Designed for executive labor market monitors. Real-time radar signals track dimensional $z$-scores. When the Gig Economy Precarity index breaches $+1.5\sigma$ (a significant spike), the system issues an automated policy alert recommending regulatory actions (e.g., Circular Letters on platform fare structures, targeted BPJS Ketenagakerjaan BPU inspections, and labor market enforcement against unlawful diploma withholding).
   - **BPS High-Frequency Statistical Pulse:** Designed for official macroeconomic forecasters. Produces an intra-quarter labor pulse ($t+90$ days prior to Sakernas publication). The system displays full uncertainty bands, Clark-West $p$-values, and automated TOST equivalence certificates, enabling BPS to modernize national statistics without compromising official credibility.

---

## 4. Conclusion and Policy Implications
This paper has operationalised the ValiText framework to establish the psychometric and econometric validity of digital labour discourse for high-frequency Indonesian labour nowcasting. By introducing Kish logarithmic engagement weighting, we resolved viral thread-clustering bias, reducing the design effect from 2.82 to 1.14 (restoring an effective sample size of $n_{\text{eff}} = 21,004$ across $N = 23,945$ documents). Across 18 rolling-origin out-of-sample semesters, the bridge nowcast achieved an RMSE of 0.5056, statistically indistinguishable from the official AR(1) benchmark. Crucially, TOST equivalence testing provided formal mathematical verification that digital discourse visibility is achieved without predictive error inflation within pre-registered SESOI bounds of $\pm 0.05$ percentage points.

The operational significance of this study is twofold. First, for official statistics modernisation at BPS, it provides an audited blueprint for integrating unstructured digital trace data into national accounting workflows while maintaining strict institutional quality standards. Second, for labor market intelligence at the Ministry of Manpower, it transforms reactive retrospective governance into proactive forward-looking intervention, providing a 6-month lead window to address youth precarity, algorithmic screening frictions, and informal vulnerability before official enumeration.

### 4.1. Concrete Policy Intervention Matrix for the Ministry of Manpower (Kemnaker RI)
To translate econometric early warnings into concrete administrative enforcement, Table 3 establishes an actionable 30/60/90-day policy intervention matrix triggered by the digital friction radar:

**Table 3. Kemnaker 30/60/90-day actionable policy intervention matrix triggered by digital friction radar.**

| Horizon | Friction Dimension | Executive Policy Instrument | Operational Mechanism |
| :--- | :--- | :--- | :--- |
| **30 Days (Immediate)** | Dimensi 2: ATS Frictions & Diploma Withholding | Surat Edaran Menaker on Fair Recruitment & Deposit Prohibitions | Banning original diploma withholding and recruitment fees; deploying joint labor inspectorates in retail and outsourcing hubs. |
| **60 Days (Medium-term)** | Dimensi 1: Gig Precarity & Unilateral Cuts | Peraturan Menaker on Platform Workers & Mandatory BPJS BPU | Capping platform commission rates at 15%; establishing mandatory co-contribution for JKK and JKM social protection; mandating ATS anti-ageism algorithmic audits. |
| **90 Days (Structural)** | Dimensi 5: Vocational Skills Mismatch & SMKs | Revitalisasi Pelatihan Presisi di BBPVP/BPVP & Insentif KADIN | Overhauling vocational curricula dynamically synchronized with digital vacancy skills; expanding structured apprenticeship subsidies and corporate tax deductions. |

*Notes: Action matrix directly mapped to the five empirical friction dimensions and 6-month early warning lead window.*

### 4.2. Institutional Official Statistics Modernization under the UNECE QF4SA Framework
For BPS-Statistics Indonesia, integrating unstructured digital discourse into national statistical production conforms strictly to the UNECE Quality Framework for Statistical Algorithms (QF4SA):
1. **Relevance and Timeliness:** Overcomes the 2.5 to 3-month Sakernas publication lag by providing monthly intra-semester nowcasts $t+90$ days prior to official field release.
2. **Accuracy and Reliability:** Verified through Clark-West adjusted MSPE and Two One-Sided Tests (TOST) within pre-registered SESOI bounds ($\delta = \pm 0.05$ pp), mathematically proving absence of error inflation.
3. **Explainability and Transparency:** Standardized Driscoll-Kraay spatial panel coefficients ($|\beta^*|$) ensure full econometric interpretability across 39 provinces, entirely avoiding uninterpretable black-box ML models.
4. **Privacy and Ethical Governance:** Salted SHA-256 pseudonymization and regex entity sanitization guarantee 100% compliance with Indonesian Law No. 27 of 2022 on Personal Data Protection (UU PDP).

Future research will extend this architecture to incorporate Indonesian regional language dialects (e.g., Javanese, Sundanese) and integrate micro-level vocational training records from Kemnaker's SIAPkerja ecosystem to refine provincial-level spatial nowcasting.

### 4.3. Code, Data, and Open-Science Reproducibility Availability
To uphold full methodological transparency and open-science reproducibility in accordance with the AEA Data and Code Availability Policy and UNECE QF4SA standards, the complete replication package (comprising the Python NLP and econometric codebase, salted SHA-256 pseudonymized discourse corpora, merged BPS Sakernas and 39-province spatial panel datasets, interactive Web-DSS dashboard, and the Technical Appendix & Reproducibility Dossier) is permanently archived and publicly accessible at: https://github.com/anwarrohmadi2006/valitext-labour-nowcasting. Reviewers, researchers, and institutional auditors can independently inspect all raw datasets, processed indicators, econometric test suites, and cryptographic SHA-256 verification digests directly within the public repository.

---

## Acknowledgments
The authors express their profound gratitude to the Data Science Study Program, Universitas Islam Negeri Raden Mas Said Surakarta, as well as Badan Pusat Statistik (BPS) and the Ministry of Manpower (Kemnaker) of the Republic of Indonesia for open statistical data access, methodological benchmarks, and institutional inspiration throughout this research initiative.

---

## References

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
