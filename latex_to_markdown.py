#!/usr/bin/env python3
"""
latex_to_markdown.py — Convert master.tex to a clean Markdown reading copy.

Preserves: headings, bold, italic, math (inline & display), bullet/numbered
           lists, paragraphs as continuous text (no line wrapping).
Omits:     template markup, page layout, footnotes, figures, tables.

Usage:
    python3 latex_to_markdown.py                → writes latex/full.md
    python3 latex_to_markdown.py --stdout       → prints to stdout
"""

import re, sys, os

HERE      = os.path.dirname(os.path.abspath(__file__))
LATEX_DIR = os.path.join(HERE, 'latex')
TEX       = os.path.join(LATEX_DIR, 'master.tex')
BBL       = os.path.join(LATEX_DIR, 'master.bbl')
OUT       = os.path.join(LATEX_DIR, 'full.md')


# ── LaTeX math → spoken/readable text ───────────────────────────────────────

GREEK = {
    'alpha': 'alpha', 'beta': 'beta', 'gamma': 'gamma', 'delta': 'delta',
    'epsilon': 'epsilon', 'varepsilon': 'epsilon', 'zeta': 'zeta',
    'eta': 'eta', 'theta': 'theta', 'iota': 'iota', 'kappa': 'kappa',
    'lambda': 'lambda', 'mu': 'mu', 'nu': 'nu', 'xi': 'xi', 'pi': 'pi',
    'rho': 'rho', 'sigma': 'sigma', 'tau': 'tau', 'upsilon': 'upsilon',
    'phi': 'phi', 'varphi': 'phi', 'chi': 'chi', 'psi': 'psi',
    'omega': 'omega', 'Gamma': 'Gamma', 'Delta': 'Delta', 'Theta': 'Theta',
    'Lambda': 'Lambda', 'Xi': 'Xi', 'Pi': 'Pi', 'Sigma': 'Sigma',
    'Phi': 'Phi', 'Psi': 'Psi', 'Omega': 'Omega', 'ell': 'l',
}


def _speak_power(exp):
    """Describe an exponent in words."""
    exp = exp.strip().strip('{}')
    if exp == '2': return ' squared'
    if exp == '3': return ' cubed'
    if exp == '1': return ''
    if exp == '-1': return ' to the negative 1'
    if exp == '-2': return ' to the negative 2'
    ordinals = {
        '1': 'first', '2': 'second', '3': 'third', '4': 'fourth',
        '5': 'fifth', '6': 'sixth', '7': 'seventh', '8': 'eighth',
        '9': 'ninth', '10': 'tenth',
    }
    # Simple integer exponent: use ordinal + "power"
    if exp in ordinals:
        return f' to the {ordinals[exp]} power'
    # Negative integer
    m = re.match(r'^-(\d+)$', exp)
    if m:
        return f' to the negative {m.group(1)}'
    # Fractions like 1/5, 1/3, 2/5
    m = re.match(r'^(\d+)/(\d+)$', exp)
    if m:
        n, d = m.group(1), m.group(2)
        if d in ordinals:
            return f' to the {n}-{ordinals[d]}'
    return f' to the {latex_math_to_text("$" + exp + "$")}'


def _speak_sub(sub):
    """Describe a subscript."""
    sub = sub.strip().strip('{}')
    # Simple cases: single letter/number/short label
    sub = latex_math_to_text('$' + sub + '$')
    return f' sub {sub}'


