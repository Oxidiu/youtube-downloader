import os
import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import markdown
from tkinter import ttk
from tkinterhtml import HtmlFrame
import yt_dlp


# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
yt_dlp_path = os.path.join(script_dir, "yt-dlp.exe")
download_txt_path = os.path.join(script_dir, "download.txt")
saved_links_dir = os.path.join(script_dir, "saved_links")

# Ensure the saved_links directory exists
os.makedirs(saved_links_dir, exist_ok=True)

# Variable to store the name of the last loaded file
last_loaded_file = None

# Function to run a command in the shell and capture the output
def run_script(command):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        output_text.insert(tk.END, result.stdout)
        messagebox.showinfo("Success", "Download Complete!")
    except subprocess.CalledProcessError as e:
        output_text.insert(tk.END, e.stderr)
        messagebox.showerror("Error", "Download failed!")

# Function to download files using yt-dlp
def download_files():
    if not os.path.exists(download_txt_path):
        with open(download_txt_path, 'w') as file:
            pass

    with open(download_txt_path, 'r') as file:
        links = file.readlines()

    for link in links:
        link = link.strip()
        if not link:
            continue

        command = [yt_dlp_path, '-U', '--geo-bypass', '-i', '-w', '-c', link]

        if playlist_var.get() and "list=" in link:
            command.append('--yes-playlist')
            output_template = f"{script_dir}\\downloads\\%(playlist_title)s\\%(title)s.%(ext)s"
        else:
            command.append('--no-playlist')
            output_template = f"{script_dir}\\downloads\\%(title)s.%(ext)s"

        if mp4_var.get():
            command.extend(['-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]', '--output', output_template])
            if no_download_again_var.get():
                command.extend(['--download-archive', f"{script_dir}\\archive.mp4.txt"])
        else:
            command.extend(['--add-metadata', '--embed-thumbnail', '-x', '--audio-format', 'mp3', '--output', output_template])
            if no_download_again_var.get():
                command.extend(['--download-archive', f"{script_dir}\\archive.txt"])

        run_script(command)

# Function to load the content of download.txt into the text widget
def load_download_txt():
    if os.path.exists(download_txt_path):
        with open(download_txt_path, 'r') as file:
            download_txt.delete(1.0, tk.END)
            download_txt.insert(tk.END, file.read())
    else:
        with open(download_txt_path, 'w') as file:
            pass
        download_txt.delete(1.0, tk.END)

# Function to save the content of the text widget into download.txt
def save_download_txt(event=None):
    with open(download_txt_path, 'w') as file:
        file.write(download_txt.get(1.0, tk.END))

# Function to save the content of the text widget into a named file in saved_links
def save_links():
    global last_loaded_file
    name = simpledialog.askstring("Save links", "Enter the name for the list:", initialvalue=last_loaded_file)
    if name:
        save_path = os.path.join(saved_links_dir, f"{name}.txt")
        with open(save_path, 'w') as file:
            file.write(download_txt.get(1.0, tk.END))
        messagebox.showinfo("Success", f"Links saved as {name}.txt")
        last_loaded_file = name

