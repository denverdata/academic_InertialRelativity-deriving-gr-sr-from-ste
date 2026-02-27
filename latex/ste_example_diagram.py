#!/usr/bin/env python3
"""
ste_example_diagram.py — Generate the STE isometric scaling diagram.
Outputs: ste_example.pdf  (in the same directory as this script)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(11, 8))
ax.set_aspect('equal')
ax.axis('off')

# ── colours ───────────────────────────────────────────────────────────────────
C_SMALL = '#4C8EC2'   # blue
C_LARGE = '#C25B4C'   # red-orange
C_ARROW = '#444444'
C_TEXT  = '#222222'

# ── geometry ──────────────────────────────────────────────────────────────────
r_small = 1.0
r_large = 2.0
cx_small = 2.5
cx_large = 8.0
cy = 5.0      # sphere centres — sits high to leave room for labels and formula

# ── spheres ───────────────────────────────────────────────────────────────────
ax.add_patch(plt.Circle((cx_small, cy), r_small,
             color=C_SMALL, alpha=0.22, zorder=2))
ax.add_patch(plt.Circle((cx_large, cy), r_large,
             color=C_LARGE, alpha=0.22, zorder=2))
ax.add_patch(plt.Circle((cx_small, cy), r_small,
             fill=False, edgecolor=C_SMALL, lw=2.0, zorder=3))
ax.add_patch(plt.Circle((cx_large, cy), r_large,
             fill=False, edgecolor=C_LARGE, lw=2.0, zorder=3))

# ── radius arrows (from centre to right edge) ─────────────────────────────────
ax.annotate('', xy=(cx_small + r_small, cy), xytext=(cx_small, cy),
            arrowprops=dict(arrowstyle='->', color=C_SMALL, lw=1.5))
ax.text(cx_small + r_small / 2, cy + 0.18, 'r = 1 m',
        ha='center', va='bottom', fontsize=11, color=C_SMALL)

ax.annotate('', xy=(cx_large + r_large, cy), xytext=(cx_large, cy),
            arrowprops=dict(arrowstyle='->', color=C_LARGE, lw=1.5))
ax.text(cx_large + r_large / 2, cy + 0.18, 'r = 2 m',
        ha='center', va='bottom', fontsize=11, color=C_LARGE)

# ── label blocks below each sphere ────────────────────────────────────────────
ax.text(cx_small, cy - r_small - 0.55,
        'm = 1 kg\n'
        'r = 1 m\n'
        'I = 0.4 kg\u00b7m\u00b2\n'
        'T\u2081  (reference)',
        ha='center', va='top', fontsize=11, color=C_SMALL,
        linespacing=1.9, family='monospace')

ax.text(cx_large, cy - r_large - 0.55,
        'm = 8 kg    (\u00d7k\u00b3 = \u00d78)\n'
        'r = 2 m    (\u00d7k  = \u00d72)\n'
        'I = 12.8 kg\u00b7m\u00b2  (\u00d7k\u2075 = \u00d732)\n'
        'T\u2082 = T\u2081/2   (clock half-speed)',
        ha='center', va='top', fontsize=11, color=C_LARGE,
        linespacing=1.9, family='monospace')

# ── scale-factor arrow — arcs through the gap between the spheres ─────────────
# Endpoints are in the gap (outside both spheres) at mid-height.
arrow_y = cy + 0.7   # 5.7 — well inside the gap and clear of sphere surfaces
gap_left  = cx_small + r_small + 0.3   # 3.8
gap_right = cx_large - r_large - 0.3   # 5.7

ax.annotate('',
            xy=(gap_right, arrow_y),
            xytext=(gap_left, arrow_y),
            arrowprops=dict(arrowstyle='->', color=C_ARROW, lw=2.0,
                            connectionstyle='arc3,rad=-0.4'))

# Label sits above the arc's peak, horizontally centred in the gap.
# Arc peak is roughly at arrow_y + 0.4 × gap_width / 2 ≈ 6.1.
# Placing the label at 6.9 keeps it above the small-sphere top (6.0) and
# well clear of the large sphere (nearest point ≈ 3.3 radii away).
mid_x = (cx_small + cx_large) / 2   # 5.25
ax.text(mid_x, arrow_y + 1.2,
        'scale factor  k = 2',
        ha='center', va='center', fontsize=13, color=C_ARROW,
        fontweight='bold')

# ── STE formula box ───────────────────────────────────────────────────────────
ax.text(mid_x, 0.3,
        r'$\dfrac{T_1}{T_2} = \left(\dfrac{I_2}{I_1}\right)^{1/5}'
        r'= 32^{1/5} = 2 \quad\Rightarrow\quad T_2 = T_1/2$',
        ha='center', va='bottom', fontsize=13, color=C_TEXT,
        bbox=dict(boxstyle='round,pad=0.55', facecolor='#f8f8f8',
                  edgecolor='#aaaaaa', lw=1.4))

# ── axis limits (tuned to equal-aspect 11 × 8 figure) ─────────────────────────
ax.set_xlim(0.0, 11.0)
ax.set_ylim(-0.4, 8.4)

plt.tight_layout(pad=0.3)
plt.savefig('ste_example.pdf', dpi=200, bbox_inches='tight')
plt.savefig('ste_example.png', dpi=200, bbox_inches='tight')
print('Saved ste_example.pdf and ste_example.png')
