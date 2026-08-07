import os
import sys
import webbrowser
import math
import queue
import threading
from typing import Any, Callable

import requests
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox

from utils.paths import relative_route_to_file
from config.config import COLORS


def working_directory():
    """
    Returns the path to the project's parent directory. If the script is bundled into an executable, it returns the executable's directory.

    Args:
        None

    Returns:
        str: Path to the parent directory of the project or the directory of the executable if running as a bundled application.
    """
    if hasattr(sys, 'frozen'):
        # If the script is bundled into an executable, it returns the directory of the executable.
        directory = os.path.dirname(sys.executable)
    else:
        # If running as a normal script, it returns the parent directory of the project
        directory = os.path.abspath(os.path.join(__file__, *(['..'] * 3)))

    return directory  # Returns the directory


def show_message(title, message):
    """
    Displays a message in a popup window using ttkbootstrap. If the message is a DataFrame, it converts it to a string.

    Args:
        title (str): The title of the popup window.
        message (str or pd.DataFrame): The message to display. If a DataFrame is provided, it will be converted to a string.

    Returns:
        None: This function does not return anything.

    Raises:
        None: This function does not raise any exceptions.
    """
    # Use the existing application window. Do not create a second root window.
    parent = ttk.Style().master

    Messagebox.show_info(
        message=str(message),
        title=title,
        parent=parent,
    )


def show_options(header_text, *args):
    """
    Displays an options window with a dynamic number of buttons based on the provided options.
    Upon selecting an option, returns the index (1-based) of the selected option.
    If canceled, closes only the options window without affecting other windows.

    Args:
        header_text (str): The text displayed at the top of the window.
        *args (str): Variable number of option texts for buttons.

    Returns:
        int: The selected option (1-based index) or None if canceled.
    """
    result = None

    def cancel_current_operation():
        """
        Cancels the operation and closes only the current options window.
        """
        nonlocal result
        result = None
        options_window.destroy()

    def select_option(option_number):
        """
        Handles the selection of an option.

        Args:
            option_number (int): The 1-based index of the selected option.
        """
        nonlocal result
        result = option_number
        options_window.destroy()

    # Reuse the root window created by the main menu.
    parent = ttk.Style().master

    # Create the options window.
    options_window = ttk.Toplevel(master=parent)
    options_window.title("Pictures to PPT")
    options_window.resizable(False, False)
    options_window.transient(parent)

    try:
        options_window.iconbitmap(
            relative_route_to_file("assets", file="Icon.ico")
        )
    except Exception:
        # Some operating systems do not support ICO files.
        pass

    # Handle the close (X) button of the window.
    options_window.protocol("WM_DELETE_WINDOW", cancel_current_operation)

    # Main content container. These styles are configured once in ui/theme.py.
    container = ttk.Frame(
        options_window,
        padding=(20, 15),
        style="App.TFrame",
    )
    container.pack(fill="both", expand=True)

    # Centered text at the top of the window.
    lbl_header = ttk.Label(
        container,
        text=header_text,
        style="SectionTitle.TLabel",
        anchor="center",
        justify="center",
        padding=(20, 0),
    )
    lbl_header.pack(fill="x", pady=(0, 15))

    # Create buttons dynamically for each option.
    for i, option in enumerate(args, start=1):
        button = ttk.Button(
            container,
            text=option,
            command=lambda opt=i: select_option(opt),
            cursor="hand2",
            bootstyle="primary",
            padding=(20, 10),
        )
        button.pack(fill="x", pady=5)

    # Cancel button.
    cancel_button = ttk.Button(
        container,
        text="Cancel",
        command=cancel_current_operation,
        cursor="hand2",
        bootstyle="warning",
        padding=(20, 10),
    )
    cancel_button.pack(side="bottom", anchor="se", padx=(0, 0), pady=(10, 0))

    # Wait for the user to select an option or cancel.
    options_window.grab_set()  # Makes the window modal.
    options_window.focus_set()
    options_window.wait_window()  # Pauses execution until the window is closed.

    return result

