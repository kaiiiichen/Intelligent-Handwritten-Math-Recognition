"""
LaTeX rendering system for candidate previews.

This module provides functionality to render LaTeX commands into images
for preview purposes in the suggestion UI.
"""

from semantic_engine.rendering.latex_renderer import (
    LaTeXRenderer,
    create_renderer,
    render_latex_to_image,
    render_latex_to_svg
)

__all__ = [
    "LaTeXRenderer",
    "create_renderer",
    "render_latex_to_image",
    "render_latex_to_svg"
]

