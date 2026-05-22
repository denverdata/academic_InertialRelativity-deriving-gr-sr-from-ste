#!/usr/bin/env python3
"""Independent audit of pair_tables_exact.tex.

Two independent checks for every visible cell:

(A) Source-match audit
    For each row whose label exists in pair_comparisons_v2_cases.md,
    read the source value, round to 10 sig figs with banker's rounding
    using a DIFFERENT code path (no shared rounding function with the
    renderer), and confirm the displayed cell matches exactly.

(B) First-principles identity audit
    Independently compute each row's value from (m_1, m_2, r_1, r_2)
    using the formulas in system_properties/, using high-precision
    Decimal. Round and compare to displayed.

Any mismatch prints loudly and the script exits non-zero. Silence = pass.
"""

import re
import sys
from decimal import Decimal, localcontext, ROUND_HALF_EVEN, getcontext

getcontext().prec = 60  # higher than the renderer's 50

# Constants from system_properties/constants.py — hardcoded canonical values.
G = Decimal('6.67430e-11')
PI = Decimal('3.1415926535')
C = Decimal('299792458')
D_CRIT = Decimal('6.7329500000000000e26')


def round_independent(val_str, prec=10):
    """Round to `prec` sig figs with banker's rounding. INDEPENDENT
    implementation — does not import from generate_pair_table_exact."""
    s = val_str.strip()
    if s in ('---', ''):
        return '---'
    d = Decimal(s)
    if d == 0:
        return '0'
    sign = '-' if d < 0 else ''
    a = abs(d)
    with localcontext() as ctx:
        ctx.prec = prec
        ctx.rounding = ROUND_HALF_EVEN
        r = +a
    e = r.adjusted()
    _, digits, _ = r.as_tuple()
    ds = ''.join(map(str, digits))
    ds = ds + '0' * (prec - len(ds)) if len(ds) < prec else ds[:prec]
    return f'{sign}{ds[0]}.{ds[1:]}e{"+" if e >= 0 else "-"}{abs(e)}'


def round10_independent(val_str):
    return round_independent(val_str, 10)


# Display columns that show 30 sig figs in the rendered table (Case 3 and STE).
# Other display columns show 10. Must match generate_pair_table_exact.py.
HI_PREC_COLS = {2, 5}


def prec_for_col(j):
    return 30 if j in HI_PREC_COLS else 10


def parse_source(path):
    """Parse the .md file into {label: [val per column]}."""
    out = {}
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s.startswith('|') or s.startswith('|--') or s.startswith('| metric'):
                continue
            parts = [p.strip() for p in s.split('|')[1:-1]]
            if len(parts) >= 9:
                out[parts[0]] = parts[1:9]
    return out


def parse_rendered(path):
    """Parse pair_tables_exact.tex into [(label, [val per displayed column])]."""
    rows = []
    cell_pat = re.compile(r'\{\\ttfamily\s+([^}]+)\}')
    with open(path) as f:
        for line in f:
            line = line.rstrip()
            if not line.startswith('$') and not line.startswith('('):
                continue
            if r'\\' not in line:
                continue
            # Split on & to get cells. First cell is label, rest are values.
            cells = [c.strip() for c in line.rstrip(r'\\').split('&')]
            if len(cells) < 2:
                continue
            label = cells[0].strip()
            vals = []
            for c in cells[1:]:
                m = cell_pat.search(c)
                vals.append(m.group(1).strip() if m else c)
            rows.append((label, vals))
    return rows