def run_task_with_progress(
    total_items: int,
    task: Callable[[Callable[..., None]], Any],
    title: str = "Creating presentation",
) -> Any:
    """
    Execute a task in a worker thread while displaying a modal progress window.

    The task receives a callback with this signature:

        report_progress(current, detail="", status=None)

    During image processing, a determinate horizontal bar is displayed.

    When every image has been processed and the presentation is being saved,
    the horizontal bar is replaced by an animated circular dots spinner.
    """
    if total_items < 0:
        raise ValueError("total_items cannot be negative.")

    parent = ttk.Style().master

    if parent is None:
        raise RuntimeError(
            "No active ttkbootstrap main window was found."
        )

    event_queue = queue.Queue()

    outcome = {
        "result": None,
        "error": None,
    }

    # -------------------------------------------------------------------------
    # Progress window
    # -------------------------------------------------------------------------
    progress_window = ttk.Toplevel(master=parent)
    progress_window.title(title)
    progress_window.resizable(False, False)
    progress_window.transient(parent)

    # Prevent closing the progress window while the task is running.
    progress_window.protocol("WM_DELETE_WINDOW", lambda: None)

    container = ttk.Frame(
        progress_window,
        padding=(24, 22),
        style="App.TFrame",
    )
    container.pack(fill="both", expand=True)

    ttk.Label(
        container,
        text=title,
        style="SectionTitle.TLabel",
    ).pack(anchor="w")

    status_var = ttk.StringVar(
        value=f"Processing image 0 of {total_items}"
    )

    detail_var = ttk.StringVar(
        value="Preparing presentation..."
    )

    progress_var = ttk.IntVar(value=0)

    status_label = ttk.Label(
        container,
        textvariable=status_var,
        style="SectionDescription.TLabel",
    )
    status_label.pack(
        anchor="w",
        pady=(12, 8),
    )

    # -------------------------------------------------------------------------
    # Determinate progress bar: 0, 1, 2... X images
    # -------------------------------------------------------------------------
    progress_bar = ttk.Progressbar(
        container,
        mode="determinate",
        maximum=max(total_items, 1),
        variable=progress_var,
        bootstyle="primary",
        length=420,
    )
    progress_bar.pack(
        fill="x",
        pady=(0, 10),
    )

    detail_label = ttk.Label(
        container,
        textvariable=detail_var,
        style="SectionDescription.TLabel",
        wraplength=420,
    )
    detail_label.pack(anchor="w")

    # -------------------------------------------------------------------------
    # Dots spinner configuration
    # -------------------------------------------------------------------------
    spinner_size = 100
    spinner_center = spinner_size / 2
    orbit_radius = 31
    dot_radius = 7
    dot_count = 10
    spinner_delay_ms = 85

    style = ttk.Style()

    # Get the actual style applied to the parent container.
    container_style = container.cget("style") or "App.TFrame"

    # Get the exact background color used by that style.
    background_color = style.lookup(
        container_style,
        "background",
    )

    # Fallback in case the style does not return a background.
    if not background_color:
        background_color = COLORS["app_bg"]

    primary_color = style.colors.primary


    def blend_hex_colors(
        foreground: str,
        background: str,
        foreground_ratio: float,
    ) -> str:
        """
        Blend a foreground color with a background color.

        Canvas circles do not support alpha transparency, so the faded dots
        are created by mixing the theme's primary color with the background.
        """
        foreground = foreground.lstrip("#")
        background = background.lstrip("#")

        foreground_rgb = tuple(
            int(foreground[index:index + 2], 16)
            for index in (0, 2, 4)
        )

        background_rgb = tuple(
            int(background[index:index + 2], 16)
            for index in (0, 2, 4)
        )

        blended_rgb = tuple(
            round(
                foreground_component * foreground_ratio
                + background_component * (1 - foreground_ratio)
            )
            for foreground_component, background_component
            in zip(foreground_rgb, background_rgb)
        )

        return "#{:02X}{:02X}{:02X}".format(*blended_rgb)


    # The first color is the active dot.
    # The remaining colors form the faded tail.
    dot_colors = [
        blend_hex_colors(
            primary_color,
            background_color,
            ratio,
        )
        for ratio in (
            1.00,
            0.80,
            0.62,
            0.46,
            0.34,
            0.25,
            0.19,
            0.14,
            0.10,
            0.07,
        )
    ]

    # Canvas is hidden until saving starts.
    spinner_canvas = tk.Canvas(
        container,
        width=spinner_size,
        height=spinner_size,
        bg=background_color,
        highlightthickness=0,
        borderwidth=0,
        relief="flat",
    )

    spinner_dots = []

    for dot_index in range(dot_count):
        angle = (
            -math.pi / 2
            + (2 * math.pi * dot_index / dot_count)
        )

        center_x = (
            spinner_center
            + orbit_radius * math.cos(angle)
        )

        center_y = (
            spinner_center
            + orbit_radius * math.sin(angle)
        )

        dot = spinner_canvas.create_oval(
            center_x - dot_radius,
            center_y - dot_radius,
            center_x + dot_radius,
            center_y + dot_radius,
            fill=dot_colors[-1],
            outline="",
        )

        spinner_dots.append(dot)

    spinner_state = {
        "active": False,
        "active_index": 0,
        "after_id": None,
    }
    # -------------------------------------------------------------------------
    # Window positioning
    # -------------------------------------------------------------------------
    def center_progress_window(
        window_width: int,
        window_height: int,
    ) -> None:
        """Center the progress window over the main application."""
        progress_window.update_idletasks()

        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        position_x = parent_x + max(
            (parent_width - window_width) // 2,
            0,
        )

        position_y = parent_y + max(
            (parent_height - window_height) // 2,
            0,
        )

        progress_window.geometry(
            f"{window_width}x{window_height}"
            f"+{position_x}+{position_y}"
        )

    progress_window.withdraw()
    center_progress_window(480, 190)
    progress_window.deiconify()

    # -------------------------------------------------------------------------
    # Dots spinner animation
    # -------------------------------------------------------------------------
    def animate_spinner() -> None:
        """
        Move the bright dot clockwise and redraw its fading trail.
        """
        if (
            not spinner_state["active"]
            or not progress_window.winfo_exists()
        ):
            return

        active_index = spinner_state["active_index"]

        for dot_index, dot in enumerate(spinner_dots):
            # Distance behind the active dot.
            color_index = (
                active_index - dot_index
            ) % dot_count

            spinner_canvas.itemconfigure(
                dot,
                fill=dot_colors[color_index],
            )

        spinner_state["active_index"] = (
            active_index + 1
        ) % dot_count

        spinner_state["after_id"] = progress_window.after(
            spinner_delay_ms,
            animate_spinner,
        )

    def start_saving_mode(
        status: str,
        detail: str,
    ) -> None:
        """
        Replace the completed horizontal bar with the rotating dots spinner.
        """
        status_var.set(status)
        detail_var.set(detail)

        if spinner_state["active"]:
            return

        spinner_state["active"] = True
        spinner_state["active_index"] = 0

        # Remove the completed horizontal progress bar.
        progress_bar.pack_forget()

        # Show the dots spinner before the filename/detail label.
        spinner_canvas.pack(
            before=detail_label,
            pady=(4, 12),
        )

        center_progress_window(480, 275)

        animate_spinner()

    def stop_spinner() -> None:
        """Stop the dots animation."""
        spinner_state["active"] = False

        after_id = spinner_state["after_id"]

        if after_id is not None:
            try:
                progress_window.after_cancel(after_id)
            except Exception:
                pass

        spinner_state["after_id"] = None

    # -------------------------------------------------------------------------
    # Callback available to the processing task
    # -------------------------------------------------------------------------
    def report_progress(
        current: int,
        detail: str = "",
        status: str | None = None,
    ) -> None:
        """
        Send progress information safely from the worker thread.

        This callback never modifies the interface directly.
        """
        event_queue.put(
            (
                "progress",
                current,
                detail,
                status,
            )
        )

    # -------------------------------------------------------------------------
    # Worker thread
    # -------------------------------------------------------------------------
    def worker() -> None:
        try:
            result = task(report_progress)
            event_queue.put(("done", result))

        except Exception as exc:
            event_queue.put(("error", exc))

    # -------------------------------------------------------------------------
    # Close progress window
    # -------------------------------------------------------------------------
    def close_progress_window() -> None:
        stop_spinner()

        if not progress_window.winfo_exists():
            return

        try:
            progress_window.grab_release()
        except Exception:
            pass

        progress_window.destroy()

    # -------------------------------------------------------------------------
    # Process messages sent by the worker thread
    # -------------------------------------------------------------------------
    def process_events() -> None:
        try:
            while True:
                event = event_queue.get_nowait()
                event_type = event[0]

                if event_type == "progress":
                    _, current, detail, status = event

                    bounded_current = max(
                        0,
                        min(current, total_items),
                    )

                    # Every image is ready and prs.save() is about to start.
                    if (
                        current >= total_items
                        and status is not None
                    ):
                        start_saving_mode(
                            status=status,
                            detail=detail,
                        )

                    else:
                        progress_var.set(bounded_current)

                        if status is None:
                            status_var.set(
                                f"Processing image "
                                f"{bounded_current} of {total_items}"
                            )
                        else:
                            status_var.set(status)

                        detail_var.set(detail)

                elif event_type == "done":
                    outcome["result"] = event[1]

                    stop_spinner()
                    status_var.set("Presentation created.")

                    progress_window.after(
                        150,
                        close_progress_window,
                    )
                    return

                elif event_type == "error":
                    outcome["error"] = event[1]
                    close_progress_window()
                    return

        except queue.Empty:
            pass

        if progress_window.winfo_exists():
            progress_window.after(
                50,
                process_events,
            )

    # -------------------------------------------------------------------------
    # Start processing
    # -------------------------------------------------------------------------
    progress_window.grab_set()

    worker_thread = threading.Thread(
        target=worker,
        daemon=True,
    )
    worker_thread.start()

    progress_window.after(
        50,
        process_events,
    )

    parent.wait_window(progress_window)

    if outcome["error"] is not None:
        raise outcome["error"]

    return outcome["result"]

