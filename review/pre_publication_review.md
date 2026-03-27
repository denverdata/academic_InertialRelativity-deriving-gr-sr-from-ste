# Pre-Publication Review: "Deriving Relativistic Time from Inertia"

Reviewer: Claude (requested by author)
Date: March 26, 2026
Reviewed file: `latex/master.tex`

---

## 1. Front Matter

**1a. "C.E." on dates (lines 133–134)**
"February 6, 2026 C.E." and "Revision 2.10 March 24, 2026 C.E." — the era designation is unusual in physics papers. Standard practice is just the date. The version number "2.10" is also atypical; journals usually use "Revised: [date]" without version numbers.

**1b. Underlined text in the abstract (line 136)**
The `\ul{}` around the key claim is non-standard for academic abstracts. Italics or bold would be conventional if emphasis is desired; many journals actively prohibit underlining.

**1c. Missing dagger footnote (line 132)**
The author name has a `$\dag$` superscript, but there's no corresponding footnote. In RSC templates, `\dag` typically marks the corresponding author or ESI note. There should be a `\footnotetext{\dag~...}` matching it.

**1d. Missing keywords**
RSC papers typically include a keywords line below the abstract. Not required for every venue, but worth noting.

**1e. Missing Conflicts of Interest statement**
Increasingly standard/required. Even a "The author declares no competing interests" line is expected by most venues.

---

## 2. Language & Tone

**2a. "a delta in rotational motion" / "a delta in translational motion" (lines 166, 177)**
"Delta" used informally. Academic standard would be "change in" or the specific physics term ("angular acceleration," "translational acceleration").

**2b. "you choose to define" (line 163)**
Second person is informal for academic writing. Standard would be "one chooses to define" or "that may be defined."

**2c. "absolutely independent" (line 202)**
"Absolutely" is emphatic/informal. "Independent" alone carries the meaning.

**2d. "however small that is" (line 275)**
Informal. "However small" suffices.

**2e. The quote about adults and children (lines 158–160)**
This is a stylistic choice — it's accessible and engaging, but it's informal for a physics paper. It's also unattributed; if it's the author's own, it shouldn't be in quotation marks (or should be introduced as "consider the following observation:" rather than as a quote). If it's from somewhere, cite it.

---

## 3. Notation & Formatting

**3a. "Linear Scale Vector" — should be "Factor" (line 253)**
Section 3.1 title says "Relating Linear Scale Vector $k$ to General Relativity." $k$ is a scalar throughout the paper. "Vector" is incorrect; "Factor" or "Parameter" is what you mean.

**3b. Dangling colon (line 258)**
The sentence ends with "...the linear scale factor derived from inertia:" followed immediately by a new subsection header. The colon promises continuation that never comes.

**3c. Inconsistent $r_s$ notation (line 371)**
The paper uses $r_s$ everywhere, but the unification section has "where $r_2$ is $R_S$" — both a different subscript naming ($r_2$ vs $r_s$) and different capitalization ($R_S$ vs $r_s$).

**3d. Double space and missing punctuation (line 371)**
"simplifies to $k = R_2^2/R_1^2$  $M/M$ cancels" — extra space, and "$M/M$ cancels" should be set off with punctuation (e.g., parenthetical or a clause like "since $M/M$ cancels").

**3e. Inconsistent cross-referencing (line 317)**
"see Appendix A: Special-Case Derivations" is hardcoded text, while everywhere else you use `\ref{app:general_ste}`. Similarly, lines 348 and 355 use `\ref{app:general_ste}` without the "Appendix~" prefix that appears elsewhere.

**3f. Duplicate package loading (lines 22 and 33)**
`\usepackage{array}` is loaded twice.

**3g. `siunitx` loaded but unused**
The package is loaded (line 13) but all units are formatted manually. Not a problem, but either use it or remove it.

---

## 4. Mathematical Exposition

**4a. Section 5.1 derivation skips the key step (lines 330–337)**
The main text goes from $(M r_s^2 / M R_1^2)^{1/5}$ directly to $(r_s^5/R^5)^{1/5} = r_s/R$. As written, this implies $r_s^2 = r_s^5$. The actual logic (shown properly in the Appendix) is that when mass cancels, the degree of homogeneity changes from $L=5$ to $L=2$, giving $(r_s^2/R^2)^{1/2} = r_s/R$. The main text either needs to show this step or reference the appendix explicitly at the point where the jump occurs.