# Map rendered LaTeX label → markdown source label
LATEX_TO_SRC = {
    r'$m_1$ (kg)': 'm_1 (kg)',
    r'$m_2$ (kg)': 'm_2 (kg)',
    r'$r_1$ (m)': 'r_1 (m)',
    r'$r_2$ (m)': 'r_2 (m)',
    r'$\rho_1$ (kg/m$^3$)': 'ρ_1 (kg/m³)',
    r'$\rho_2$ (kg/m$^3$)': 'ρ_2 (kg/m³)',
    r'$I_1$ (kg$\cdot$m$^2$)': 'I_1 (kg·m²)',
    r'$I_2$ (kg$\cdot$m$^2$)': 'I_2 (kg·m²)',
    r'$D_1$ (kg/m)': 'D_1 (kg/m)',
    r'$D_2$ (kg/m)': 'D_2 (kg/m)',
    r'$D_{1\_norm}$': 'D_1_norm',
    r'$D_{2\_norm}$': 'D_2_norm',
    r'$r_{s\_1}$ (m)': 'r_s_1 (m)',
    r'$r_{s\_2}$ (m)': 'r_s_2 (m)',
    r'$gtd_1$': 'gtd_1',
    r'$gtd_2$': 'gtd_2',
    r'$dtd_1$': 'dtd_1',
    r'$dtd_2$': 'dtd_2',
    r'$dtd_1/dtd_2$': 'dtd_1/dtd_2',
    r'$\sqrt{D_1/D_2}$': 'sqrt(D_1/D_2)',
    r'$\sqrt{(m_1 r_2)/(m_2 r_1)}$': 'sqrt((m_1·r_2)/(m_2·r_1))',
    r'$\sqrt{(I_1/I_2)(r_2/r_1)^3}$': 'sqrt((I_1/I_2)*(r_2/r_1)³)',
    r'$(I_1/I_2)^{1/5}(\rho_1/\rho_2)^{3/10}$': '(I_1/I_2)^(1/5)*(ρ_1/ρ_2)^(3/10)',
    r'$(m_1 r_2)/(m_2 r_1)$': '(m_1·r_2)/(m_2·r_1)',
    r'$D_1/D_2$': '(*k) D_1/D_2',
    r'$gtd_1/gtd_2$': '(*G) gtd_1/gtd_2',
    r'$\sqrt{1-dtd_1^2}/\sqrt{1-dtd_2^2}$': 'sqrt(1-dtd_1²)/sqrt(1-dtd_2²)',
    r'$I_1/I_2$': 'I_1/I_2',
    r'$I_2/I_1$': 'I_2/I_1',
    r'$(I_1/I_2)^{1/2}$': '(I_1/I_2)^(1/2)',
    r'$(I_2/I_1)^{1/2}$': '(I_2/I_1)^(1/2)',
    r'$(\rho_1/\rho_2)^{1/5}(r_1/r_2)$': 'k_i=(ρ_1/ρ_2)^(1/5)*(r_1/r_2)',
    r'$(I_1/I_2)^{1/5}$': '(I_1/I_2)^(1/5)',
    r'$(I_2/I_1)^{1/5}$': '(I_2/I_1)^(1/5)',
    r'$(dtd_1/dtd_2)^2(r_1/r_2)^3$': '(dtd_1/dtd_2)²*(r_1/r_2)³',
    r'$m_1/m_2$': '(*k) k_m=m_1/m_2',
    r'$\sqrt{m_1/m_2}$': 'sqrt(m_1/m_2)',
    r'$\sqrt{r_2/r_1}$': 'sqrt(r_2/r_1)',
    # Computed rows (no source row exists — verified by check B only):
    r'$(I_1/I_2)(r_2/r_1)^3$': None,
    r'$r_2/r_1$': None,
}

# Displayed → source column index. Renderer keeps [0,2,3,4,5,6]: skip case1b (1) and General2 (7).
DISPLAYED_TO_SRC_COL = [0, 2, 3, 4, 5, 6]


def first_principles(m1, m2, r1, r2):
    """Compute every relevant quantity from (m_1, m_2, r_1, r_2) using the
    same formulas as system_properties/uniform_sphere.py. Returns a dict
    label → Decimal."""
    vol1 = Decimal(4) / Decimal(3) * PI * r1 ** 3
    vol2 = Decimal(4) / Decimal(3) * PI * r2 ** 3
    rho1 = m1 / vol1
    rho2 = m2 / vol2
    I1 = Decimal(2) / Decimal(5) * m1 * r1 ** 2
    I2 = Decimal(2) / Decimal(5) * m2 * r2 ** 2
    D1 = m1 / r1
    D2 = m2 / r2
    Dn1 = D1 / D_CRIT
    Dn2 = D2 / D_CRIT
    rs1 = Decimal(2) * G * m1 / (C * C)
    rs2 = Decimal(2) * G * m2 / (C * C)

    def safe_sqrt_1_minus(x):
        if x < Decimal('1e-50'):
            return Decimal(1) - x / Decimal(2)
        v = Decimal(1) - x
        if v < 0:
            return Decimal(0)
        return v.sqrt()

    td_term_1 = Decimal(2) * G * m1 / (r1 * C * C)
    td_term_2 = Decimal(2) * G * m2 / (r2 * C * C)
    gtd1 = safe_sqrt_1_minus(td_term_1)
    gtd2 = safe_sqrt_1_minus(td_term_2)
    dtd1 = Dn1.sqrt() if Dn1 >= 0 else Decimal(0)
    dtd2 = Dn2.sqrt() if Dn2 >= 0 else Decimal(0)

    return {
        'm_1 (kg)': m1, 'm_2 (kg)': m2,
        'r_1 (m)': r1, 'r_2 (m)': r2,
        'ρ_1 (kg/m³)': rho1, 'ρ_2 (kg/m³)': rho2,
        'I_1 (kg·m²)': I1, 'I_2 (kg·m²)': I2,
        'D_1 (kg/m)': D1, 'D_2 (kg/m)': D2,
        'D_1_norm': Dn1, 'D_2_norm': Dn2,
        'r_s_1 (m)': rs1, 'r_s_2 (m)': rs2,
        'gtd_1': gtd1, 'gtd_2': gtd2,
        'dtd_1': dtd1, 'dtd_2': dtd2,
        'dtd_1/dtd_2': dtd1 / dtd2,
        'sqrt(D_1/D_2)': (Dn1 / Dn2).sqrt(),
        'sqrt((m_1·r_2)/(m_2·r_1))': ((m1 * r2) / (m2 * r1)).sqrt(),
        'sqrt((I_1/I_2)*(r_2/r_1)³)': ((I1 / I2) * (r2 / r1) ** 3).sqrt(),
        '(I_1/I_2)^(1/5)*(ρ_1/ρ_2)^(3/10)': (I1 / I2) ** (Decimal(1) / Decimal(5)) * (rho1 / rho2) ** (Decimal(3) / Decimal(10)),
        '(m_1·r_2)/(m_2·r_1)': (m1 * r2) / (m2 * r1),
        '(*k) D_1/D_2': D1 / D2,
        '(I_1/I_2)*(r_2/r_1)³': (I1 / I2) * (r2 / r1) ** 3,
        '(*G) gtd_1/gtd_2': gtd1 / gtd2,
        'sqrt(1-dtd_1²)/sqrt(1-dtd_2²)': (Decimal(1) - dtd1 ** 2).sqrt() / (Decimal(1) - dtd2 ** 2).sqrt(),
        'I_1/I_2': I1 / I2,
        'I_2/I_1': I2 / I1,
        '(I_1/I_2)^(1/2)': (I1 / I2).sqrt(),
        '(I_2/I_1)^(1/2)': (I2 / I1).sqrt(),
        'k_i=(ρ_1/ρ_2)^(1/5)*(r_1/r_2)': (rho1 / rho2) ** (Decimal(1) / Decimal(5)) * (r1 / r2),
        '(I_1/I_2)^(1/5)': (I1 / I2) ** (Decimal(1) / Decimal(5)),
        '(I_2/I_1)^(1/5)': (I2 / I1) ** (Decimal(1) / Decimal(5)),
        '(dtd_1/dtd_2)²*(r_1/r_2)³': (dtd1 / dtd2) ** 2 * (r1 / r2) ** 3,
        '(*k) k_m=m_1/m_2': m1 / m2,
        'sqrt(m_1/m_2)': (m1 / m2).sqrt(),
        'r_2/r_1': r2 / r1,
        'sqrt(r_2/r_1)': (r2 / r1).sqrt(),
    }