def check_presentation_exists(ppt_path):
    """
    Checks if a PowerPoint file already exists in the working directory.
    If it exists, asks the user whether to replace it.

    Args:
        ppt_path (str): Full path to the PowerPoint file.

    Returns:
        bool: True if the file can be replaced or does not exist, False if the replacement is declined.
    """
    if os.path.exists(ppt_path):
        choice = show_options(f"The presentation '{os.path.basename(ppt_path)}' already exists.\nDo you want to replace it?", "Yes", "No")
        if choice == 1:  # Yes
            return True
        else:  # No or canceled
            return False
    return True


## FUNCTIONS FOR MAIN MENU
def open_web_page(*links):
    """
    Attempts to open a list of web links in the default web browser. For each link,
    it checks if the URL is accessible before opening it. Stops at the first successful link.

    Args:
        *links (str): One or more URLs to open.

    Returns:
        None
    """
    for link in links:
        try:
            # Perform a GET request to check if the link is accessible
            response = requests.get(link, timeout=5)
            if response.status_code == 200:
                webbrowser.open(link)
                print(f"Opening: {link}")
                break  # Stop if the link was successfully opened
            else:
                print(f"The link {link} is not available, status code: {response.status_code}")
        except requests.ConnectionError:
            print(f"Connection error while checking {link}. The link might not exist.")
        except requests.Timeout:
            print(f"Timeout expired while checking {link}.")
        except requests.RequestException as e:
            print(f"Error while checking {link}: {e}")
    else:
        print("No links could be opened.")


