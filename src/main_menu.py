from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import ttkbootstrap as ttk
from PIL import Image, ImageOps, ImageTk
from ttkbootstrap import Messagebox, register_style

from functions.functions import (
    open_web_page,
    run_picture_center,
    run_picture_covering_panoramic_slide,
    run_picture_in_panoramic_slide,
)
from config.config import (
    __version__,
    icon_picture_ico,
    icon_picture_png,
    logo_github_png,
    pictures_center,
    pictures_covering_slide,
    pictures_in_pan_slide,
)


# -----------------------------------------------------------------------------
# Application configuration
# -----------------------------------------------------------------------------
THEME_NAME = "bootstrap-light"  # Current light ttkbootstrap theme
WINDOW_SIZE = (820, 900)
MINIMUM_WINDOW_SIZE = (720, 610)

PROJECT_TITLE = "Pictures to PowerPoint"
PROJECT_SUBTITLE = "Turn the images in the current folder into a presentation."
CURRENT_VERSION = f"v{__version__}"

REPOSITORY_URLS = (
    "https://github.com/JoseChirif/Pictures-to-slides",
    "https://github.com/JoseChirif?tab=repositories",
    "https://github.com/JoseChirif",
)

COLORS = {
    "app_bg": "#F5F7FA",
    "surface": "#FFFFFF",
    "border": "#D9E1EA",
    "text": "#172033",
    "muted": "#667085",
    "subtle": "#F0F4F8",
}


# -----------------------------------------------------------------------------
# Image helpers
# -----------------------------------------------------------------------------
def load_photo_image(
    image_path: str | os.PathLike[str],
    size: tuple[int, int],
    *,
    contain: bool = False,
    border: int = 0,
) -> ImageTk.PhotoImage:
    """Load an image and return a Tk-compatible image with consistent sizing."""
    with Image.open(image_path) as source:
        image = source.convert("RGBA")

        if contain:
            image.thumbnail((size[0] - 12, size[1] - 12), Image.Resampling.LANCZOS)
            canvas = Image.new("RGBA", size, "white")
            x = (size[0] - image.width) // 2
            y = (size[1] - image.height) // 2
            canvas.alpha_composite(image, (x, y))
            image = canvas
        else:
            image = ImageOps.contain(image, size, Image.Resampling.LANCZOS)

        if border:
            image = ImageOps.expand(image, border=border, fill=COLORS["border"])

        return ImageTk.PhotoImage(image)


# -----------------------------------------------------------------------------
# Reusable interface components
# -----------------------------------------------------------------------------
def create_layout_card(
    parent: ttk.Frame,
    *,
    preview_path: str,
    title: str,
    description: str,
    command: Callable[[], None],
) -> ttk.Frame:
    """Create a modern, horizontally aligned layout option card."""
    border_frame = ttk.Frame(parent, style="CardBorder.TFrame")
    border_frame.pack(fill="x", pady=6)

    card = ttk.Frame(border_frame, style="Card.TFrame", padding=(14, 12))
    card.pack(fill="x", padx=1, pady=1)
    card.columnconfigure(1, weight=1)

    preview = load_photo_image(preview_path, (150, 96), contain=True)
    preview_label = ttk.Label(
        card,
        image=preview,
        style="Card.TLabel",
        cursor="hand2",
    )
    preview_label.image = preview
    preview_label.grid(row=0, column=0, rowspan=2, sticky="w", padx=(0, 16))

    title_label = ttk.Label(
        card,
        text=title,
        style="CardTitle.TLabel",
        cursor="hand2",
    )
    title_label.grid(row=0, column=1, sticky="sw", pady=(2, 3))

    description_label = ttk.Label(
        card,
        text=description,
        style="CardDescription.TLabel",
        cursor="hand2",
        wraplength=330,
    )
    description_label.grid(row=1, column=1, sticky="nw", padx=(0, 14))

    action_button = ttk.Button(
        card,
        text="Use this layout",
        command=command,
        bootstyle="primary outline",
        cursor="hand2",
        width=16,
    )
    action_button.grid(row=0, column=2, rowspan=2, sticky="e", padx=(8, 0))

    clickable_widgets = (border_frame, card, preview_label, title_label, description_label)
    for widget in clickable_widgets:
        widget.bind("<Button-1>", lambda _event, callback=command: callback())
        widget.configure(cursor="hand2")

    return border_frame


