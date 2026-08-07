import os
import sys


def relative_route_to_file(*path_to_folder, file):
    """
    Returns the relative path to a file, accounting for whether the application 
    is running in a PyInstaller bundle or a standard script environment.

    Args:
        *path_to_folder (str): The folder path(s) where the file is located.
        file (str): The name of the file.

    Returns:
        str: The complete relative path to the specified file.
    """
    if not path_to_folder:
        raise ValueError("At least one folder path must be provided.")

    # Combine the folder paths into a single path
    folder_path = os.path.join(*path_to_folder)
    
    if hasattr(sys, '_MEIPASS'):
        # Running as a PyInstaller bundle, use _MEIPASS to locate files
        route = os.path.join(sys._MEIPASS, folder_path, file)
    else:
        # Running as a regular script, use standard relative path
        route = os.path.join(folder_path, file)
    
    return route
