import os
import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
yt_dlp_path = os.path.join(script_dir, "yt-dlp.exe")
download_txt_path = os.path.join(script_dir, "download.txt")
saved_links_dir = os.path.join(script_dir, "saved_links")

# Ensure the saved_links directory exists
os.makedirs(saved_links_dir, exist_ok=True)

# Variable to store the name of the last loaded file
last_loaded_file = None

# Function to run a command in the shell
def run_script(command):
    try:
        subprocess.run(command, check=True, text=True)
        messagebox.showinfo("Success", "Download Complete!")
    except subprocess.CalledProcessError:
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

# Create the GUI
root = tk.Tk()
root.title("YouTube Downloader")

# Add a label for the options
tk.Label(root, text="Choose an option:", font=("Arial", 14)).pack(pady=10)

# Add a single button for downloading
tk.Button(root, text="Download", command=download, width=20, height=2).pack(pady=5)

# Add a label and text widget for editing download.txt
tk.Label(root, text="Edit download.txt:", font=("Arial", 14)).pack(pady=10)
download_txt = tk.Text(root, width=60, height=10)
download_txt.pack(pady=5)

# Add checkboxes for selecting playlist and mp4
playlist_var = tk.BooleanVar()
playlist_checkbox = tk.Checkbutton(root, text="Playlist", variable=playlist_var, command=load_download_txt)
playlist_checkbox.pack(pady=5)

mp4_var = tk.BooleanVar()
mp4_checkbox = tk.Checkbutton(root, text="MP4", variable=mp4_var, command=load_download_txt)
mp4_checkbox.pack(pady=5)

# Add a checkbox for "Do not download again"
no_download_again_var = tk.BooleanVar()
no_download_again_checkbox = tk.Checkbutton(root, text="Do not download again", variable=no_download_again_var, command=load_download_txt)
no_download_again_checkbox.pack(pady=5)

# Add a button to save links
tk.Button(root, text="Save links", command=save_links, width=20, height=2).pack(pady=5)

# Add a button to load links
tk.Button(root, text="Load links", command=load_links, width=20, height=2).pack(pady=5)

# Load the initial content of download.txt
load_download_txt()

# Bind the text widget to save content while typing
download_txt.bind('<KeyRelease>', save_download_txt)
tk.Button(root, text="Exit", command=root.quit, width=20, height=2, bg="red", fg="white").pack(pady=10)

# Run the GUI
root.mainloop()