def adjust_text(event, *args, margin):
    """
    Adjusts the text wrapping length for given labels based on the available width minus a specified margin.

    Args:
        event: The triggering event, typically a window resize event.
        *args: Variable number of label widgets to adjust.
        margin (int): The margin to subtract from the label width for text wrapping.

    Returns:
        List of labels with updated wraplength configurations (optional).
    """
    updated_labels = []
    for label in args:
        # Adjust the text wrapping length to the available width minus the margin
        new_wraplength = label.winfo_width() - margin
        if new_wraplength > 0:  # Ensure the new wrap length is positive
            label.config(wraplength=new_wraplength)
            updated_labels.append(label)  # Store updated label

    return updated_labels  # Return the list of updated labels


# FUNCTIONS TO EXECUTE SCRIPTS

class DirectExecutionExit(Exception):
    """Custom exception to handle script exit without closing the Tkinter menu."""
    pass


def exit_if_directly_executed():
    """
    Raises an exception that can be caught to stop the script.

    Args:
        None

    Returns:
        None
    """
    raise DirectExecutionExit("The script was stopped.")


def execute_script_src(script):
    """
    Executes the corresponding script.

    Args:
        script (str): The name of the script to execute.

    Returns:
        None: This function does not return any value. It only executes the script and handles errors.
    """
    try:
        # Attempt to import and execute the corresponding script
        module = __import__(f'src.{script}', fromlist=['create_presentation'])
        module.create_presentation()  # Call the function create_presentation with no arguments

    except DirectExecutionExit as e:
        print(f"The script was stopped: {e}")
    except ImportError as e:
        print(f"Error importing the script '{script}': {e}")
    except AttributeError as e:
        print(f"The script '{script}' does not have a 'main' function: {e}")
    except Exception as e:
        print(f"An error occurred while executing the script '{script}': {e}")


def run_picture_center():
    """
    Executes the 'Imagen_to_ppt - Picture center' script

    Returns:
        None: This function does not return any value. It only calls the execute_script_src function.
    """
    execute_script_src('Imagen_to_ppt - Picture center')


def run_picture_covering_panoramic_slide():
    """
    Executes the 'Imagen_to_ppt- Picture covering panoramic slice' script

    Returns:
        None: This function does not return any value. It only calls the execute_script_src function.
    """
    execute_script_src('Imagen_to_ppt- Picture covering panoramic slice')


def run_picture_in_panoramic_slide():
    """
    Executes the 'Imagen_to_ppt- Picture in panoramic slice' script

    Returns:
        None: This function does not return any value. It only calls the execute_script_src function.
    """
    execute_script_src('Imagen_to_ppt- Picture in panoramic slice')
