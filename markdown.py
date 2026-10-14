"""Minimal Markdown -> HTML parser (stdlib only).

Supported block syntax:
  ## H2, ### H3, paragraphs, - unordered lists, 1. ordered lists,
  > blockquotes, --- horizontal rule.
Supported inline syntax: **bold**, *italic*, `code`, [text](url).

FAQ extraction: a section headed "## Frequently Asked Questions" (or "## FAQ")
whose questions are "### ..." headings. Returns (html, faq_items) where
faq_items = [(question, answer_text), ...] for FAQ JSON-LD.
"""
import re
import html as htmllib

def esc(s):
    return htmllib.escape(s, quote=True)

def inline(text):
    text = esc(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text

def strip_tags(html):
    return re.sub(r"<[^>]+>", "", html)

def tokenize(md):
    lines = md.splitlines()
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if s == "---":
            blocks.append(("hr", None)); i += 1; continue
        m = re.match(r"^(#{2,3})\s+(.*)$", s)
        if m:
            blocks.append((f"h{len(m.group(1))}", m.group(2).strip())); i += 1; continue
        if s.startswith(">"):
            quote = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip()); i += 1
            blocks.append(("quote", " ".join(quote))); continue
        if re.match(r"^[-*]\s+", s):
            items = []
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(re.sub(r"^[-*]\s+", "", lines[i].strip())); i += 1
            blocks.append(("ul", items)); continue
        if re.match(r"^\d+\.\s+", s):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip())); i += 1
            blocks.append(("ol", items)); continue
        para = []
        while i < n:
            s2 = lines[i].strip()
            if not s2:
                break
            if (s2 == "---" or re.match(r"^#{2,3}\s+", s2) or s2.startswith(">")
                    or re.match(r"^[-*]\s+", s2) or re.match(r"^\d+\.\s+", s2)):
                break
            para.append(s2); i += 1
        if para:
            blocks.append(("p", " ".join(para)))
    return blocks

def render_block(kind, payload):
    if kind == "h2":
        return f"<h2>{inline(payload)}</h2>"
    if kind == "h3":
        return f"<h3>{inline(payload)}</h3>"
    if kind == "p":
        return f"<p>{inline(payload)}</p>"
    if kind == "quote":
        return f"<blockquote>{inline(payload)}</blockquote>"
    if kind == "hr":
        return "<hr>"
    if kind == "ul":
        return "<ul>" + "".join(f"<li>{inline(x)}</li>" for x in payload) + "</ul>"
    if kind == "ol":
        return "<ol>" + "".join(f"<li>{inline(x)}</li>" for x in payload) + "</ol>"
    return ""

def block_text(kind, payload):
    if payload is None:
        return ""
    if isinstance(payload, list):
        return " ".join(payload)
    return payload

def parse(md):
    blocks = tokenize(md)

    # locate FAQ section: h2 matching FAQ, runs until next h2 or end
    faq_start = faq_end = None
    for idx, (kind, payload) in enumerate(blocks):
        if kind == "h2" and re.search(r"frequently asked questions|^faq$", payload, re.I):
            faq_start = idx
            break
    faq_title = "Frequently Asked Questions"
    faq_groups = []  # [(question, [blocks])]
    if faq_start is not None:
        faq_end = len(blocks)
        for idx in range(faq_start + 1, len(blocks)):
            if blocks[idx][0] == "h2":
                faq_end = idx
                break
        faq_title = blocks[faq_start][1]
        cur_q, cur_blocks = None, []
        for kind, payload in blocks[faq_start + 1:faq_end]:
            if kind == "h3":
                if cur_q is not None:
                    faq_groups.append((cur_q, cur_blocks))
                cur_q, cur_blocks = payload, []
            elif cur_q is not None:
                cur_blocks.append((kind, payload))
        if cur_q is not None:
            faq_groups.append((cur_q, cur_blocks))
        main_blocks = blocks[:faq_start] + blocks[faq_end:]
    else:
        main_blocks = blocks

    out = [render_block(k, p) for k, p in main_blocks]

    faq_items = []
    if faq_groups:
        out.append('<div class="faq">')
        out.append(f"<h2>{inline(faq_title)}</h2>")
        for q, qblocks in faq_groups:
            out.append('<div class="faq-item">')
            out.append(f"<h3>{inline(q)}</h3>")
            for k, p in qblocks:
                out.append(render_block(k, p))
            out.append("</div>")
            answer = " ".join(strip_tags(render_block(k, p)) for k, p in qblocks)
            faq_items.append((strip_tags(inline(q)), answer.strip()))
        out.append("</div>")

    return "\n".join(out), faq_items

def word_count(md):
    text = re.sub(r"[#>*`\[\]()\-]", " ", md)
    return len(re.findall(r"[A-Za-z0-9']+", text))