def get_license_path() -> Path:
    """Return the absolute path to the LICENSE file."""
    return Path(__file__).resolve().parent.parent / "LICENSE"


def open_license(parent: ttk.App) -> None:
    """Open the license with the operating system's default text viewer."""
    license_path = get_license_path()

    if not license_path.exists():
        Messagebox.show_error(
            f"The license file was not found:\n{license_path}",
            "License not found",
            parent=parent,
        )
        return

    try:
        if sys.platform.startswith("win"):
            os.startfile(license_path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(license_path)])
        else:
            subprocess.Popen(["xdg-open", str(license_path)])
    except OSError as exc:
        Messagebox.show_error(
            f"The license could not be opened.\n\n{exc}",
            "Unable to open license",
            parent=parent,
        )



# -----------------------------------------------------------------------------
# Main window
# -----------------------------------------------------------------------------
def main_menu() -> None:
    """Display the application's main menu."""
    window = ttk.App(
        title=PROJECT_TITLE,
        theme=THEME_NAME,
        size=WINDOW_SIZE,
        minsize=MINIMUM_WINDOW_SIZE,
        iconphoto=None,
    )
    window.configure(background=COLORS["app_bg"])
    window.place_window_center()

    try:
        window.iconbitmap(icon_picture_ico)
    except Exception:
        # The ICO format is not supported by every operating system.
        pass

    window.attributes("-topmost", True)
    window.after(100, lambda: window.attributes("-topmost", False))
    window.protocol("WM_DELETE_WINDOW", window.destroy)

    style = ttk.Style()
    for custom_style in (
        "App.TFrame",
        "CardBorder.TFrame",
        "Card.TFrame",
        "Card.TLabel",
        "HeaderTitle.TLabel",
        "HeaderSubtitle.TLabel",
        "SectionTitle.TLabel",
        "SectionDescription.TLabel",
        "CardTitle.TLabel",
        "CardDescription.TLabel",
        "Info.TFrame",
        "InfoTitle.TLabel",
        "InfoText.TLabel",
        "Footer.TLabel",
    ):
        register_style(style, custom_style)

    style.configure("App.TFrame", background=COLORS["app_bg"])
    style.configure("CardBorder.TFrame", background=COLORS["border"])
    style.configure("Card.TFrame", background=COLORS["surface"])
    style.configure("Card.TLabel", background=COLORS["surface"])
    style.configure(
        "HeaderTitle.TLabel",
        background=COLORS["app_bg"],
        foreground=COLORS["text"],
        font=("Segoe UI Semibold", 20),
    )
    style.configure(
        "HeaderSubtitle.TLabel",
        background=COLORS["app_bg"],
        foreground=COLORS["muted"],
        font=("Segoe UI", 10),
    )
    style.configure(
        "SectionTitle.TLabel",
        background=COLORS["app_bg"],
        foreground=COLORS["text"],
        font=("Segoe UI Semibold", 13),
    )
    style.configure(
        "SectionDescription.TLabel",
        background=COLORS["app_bg"],
        foreground=COLORS["muted"],
        font=("Segoe UI", 9),
    )
    style.configure(
        "CardTitle.TLabel",
        background=COLORS["surface"],
        foreground=COLORS["text"],
        font=("Segoe UI Semibold", 11),
    )
    style.configure(
        "CardDescription.TLabel",
        background=COLORS["surface"],
        foreground=COLORS["muted"],
        font=("Segoe UI", 9),
    )
    style.configure("Info.TFrame", background=COLORS["subtle"])
    style.configure(
        "InfoTitle.TLabel",
        background=COLORS["subtle"],
        foreground=COLORS["text"],
        font=("Segoe UI Semibold", 10),
    )
    style.configure(
        "InfoText.TLabel",
        background=COLORS["subtle"],
        foreground=COLORS["muted"],
        font=("Segoe UI", 9),
    )
    style.configure(
        "Footer.TLabel",
        background=COLORS["app_bg"],
        foreground=COLORS["muted"],
        font=("Segoe UI", 8),
    )



    app = ttk.Frame(window, style="App.TFrame", padding=(28, 22, 28, 16))
    app.pack(fill="both", expand=True)

    # Header: application icon remains deliberately aligned to the left.
    header = ttk.Frame(app, style="App.TFrame")
    header.pack(fill="x")
    header.columnconfigure(1, weight=1)

    app_icon = load_photo_image(icon_picture_png, (48, 48))
    app_icon_label = ttk.Label(header, image=app_icon, style="HeaderSubtitle.TLabel")
    app_icon_label.image = app_icon
    app_icon_label.grid(row=0, column=0, rowspan=2, sticky="w", padx=(0, 14))

    ttk.Label(header, text=PROJECT_TITLE, style="HeaderTitle.TLabel").grid(
        row=0,
        column=1,
        sticky="sw",
    )
    ttk.Label(header, text=PROJECT_SUBTITLE, style="HeaderSubtitle.TLabel").grid(
        row=1,
        column=1,
        sticky="nw",
        pady=(2, 0),
    )

    github_icon = load_photo_image(logo_github_png, (23, 23))
    github_button = ttk.Button(
        header,
        text="GitHub",
        image=github_icon,
        compound="left",
        command=lambda: open_web_page(*REPOSITORY_URLS),
        bootstyle="primary link",
        cursor="hand2",
        padding=(8, 6),
    )
    github_button.image = github_icon
    github_button.grid(row=0, column=2, rowspan=2, sticky="e")

    ttk.Separator(app, bootstyle="secondary").pack(fill="x", pady=(18, 20))

    # Layout options.
    ttk.Label(app, text="Choose a slide layout", style="SectionTitle.TLabel").pack(
        anchor="w"
    )
    ttk.Label(
        app,
        text="Select how each image should be positioned in the generated presentation.",
        style="SectionDescription.TLabel",
    ).pack(anchor="w", pady=(3, 10))

    cards_container = ttk.Frame(app, style="App.TFrame")
    cards_container.pack(fill="x")

    create_layout_card(
        cards_container,
        preview_path=pictures_center,
        title="Centered with border",
        description=(
            "Keeps the complete image visible, centers it at 17.43 cm high, "
            "and adds a thin black border."
        ),
        command=run_picture_center,
    )
    create_layout_card(
        cards_container,
        preview_path=pictures_in_pan_slide,
        title="Fit to widescreen slide",
        description="Fits the complete image inside a 16:9 slide without cropping it.",
        command=run_picture_in_panoramic_slide,
    )
    create_layout_card(
        cards_container,
        preview_path=pictures_covering_slide,
        title="Fill widescreen slide",
        description=(
            "Fills the entire 16:9 slide and crops excess areas when the image "
            "aspect ratio is different."
        ),
        command=run_picture_covering_panoramic_slide,
    )

    # Compact instructions replace the large instruction and notes blocks.
    info_border = ttk.Frame(app, style="CardBorder.TFrame")
    info_border.pack(fill="x", pady=(14, 0))

    info = ttk.Frame(info_border, padding=(14, 11), style="Info.TFrame")
    info.pack(fill="x", padx=1, pady=1)
    ttk.Label(info, text="Before you start", style="InfoTitle.TLabel").pack(anchor="w")
    info_text = ttk.Label(
        info,
        text=(
            "Place the executable in the folder that contains the images, run the "
            "program, and choose one of the three layouts above."
        ),
        style="InfoText.TLabel",
        wraplength=690,
        justify="left",
    )
    info_text.pack(anchor="w", pady=(3, 0))

    # Footer.
    footer = ttk.Frame(app, style="App.TFrame")
    footer.pack(side="bottom", fill="x", pady=(14, 0))
    footer.columnconfigure(1, weight=1)

    license_button = ttk.Button(
        footer,
        text="MIT License",
        command=lambda: open_license(window),
        bootstyle="primary link",
        cursor="hand2",
        padding=0,
    )
    license_button.grid(row=0, column=0, sticky="w")

    ttk.Label(footer, text="Pictures to PowerPoint", style="Footer.TLabel").grid(
        row=0,
        column=1,
    )
    ttk.Label(footer, text=CURRENT_VERSION, style="Footer.TLabel").grid(
        row=0,
        column=2,
        sticky="e",
    )

    def update_wraplength(event: object) -> None:
        width = max(window.winfo_width() - 130, 420)
        info_text.configure(wraplength=width)

    window.bind("<Configure>", update_wraplength)
    window.mainloop()


if __name__ == "__main__":
    main_menu()
