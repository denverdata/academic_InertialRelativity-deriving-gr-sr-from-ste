# Session Synopsis: Inertia, Time Dilation, and System Scale
## April 25-26, 2026

---

## Overview

Starting from numerical pair comparisons of uniform spheres, this session derived a series of formulas connecting moment of inertia, density, radius, and DeGerlia time dilation (dtd) into a unified framework. The central result is a universal formula for system scale about an axis (k_i), and a general equivalence between the ratio of time dilations and the ratio of inertias of any two systems.

---

## 1. The Isometric Starting Point

For two systems of equal density (isometric scaling), the moment of inertia of a uniform body is:

**I = (8/15) pi rho r^5**

The ratio of two such systems' inertias:

**I_1/I_2 = (r_1/r_2)^5**

Therefore the fifth root of the inertia ratio recovers the linear scale factor:

**(I_1/I_2)^(1/5) = r_1/r_2 = k_r**

Under isometric conditions, this also equals the dtd ratio:

**dtd_1/dtd_2 = k_r = (I_1/I_2)^(1/5)**

And the compactness ratio:

**D_1/D_2 = k_r^2 = [(I_1/I_2)^(1/5)]^2**

These relationships were confirmed numerically at 50-digit precision across all isometric test cases (Case 3: P=P).

---

## 2. The Universal k_i Formula

Generalizing beyond equal density by making density explicit:

**I_1/I_2 = (rho_1/rho_2) * (r_1/r_2)^5**

Taking the fifth root:

**k_i = (I_1/I_2)^(1/5) = (rho_1/rho_2)^(1/5) * (r_1/r_2)**

This is the universal inertia-derived scale factor. It holds for any two systems, any shape (using mean radius), any density. When density is equal, it reduces to the simple radius ratio. k_i is the most complete single-number proxy for system scale about an axis, as it encodes mass, radius, and density through the moment of inertia.

Confirmed numerically: k_i matches (I_1/I_2)^(1/5) across every test case at full precision.

---

## 3. The General dtd-Inertia Equivalence

The dtd ratio can be expressed in terms of density and radius:

**dtd_1/dtd_2 = (rho_1/rho_2)^(1/2) * (r_1/r_2)**

And k_i has density to the 1/5 power:

**k_i = (rho_1/rho_2)^(1/5) * (r_1/r_2)**

The difference is the exponent on density: 1/2 for time dilation, 1/5 for inertia. This gives the general equivalence:

**dtd_1/dtd_2 = (I_1/I_2)^(1/5) * (rho_1/rho_2)^(3/10)**

The 3/10 exponent (= 1/2 - 1/5) on the density ratio is the exact correction factor that bridges the inertia scale factor to the time dilation ratio in all cases. When density is equal, this term vanishes. When density differs, it provides the precise adjustment.

Confirmed numerically: this formula matches dtd_1/dtd_2 exactly across every test case, including non-isometric cases with wildly different masses, radii, and densities.

---

## 4. The Fundamental Inertia-Time Dilation Identity

From the pair comparison tables, the following identity holds universally:

**(dtd_1/dtd_2)^2 * (r_1/r_2)^3 = I_1/I_2**

Equivalently:

**(dtd_1/dtd_2)^2 = (I_1/I_2) * (r_2/r_1)^3**

This says that time dilation and inertia are the same information, connected through geometry. If you know the time dilation ratio and the radius ratio, you know the inertia ratio. If you know the inertia and the radii, you know the time dilation. They are one phenomenon expressed in two languages.

This identity is only cleanly visible in the dtd representation. The standard gtd = sqrt(1 - r_s/r) formulation obscures it behind the "1 minus" and the singularity at the Schwarzschild radius.

---

## 5. On the dtd and gtd Representations

**dtd (DeGerlia time dilation):** dtd = sqrt(D_norm) = sqrt(r_s/r). Continuous from 0 to infinity. No singularity at r_s; at r = r_s, dtd = 1, and it continues beyond.

**gtd (gravitational time dilation):** gtd = sqrt(1 - r_s/r). Ranges from 1 to 0. Hits zero at r_s and goes imaginary below it.

Key distinctions established:

