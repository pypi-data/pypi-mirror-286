import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
from PIL import Image, ImageTk
import io
import requests

def execute_curl_command(node, command, results):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            results[node] = (f"{node} app installation is In-Progress.", "success")
        else:
            results[node] = (f"{node} Check the Network & Try Again.", "failure")
    except Exception as e:
        results[node] = (f"{node} app failed. Error: {str(e)}", "failure")

def submit_selection():
    selected_nodes = []
    if var1.get():
        selected_nodes.append(("Node 1", "curl -I http://172.18.69.29:8080/job/COLLAB%20TEAM/job/MOBILE/job/iOS%20Mobile%20App/job/REGRESSION/job/Discovery/job/TEST_APP_INSTALL/buildWithParameters?token=116ec8a3d7f804033452db1feb428d7ddb"))
    if var2.get():
        selected_nodes.append(("Node 2", "curl -I https://examdhdple.com/node2"))
    if var3.get():
        selected_nodes.append(("Node 3", "curl -I https://example.com/node3"))
    if var_all.get():
        selected_nodes = [
            ("Node 1", "curl -I http://172.18.69.29:8080/job/COLLAB%20TEAM/job/MOBILE/job/iOS%20Mobile%20App/job/REGRESSION/job/Discovery/job/TEST_APP_INSTALL/buildWithParameters?token=116ec8a3d7f804033452db1feb428d7ddb"),
            ("Node 2", "curl -I https://examplddde.com/node2"),
            ("Node 3", "curl -I https://example.com/node3")
        ]
    
    if not selected_nodes:
        messagebox.showinfo("Selected Nodes", "No nodes selected")
        return

    # Hide the initial screen elements and show the loader
    main_frame.pack_forget()
    loader_label.pack(pady=20)
    root.update_idletasks()  # Force GUI to update

    results = {}
    threads = []

    for node, command in selected_nodes:
        thread = threading.Thread(target=execute_curl_command, args=(node, command, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    show_summary_screen(results)

def show_summary_screen(results):
    global summary_frame

    loader_label.pack_forget()
    summary_frame.pack(fill=tk.BOTH, expand=True)
    root.update_idletasks()  # Force GUI to update

    # Load and display the image at the top of the summary screen
    summary_image_url = "https://cdn-icons-png.flaticon.com/512/107/107822.png"
    response = requests.get(summary_image_url)
    image_bytes = io.BytesIO(response.content)
    summary_image = Image.open(image_bytes)
    summary_image = summary_image.resize((100, 100), Image.LANCZOS)
    summary_photo = ImageTk.PhotoImage(summary_image)

    image_label = tk.Label(summary_frame, image=summary_photo, bg='#f0f0f0')
    image_label.image = summary_photo  # Keep a reference to avoid garbage collection
    image_label.pack(pady=(10, 5))

    for node, (result, status) in results.items():
        # Create a frame to hold the icon and the text
        result_frame = tk.Frame(summary_frame, bg='#f0f0f0')
        result_frame.pack(pady=5)

        # Create a canvas to display the status icon
        icon_canvas = tk.Canvas(result_frame, width=50, height=50, bg='#f0f0f0', highlightthickness=0)
        icon_canvas.pack(side=tk.LEFT, padx=10)
        
        if status == "success":
            icon_canvas.create_text(25, 25, text="✔", font=("Arial", 40, "bold"), fill="green")
        else:
            icon_canvas.create_text(25, 25, text="❌", font=("Arial", 40, "bold"), fill="red")

        # Create a label to display the result text
        result_label = tk.Label(result_frame, text=result, font=('Arial', 12), bg='#f0f0f0', fg='#333')
        result_label.pack(side=tk.LEFT)

    go_back_button = tk.Button(summary_frame, text="Go Back", command=go_back, font=('Arial', 16, 'bold'), bg='#007BFF', fg='black', relief='raised', padx=20, pady=10, borderwidth=2)
    go_back_button.pack(side=tk.LEFT, padx=10, pady=10)
    close_button = tk.Button(summary_frame, text="Close", command=close_app, font=('Arial', 16, 'bold'), bg='#FF4C4C', fg='black', relief='raised', padx=20, pady=10, borderwidth=2)
    close_button.pack(side=tk.RIGHT, padx=10, pady=10)

def go_back():
    # Hide the summary frame
    summary_frame.pack_forget()
    root.update_idletasks()  # Force GUI to update
    
    # Show the main frame
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Reset selections
    var1.set(False)
    var2.set(False)
    var3.set(False)
    var_all.set(False)
    
    # Clear any previous results or messages
    for widget in summary_frame.winfo_children():
        widget.pack_forget()
    
    root.update_idletasks()  # Force GUI to update

def close_app():
    try:
        root.destroy()  # Properly destroys the Tkinter root window
    except Exception as e:
        print(f"Error closing app: {e}")

def select_all_nodes():
    state = var_all.get()
    var1.set(state)
    var2.set(state)
    var3.set(state)

def handle_checkbox_change(*args):
    # Check if any checkbox is deselected
    if not (var1.get() and var2.get() and var3.get()):
        var_all.set(False)
    else:
        var_all.set(True)

def initialize_ui():
    global root, main_frame, summary_frame, loader_label, logo_photo, loader_photo, unchecked_image, checked_image, instruction_logo_photo

    root = tk.Tk()
    root.title("iDeploy Master")
    root.configure(bg='#f0f0f0')
    root.resizable(False, False)

    # Define window dimensions and position
    window_width = 400
    window_height = 500
    position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
    position_top = int(root.winfo_screenheight() / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Load images
    response = requests.get("https://cdn-icons-png.flaticon.com/512/2502/2502370.png")
    image_bytes = io.BytesIO(response.content)
    logo_image = Image.open(image_bytes)
    logo_image = logo_image.resize((100, 100), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)

    response = requests.get("https://cdn-icons-png.flaticon.com/512/107/107803.png")
    image_bytes = io.BytesIO(response.content)
    loader_image = Image.open(image_bytes)
    loader_image = loader_image.resize((100, 100), Image.LANCZOS)
    loader_photo = ImageTk.PhotoImage(loader_image)

    unchecked_image = ImageTk.PhotoImage(Image.open(requests.get("https://cdn-icons-png.flaticon.com/512/32/32216.png", stream=True).raw).resize((20, 20), Image.LANCZOS))
    checked_image = ImageTk.PhotoImage(Image.open(requests.get("https://cdn-icons-png.flaticon.com/512/32/32212.png", stream=True).raw).resize((20, 20), Image.LANCZOS))

    # New image for selecting an option
    instruction_logo_url = "https://cdn-icons-png.flaticon.com/512/107/107800.png"
    response = requests.get(instruction_logo_url)
    image_bytes = io.BytesIO(response.content)
    instruction_logo_image = Image.open(image_bytes)
    instruction_logo_image = instruction_logo_image.resize((50, 50), Image.LANCZOS)
    instruction_logo_photo = ImageTk.PhotoImage(instruction_logo_image)

    # Define variables for checkbuttons
    global var_all, var1, var2, var3
    var_all = tk.BooleanVar()
    var1 = tk.BooleanVar()
    var2 = tk.BooleanVar()
    var3 = tk.BooleanVar()

    # Initialize UI components
    initialize_main_frame()
    initialize_loader()

    # Initialize summary frame
    summary_frame = tk.Frame(root, bg='#f0f0f0')

    root.mainloop()

def initialize_main_frame():
    global main_frame

    # Main frame for the initial screen
    main_frame = tk.Frame(root, bg='#f0f0f0')
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame for welcome label and logo
    top_frame = tk.Frame(main_frame, bg='#007BFF')
    top_frame.pack(fill=tk.X, pady=(10, 0))

    logo_label = tk.Label(top_frame, image=logo_photo, bg='#007BFF')
    logo_label.pack(side=tk.LEFT, padx=10, pady=10)

    welcome_label = tk.Label(top_frame, text="iDeploy Master", font=('Comic Sans MS', 18, 'bold'), bg='#007BFF', fg='white')
    welcome_label.pack(side=tk.LEFT, padx=10, pady=10)

    # Frame for instruction text, logo, checkboxes, and submit button
    controls_frame = tk.Frame(main_frame, bg='#f0f0f0')
    controls_frame.pack(pady=(10, 20), expand=True)

    # Add a new instruction logo before the "Select Nodes" label
    instruction_logo_label = tk.Label(controls_frame, image=instruction_logo_photo, bg='#f0f0f0')
    instruction_logo_label.pack(pady=(0, 10))

    select_label = tk.Label(controls_frame, text="Select Nodes", font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#333')
    select_label.pack(pady=(0, 10))

    # Checkbox for selecting all nodes
    all_nodes_check = tk.Checkbutton(
        controls_frame,
        text="Select All Nodes",
        variable=var_all,
        command=select_all_nodes,
        bg='#f0f0f0',
        fg='#333333',
        font=('Arial', 14),
        selectcolor='#007BFF',
        image=unchecked_image,
        selectimage=checked_image,
        compound='left'
    )
    all_nodes_check.pack(pady=5)

    # Checkbox for individual nodes
    var1.trace_add('write', handle_checkbox_change)
    tk.Checkbutton(
        controls_frame,
        text="Node 1",
        variable=var1,
        onvalue=True,
        offvalue=False,
        bg='#f0f0f0',
        fg='#333333',
        font=('Arial', 14),
        selectcolor='#007BFF',
        image=unchecked_image,
        selectimage=checked_image,
        compound='left'
    ).pack(pady=5)

    var2.trace_add('write', handle_checkbox_change)
    tk.Checkbutton(
        controls_frame,
        text="Node 2",
        variable=var2,
        onvalue=True,
        offvalue=False,
        bg='#f0f0f0',
        fg='#333333',
        font=('Arial', 14),
        selectcolor='#007BFF',
        image=unchecked_image,
        selectimage=checked_image,
        compound='left'
    ).pack(pady=5)

    var3.trace_add('write', handle_checkbox_change)
    tk.Checkbutton(
        controls_frame,
        text="Node 3",
        variable=var3,
        onvalue=True,
        offvalue=False,
        bg='#f0f0f0',
        fg='#333333',
        font=('Arial', 14),
        selectcolor='#007BFF',
        image=unchecked_image,
        selectimage=checked_image,
        compound='left'
    ).pack(pady=5)

    submit_button = tk.Button(
        controls_frame,
        text="Deploy",
        command=submit_selection,
        font=('Arial', 16, 'bold'),
        bg='#007BFF',
        fg='black',
        relief='raised',
        padx=20,
        pady=10,
        borderwidth=2
    )
    submit_button.pack(pady=20)

def initialize_loader():
    global loader_label

    loader_label = tk.Label(root, image=loader_photo, bg='#f0f0f0')

if __name__ == "__main__":
    initialize_ui()
