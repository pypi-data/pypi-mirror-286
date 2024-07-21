import sys, traceback, matplotlib, ctypes
import tkinter as tk
from tkinter import ttk, scrolledtext
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('Agg')  # Use the non-GUI Agg backend
from multiprocessing import Process, Queue, Value
from tkinter import filedialog

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except AttributeError:
    pass

from .logger import log_function_call
from .settings import get_measure_crop_settings
from .gui_utils import ScrollableFrame, StdoutRedirector, CustomButton, ToggleSwitch
from .gui_utils import process_stdout_stderr, set_dark_style, set_default_font, generate_fields, main_thread_update_function, create_menu_bar, convert_settings_dict_for_gui
from .gui_utils import measure_crop_wrapper, clear_canvas, check_measure_gui_settings, read_settings_from_csv, update_settings_from_csv, set_dark_style

thread_control = {"run_thread": None, "stop_requested": False}

def import_settings(scrollable_frame):
    global vars_dict

    csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    csv_settings = read_settings_from_csv(csv_file_path)
    settings = get_measure_crop_settings({})
    variables = convert_settings_dict_for_gui(settings)
    new_settings = update_settings_from_csv(variables, csv_settings)
    vars_dict = generate_fields(new_settings, scrollable_frame)

test_mode_button = None

def toggle_test_mode():
    global vars_dict
    current_state = vars_dict['test_mode'][2].get()
    new_state = not current_state
    vars_dict['test_mode'][2].set(new_state)
    if new_state:
        test_mode_button.config(bg="blue")
    else:
        test_mode_button.config(bg="gray")

def toggle_advanced_settings():
    global vars_dict

    timelapse_settings = ['timelapse', 'timelapse_objects']
    misc_settings = ['representative_images', 'plot', 'plot_filtration', 'include_uninfected', 'dialate_pngs', 'dialate_png_ratios']
    opperational_settings = ['max_workers','experiment','cells','cell_loc','pathogens','pathogen_loc','treatments','treatment_loc','channel_of_interest','compartments','measurement','nr_imgs', 'um_per_pixel']
    
    advanced_settings = timelapse_settings+misc_settings+opperational_settings

    # Toggle visibility of advanced settings
    for setting in advanced_settings:
        label, widget, var = vars_dict[setting]
        if advanced_var.get() is False:
            label.grid_remove()  # Hide the label
            widget.grid_remove()  # Hide the widget
        else:
            label.grid()  # Show the label
            widget.grid()  # Show the widget

#@log_function_call
def run_measure_gui(q, fig_queue, stop_requested):
    global vars_dict
    process_stdout_stderr(q)
    try:
        print('hello')
        settings = check_measure_gui_settings(vars_dict)
        measure_crop_wrapper(settings=settings, q=q, fig_queue=fig_queue)
    except Exception as e:
        q.put(f"Error during processing: {e}")
        traceback.print_exc()
    finally:
        stop_requested.value = 1

#@log_function_call
def start_process(q, fig_queue):
    global thread_control
    if thread_control.get("run_thread") is not None:
        initiate_abort()

    stop_requested = Value('i', 0)  # multiprocessing shared value for inter-process communication
    thread_control["stop_requested"] = stop_requested
    thread_control["run_thread"] = Process(target=run_measure_gui, args=(q, fig_queue, stop_requested))
    thread_control["run_thread"].start()

#@log_function_call
def initiate_abort():
    global thread_control
    if thread_control.get("stop_requested") is not None:
        thread_control["stop_requested"].value = 1

    if thread_control.get("run_thread") is not None:
        thread_control["run_thread"].join(timeout=5)
        if thread_control["run_thread"].is_alive():
            thread_control["run_thread"].terminate()
        thread_control["run_thread"] = None

