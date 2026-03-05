#!/usr/bin/env python3
"""
ste_example_diagram.py — Generate the STE isometric scaling diagram.
Outputs: ste_example.pdf  (in the same directory as this script)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── Global style: serif fonts to match the paper ────────────────────────────
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif', 'Computer Modern Roman'],
    'mathtext.fontset': 'cm',
    'font.size': 9,
})

fig, ax = plt.subplots(figsize=(7.0, 4.2))
ax.set_aspect('equal')
ax.axis('off')

# ── Colours ──────────────────────────────────────────────────────────────────
C_FILL  = '#e8e8e8'
C_EDGE  = '#333333'
C_TEXT  = '#000000'
C_DIM   = '#555555'
C_NOTE  = '#444444'

# ── Geometry ─────────────────────────────────────────────────────────────────
r1 = 0.65
r2 = 1.15
cx1 = 1.4
cx2 = 5.3
cy  = 2.8

# ── Spheres ──────────────────────────────────────────────────────────────────
for cx, r in [(cx1, r1), (cx2, r2)]:
    ax.add_patch(plt.Circle((cx, cy), r,
                 facecolor=C_FILL, edgecolor=C_EDGE, lw=1.0, zorder=2))
    ax.plot(cx, cy, 'o', color=C_EDGE, ms=2, zorder=3)

# ── Radius dimension lines ──────────────────────────────────────────────────
for cx, r, label in [(cx1, r1, r'$R = 1\;\mathrm{m}$'),
                      (cx2, r2, r'$R = 2\;\mathrm{m}$')]:
    ax.annotate('', xy=(cx + r, cy), xytext=(cx, cy),
                arrowprops=dict(arrowstyle='-|>', color=C_DIM, lw=0.8,
                                mutation_scale=8))
    ax.text(cx + r / 2, cy + 0.10, label,
            ha='center', va='bottom', fontsize=8, color=C_TEXT)

# ── System labels above each sphere ─────────────────────────────────────────
ax.text(cx1, cy + r1 + 0.18, 'System 1', ha='center', va='bottom',
        fontsize=9, fontweight='bold', color=C_TEXT)
ax.text(cx2, cy + r2 + 0.18, 'System 2', ha='center', va='bottom',
        fontsize=9, fontweight='bold', color=C_TEXT)

# ── Property tables — aligned at the same vertical level ─────────────────────
prop_y_top = 1.15      # both property blocks start at same height
line_h = 0.30

# System 1
p1_lines = [
    r'$M = 1\;\mathrm{kg}$',
    r'$I = 0.4\;\mathrm{kg\cdot m^2}$',
]
for i, txt in enumerate(p1_lines):
    ax.text(cx1, prop_y_top - i * line_h, txt,
            ha='center', va='center', fontsize=8, color=C_TEXT)

# System 2 (value + scaling note)
p2_lines = [
    (r'$M = 8\;\mathrm{kg}$',                 r'$(\times k^3)$'),
    (r'$I = 12.8\;\mathrm{kg\cdot m^2}$',     r'$(\times k^5)$'),
]
for i, (val, note) in enumerate(p2_lines):
    y = prop_y_top - i * line_h
    ax.text(cx2 - 0.10, y, val, ha='right', va='center',
            fontsize=8, color=C_TEXT)
    ax.text(cx2 + 0.05, y, note, ha='left', va='center',
            fontsize=7.5, color=C_NOTE)

# ── Transformation arrow between spheres ─────────────────────────────────────
arr_y = cy + 0.12
arr_x1 = cx1 + r1 + 0.18
arr_x2 = cx2 - r2 - 0.18

ax.annotate('', xy=(arr_x2, arr_y), xytext=(arr_x1, arr_y),
            arrowprops=dict(arrowstyle='->', color=C_TEXT, lw=1.2))

ax.text((arr_x1 + arr_x2) / 2, arr_y + 0.15,
        r'$k = 2$', ha='center', va='bottom',
        fontsize=9, fontweight='bold', color=C_TEXT)

# ── STE equation centred at the bottom ───────────────────────────────────────
eq_x = (cx1 + cx2) / 2
eq_y = 0.10
ax.text(eq_x, eq_y,
        r'$k = \left(\dfrac{I_2}{I_1}\right)^{\!1/5}'
        r'= \left(\dfrac{12.8}{0.4}\right)^{\!1/5}'
        r'= 32^{1/5} = 2$',
        ha='center', va='bottom', fontsize=9.5, color=C_TEXT,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#f5f5f5',
                  edgecolor='#999999', lw=0.8))

# ── Axis limits ──────────────────────────────────────────────────────────────
ax.set_xlim(-0.3, 7.3)
ax.set_ylim(-0.3, 4.5)

plt.tight_layout(pad=0.2)
plt.savefig('ste_example.pdf', dpi=300, bbox_inches='tight')
plt.savefig('ste_example.png', dpi=300, bbox_inches='tight')
print('Saved ste_example.pdf and ste_example.png')