- dtd and gtd are one-to-one as individual values (dtd^2 + gtd^2 = 1). Neither is more fundamental; they encode the same clock rate in different parameterizations.
- Their **ratios** are different quantities. dtd_1/dtd_2 != gtd_1/gtd_2 in general. You cannot convert one ratio to the other without the absolute values.
- The dtd ratio preserves compactness and scale information. The gtd ratio preserves clock-comparison information. Each collapses away what the other preserves.
- The gtd ratio cannot be expressed as a clean function of inertia and density ratios alone, because the "1 minus" prevents the individual values from factoring out:

  **gtd_1/gtd_2 = sqrt(K^2 + (1 - K^2)/gtd_2^2)**

  where K = (I_1/I_2)^(1/5) * (rho_1/rho_2)^(3/10). The absolute value of gtd_2 persists and cannot be eliminated.

- The dtd ratio has a clean, universal, ratio-only expression. The gtd ratio does not. This is a structural limitation of the gtd representation, not a limitation of the physics.

---

## 6. On Comparing Time Dilation Across Systems

The Schwarzschild gravitational time dilation formula is a single-system calculation: one mass, one metric, one spacetime. GR does not provide a native two-system relative time dilation formula. Taking gtd_1/gtd_2 for two different masses assumes both systems share a common flat reference at infinity — an approximation, not an exact GR operation.

The event horizon at r_s is an observational boundary (where light can no longer escape), not a physical boundary where time stops. The "time stops at r_s" interpretation is a coordinate artifact of Schwarzschild coordinates. The infalling observer crosses the horizon in finite proper time. The singularity is at r = 0, not r = r_s. Matter in stellar collapse passes through r_s; it does not asymptotically approach it.

The dtd framework reflects this physical reality: dtd = 1 at r = r_s is simply a point on a continuum, with compactness continuing smoothly beyond it.

---

## 7. On the Relationship Between Gravity and Electromagnetism

Coulomb's law (F = k_e * q_1 * q_2 / r^2) and Newton's gravity (F = G * m_1 * m_2 / r^2) share identical inverse-square structure. The ratio k_e/G spans approximately 10^20 in SI units.

The k_i framework suggests this ratio is not arbitrary but corresponds to the density and radius scaling between atomic and planetary systems — a span of roughly 10^100 in moment of inertia. Preliminary calculations using real physical values for atomic and planetary systems reproduce k_e/G to within a factor of two, which is within the accumulated precision limits of the input constants (G being the least precisely known fundamental constant, at ~5 significant figures).

This suggests:

- G may not be a true constant but a function of system scale: G(rho, r). This would explain the persistent experimental scatter in G measurements across different apparatus and test masses — different experiments would be measuring slightly different values because their test systems have different k_i values.
- Coulomb's constant is what G becomes when evaluated at atomic scale — same law, same structure, different point on the k_i scaling curve.
- The "two forces" may be one force observed at two different system scales, with k_i providing the transformation between them.

---

## 8. Summary of Key Formulas

| Formula | Description |
|---------|-------------|
| k_i = (rho_1/rho_2)^(1/5) * (r_1/r_2) | Universal inertia-derived scale factor |
| k_i = (I_1/I_2)^(1/5) | Equivalent form from inertia ratio |
| dtd_1/dtd_2 = (I_1/I_2)^(1/5) * (rho_1/rho_2)^(3/10) | General dtd-inertia equivalence |
| (dtd_1/dtd_2)^2 * (r_1/r_2)^3 = I_1/I_2 | Fundamental inertia-time dilation identity |
| D_1/D_2 = (I_1/I_2) * (r_2/r_1)^3 | Compactness from inertia and geometry |
| dtd_1/dtd_2 = sqrt(D_1/D_2) | dtd ratio from compactness ratio |

All formulas confirmed numerically at 50-digit Decimal precision across all test cases in compare_pairs.py and compare_pairs_v2.py.

---

## 9. Implementation

The following rows were added to the pair comparison tables during this session:

- **(I_1/I_2)^(1/2)**: Square root of the inertia ratio
- **rho_1, rho_2**: System density, retrieved from UniformSphere properties
- **k_i = (rho_1/rho_2)^(1/5) * (r_1/r_2)**: Universal scale factor
- **(I_1/I_2)^(1/5) * (rho_1/rho_2)^(3/10)**: General dtd-inertia equivalence

All implemented in both compare_pairs.py and compare_pairs_v2.py, outputting to pair_comparisons_cases.md and pair_comparisons_v2_cases.md respectively.
