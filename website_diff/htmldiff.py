"""HTML diff — uses the Rust extension if available, otherwise pure Python."""

try:
    from website_diff._htmldiff_rs import _htmldiff
except ImportError:
    from website_diff._htmldiff_py import _htmldiff

__all__ = ["_htmldiff"]
