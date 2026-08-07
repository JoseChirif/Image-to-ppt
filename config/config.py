# Import functions
from utils.paths import relative_route_to_file

# Version
__version__ = '2.0.0'

# Common routes and variables
# icon_picture_ico
icon_picture_ico = relative_route_to_file("assets", file="Icon.ico")

# icon_picture_png
icon_picture_png = relative_route_to_file("assets", file="Icon.png")
  
# logo_github
logo_github_png = relative_route_to_file("assets", file="Logo_github.png")

# Example picutres
pictures_center = relative_route_to_file("assets", "example pictures", file="Presentation - Pictures center ppt.JPG")
pictures_in_pan_slide = relative_route_to_file("assets", "example pictures", file="Presentation - pictures in panoramic slides.JPG")
pictures_covering_slide = relative_route_to_file("assets", "example pictures", file="Presentation - pictures covering panoramic slides.JPG")




# Pictures extensions supported by ppt
pictures_extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tiff",
    ".tif",
    ".svg",
    ".ico"
)

        
# -----------------------------------------------------------------------------
# Application menu
# -----------------------------------------------------------------------------

PROJECT_TITLE = "Pictures to PowerPoint"
THEME_NAME = "bootstrap-light"


# -----------------------------------------------------------------------------
# Shared visual configuration
# -----------------------------------------------------------------------------

COLORS = {
    "app_bg": "#F5F7FA",
    "surface": "#FFFFFF",
    "border": "#D9E1EA",
    "text": "#172033",
    "muted": "#667085",
    "subtle": "#F0F4F8",
}

FONTS = {
    "title": ("Segoe UI Semibold", 20),
    "subtitle": ("Segoe UI", 10),
    "section_title": ("Segoe UI Semibold", 13),
    "card_title": ("Segoe UI Semibold", 11),
    "body": ("Segoe UI", 9),
    "footer": ("Segoe UI", 8),
}


