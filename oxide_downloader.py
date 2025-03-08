import os
import subprocess
import tkinter as tk
from tkinter import messagebox

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
yt_dlp_path = os.path.join(script_dir, "yt-dlp.exe")
download_mp3_txt_path = os.path.join(script_dir, "download_mp3.txt")
download_mp4_txt_path = os.path.join(script_dir, "download_mp4.txt")
download_mp4_list_txt_path = os.path.join(script_dir, "download_mp4_list.txt")
download_mp3_list_txt_path = os.path.join(script_dir, "download_mp3_list.txt")

# Function to run a command in the shell
def run_script(command):
    try:
        subprocess.run(command, shell=True, check=True, text=True)
        messagebox.showinfo("Success", "Download Complete!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Download failed!")

# Function to download MP3 files using yt-dlp
def download_mp3():
    command = rf'"{yt_dlp_path}" -U -i --geo-bypass --yes-playlist --add-metadata --embed-thumbnail -x --audio-format mp3 -w -c -a "{download_mp3_txt_path}" --output "{script_dir}\downloads\%(title)s.%(ext)s" --download-archive "{script_dir}\archive.txt"'
    run_script(command)

# Function to download MP4 files using yt-dlp
def download_mp4():
    command = rf'"{yt_dlp_path}" -U --geo-bypass -i -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" -w -c -a "{download_mp4_txt_path}" --output "{script_dir}\downloads\%(title)s.%(ext)s" --download-archive "{script_dir}\archive.mp4.txt"'
    run_script(command)

# Function to download MP3 playlists using yt-dlp
def download_mp3_list():
    command = rf'"{yt_dlp_path}" -i -U --geo-bypass --add-metadata --embed-thumbnail -f bestaudio -x --audio-format mp3 -w -c -a "{download_mp3_list_txt_path}" --output "{script_dir}\downloads\%(title)s.%(ext)s" --download-archive "{script_dir}\archive.txt"'
    run_script(command)

def download_mp4_list():
    command = rf'"{yt_dlp_path}" -U --geo-bypass -i -f --yes-playlist"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" -w -c -a "{download_mp4_list_txt_path}" --output "{script_dir}\downloads\%(title)s.%(ext)s" --download-archive "{script_dir}\archive.mp4.txt"'
    run_script(command)

# Function to load the content of download.txt into the text widget
def load_download_txt():
    if playlist_var.get() and mp4_var.get():
        file_path = download_mp4_list_txt_path
    elif playlist_var.get():
        file_path = download_mp3_list_txt_path
    elif mp4_var.get():
        file_path = download_mp4_txt_path
    else:
        file_path = download_mp3_txt_path

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            download_txt.delete(1.0, tk.END)
            download_txt.insert(tk.END, file.read())
    else:
        download_txt.delete(1.0, tk.END)

# Function to save the content of the text widget into download.txt
def save_download_txt(event=None):
    if playlist_var.get() and mp4_var.get():
        file_path = download_mp4_list_txt_path
    elif playlist_var.get():
        file_path = download_mp3_list_txt_path
    elif mp4_var.get():
        file_path = download_mp4_txt_path
    else:
        file_path = download_mp3_txt_path

    with open(file_path, 'w') as file:
        file.write(download_txt.get(1.0, tk.END))

# Create the GUI
root = tk.Tk()
root.title("YouTube Downloader")

# Add a label for the options
tk.Label(root, text="Choose an option:", font=("Arial", 14)).pack(pady=10)

# Add buttons for downloading MP3, MP4, and MP3 playlists
tk.Button(root, text="Download MP3", command=download_mp3, width=20, height=2).pack(pady=5)
tk.Button(root, text="Download MP4", command=download_mp4, width=20, height=2).pack(pady=5)
tk.Button(root, text="Download MP3 Playlist", command=download_mp3_list, width=20, height=2).pack(pady=5)

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

# Load the initial content of download.txt
load_download_txt()

# Bind the text widget to save content while typing
download_txt.bind('<KeyRelease>', save_download_txt)
tk.Button(root, text="Exit", command=root.quit, width=20, height=2, bg="red", fg="white").pack(pady=10)

# Run the GUI
root.mainloop()