# Function to load a saved links file
def load_links():
    global last_loaded_file
    file_path = filedialog.askopenfilename(initialdir=saved_links_dir, title="Select file", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file_path:
        with open(file_path, 'r') as file:
            download_txt.delete(1.0, tk.END)
            download_txt.insert(tk.END, file.read())
        last_loaded_file = os.path.splitext(os.path.basename(file_path))[0]

# Function to determine which download function to call
def download():
    download_files()

# Function to open the downloads location
def open_downloads_location():
    downloads_path = os.path.join(script_dir, "downloads")
    if not os.path.exists(downloads_path):
        os.makedirs(downloads_path)
    subprocess.Popen(f'explorer "{downloads_path}"')

# Function to open supported_sites.md in a dialog with a searchbox
def open_supported_sites():
    supported_sites_path = os.path.join(script_dir, "supported_sites.md")
    if not os.path.exists(supported_sites_path):
        with open(supported_sites_path, 'w') as file:
            file.write("This file contains the list of supported sites.")

    # Create a new window
    top = tk.Toplevel(root)
    top.title("Supported Sites")

    # Create a frame for the search box and text widget
    frame = tk.Frame(top)
    frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Create a search box
    search_var = tk.StringVar()
    search_box = tk.Entry(frame, textvariable=search_var, width=50)
    search_box.pack(pady=5)

    # Create a text widget with a scrollbar
    text_frame = tk.Frame(frame)
    text_frame.pack(fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    text_widget.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=text_widget.yview)

    # Load the content of supported_sites.md into the text widget
    with open(supported_sites_path, 'r', encoding='utf-8') as file:
        md_content = file.read()
        text_widget.insert(tk.END, md_content)

    # Function to search the text widget
    def search():
        text_widget.tag_remove('highlight', '1.0', tk.END)
        search_text = search_var.get()
        if search_text:
            start_pos = '1.0'
            while True:
                start_pos = text_widget.search(search_text, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(search_text)}c"
                text_widget.tag_add('highlight', start_pos, end_pos)
                start_pos = end_pos
            text_widget.tag_config('highlight', background='yellow', foreground='black')

    # Bind the search function to the search box
    search_box.bind('<KeyRelease>', lambda _: search())

    # Format the text widget content with markdown
    def format_markdown():
        text_widget.delete(1.0, tk.END)
        with open(supported_sites_path, 'r', encoding='utf-8') as file:
            md_content = file.read()
            html_content = markdown.markdown(md_content)
            text_widget.insert(tk.END, html_content)

    format_markdown()



# Create the GUI
root = tk.Tk()
root.title("OXiDE Downloader")

# Add a label for the options
tk.Label(root, text="Choose an option:", font=("Arial", 14)).pack(pady=10)
# Add checkboxes for selecting playlist, mp4, and "Do not download again"
options_frame = tk.Frame(root)
options_frame.pack(pady=5)

playlist_var = tk.BooleanVar()
playlist_checkbox = tk.Checkbutton(options_frame, text="Playlist", variable=playlist_var, command=load_download_txt)
playlist_checkbox.pack(side=tk.LEFT, padx=5)

mp4_var = tk.BooleanVar()
mp4_checkbox = tk.Checkbutton(options_frame, text="MP4", variable=mp4_var, command=load_download_txt)
mp4_checkbox.pack(side=tk.LEFT, padx=5)

no_download_again_var = tk.BooleanVar()
no_download_again_checkbox = tk.Checkbutton(options_frame, text="Do not download again", variable=no_download_again_var, command=load_download_txt)
no_download_again_checkbox.pack(side=tk.LEFT, padx=5)

# Add a label and text widget for editing download.txt
tk.Label(root, text="Place the links here:", font=("Console", 13)).pack(pady=10)
download_txt = tk.Text(root, width=60, height=10)
download_txt.pack(pady=5)

# Create a frame for the buttons
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)

# Create a frame for the first column of buttons
left_buttons_frame = tk.Frame(buttons_frame)
left_buttons_frame.pack(side=tk.LEFT, padx=10)

# Add a button to save links
tk.Button(left_buttons_frame, text="Save links", command=save_links, width=20, height=2).pack(pady=5)

# Add a button to load links
tk.Button(left_buttons_frame, text="Load links", command=load_links, width=20, height=2).pack(pady=5)

# Load the initial content of download.txt
load_download_txt()

# Create a frame for the second column of buttons
right_buttons_frame = tk.Frame(buttons_frame)
right_buttons_frame.pack(side=tk.LEFT, padx=10)



# Add a button to open the downloads location
tk.Button(right_buttons_frame, text="Downloads location", command=open_downloads_location, width=20, height=2).pack(pady=5)

# Add a button to open the supported sites file
tk.Button(right_buttons_frame, text="Supported Sites", command=open_supported_sites, width=20, height=2).pack(pady=5)

# Add a single button for downloading
tk.Button(root, text="Download", command=download, width=20, height=2).pack(pady=5)

# Add a text widget to display the output of the commands
output_text = tk.Text(root, width=60, height=10)
output_text.pack(pady=5)

# Function to run a command in the shell and capture the output in real-time
def run_script(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output_text.delete(1.0, tk.END)
    for line in iter(process.stdout.readline, ''):
        output_text.insert(tk.END, line)
        output_text.see(tk.END)
        root.update_idletasks()
    process.stdout.close()
    process.wait()
    if process.returncode == 0:
        messagebox.showinfo("Success", "Download Complete!")
    else:
        for line in iter(process.stderr.readline, ''):
            output_text.insert(tk.END, line)
            output_text.see(tk.END)
            root.update_idletasks()
        messagebox.showerror("Error", "Download failed!")
    process.stderr.close()

# Bind the text widget to save content while typing
download_txt.bind('<KeyRelease>', save_download_txt)
tk.Button(root, text="Exit", command=root.quit, width=20, height=2, bg="red", fg="white").pack(pady=10)

# Run the GUI
root.mainloop()