def latex_math_to_text(math):
    """Convert a LaTeX math string to readable spoken English."""
    s = math.strip()

    # Remove math delimiters
    s = re.sub(r'^\$\$|\$\$$', '', s)
    s = re.sub(r'^\$|\$$', '', s)

    # Remove alignment characters from align environments
    s = s.replace('&=', ' = ').replace('& =', ' = ').replace('&', ' ')
    # Line breaks → newlines
    s = re.sub(r'\\\\(?:\[[^\]]*\])?', '\n', s)
    # Remove \nonumber, \notag, \label
    s = re.sub(r'\\(?:nonumber|notag)', '', s)
    s = re.sub(r'\\label\{[^}]*\}', '', s)

    # Strip \left, \right, sizing
    for cmd in ['left', 'right', 'bigg', 'Bigg', 'Big', 'big', 'displaystyle']:
        s = re.sub(r'\\' + cmd + r'(?![a-zA-Z])', '', s)

    # Spacing commands
    for cmd in [r'\,', r'\;', r'\!', r'\quad', r'\qquad']:
        s = s.replace(cmd, ' ')

    # Greek letters (longer names first)
    for name in sorted(GREEK.keys(), key=len, reverse=True):
        s = re.sub(r'\\' + name + r'(?![a-zA-Z])', GREEK[name], s)

    # \text{...}, \mathrm{...} etc. → just the text
    s = re.sub(r'\\(?:text|mathrm|mathit|mathbf|textit|textbf|operatorname)\{([^}]*)\}', r'\1', s)

    # \sqrt{...} → the square root of the quantity ...
    def replace_sqrt(m):
        content = latex_math_to_text('$' + m.group(1) + '$')
        return f'the square root of the quantity {content}'
    s = re.sub(r'\\sqrt\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', replace_sqrt, s)

    # \frac{num}{den} → (num) over (den)
    def _needs_grouping(text):
        """Only group with 'the quantity' when there's an actual
        multi-term expression (addition, subtraction) that would
        be ambiguous without it."""
        t = text.strip()
        # Check for + or - that aren't part of scientific notation
        # Strip leading minus (negative sign)
        inner = re.sub(r'^-\s*', '', t)
        return bool(re.search(r'[+\-]', inner))

    def replace_frac(m):
        num = latex_math_to_text('$' + m.group(1) + '$')
        den = latex_math_to_text('$' + m.group(2) + '$')
        if _needs_grouping(den):
            den = f'the quantity {den}'
        if _needs_grouping(num):
            num = f'the quantity {num}'
        return f'{num} over {den}'
    for _ in range(4):
        s = re.sub(r'\\(?:frac|dfrac|tfrac)\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}',
                    replace_frac, s)

    # Summation and product (must come before subscript handling)
    s = re.sub(r'\\sum_\{([^}]*)\}', r'the sum over \1 of ', s)
    s = re.sub(r'\\sum_([a-zA-Z0-9])', r'the sum over \1 of ', s)
    s = re.sub(r'\\sum', 'the sum of ', s)
    s = re.sub(r'\\prod_\{([^}]*)\}', r'the product over \1 of ', s)
    s = re.sub(r'\\prod', 'the product of ', s)

    # Superscripts: ^{...}
    def replace_sup(m):
        return _speak_power(m.group(1))
    s = re.sub(r'\^\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', replace_sup, s)
    # Single char superscript without braces: ^2, ^3, ^n etc.
    s = re.sub(r'\^([a-zA-Z0-9])', lambda m: _speak_power(m.group(1)), s)

    # Subscripts: _{...}
    def replace_sub_match(m):
        return _speak_sub(m.group(1))
    s = re.sub(r'_\{([^{}]*)\}', replace_sub_match, s)
    s = re.sub(r'_([a-zA-Z0-9])', lambda m: _speak_sub(m.group(1)), s)

    # \underbrace{...}_{...}
    s = re.sub(r'\\underbrace\{([^}]*)\}', r'\1', s)
    s = re.sub(r'\\overbrace\{([^}]*)\}', r'\1', s)

    # Symbol words
    s = s.replace(r'\times', ' times ')
    s = s.replace(r'\cdot', ' times ')
    s = s.replace(r'\pm', ' plus or minus ')
    s = s.replace(r'\leq', ' less than or equal to ')
    s = s.replace(r'\geq', ' greater than or equal to ')
    s = s.replace(r'\neq', ' not equal to ')
    s = s.replace(r'\approx', ' approximately equal to ')
    s = s.replace(r'\equiv', ' is equivalent to ')
    s = s.replace(r'\propto', ' is proportional to ')
    s = s.replace(r'\infty', 'infinity')
    s = s.replace(r'\rightarrow', ' yields ')
    s = s.replace(r'\to', ' yields ')

    # \hat, \bar, \dot, \vec
    s = re.sub(r'\\hat\{([^}]*)\}', r'\1-hat', s)
    s = re.sub(r'\\bar\{([^}]*)\}', r'\1-bar', s)
    s = re.sub(r'\\dot\{([^}]*)\}', r'\1-dot', s)
    s = re.sub(r'\\vec\{([^}]*)\}', r'vector \1', s)

    # Primes after variables: x' → x prime, x'' → x double prime
    # Only match prime marks right after a letter (math variable context)
    s = re.sub(r"([a-zA-Z])''", r'\1 double prime', s)
    s = re.sub(r"([a-zA-Z])'", r'\1 prime', s)

    # Strip any remaining backslash commands
    s = re.sub(r'\\[a-zA-Z]+', '', s)

    # Clean braces
    s = s.replace('{', '').replace('}', '')

    # Clean up
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r' *\n *', '\n', s)

    # Grouped expressions with exponents: "(X) to the ..." → "the quantity of X, to the ..."
    # The reader can't hear parentheses, so we need "the quantity of" to convey grouping
    s = re.sub(r'\(([^()]+)\) (to the [^,.\n]+)', r'the quantity of \1, \2', s)
    # Remaining bare parens that the reader won't voice — just remove them
    # (single terms in parens don't need grouping language)
    s = s.replace('(', '').replace(')', '')

    # Split adjacent single variables: "kR" → "k R", "kl" → "k l"
    # Just add a space so the reader pauses naturally
    known_words = {'dt', 'kg', 'km', 'pi', 'ln', 'of', 'or', 'is', 'if',
                   'to', 'an', 'at', 'by', 'in', 'on', 'no', 'do', 'so',
                   'the', 'and', 'for', 'not', 'sub', 'over', 'sum', 'all',
                   'its', 'two', 'has', 'may', 'per', 'any'}
    def _split_adjacent_vars(m):
        full = m.group(0)
        if full.lower() in known_words:
            return full
        return f'{full[0]} {full[1]}'
    s = re.sub(r'(?<![a-zA-Z])([a-zA-Z])([a-zA-Z])(?![a-zA-Z])', _split_adjacent_vars, s)

    # \LaTeX → LaTeX
    s = s.replace('\\LaTeX', 'LaTeX')

    return s.strip()


