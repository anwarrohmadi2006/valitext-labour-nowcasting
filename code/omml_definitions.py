"""
Microscopic OMML (Office Math Markup Language) Definitions for Word Equations.
Strictly audited to eliminate all empty elements (<m:e><m:r><m:t></m:t></m:r></m:e> or empty <m:sup>),
ensuring Word renders zero placeholder dotted square boxes.
"""

OMML_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"

OMML_EQS = {
    # Eq 1: Logarithmic Engagement Weight: w_i = 1 + ln(1 + C_i)
    "eq1_log_weight": f'''<m:oMath xmlns:m="{OMML_NS}">
        <m:sSub><m:e><m:r><m:t>w</m:t></m:r></m:e><m:sub><m:r><m:t>i</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = 1 + ln(1 + </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>C</m:t></m:r></m:e><m:sub><m:r><m:t>i</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t>)</m:t></m:r>
    </m:oMath>''',

    # Eq 2: Kish Effective Sample Size: n_eff = (sum_{i=1}^N w_i)^2 / sum_{i=1}^N w_i^2
    "eq2_kish_neff": f'''<m:oMath xmlns:m="{OMML_NS}">
        <m:sSub><m:e><m:r><m:t>n</m:t></m:r></m:e><m:sub><m:r><m:t>eff</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = </m:t></m:r>
        <m:f>
            <m:num>
                <m:sSup>
                    <m:e>
                        <m:d>
                            <m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr>
                            <m:e>
                                <m:nary>
                                    <m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>
                                    <m:sub><m:r><m:t>i=1</m:t></m:r></m:sub>
                                    <m:sup><m:r><m:t>N</m:t></m:r></m:sup>
                                    <m:e><m:sSub><m:e><m:r><m:t>w</m:t></m:r></m:e><m:sub><m:r><m:t>i</m:t></m:r></m:sub></m:sSub></m:e>
                                </m:nary>
                            </m:e>
                        </m:d>
                    </m:e>
                    <m:sup><m:r><m:t>2</m:t></m:r></m:sup>
                </m:sSup>
            </m:num>
            <m:den>
                <m:nary>
                    <m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>
                    <m:sub><m:r><m:t>i=1</m:t></m:r></m:sub>
                    <m:sup><m:r><m:t>N</m:t></m:r></m:sup>
                    <m:e>
                        <m:sSup>
                            <m:e><m:sSub><m:e><m:r><m:t>w</m:t></m:r></m:e><m:sub><m:r><m:t>i</m:t></m:r></m:sub></m:sSub></m:e>
                            <m:sup><m:r><m:t>2</m:t></m:r></m:sup>
                        </m:sSup>
                    </m:e>
                </m:nary>
            </m:den>
        </m:f>
    </m:oMath>''',

    # Eq 3: Design Effect: Deff = N / n_eff = 1 + (m_bar - 1) rho_intra
    "eq3_deff": f'''<m:oMath xmlns:m="{OMML_NS}">
        <m:r><m:t>Deff = </m:t></m:r>
        <m:f>
            <m:num><m:r><m:t>N</m:t></m:r></m:num>
            <m:den><m:sSub><m:e><m:r><m:t>n</m:t></m:r></m:e><m:sub><m:r><m:t>eff</m:t></m:r></m:sub></m:sSub></m:den>
        </m:f>
        <m:r><m:t> = 1 + (</m:t></m:r>
        <m:acc><m:accPr><m:chr m:val="¯"/></m:accPr><m:e><m:r><m:t>m</m:t></m:r></m:e></m:acc>
        <m:r><m:t> - 1)</m:t></m:r>
        <m:sSub><m:e><m:r><m:t>ρ</m:t></m:r></m:e><m:sub><m:r><m:t>intra</m:t></m:r></m:sub></m:sSub>
    </m:oMath>''',

    # Eq 4: Monthly Concept Share & Composite Friction Dilemma Index
    # I_t^(c) = sum_{i in D_t} w_i * I(c in d_i) / sum_{i in D_t} w_i , D_t = 1/K sum_{k=1}^K Z_t^(k)
    "eq4_concept_composite": f'''<m:oMath xmlns:m="{OMML_NS}">
        <m:sSubSup>
            <m:e><m:r><m:t>I</m:t></m:r></m:e>
            <m:sub><m:r><m:t>t</m:t></m:r></m:sub>
            <m:sup><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:t>c</m:t></m:r></m:e></m:d></m:sup>
        </m:sSubSup>
        <m:r><m:t> = </m:t></m:r>
        <m:f>
            <m:num>
                <m:nary>
                    <m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="und"/></m:naryPr>
                    <m:sub><m:r><m:t>i ∈ </m:t></m:r><m:sSub><m:e><m:r><m:t>D</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub></m:sub>
                    <m:e>
                        <m:sSub><m:e><m:r><m:t>w</m:t></m:r></m:e><m:sub><m:r><m:t>i</m:t></m:r></m:sub></m:sSub>
                        <m:r><m:t> · 𝕀(c ∈ </m:t></m:r>
                        <m:sSub><m:e><m:r><m:t>d</m:t></m:r></m:e><m:sub><m:r><m:t>i</m:t></m:r></m:sub></m:sSub>
                        <m:r><m:t>)</m:t></m:r>
                    </m:e>
                </m:nary>
            </m:num>
            <m:den>
                <m:nary>
                    <m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="und"/></m:naryPr>
                    <m:sub><m:r><m:t>i ∈ </m:t></m:r><m:sSub><m:e><m:r><m:t>D</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub></m:sub>
                    <m:e><m:sSub><m:e><m:r><m:t>w</m:t></m:r></m:e><m:sub><m:r><m:t>i</m:t></m:r></m:sub></m:sSub></m:e>
                </m:nary>
            </m:den>
        </m:f>
        <m:r><m:t>,    </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>D</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = </m:t></m:r>
        <m:f>
            <m:num><m:r><m:t>1</m:t></m:r></m:num>
            <m:den><m:r><m:t>K</m:t></m:r></m:den>
        </m:f>
        <m:nary>
            <m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>
            <m:sub><m:r><m:t>k=1</m:t></m:r></m:sub>
            <m:sup><m:r><m:t>K</m:t></m:r></m:sup>
            <m:e>
                <m:sSubSup>
                    <m:e><m:r><m:t>Z</m:t></m:r></m:e>
                    <m:sub><m:r><m:t>t</m:t></m:r></m:sub>
                    <m:sup><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:t>k</m:t></m:r></m:e></m:d></m:sup>
                </m:sSubSup>
            </m:e>
        </m:nary>
    </m:oMath>''',

    # Eq 5: Dirichlet-Prior Log-Odds Ratio (Monroe et al., 2008)
    "eq5_dirichlet_logodds": f'''<m:oMath xmlns:m="{OMML_NS}">
        <m:sSubSup>
            <m:e><m:r><m:t>δ</m:t></m:r></m:e>
            <m:sub><m:r><m:t>w</m:t></m:r></m:sub>
            <m:sup><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:t>A - B</m:t></m:r></m:e></m:d></m:sup>
        </m:sSubSup>
        <m:r><m:t> = ln</m:t></m:r>
        <m:d>
            <m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr>
            <m:e>
                <m:f>
                    <m:num><m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>wA</m:t></m:r></m:sub></m:sSub><m:r><m:t> + </m:t></m:r><m:sSub><m:e><m:r><m:t>α</m:t></m:r></m:e><m:sub><m:r><m:t>w</m:t></m:r></m:sub></m:sSub></m:num>
                    <m:den><m:sSub><m:e><m:r><m:t>n</m:t></m:r></m:e><m:sub><m:r><m:t>A</m:t></m:r></m:sub></m:sSub><m:r><m:t> + </m:t></m:r><m:sSub><m:e><m:r><m:t>α</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub><m:r><m:t> - (</m:t></m:r><m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>wA</m:t></m:r></m:sub></m:sSub><m:r><m:t> + </m:t></m:r><m:sSub><m:e><m:r><m:t>α</m:t></m:r></m:e><m:sub><m:r><m:t>w</m:t></m:r></m:sub></m:sSub><m:r><m:t>)</m:t></m:r></m:den>
                </m:f>
            </m:e>
        </m:d>
        <m:r><m:t> - ln</m:t></m:r>
        <m:d>
            <m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr>
            <m:e>
                <m:f>
                    <m:num><m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>wB</m:t></m:r></m:sub></m:sSub><m:r><m:t> + </m:t></m:r><m:sSub><m:e><m:r><m:t>α</m:t></m:r></m:e><m:sub><m:r><m:t>w</m:t></m:r></m:sub></m:sSub></m:num>
                    <m:den><m:sSub><m:e><m:r><m:t>n</m:t></m:r></m:e><m:sub><m:r><m:t>B</m:t></m:r></m:sub></m:sSub><m:r><m:t> + </m:t></m:r><m:sSub><m:e><m:r><m:t>α</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub><m:r><m:t> - (</m:t></m:r><m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>wB</m:t></m:r></m:sub></m:sSub><m:r><m:t> + </m:t></m:r><m:sSub><m:e><m:r><m:t>α</m:t></m:r></m:e><m:sub><m:r><m:t>w</m:t></m:r></m:sub></m:sSub><m:r><m:t>)</m:t></m:r></m:den>
                </m:f>
            </m:e>
        </m:d>
    </m:oMath>''',

    # Eq 6: Dynamic Cross-Correlation Lead-Lag
    "eq6_cross_corr": f'''<m:oMath xmlns:m="{OMML_NS}">
        <m:sSub><m:e><m:r><m:t>r</m:t></m:r></m:e><m:sub><m:r><m:t>k</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t>(X, Y) = </m:t></m:r>
        <m:f>
            <m:num>
                <m:nary>
                    <m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>
                    <m:sub><m:r><m:t>t=1</m:t></m:r></m:sub>
                    <m:sup><m:r><m:t>T - |k|</m:t></m:r></m:sup>
                    <m:e>
                        <m:r><m:t>(</m:t></m:r>
                        <m:sSub><m:e><m:r><m:t>X</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>
                        <m:r><m:t> - </m:t></m:r>
                        <m:acc><m:accPr><m:chr m:val="¯"/></m:accPr><m:e><m:r><m:t>X</m:t></m:r></m:e></m:acc>
                        <m:r><m:t>)(</m:t></m:r>
                        <m:sSub><m:e><m:r><m:t>Y</m:t></m:r></m:e><m:sub><m:r><m:t>t+k</m:t></m:r></m:sub></m:sSub>
                        <m:r><m:t> - </m:t></m:r>
                        <m:acc><m:accPr><m:chr m:val="¯"/></m:accPr><m:e><m:r><m:t>Y</m:t></m:r></m:e></m:acc>
                        <m:r><m:t>)</m:t></m:r>
                    </m:e>
                </m:nary>
            </m:num>
            <m:den>
                <m:rad>
                    <m:radPr><m:degHide m:val="1"/></m:radPr>
                    <m:e>
                        <m:nary>
                            <m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>
                            <m:sub><m:r><m:t>t=1</m:t></m:r></m:sub><m:sup><m:r><m:t>T</m:t></m:r></m:sup>
                            <m:e>
                                <m:sSup>
                                    <m:e><m:r><m:t>(</m:t></m:r><m:sSub><m:e><m:r><m:t>X</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub><m:r><m:t> - </m:t></m:r><m:acc><m:accPr><m:chr m:val="¯"/></m:accPr><m:e><m:r><m:t>X</m:t></m:r></m:e></m:acc><m:r><m:t>)</m:t></m:r></m:e>
                                    <m:sup><m:r><m:t>2</m:t></m:r></m:sup>
                                </m:sSup>
                            </m:e>
                        </m:nary>
                        <m:nary>
                            <m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>
                            <m:sub><m:r><m:t>t=1</m:t></m:r></m:sub><m:sup><m:r><m:t>T</m:t></m:r></m:sup>
                            <m:e>
                                <m:sSup>
                                    <m:e><m:r><m:t>(</m:t></m:r><m:sSub><m:e><m:r><m:t>Y</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub><m:r><m:t> - </m:t></m:r><m:acc><m:accPr><m:chr m:val="¯"/></m:accPr><m:e><m:r><m:t>Y</m:t></m:r></m:e></m:acc><m:r><m:t>)</m:t></m:r></m:e>
                                    <m:sup><m:r><m:t>2</m:t></m:r></m:sup>
                                </m:sSup>
                            </m:e>
                        </m:nary>
                    </m:e>
                </m:rad>
            </m:den>
        </m:f>
    </m:oMath>''',

    # Eq 7: Bivariate VAR Granger Causality & Wald F
    "eq7_granger_var": f'''<m:oMath xmlns:m="{OMML_NS}">
        <m:sSub><m:e><m:r><m:t>Y</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>α</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> + </m:t></m:r>
        <m:nary>
            <m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>
            <m:sub><m:r><m:t>p=1</m:t></m:r></m:sub><m:sup><m:r><m:t>P</m:t></m:r></m:sup>
            <m:e><m:sSub><m:e><m:r><m:t>α</m:t></m:r></m:e><m:sub><m:r><m:t>p</m:t></m:r></m:sub></m:sSub><m:sSub><m:e><m:r><m:t>Y</m:t></m:r></m:e><m:sub><m:r><m:t>t-p</m:t></m:r></m:sub></m:sSub></m:e>
        </m:nary>
        <m:r><m:t> + </m:t></m:r>
        <m:nary>
            <m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>
            <m:sub><m:r><m:t>q=1</m:t></m:r></m:sub><m:sup><m:r><m:t>Q</m:t></m:r></m:sup>
            <m:e><m:sSub><m:e><m:r><m:t>β</m:t></m:r></m:e><m:sub><m:r><m:t>q</m:t></m:r></m:sub></m:sSub><m:sSub><m:e><m:r><m:t>X</m:t></m:r></m:e><m:sub><m:r><m:t>t-q</m:t></m:r></m:sub></m:sSub></m:e>
        </m:nary>
        <m:r><m:t> + </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>ϵ</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t>,    F = </m:t></m:r>
        <m:f>
            <m:num>
                <m:f>
                    <m:num>
                        <m:r><m:t>(</m:t></m:r>
                        <m:sSub><m:e><m:r><m:t>SSR</m:t></m:r></m:e><m:sub><m:r><m:t>R</m:t></m:r></m:sub></m:sSub>
                        <m:r><m:t> - </m:t></m:r>
                        <m:sSub><m:e><m:r><m:t>SSR</m:t></m:r></m:e><m:sub><m:r><m:t>UR</m:t></m:r></m:sub></m:sSub>
                        <m:r><m:t>)</m:t></m:r>
                    </m:num>
                    <m:den><m:r><m:t>Q</m:t></m:r></m:den>
                </m:f>
            </m:num>
            <m:den>
                <m:f>
                    <m:num><m:sSub><m:e><m:r><m:t>SSR</m:t></m:r></m:e><m:sub><m:r><m:t>UR</m:t></m:r></m:sub></m:sSub></m:num>
                    <m:den><m:r><m:t>(T - P - Q - 1)</m:t></m:r></m:den>
                </m:f>
            </m:den>
        </m:f>
    </m:oMath>''',

    # Eq 8: Bridge Nowcasting Equation & RMSFE
    "eq8_bridge": f'''<m:oMath xmlns:m="{OMML_NS}">
        <m:sSubSup>
            <m:e><m:acc><m:accPr><m:chr m:val="^"/></m:accPr><m:e><m:r><m:t>y</m:t></m:r></m:e></m:acc></m:e>
            <m:sub><m:r><m:t>t|t</m:t></m:r></m:sub>
            <m:sup><m:r><m:t>Bridge</m:t></m:r></m:sup>
        </m:sSubSup>
        <m:r><m:t> = μ + ϕ</m:t></m:r>
        <m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>t-1</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> + γ</m:t></m:r>
        <m:sSub><m:e><m:r><m:t>D</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t>,    RMSFE = </m:t></m:r>
        <m:rad>
            <m:radPr><m:degHide m:val="1"/></m:radPr>
            <m:e>
                <m:f>
                    <m:num><m:r><m:t>1</m:t></m:r></m:num>
                    <m:den><m:r><m:t>P</m:t></m:r></m:den>
                </m:f>
                <m:nary>
                    <m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>
                    <m:sub><m:r><m:t>p=1</m:t></m:r></m:sub><m:sup><m:r><m:t>P</m:t></m:r></m:sup>
                    <m:e>
                        <m:sSup>
                            <m:e>
                                <m:r><m:t>(</m:t></m:r><m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>t+p</m:t></m:r></m:sub></m:sSub><m:r><m:t> - </m:t></m:r>
                                <m:sSub><m:e><m:acc><m:accPr><m:chr m:val="^"/></m:accPr><m:e><m:r><m:t>y</m:t></m:r></m:e></m:acc></m:e><m:sub><m:r><m:t>t+p</m:t></m:r></m:sub></m:sSub><m:r><m:t>)</m:t></m:r>
                            </m:e>
                            <m:sup><m:r><m:t>2</m:t></m:r></m:sup>
                        </m:sSup>
                    </m:e>
                </m:nary>
            </m:e>
        </m:rad>
    </m:oMath>''',

    # Eq 9: Clark-West (2007) Adjusted MSPE
    "eq9_clark_west": f'''<m:oMath xmlns:m="{OMML_NS}">
        <m:sSub><m:e><m:acc><m:accPr><m:chr m:val="^"/></m:accPr><m:e><m:r><m:t>f</m:t></m:r></m:e></m:acc></m:e><m:sub><m:r><m:t>t+1</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = </m:t></m:r>
        <m:sSup>
            <m:e><m:r><m:t>(</m:t></m:r><m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>t+1</m:t></m:r></m:sub></m:sSub><m:r><m:t> - </m:t></m:r><m:sSubSup><m:e><m:acc><m:accPr><m:chr m:val="^"/></m:accPr><m:e><m:r><m:t>y</m:t></m:r></m:e></m:acc></m:e><m:sub><m:r><m:t>1, t+1</m:t></m:r></m:sub><m:sup><m:r><m:t>AR</m:t></m:r></m:sup></m:sSubSup><m:r><m:t>)</m:t></m:r></m:e>
            <m:sup><m:r><m:t>2</m:t></m:r></m:sup>
        </m:sSup>
        <m:r><m:t> - </m:t></m:r>
        <m:d>
            <m:dPr><m:begChr m:val="["/><m:endChr m:val="]"/></m:dPr>
            <m:e>
                <m:sSup>
                    <m:e><m:r><m:t>(</m:t></m:r><m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>t+1</m:t></m:r></m:sub></m:sSub><m:r><m:t> - </m:t></m:r><m:sSubSup><m:e><m:acc><m:accPr><m:chr m:val="^"/></m:accPr><m:e><m:r><m:t>y</m:t></m:r></m:e></m:acc></m:e><m:sub><m:r><m:t>2, t+1</m:t></m:r></m:sub><m:sup><m:r><m:t>Bridge</m:t></m:r></m:sup></m:sSubSup><m:r><m:t>)</m:t></m:r></m:e>
                    <m:sup><m:r><m:t>2</m:t></m:r></m:sup>
                </m:sSup>
                <m:r><m:t> - </m:t></m:r>
                <m:sSup>
                    <m:e><m:r><m:t>(</m:t></m:r><m:sSubSup><m:e><m:acc><m:accPr><m:chr m:val="^"/></m:accPr><m:e><m:r><m:t>y</m:t></m:r></m:e></m:acc></m:e><m:sub><m:r><m:t>1, t+1</m:t></m:r></m:sub><m:sup><m:r><m:t>AR</m:t></m:r></m:sup></m:sSubSup><m:r><m:t> - </m:t></m:r><m:sSubSup><m:e><m:acc><m:accPr><m:chr m:val="^"/></m:accPr><m:e><m:r><m:t>y</m:t></m:r></m:e></m:acc></m:e><m:sub><m:r><m:t>2, t+1</m:t></m:r></m:sub><m:sup><m:r><m:t>Bridge</m:t></m:r></m:sup></m:sSubSup><m:r><m:t>)</m:t></m:r></m:e>
                    <m:sup><m:r><m:t>2</m:t></m:r></m:sup>
                </m:sSup>
            </m:e>
        </m:d>
    </m:oMath>''',

    # Eq 10: TOST Equivalence Testing
    "eq10_tost": f'''<m:oMath xmlns:m="{OMML_NS}">
        <m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>1</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = </m:t></m:r>
        <m:f>
            <m:num><m:acc><m:accPr><m:chr m:val="¯"/></m:accPr><m:e><m:r><m:t>d</m:t></m:r></m:e></m:acc><m:r><m:t> - (-δ)</m:t></m:r></m:num>
            <m:den><m:r><m:t>SE(</m:t></m:r><m:acc><m:accPr><m:chr m:val="¯"/></m:accPr><m:e><m:r><m:t>d</m:t></m:r></m:e></m:acc><m:r><m:t>)</m:t></m:r></m:den>
        </m:f>
        <m:r><m:t>,    </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>2</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = </m:t></m:r>
        <m:f>
            <m:num><m:acc><m:accPr><m:chr m:val="¯"/></m:accPr><m:e><m:r><m:t>d</m:t></m:r></m:e></m:acc><m:r><m:t> - δ</m:t></m:r></m:num>
            <m:den><m:r><m:t>SE(</m:t></m:r><m:acc><m:accPr><m:chr m:val="¯"/></m:accPr><m:e><m:r><m:t>d</m:t></m:r></m:e></m:acc><m:r><m:t>)</m:t></m:r></m:den>
        </m:f>
        <m:r><m:t>,    </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>p</m:t></m:r></m:e><m:sub><m:r><m:t>TOST</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = max(</m:t></m:r>
        <m:sSub><m:e><m:r><m:t>p</m:t></m:r></m:e><m:sub><m:r><m:t>1</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t>, </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>p</m:t></m:r></m:e><m:sub><m:r><m:t>2</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t>)</m:t></m:r>
    </m:oMath>''',

    # Eq 11: Spatial Panel Macro Model with Driscoll-Kraay Robust Covariance
    "eq11_panel_dk": f'''<m:oMath xmlns:m="{OMML_NS}">
        <m:sSub><m:e><m:r><m:t>Informal</m:t></m:r></m:e><m:sub><m:r><m:t>it</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>α</m:t></m:r></m:e><m:sub><m:r><m:t>i</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> + </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>β</m:t></m:r></m:e><m:sub><m:r><m:t>1</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> ln(</m:t></m:r>
        <m:sSub><m:e><m:r><m:t>PDRB</m:t></m:r></m:e><m:sub><m:r><m:t>it</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t>) + </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>β</m:t></m:r></m:e><m:sub><m:r><m:t>2</m:t></m:r></m:sub></m:sSub>
        <m:sSub><m:e><m:r><m:t> RLS</m:t></m:r></m:e><m:sub><m:r><m:t>it</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> + </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>β</m:t></m:r></m:e><m:sub><m:r><m:t>3</m:t></m:r></m:sub></m:sSub>
        <m:sSub><m:e><m:r><m:t> Internet</m:t></m:r></m:e><m:sub><m:r><m:t>it</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> + </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>β</m:t></m:r></m:e><m:sub><m:r><m:t>4</m:t></m:r></m:sub></m:sSub>
        <m:sSub><m:e><m:r><m:t> TPT</m:t></m:r></m:e><m:sub><m:r><m:t>it</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> + </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>μ</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> + </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>ϵ</m:t></m:r></m:e><m:sub><m:r><m:t>it</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t>,    </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>V</m:t></m:r></m:e><m:sub><m:r><m:t>DK</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = </m:t></m:r>
        <m:sSup><m:e><m:r><m:t>(X'X)</m:t></m:r></m:e><m:sup><m:r><m:t>-1</m:t></m:r></m:sup></m:sSup>
        <m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e>
            <m:nary>
                <m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>
                <m:sub><m:r><m:t>t=1</m:t></m:r></m:sub><m:sup><m:r><m:t>T</m:t></m:r></m:sup>
                <m:e>
                    <m:sSub><m:e><m:r><m:t>h</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub>
                    <m:sSubSup><m:e><m:r><m:t>h</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub><m:sup><m:r><m:t>'</m:t></m:r></m:sup></m:sSubSup>
                </m:e>
            </m:nary>
        </m:e></m:d>
        <m:sSup><m:e><m:r><m:t>(X'X)</m:t></m:r></m:e><m:sup><m:r><m:t>-1</m:t></m:r></m:sup></m:sSup>
    </m:oMath>'''
}
