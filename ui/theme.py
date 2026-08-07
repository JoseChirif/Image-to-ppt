from __future__ import annotations

import ttkbootstrap as ttk

from config.config import COLORS, FONTS


def configure_styles(style: ttk.Style | None = None) -> None:
    """Register the custom styles shared by the application's windows."""
    style = style or ttk.Style()

    style.configure(
        "App.TFrame",
        background=COLORS["app_bg"],
    )
    style.configure(
        "App.TLabel",
        background=COLORS["app_bg"],
        foreground=COLORS["text"],
        font=FONTS["body"],
    )

    style.configure(
        "HeaderTitle.TLabel",
        background=COLORS["app_bg"],
        foreground=COLORS["text"],
        font=FONTS["title"],
    )
    style.configure(
        "HeaderSubtitle.TLabel",
        background=COLORS["app_bg"],
        foreground=COLORS["muted"],
        font=FONTS["subtitle"],
    )

    style.configure(
        "SectionTitle.TLabel",
        background=COLORS["app_bg"],
        foreground=COLORS["text"],
        font=FONTS["section_title"],
    )
    style.configure(
        "SectionDescription.TLabel",
        background=COLORS["app_bg"],
        foreground=COLORS["muted"],
        font=FONTS["body"],
    )

    style.configure(
        "CardBorder.TFrame",
        background=COLORS["border"],
    )
    style.configure(
        "Card.TFrame",
        background=COLORS["surface"],
    )
    style.configure(
        "Card.TLabel",
        background=COLORS["surface"],
        foreground=COLORS["text"],
    )
    style.configure(
        "CardTitle.TLabel",
        background=COLORS["surface"],
        foreground=COLORS["text"],
        font=FONTS["card_title"],
    )
    style.configure(
        "CardDescription.TLabel",
        background=COLORS["surface"],
        foreground=COLORS["muted"],
        font=FONTS["body"],
    )

    style.configure(
        "Info.TFrame",
        background=COLORS["subtle"],
    )
    style.configure(
        "InfoTitle.TLabel",
        background=COLORS["subtle"],
        foreground=COLORS["text"],
        font=FONTS["card_title"],
    )
    style.configure(
        "InfoText.TLabel",
        background=COLORS["subtle"],
        foreground=COLORS["muted"],
        font=FONTS["body"],
    )

    style.configure(
        "Footer.TLabel",
        background=COLORS["app_bg"],
        foreground=COLORS["muted"],
        font=FONTS["footer"],
    )