# ── LaTeX → Markdown text cleanup ───────────────────────────────────────────

def clean_inline(text):
    """Convert LaTeX inline markup to Markdown, with math spelled out."""
    # Convert inline math $...$ to spoken text FIRST (before braces are stripped)
    text = re.sub(r'\$([^$]+)\$', lambda m: latex_math_to_text(m.group(0)), text)

    # Strip comments
    text = re.sub(r'(?<!\\)%[^\n]*', '', text)

    # Non-breaking space and LaTeX thin spaces
    text = text.replace('~', ' ')
    text = text.replace(r'\,', ' ')
    text = text.replace(r'\LaTeX', 'LaTeX')

    # Bold, italic, monospace: just keep the text
    text = re.sub(r'\\textbf\{([^{}]*)\}', r'\1', text)
    text = re.sub(r'\\(?:textit|emph)\{([^{}]*)\}', r'\1', text)
    text = re.sub(r'\\texttt\{([^{}]*)\}', r'\1', text)

    # Hyperlinks: just keep display text
    text = re.sub(r'\\href\{([^}]*)\}\{([^}]*)\}', r'\2', text)
    text = re.sub(r'\\url\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\nolinkurl\{([^}]*)\}', r'\1', text)

    # Citations: strip entirely for readable output
    text = re.sub(r'\\(?:citep?|citet)\{[^}]*\}', '', text)

    # Cross-references
    text = re.sub(r'\\ref\{([^}]*)\}', r'§\1', text)
    text = re.sub(r'\\label\{[^}]*\}', '', text)

    # Drop footnotes
    text = re.sub(r'\\footnote(?:text)?\{[^}]*\}', '', text)

    # Unwrap sizing commands (keep content)
    for cmd in ['normalsize', 'large', 'Large', 'LARGE', 'small', 'tiny',
                'noindent', 'text', 'mathrm', 'mathit', 'mathbf', 'mathbb',
                'textrm', 'textsc', 'mbox', 'hbox', 'textsuperscript']:
        text = re.sub(r'\\' + cmd + r'\{([^{}]*)\}', r'\1', text)

    # \left, \right, \cdot, \times etc. — leave for math rendering
    # But strip non-math bare commands
    # Remove \vspace, \hspace, \hfill etc.
    text = re.sub(r'\\(?:vspace|hspace|hfill|phantom|vphantom)\{[^}]*\}', '', text)
    text = re.sub(r'\\(?:vspace|hspace|hfill|phantom|vphantom)\b', '', text)

    # Remove \par, \newline, \\  (but not inside math)
    text = re.sub(r'\\par\b', '', text)

    # Remaining \command{content} outside math → content
    # Be careful not to eat math commands — only strip if not inside $...$
    # We'll do a conservative pass: only strip known non-math commands
    for cmd in ['underline', 'overline', 'centering', 'raggedright']:
        text = re.sub(r'\\' + cmd + r'\{([^{}]*)\}', r'\1', text)

    # Strip stray braces (not part of math)
    # Only strip braces that aren't preceded by \ or inside $
    text = re.sub(r'(?<![\\$])\{([^{}]*)\}', r'\1', text)

    # Typographic dashes
    text = text.replace('---', '\u2014')
    text = text.replace('--', '\u2013')

    # Typographic quotes
    text = text.replace('``', '\u201c').replace("''", '\u201d').replace('`', '\u2018')

    # Clean up extra spaces before punctuation
    text = re.sub(r' +([.,;:!?])', r'\1', text)

    # Collapse whitespace (but not newlines)
    text = re.sub(r'[ \t]+', ' ', text)

    # Spell out units for reader
    text = text.replace('kgtimesmsquared', 'kilogram meters squared')
    text = text.replace('kg/m', 'kilograms per meter')
    text = re.sub(r'msquared', 'meters squared', text)
    text = re.sub(r'mcubed', 'meters cubed', text)
    text = re.sub(r'\bkg\b', 'kilograms', text)
    text = text.replace('\\LaTeX', 'LaTeX')

    return text.strip()