#@log_function_call
def initiate_measure_root(parent_frame):
    global vars_dict, q, canvas, fig_queue, canvas_widget, thread_control, variables, advanced_var, scrollable_frame
    
    style = ttk.Style(parent_frame)
    set_dark_style(style)
    set_default_font(parent_frame, font_name="Helvetica", size=8)

    parent_frame.configure(bg='black')
    parent_frame.grid_rowconfigure(0, weight=1)
    parent_frame.grid_columnconfigure(0, weight=1)

    fig_queue = Queue()
    
    # Initialize after_tasks if not already done
    if not hasattr(parent_frame, 'after_tasks'):
        parent_frame.after_tasks = []

    def _process_fig_queue():
        global canvas
        try:
            while not fig_queue.empty():
                clear_canvas(canvas)
                fig = fig_queue.get_nowait()
                for ax in fig.get_axes():
                    ax.set_xticks([])  # Remove x-axis ticks
                    ax.set_yticks([])  # Remove y-axis ticks
                    ax.xaxis.set_visible(False)  # Hide the x-axis
                    ax.yaxis.set_visible(False)  # Hide the y-axis
                fig.tight_layout()
                fig.set_facecolor('black')
                canvas.figure = fig
                fig_width, fig_height = canvas_widget.winfo_width(), canvas_widget.winfo_height()
                fig.set_size_inches(fig_width / fig.dpi, fig_height / fig.dpi, forward=True)
                canvas.draw_idle()
        except Exception as e:
            traceback.print_exc()
        finally:
            after_id = canvas_widget.after(100, _process_fig_queue)
            parent_frame.after_tasks.append(after_id)

    def _process_console_queue():
        while not q.empty():
            message = q.get_nowait()
            console_output.insert(tk.END, message)
            console_output.see(tk.END)
        after_id = console_output.after(100, _process_console_queue)
        parent_frame.after_tasks.append(after_id)

    # Clear previous content if any
    for widget in parent_frame.winfo_children():
        widget.destroy()

    vertical_container = tk.PanedWindow(parent_frame, orient=tk.HORIZONTAL)
    vertical_container.grid(row=0, column=0, sticky=tk.NSEW)
    parent_frame.grid_rowconfigure(0, weight=1)
    parent_frame.grid_columnconfigure(0, weight=1)

    # Settings Section
    settings_frame = tk.Frame(vertical_container, bg='black')
    vertical_container.add(settings_frame, stretch="always")
    settings_label = ttk.Label(settings_frame, text="Settings", background="black", foreground="white")
    settings_label.grid(row=0, column=0, pady=10, padx=10)
    scrollable_frame = ScrollableFrame(settings_frame, bg='black')
    scrollable_frame.grid(row=1, column=0, sticky="nsew")
    settings_frame.grid_rowconfigure(1, weight=1)
    settings_frame.grid_columnconfigure(0, weight=1)
    
    # Create advanced settings checkbox
    advanced_var = tk.BooleanVar(value=False)
    advanced_Toggle = ToggleSwitch(scrollable_frame.scrollable_frame, text="Advanced Settings", variable=advanced_var, command=toggle_advanced_settings)
    advanced_Toggle.grid(row=4, column=0, pady=10, padx=10)
    settings = get_measure_crop_settings({})
    variables = convert_settings_dict_for_gui(settings)
    vars_dict = generate_fields(variables, scrollable_frame)
    toggle_advanced_settings()
    vars_dict['Test mode'] = (None, None, tk.BooleanVar(value=False))
    
    # Button section
    btn_row = 1
    run_button = CustomButton(scrollable_frame.scrollable_frame, text="Run", command=lambda: start_process(q, fig_queue), font=('Helvetica', 10))
    run_button.grid(row=btn_row, column=0, pady=5, padx=5)
    abort_button = CustomButton(scrollable_frame.scrollable_frame, text="Abort", command=initiate_abort, font=('Helvetica', 10))
    abort_button.grid(row=btn_row, column=1, pady=5, padx=5)
    btn_row += 1
    test_mode_button = CustomButton(scrollable_frame.scrollable_frame, text="Test Mode", command=toggle_test_mode)
    test_mode_button.grid(row=btn_row, column=0, pady=5, padx=5)
    import_btn = CustomButton(scrollable_frame.scrollable_frame, text="Import", command=lambda: import_settings(scrollable_frame), font=('Helvetica', 10))
    import_btn.grid(row=btn_row, column=1, pady=5, padx=5)
    btn_row += 1
    progress_label = ttk.Label(scrollable_frame.scrollable_frame, text="Processing: 0%", background="black", foreground="white") # Create progress field
    progress_label.grid(row=btn_row, column=0, columnspan=2, sticky="ew", pady=(5, 0), padx=10)

    # Plot Canvas Section
    plot_frame = tk.PanedWindow(vertical_container, orient=tk.VERTICAL)
    vertical_container.add(plot_frame, stretch="always")
    figure = Figure(figsize=(30, 4), dpi=100, facecolor='black')
    plot = figure.add_subplot(111)
    plot.plot([], [])
    plot.axis('off')
    canvas = FigureCanvasTkAgg(figure, master=plot_frame)
    canvas.get_tk_widget().configure(cursor='arrow', background='black', highlightthickness=0)
    canvas_widget = canvas.get_tk_widget()
    plot_frame.add(canvas_widget, stretch="always")
    canvas.draw()
    canvas.figure = figure

    # Console Section
    console_frame = tk.Frame(vertical_container, bg='black')
    vertical_container.add(console_frame, stretch="always")
    console_label = ttk.Label(console_frame, text="Console", background="black", foreground="white")
    console_label.grid(row=0, column=0, pady=10, padx=10)
    console_output = scrolledtext.ScrolledText(console_frame, height=10, bg='black', fg='white', insertbackground='white')
    console_output.grid(row=1, column=0, sticky="nsew")
    console_frame.grid_rowconfigure(1, weight=1)
    console_frame.grid_columnconfigure(0, weight=1)

    q = Queue()
    sys.stdout = StdoutRedirector(console_output)
    sys.stderr = StdoutRedirector(console_output)
    
    _process_console_queue()
    _process_fig_queue()
    
    after_id = parent_frame.after(100, lambda: main_thread_update_function(parent_frame, q, fig_queue, canvas_widget, progress_label))
    parent_frame.after_tasks.append(after_id)
    
    return parent_frame, vars_dict

def gui_measure():
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f"{width}x{height}") 
    root.title("SpaCr: measure objects")
    
    # Clear previous content if any
    if hasattr(root, 'content_frame'):
        for widget in root.content_frame.winfo_children():
            widget.destroy()
        root.content_frame.grid_forget()
    else:
        root.content_frame = tk.Frame(root)
        root.content_frame.grid(row=1, column=0, sticky="nsew")
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
    
    initiate_measure_root(root.content_frame)
    create_menu_bar(root)
    root.mainloop()

if __name__ == "__main__":
    gui_measure()