**4b. Section 3.1 is nearly empty**
Section 3.1 ("Relating Linear Scale Vector $k$ to General Relativity") contains one equation, a half-sentence description, and then ends. This is unusually thin for a titled subsection. Consider merging it into the preceding or following section.

**4c. Redundancy across Sections 5, 6, and 7**
Section 5 derives each case. Section 6 restates the same derivations in paragraph form. Section 7 restates the key results again. The content overlaps significantly. A reviewer may flag this as repetitive. Consider whether Section 6 can be tightened to focus only on the unification argument rather than re-deriving.

**4d. $v^2/c^2$ described as "a ratio of two lengths" (line 352)**
Strictly, it's the square of a ratio of two lengths (or a ratio of two squared lengths). Minor imprecision.

---

## 5. Case 1 Example — Gratuitous Approximation (lines 433–446)

The derivation sets $R_2 = r_s$ exactly, but the example uses $R_2 = 2954$ m while $r_s = 2953.34$ m ("just above"). This means the STE calculation uses $k = 2954/R_1$ while the Schwarzschild confirmation uses $k = r_s/R_1 = 2953.34/R_1$. The results match to 11 figures, which is fine, but the discrepancy is self-inflicted. Since the Schwarzschild formula is evaluated at $R_1$ (not at $r_s$), there's no singularity to avoid. Using $R_2 = r_s$ exactly would give exact agreement and be cleaner.

---

## 6. Case 4 — Potential Clarity Issue (lines 500–513)

When $I_1 = I_2$, the STE gives $k = 1$, and the paper states "no relative time dilation exists." But the time dilation formula (Equation 13) says $d\tau/dt = \sqrt{1-k}$, so $k=1$ gives $d\tau/dt = 0$ (complete time stoppage — the black hole horizon). The paper doesn't use Equation 13 in Case 4, but a reader following the formalism will notice the apparent conflict. A sentence clarifying that $k=1$ here means the scale factor is unity (equal inertia, equal time rates) — distinct from $k_{gravitational}=1$ where $R=r_s$ — would preempt this confusion.

---

## 7. Bibliography

**7a. DOI in `note` field (bib entries for degerlia202501, degerlia202505)**
The DOIs are in the `note` field as text. Most BibTeX styles expect a `doi` field for proper formatting/hyperlinking.

**7b. Missing volume numbers**
Einstein 1915 and Schwarzschild 1916 entries lack volume numbers. These are historical entries and the information is available.

**7c. Euler 1755**
No page numbers or chapter reference. "Euler's theorem on homogeneous functions" is commonly attributed to this work, but a modern reference (e.g., a textbook that states the theorem) might be more accessible to reviewers and readers.

---

## 8. Structural / Missing Elements

**8a. No acknowledgments section**
Optional, but conventional even if brief.

**8b. GitHub URL (line 545)**
Verify that `https://github.com/denverdata/academic_InertialRelativity-deriving-gr-sr-from-ste` is publicly accessible and contains what you want people to see.

---

## Priority Tiers

### Should fix (will look like errors to reviewers)
- 3a: "Vector" → "Factor" in section title
- 3b: Dangling colon
- 3c: Inconsistent $r_s$ / $R_S$ notation
- 3d: Double space / missing punctuation in §6
- 4a: Skipped step in §5.1 derivation
- 1c: Missing dagger footnote

### Worth fixing (polish)
- 1a: Remove "C.E." from dates
- 1b: Replace underline with italics in abstract
- 2a: "delta" → "change in"
- 2b: Second person → third person
- 3e: Consistent cross-references
- 3f: Remove duplicate `array` package
- 5: Use $R_2 = r_s$ exactly in Case 1 example
- 6: Add clarifying sentence to Case 4
- 7a: Move DOIs to proper field

### Consider (reviewer-dependent)
- 1d: Add keywords
- 1e: Add conflicts of interest statement
- 2e: The quotation — keep or formalize
- 4b: Merge or expand §3.1
- 4c: Reduce redundancy in §5–7
- 7c: Modernize the Euler citation
