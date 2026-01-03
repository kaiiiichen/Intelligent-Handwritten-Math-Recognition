"""
LaTeX rendering utilities for generating preview images of LaTeX commands.

This module provides functionality to render LaTeX commands into images
for preview purposes. It supports multiple backends:
- matplotlib (default, for development)
- PIL/Pillow (for production)
- Optional: MathJax/KaTeX for web deployment
"""

import os
import tempfile
from typing import Optional, Tuple
from pathlib import Path
import warnings

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class LaTeXRenderer:
    """
    Renders LaTeX commands to images for preview purposes.
    
    This is a lightweight renderer suitable for development and testing.
    For production use, consider using more robust solutions like:
    - MathJax (web)
    - KaTeX (web)
    - Sympy's preview (Python)
    - External LaTeX compiler (highest quality)
    """
    
    def __init__(self, backend: str = "matplotlib"):
        """
        Initialize the renderer.
        
        Args:
            backend: Rendering backend ("matplotlib" or "pil")
        """
        self.backend = backend
        
        if backend == "matplotlib" and not MATPLOTLIB_AVAILABLE:
            raise ImportError(
                "matplotlib is required for matplotlib backend. "
                "Install with: pip install matplotlib"
            )
        if backend == "pil" and not PIL_AVAILABLE:
            raise ImportError(
                "Pillow is required for PIL backend. "
                "Install with: pip install Pillow"
            )
    
    def render_to_image(
        self,
        latex_command: str,
        output_path: Optional[str] = None,
        dpi: int = 100,
        fontsize: int = 14
    ) -> Optional[bytes]:
        """
        Render a LaTeX command to an image.
        
        Args:
            latex_command: LaTeX command (e.g., "\\sum", "\\alpha")
            output_path: Optional path to save the image. If None, returns image bytes.
            dpi: Resolution in dots per inch
            fontsize: Font size for rendering
        
        Returns:
            Image bytes if output_path is None, otherwise None
        """
        if self.backend == "matplotlib":
            return self._render_with_matplotlib(latex_command, output_path, dpi, fontsize)
        elif self.backend == "pil":
            return self._render_with_pil(latex_command, output_path, dpi, fontsize)
        else:
            raise ValueError(f"Unknown backend: {self.backend}")
    
    def _render_with_matplotlib(
        self,
        latex_command: str,
        output_path: Optional[str],
        dpi: int,
        fontsize: int
    ) -> Optional[bytes]:
        """Render using matplotlib."""
        # Prepare LaTeX command for matplotlib
        # Wrap in $...$ for math mode
        if not latex_command.startswith('$'):
            latex_text = f"${latex_command}$"
        else:
            latex_text = latex_command
        
        # Create figure with minimal size
        fig, ax = plt.subplots(figsize=(2, 1))
        ax.axis('off')
        
        try:
            # Render LaTeX
            ax.text(0.5, 0.5, latex_text, 
                   fontsize=fontsize,
                   ha='center', va='center',
                   transform=ax.transAxes)
            
            # Save or return bytes
            if output_path:
                plt.savefig(output_path, dpi=dpi, bbox_inches='tight', 
                           pad_inches=0.1, transparent=True)
                plt.close(fig)
                return None
            else:
                # Save to temporary buffer
                import io
                buf = io.BytesIO()
                plt.savefig(buf, format='png', dpi=dpi, bbox_inches='tight',
                           pad_inches=0.1, transparent=True)
                plt.close(fig)
                buf.seek(0)
                return buf.read()
        except Exception as e:
            plt.close(fig)
            warnings.warn(f"Failed to render LaTeX '{latex_command}': {e}")
            # Return a placeholder or None
            return None
    
    def _render_with_pil(
        self,
        latex_command: str,
        output_path: Optional[str],
        dpi: int,
        fontsize: int
    ) -> Optional[bytes]:
        """Render using PIL (basic text rendering, no LaTeX parsing)."""
        # PIL doesn't support LaTeX rendering natively
        # This is a fallback that just renders the text
        warnings.warn(
            "PIL backend does not support LaTeX rendering. "
            "Rendering as plain text. Use matplotlib backend for LaTeX support."
        )
        
        # Create a simple text image
        img = Image.new('RGB', (100, 50), color='white')
        draw = ImageDraw.Draw(img)
        
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw text
        text = latex_command.replace('\\', '')
        draw.text((10, 10), text, fill='black', font=font)
        
        if output_path:
            img.save(output_path)
            return None
        else:
            import io
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            return buf.read()
    
    def render_to_svg(self, latex_command: str, output_path: Optional[str] = None) -> Optional[str]:
        """
        Render a LaTeX command to SVG (if supported).
        
        Args:
            latex_command: LaTeX command
            output_path: Optional path to save the SVG
        
        Returns:
            SVG content as string if output_path is None, otherwise None
        """
        # For now, this is a placeholder
        # In production, you might use:
        # - MathJax server-side rendering
        # - KaTeX server-side rendering
        # - External LaTeX compiler (pdflatex + pdf2svg)
        
        warnings.warn("SVG rendering not yet implemented. Use render_to_image() instead.")
        return None


def create_renderer(backend: str = "matplotlib") -> LaTeXRenderer:
    """Create a LaTeX renderer with the specified backend."""
    return LaTeXRenderer(backend=backend)


def render_latex_to_image(
    latex_command: str,
    output_path: Optional[str] = None,
    backend: str = "matplotlib",
    dpi: int = 100,
    fontsize: int = 14
) -> Optional[bytes]:
    """
    Convenience function to render LaTeX to an image.
    
    Args:
        latex_command: LaTeX command to render
        output_path: Optional path to save the image
        backend: Rendering backend ("matplotlib" or "pil")
        dpi: Resolution in dots per inch
        fontsize: Font size
    
    Returns:
        Image bytes if output_path is None, otherwise None
    """
    renderer = create_renderer(backend)
    return renderer.render_to_image(latex_command, output_path, dpi, fontsize)


def render_latex_to_svg(
    latex_command: str,
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    Convenience function to render LaTeX to SVG.
    
    Args:
        latex_command: LaTeX command to render
        output_path: Optional path to save the SVG
    
    Returns:
        SVG content as string if output_path is None, otherwise None
    """
    renderer = create_renderer()
    return renderer.render_to_svg(latex_command, output_path)