# ── Extract document parts ──────────────────────────────────────────────────

def get_title(src):
    m = re.search(r'\\LARGE\{\\textbf\{([^}]+)\}\}', src)
    return clean_inline(m.group(1)) if m else ''


def get_author(src):
    m = re.search(r'\\large\{(Thomas[^}]+)\}', src)
    if not m:
        return ''
    a = re.sub(r'\$[^$]*\$', '', m.group(1))
    a = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', a)
    a = re.sub(r'\\[a-zA-Z]+', '', a)
    a = re.sub(r'[{},$^\u2020]', '', a)
    return a.strip().rstrip(',').strip()


def get_dates(src):
    return [clean_inline(m.group(1))
            for m in re.finditer(r'\\small\{((?:Originally|Revision)[^}]+)\}', src)]


def get_abstract(src):
    m = re.search(r'ABSTRACT:\s*(.*?)(?=\\end\{tabular\})', src, re.DOTALL)
    if not m:
        return ''
    text = m.group(1)
    # Trim at the closing brace+backslash that ends the abstract cell
    text = re.sub(r'\}\s*\\\\.*', '', text, flags=re.DOTALL)
    return clean_inline(text)


# ── Bibliography ────────────────────────────────────────────────────────────

def get_refs(path):
    if not os.path.exists(path):
        return []
    text = open(path).read()
    text = re.sub(r'\\(?:begin|end)\{(?:mcite)?thebibliography\}\{?[^}]*\}?', '', text)
    # Remove mcite control commands
    text = re.sub(r'\\(?:mcite|providecommand)[^\n]*\n', '', text)
    items = re.split(r'\\bibitem(?:\[[^\]]*\])?\{[^}]+\}', text)[1:]
    refs = []
    for item in items:
        # Stop at \relax or \mcite
        t = re.sub(r'\\relax.*', '', item, flags=re.DOTALL)
        t = re.sub(r'\\mcite[^\n]*', '', t)
        t = re.sub(r'\\EndOfBibitem', '', t)
        t = t.replace('\\newblock', ' ')
        t = re.sub(r'\\emph\{([^}]*)\}', r'\1', t)
        t = re.sub(r'\\textbf\{([^}]*)\}', r'\1', t)
        t = re.sub(r'\\href\{([^}]*)\}\{([^}]*)\}', r'\2', t)
        # Strip remaining commands
        t = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', t)
        t = re.sub(r'\\[a-zA-Z]+', ' ', t)
        t = re.sub(r'[{}~]', ' ', t)
        t = t.replace('--', '\u2013')
        t = re.sub(r'\s+', ' ', t).strip()
        if t:
            refs.append(t)
    return refs


