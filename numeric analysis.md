$$k = \left(\frac{I_2}{I_1}\right)^{1/L} = \left(\frac{m_2 r_2^2}{m_1 r_1^2}\right)^{1/L}$$

where $L$ is the isometric degree of homogeneity for characteristic length.

---

**Scaling reference — isometric scaling at static density:**

| Ratio | L |
|-------|---|
| $I_a/I_b$ | 5 |
| $E_a/E_b$ | 5 |
| $F_a/F_b$ | 4 |
| $M_a/M_b$ | 3 |
| $V_a/V_b$ | 3 |
| $A_a/A_b$ | 2 |
| $r_a/r_b$ | 1 |
| $l_a/l_b$ | 1 |

$I = mr_{mean}^2$ where $r$ refers to mean radius about the selected axis.

---

**Case 1 — Static Mass** $(m_1 = m_2 = m_s,\ r_1 \neq r_2)$

$$k = \left(\frac{I_2}{I_1}\right)^{1/L} = \left(\frac{m_s r_2^2}{m_s r_1^2}\right)^{1/L} = \left(\frac{r_2^2}{r_1^2}\right)^{1/2} = \frac{r_2}{r_1}$$

---

**Case 2 — Static Radius** $(r_1 = r_2 = r_s,\ m_1 \neq m_2)$

$$k = \left(\frac{I_2}{I_1}\right)^{1/L} = \left(\frac{m_2 r_s^2}{m_1 r_s^2}\right)^{1/L} = \left(\frac{m_2}{m_1}\right)^{1/3}$$

---

**General Case** $(m_1 \neq m_2,\ r_1 \neq r_2)$

$$k = \left(\frac{I_2}{I_1}\right)^{1/5} = \left(\frac{m_2 r_2^2}{m_1 r_1^2}\right)^{1/5}$$



# Mathematics and Verification for master "Deriving Relativistic Time Dilation from Inertia: A Unified Origin of the Lorentz and Schwarzschild Metrics"
By Tom DeGerlia, 2026

## Abstract

A single generalized expression — the Spacetime Equivalence (STE) — is shown to produce both the Lorentz factor and the Schwarzschild metric time dilation term as exact special cases. The STE yields the linear scale factor between any two physical systems, and all three of its forms reduce to a ratio of radii under their respective conditions. Both classical relativistic results emerge from this expression without additional parameters, geometric similarity, or domain restrictions. Internal consistency is demonstrated by independent two-path verification.

---

## The Spacetime Equivalence

The STE takes two forms depending on available physical description.

**General form — moment of inertia:**
$$\boxed{k = \left(\frac{I_2}{I_1}\right)^{1/5}}$$

**Linear form — mass only:**
$$\boxed{k = \left(\frac{m_2}{m_1}\right)^{1/3}}$$

By convention, System 1 denotes the observer and System 2 the observed, consistent with the Schwarzschild convention.

In all cases, $k$ is the linear scale factor between the two systems. Under their respective scaling conditions, all forms of STE reduce identically to:

$$k = \frac{r_2}{r_1}$$

The moment of inertia form is the most general — it carries both mass and geometric information simultaneously and covers all cases. The mass-only form applies where geometry is unavailable or irrelevant. Both are exact; neither is an approximation of the other.

---

## Unified Time Dilation

All relativistic time dilation — gravitational and kinematic — is expressed through a single relation:

$$\frac{d\tau}{dt} = \sqrt{1 - k}$$

The Schwarzschild and Lorentz results are not independent discoveries. They are the same expression evaluated under different physical constraints on the same underlying parameter $k$.

---

## Special Cases

### Schwarzschild Metric — Constant Mass

When mass is held constant and radius varies, STE reduces exactly to the Schwarzschild gravitational time dilation term:

$$k = \frac{r_s}{r} = \frac{2GM}{rc^2} \qquad \Rightarrow \qquad \frac{d\tau}{dt} = \sqrt{1 - \frac{r_s}{r}}$$

### Lorentz Factor — Constant Radius

When radius is held constant and mass varies, STE reduces exactly to the Lorentz kinematic time dilation factor:

$$k = \left(\frac{m_2}{m_1}\right)^{1/3} \equiv \frac{v^2}{c^2} \qquad \Rightarrow \qquad \frac{d\tau}{dt} = \sqrt{1 - \frac{v^2}{c^2}}$$

### Constant Density

When density is held constant, STE reduces directly to a pure linear scale ratio:

$$k = \frac{r_2}{r_1} \qquad \Rightarrow \qquad \frac{d\tau}{dt} = \sqrt{1 - \frac{r_2}{r_1}}$$

---

## The General Case

When neither mass nor radius is constrained — two genuinely dissimilar systems — the full moment of inertia form applies:

$$k = \left(\frac{I_2}{I_1}\right)^{1/5}$$

This is the form that subsumes all special cases. It applies at any scale, about any axis, between any two physically distinct systems, and requires no assumption about which physical parameter varies.

---

## Verification

The general case was verified by demonstrating that it decomposes exactly into its two special cases applied sequentially.

Starting from $I = mr^2$:

$$k = \left(\frac{I_2}{I_1}\right)^{1/5}$$

$$= \left(\frac{m_2 r_2^2}{m_1 r_1^2}\right)^{1/5}$$

$$= \left(\frac{m_2}{m_1} \cdot \frac{r_2^2}{r_1^2}\right)^{1/5}$$

$$= \left(\frac{m_2}{m_1}\right)^{1/5} \cdot \left(\frac{r_2^2}{r_1^2}\right)^{1/5}$$

$$= \left(\frac{m_2}{m_1}\right)^{1/5} \cdot \left(\frac{r_2}{r_1}\right)^{2/5}$$

$$= k_{\text{mass}} \times k_{\text{radius}}$$

Computed independently for $S_1 = \{m=10^{30}\text{kg},\ r=10^{8}\text{m}\}$, $S_2 = \{m=10^{20}\text{kg},\ r=10^{7}\text{m}\}$:

| Path | $k$ | $d\tau/dt$ |
|---|---|---|
| Direct — general form | 0.003981 | 0.998007 |
| Two-step — sequential special cases | 0.003981 | 0.998007 |

Both paths produce identical results. The special cases are exact multiplicative decompositions of the general case. This confirms that STE is internally consistent across all forms and all scaling conditions.

---

## Conclusion

The Schwarzschild metric and the Lorentz factor share a common origin. Both are instances of the single relation $\frac{d\tau}{dt} = \sqrt{1-k}$, where $k$ is the STE — the linear scale factor between any two systems, expressed as the fifth root of their moment of inertia ratio. Gravitational and kinematic time dilation are not distinct phenomena requiring separate theoretical frameworks. They are the same phenomenon, expressed under different physical constraints, unified by a single inertial parameter whose physical meaning is always and only linear scale.