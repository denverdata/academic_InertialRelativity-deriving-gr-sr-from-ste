# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

Compile the LaTeX paper (from the `latex/` directory):
```bash
# Full build with bibliography
cd latex && pdflatex master.tex && bibtex master && pdflatex master.tex && pdflatex master.tex

# Quick compile (no bibliography update)
cd latex && pdflatex master.tex

# Using latexmk (preferred, handles all passes automatically)
cd latex && latexmk -pdf master.tex

# Clean auxiliary files
cd latex && latexmk -c
```

## Repository Structure

| Path | Purpose |
|------|---------|
| `latex/master.tex` | Primary deliverable — the academic preprint paper (RSC journal template) |
| `latex/rsc.bib` | BibTeX bibliography (all citations live here) |
| `latex/master_template.tex` | Original unmodified RSC template — do not use as content source |
| `latex/master_backup.tex` | Backup of prior revision |
| `referenced_docs/derivation_lean_v3.txt` | Canonical content source for the derivation — serves as literal content source for the paper |
| `project/project_theoretical_foundation.md` | Author's stated objectives, core formulas, and final document requirements |
| `supporting_materials/` | Background notes and prior thinking (not primary sources) |
| `output/` | Draft outputs and intermediate documents |

## Core Physics (from `project/project_theoretical_foundation.md`)

The paper's central claim is **Inertial Relativity**: that GR and SR are edge cases of the Space-Time Equivalence (STE):

$$\frac{T_1}{T_2} = \left(\frac{I_2}{I_1}\right)^{1/5} \quad \text{[rotational --- moment of inertia]}$$

$$\frac{T_1}{T_2} = \left(\frac{M_2}{M_1}\right)^{1/3} \quad \text{[linear --- mass only]}$$

Key prior works cited in `latex/rsc.bib`:
- `degerlia2025` — "Introducing Inertial Density" (Schwarzschild threshold as M/R constant)
- `degerlia2025universe` — "The Universe of Light" (STE origin)

The LaTeX template structure (two-column RSC journal format) must not be altered. All page setup, header/footer, and font commands in the preamble are locked per template instructions embedded in comments.