def main():
    src = parse_source('../pair_comparisons_v2_cases.md')
    rendered = parse_rendered('pair_tables_exact.tex')

    if not src or not rendered:
        print('FAIL: could not parse source or rendered tex')
        sys.exit(2)

    # Pull (m,r) for each displayed column from source
    cols = []
    for col_idx in DISPLAYED_TO_SRC_COL:
        m1 = Decimal(src['m_1 (kg)'][col_idx])
        m2 = Decimal(src['m_2 (kg)'][col_idx])
        r1 = Decimal(src['r_1 (m)'][col_idx])
        r2 = Decimal(src['r_2 (m)'][col_idx])
        cols.append(first_principles(m1, m2, r1, r2))

    failures = []
    checked = 0

    for latex_label, rendered_vals in rendered:
        src_label = LATEX_TO_SRC.get(latex_label)
        if src_label is None and latex_label not in LATEX_TO_SRC:
            failures.append(f'UNMAPPED LABEL: {latex_label!r}')
            continue

        for j, rendered_val in enumerate(rendered_vals):
            checked += 1
            col_data = cols[j]

            prec = prec_for_col(j)

            # Check A: against source .md (if label is in source)
            if src_label is not None and src_label in src:
                src_col_idx = DISPLAYED_TO_SRC_COL[j]
                src_val = src[src_label][src_col_idx]
                expected_a = round_independent(src_val, prec)
                if rendered_val != expected_a:
                    failures.append(
                        f'(A) source mismatch  row={latex_label!r}  col={j}  '
                        f'rendered={rendered_val!r}  source-rounded={expected_a!r}  '
                        f'source-raw={src_val!r}'
                    )

            # Check B: against first-principles recomputation
            fp_label = src_label if src_label in col_data else latex_label
            # Strip $ for some computed labels
            fp_key = {
                r'$r_2/r_1$': 'r_2/r_1',
                r'$(I_1/I_2)(r_2/r_1)^3$': '(I_1/I_2)*(r_2/r_1)³',
            }.get(latex_label, fp_label)

            if fp_key in col_data:
                fp_dec = col_data[fp_key]
                expected_b = round_independent(f'{fp_dec:E}', prec)
                if rendered_val != expected_b:
                    failures.append(
                        f'(B) first-principles mismatch  row={latex_label!r}  col={j}  '
                        f'rendered={rendered_val!r}  computed={expected_b!r}  '
                        f'raw={fp_dec}'
                    )

    print(f'Audited {checked} cells across {len(rendered)} rows × {len(cols)} columns.')
    if failures:
        print(f'\n{len(failures)} FAILURE(S):')
        for f in failures[:30]:
            print(f'  {f}')
        if len(failures) > 30:
            print(f'  ... and {len(failures) - 30} more')
        sys.exit(1)
    print('PASS: every cell matches both source data and first-principles recomputation at 10 sig digits.')


if __name__ == '__main__':
    main()
