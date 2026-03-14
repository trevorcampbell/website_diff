"""Pure Python HTML diff — fallback for when the Rust extension is unavailable.

Implements the same HTML tokenizer and Wu-Manber-Myers O(NP) diff algorithm
that the Rust extension provides, producing byte-identical output.
"""

import enum

__all__ = ["_htmldiff"]


# ---------------------------------------------------------------------------
# HTML tokenizer (equivalent to src/html.rs)
# ---------------------------------------------------------------------------

class _Mode(enum.Enum):
    CHAR = 0
    TAG = 1
    WHITESPACE = 2


def _split_html(s: str) -> list[str]:
    words: list[str] = []
    start = 0
    mode = _Mode.CHAR

    for i, c in enumerate(s):
        if mode == _Mode.CHAR:
            if c == "<":
                if start != i:
                    words.append(s[start:i])
                start = i
                mode = _Mode.TAG
            elif c.isspace():
                if start != i:
                    words.append(s[start:i])
                start = i
                mode = _Mode.WHITESPACE
        elif mode == _Mode.TAG:
            if c == ">":
                words.append(s[start : i + 1])
                start = i + 1
                mode = _Mode.CHAR
        elif mode == _Mode.WHITESPACE:
            if c == "<":
                if start != i:
                    words.append(s[start:i])
                start = i
                mode = _Mode.TAG
            elif not c.isspace():
                if start != i:
                    words.append(s[start:i])
                start = i
                mode = _Mode.CHAR

    if start < len(s):
        words.append(s[start:])
    return words


# ---------------------------------------------------------------------------
# Wu-Manber-Myers O(NP) diff (equivalent to src/wu.rs)
# ---------------------------------------------------------------------------

class _Edit:
    __slots__ = ()


class _Common(_Edit):
    __slots__ = ("old", "new")

    def __init__(self, old: int, new: int):
        self.old = old
        self.new = new


class _Add(_Edit):
    __slots__ = ("new",)

    def __init__(self, new: int):
        self.new = new


class _Delete(_Edit):
    __slots__ = ("old",)

    def __init__(self, old: int):
        self.old = old


def _diff(a: list[str], b: list[str]) -> list[_Edit]:
    reverse = len(a) > len(b)
    if reverse:
        a, b = b, a

    m = len(a)
    n = len(b)
    delta = n - m
    offset = m + 1
    sz = m + n + 3

    ids: list[int] = [-1] * sz
    points: list[tuple[int, int, int]] = []  # (x, y, prev)

    def snake(k: int, fp1: int, fp2: int) -> int:
        fp = max(fp1, fp2)
        y = fp
        x = fp - k
        while x < m and y < n and a[x] == b[y]:
            x += 1
            y += 1
        ko = k + offset
        prev = ids[ko - 1] if fp1 >= fp2 else ids[ko + 1]
        ids[ko] = len(points)
        points.append((x, y, prev))
        return y

    fp = [-1] * sz
    p = -1
    delta_offset = delta + offset
    while True:
        p += 1
        for k in range(-p, delta):
            ko = k + offset
            fp[ko] = snake(k, fp[ko - 1] + 1, fp[ko + 1])
        for k in range(delta + p, delta, -1):
            ko = k + offset
            fp[ko] = snake(k, fp[ko - 1] + 1, fp[ko + 1])
        fp[delta_offset] = snake(
            delta, fp[delta_offset - 1] + 1, fp[delta_offset + 1]
        )
        if fp[delta_offset] >= n:
            break

    route: list[tuple[int, int]] = []
    prev = ids[delta_offset]
    while prev != -1:
        px, py, prev = points[prev]
        route.append((px, py))

    ses: list[_Edit] = []
    cx, cy = 0, 0
    for px, py in reversed(route):
        while cx < px or cy < py:
            if py + cx > px + cy:
                ses.append(_Delete(cy) if reverse else _Add(cy))
                cy += 1
            elif py + cx < px + cy:
                ses.append(_Add(cx) if reverse else _Delete(cx))
                cx += 1
            else:
                ses.append(
                    _Common(cy, cx) if reverse else _Common(cx, cy)
                )
                cx += 1
                cy += 1
    return ses


# ---------------------------------------------------------------------------
# HTML diff builder (equivalent to src/builder.rs)
# ---------------------------------------------------------------------------

def _htmldiff(old_html: str, new_html: str) -> str:
    """Return *new_html* with ``<ins>`` / ``<del>`` tags marking changes."""
    old_words = _split_html(old_html)
    new_words = _split_html(new_html)
    edits = _diff(old_words, new_words)

    parts: list[str] = []
    for edit in edits:
        if isinstance(edit, _Common):
            parts.append(old_words[edit.old])
        elif isinstance(edit, _Add):
            word = new_words[edit.new]
            if word.startswith("<") and not word.startswith("<img"):
                parts.append(word)
            else:
                parts.extend(["<ins>", word, "</ins>"])
        elif isinstance(edit, _Delete):
            word = old_words[edit.old]
            if word.startswith("<") and not word.startswith("<img"):
                parts.append(word)
            else:
                parts.extend(["<del>", word, "</del>"])
    return "".join(parts)