# ── Body processing ─────────────────────────────────────────────────────────

def process_body(src):
    """Parse the document body; return list of markdown lines."""

    # Isolate body
    m = re.search(r'%%%END OF TITLE, AUTHORS AND ABSTRACT%%%', src)
    body = src[m.end():] if m else src

    # Strip structural noise
    body = re.sub(r'%%%[^\n]*\n', '', body)
    body = re.sub(r'^\\footnotetext.*$', '', body, flags=re.MULTILINE)
    body = re.sub(r'\\renewcommand[^\n]+', '', body)
    body = re.sub(r'\\rmfamily|\\normalfont|\\upshape', '', body)
    body = re.sub(r'\\vspace\{[^}]*\}', '', body)
    body = re.sub(r'\\bibliography(?:style)?\{[^}]*\}', '', body)
    body = re.sub(r'\\balance|\\clearpage|\\end\{document\}', '', body)

    # Display equations: \begin{equation}...\end{equation} → $$ ... $$
    def convert_display_eq(m):
        eq = m.group(1).strip()
        eq = re.sub(r'\\label\{[^}]*\}', '', eq)
        return f'\n\n$$\n{eq}\n$$\n\n'

    body = re.sub(
        r'\\begin\{equation\}(.*?)\\end\{equation\}',
        convert_display_eq, body, flags=re.DOTALL)

    # Align environments → $$ ... $$ (preserve the LaTeX math content)
    def convert_align_eq(m):
        eq = m.group(1).strip()
        eq = re.sub(r'\\label\{[^}]*\}', '', eq)
        eq = re.sub(r'\\notag', '', eq)
        return f'\n\n$$\n{eq}\n$$\n\n'

    for env in ['align', 'align\\*', 'eqnarray', 'eqnarray\\*']:
        body = re.sub(
            r'\\begin\{' + env + r'\}(.*?)\\end\{' + env + r'\}',
            convert_align_eq, body, flags=re.DOTALL)

    # Unnumbered display math \[...\]
    def convert_bracket_eq(m):
        eq = m.group(1).strip()
        return f'\n\n$$\n{eq}\n$$\n\n'

    body = re.sub(r'\\\[(.*?)\\\]', convert_bracket_eq, body, flags=re.DOTALL)

    # Remove figure/table/tabular environments entirely
    for env in ['figure', 'table', 'tabular']:
        body = re.sub(
            r'\\begin\{' + env + r'\*?\}.*?\\end\{' + env + r'\*?\}',
            '', body, flags=re.DOTALL)

    # Convert mdframed (example boxes) — keep content
    body = re.sub(r'\\begin\{mdframed\}(?:\[[^\]]*\])?', '', body)
    body = re.sub(r'\\end\{mdframed\}', '', body)

    # Convert itemize/enumerate
    body = re.sub(r'\\begin\{(?:itemize|enumerate)\}(?:\[[^\]]*\])?', '\n[LIST_START]\n', body)
    body = re.sub(r'\\end\{(?:itemize|enumerate)\}', '\n[LIST_END]\n', body)
    body = re.sub(r'\\item\s*', '\n[ITEM] ', body)

    # ── line-by-line pass ───────────────────────────────────────────────
    out = []
    para = []
    in_list = 0
    in_math = False
    in_appendix = False
    appendix_letter = 'A'
    math_lines = []
    sec_num = sub_num = ssub_num = 0

    def flush():
        """Emit current paragraph as a single continuous line."""
        if not para:
            return
        text = clean_inline(' '.join(para))
        text = re.sub(r'\s+', ' ', text).strip()
        para.clear()
        if len(text) > 4:
            out.append(text)
            out.append('')

    for line in body.split('\n'):
        s = line.strip()

        # Track math blocks ($$)
        if s.startswith('$$'):
            if in_math:
                math_lines.append(s)
                raw = '\n'.join(math_lines)
                spoken = latex_math_to_text(raw)
                for line in spoken.split('\n'):
                    line = line.strip()
                    if line:
                        out.append(f'    {line}')
                out.append('')
                math_lines = []
                in_math = False
            else:
                flush()
                math_lines = [s]
                in_math = True
            continue
        if in_math:
            math_lines.append(s)
            continue

        # List markers
        if s == '[LIST_START]':
            flush()
            in_list += 1
            continue
        if s == '[LIST_END]':
            flush()
            in_list = max(0, in_list - 1)
            continue
        if s.startswith('[ITEM] '):
            flush()
            content = s[7:]
            para.append(content)
            # We'll flush this as a bullet when we hit the next item or list end
            text = clean_inline(' '.join(para))
            text = re.sub(r'\s+', ' ', text).strip()
            para.clear()
            if text:
                indent = '  ' * max(0, in_list - 1)
                out.append(f'{indent}- {text}')
            continue

        # \appendix
        if s == '\\appendix':
            flush()
            in_appendix = True
            appendix_letter = 'A'
            sec_num = 0; sub_num = 0; ssub_num = 0
            continue

        # \section{...} or \section*{...}
        m = re.match(r'\\section\*?\{([^}]+)\}(.*)', s)
        if m:
            flush()
            starred = '*' in s.split('{')[0]
            heading = clean_inline(m.group(1))
            if starred:
                out.append('')
                out.append(heading)
            elif in_appendix:
                out.append('')
                out.append(f'Appendix {appendix_letter}: {heading}')
                appendix_letter = chr(ord(appendix_letter) + 1)
            else:
                sec_num += 1; sub_num = 0; ssub_num = 0
                out.append('')
                out.append(f'Section {sec_num}: {heading}')
            out.append('')
            rest = m.group(2).strip()
            if rest:
                para.append(rest)
            continue

        # \subsection{...}
        m = re.match(r'\\subsection\{([^}]+)\}(.*)', s)
        if m:
            flush()
            sub_num += 1; ssub_num = 0
            heading = clean_inline(m.group(1))
            out.append('')
            out.append(f'Section {sec_num}.{sub_num}: {heading}')
            out.append('')
            rest = m.group(2).strip()
            if rest:
                para.append(rest)
            continue

        # \subsubsection{...} or \subsubsection*{...}
        m = re.match(r'\\subsubsection\*?\{([^}]+)\}(.*)', s)
        if m:
            flush()
            ssub_num += 1
            heading = clean_inline(m.group(1))
            out.append('')
            out.append(heading)
            out.append('')
            rest = m.group(2).strip()
            if rest:
                para.append(rest)
            continue

        # Skip \begin{...} / \end{...} lines
        if re.match(r'\\(?:begin|end)\{', s):
            continue

        # Blank line → paragraph break
        if s == '':
            flush()
            continue

        para.append(s)

    flush()
    return out


# ── main ────────────────────────────────────────────────────────────────────

def main():
    to_stdout = '--stdout' in sys.argv
    src = open(TEX).read()
    out = []

    # Title
    title = get_title(src)
    if title:
        out.append(title)
        out.append('')

    # Author + dates
    author = get_author(src)
    if author:
        out.append(author)
    for d in get_dates(src):
        out.append(d)
    out.append('')

    # Abstract
    abstract = get_abstract(src)
    if abstract:
        out.append('Abstract')
        out.append('')
        out.append(abstract)
        out.append('')

    # Body
    out += process_body(src)

    # References
    refs = get_refs(BBL)
    if refs:
        out.append('')
        out.append('References')
        out.append('')
        for i, ref in enumerate(refs, 1):
            out.append(f'{i}. {ref}')
        out.append('')

    text = '\n'.join(out)

    # Clean up excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)

    if to_stdout:
        print(text)
    else:
        with open(OUT, 'w') as f:
            f.write(text)
        print(f'Written: {OUT}', file=sys.stderr)


if __name__ == '__main__':
    main()
