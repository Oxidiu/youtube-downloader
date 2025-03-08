import os
import subprocess
import tkinter as tk
from tkinter import messagebox

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
yt_dlp_path = os.path.join(script_dir, "yt-dlp.exe")

def run_script(command):
    try:
        subprocess.run(command, shell=True, check=True, text=True)
        messagebox.showinfo("Success", "Download Complete!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Download failed!")

def download_mp3():
    command = rf'"{yt_dlp_path}" -U -i --geo-bypass --yes-playlist --add-metadata --embed-thumbnail -x --audio-format mp3 -w -c -a "{script_dir}\download.txt" --output "{script_dir}\downloads\%(title)s.%(ext)s" --download-archive "{script_dir}\archive.txt'
    run_script(command)

def download_mp4():
    command = rf'"{yt_dlp_path}" -U --geo-bypass -i -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" -w -c -a "{script_dir}\download.txt" --output "{script_dir}\downloads\%(title)s.%(ext)s" --download-archive "{script_dir}\archive.txt"'
    run_script(command)

def download_mp3_playlist():
    command = rf'"{yt_dlp_path}" -i -U --geo-bypass --add-metadata --embed-thumbnail -f bestaudio -x --audio-format mp3 -w -c -a "{script_dir}\download_playlists.txt" --output "{script_dir}\downloads\%(title)s.%(ext)s" --download-archive "{script_dir}\archive_mp4.txt"'
    run_script(command)

# Create the GUI
root = tk.Tk()
root.title("YouTube Downloader")

tk.Label(root, text="Choose an option:", font=("Arial", 14)).pack(pady=10)

tk.Button(root, text="Download MP3", command=download_mp3, width=20, height=2).pack(pady=5)
tk.Button(root, text="Download MP4", command=download_mp4, width=20, height=2).pack(pady=5)
tk.Button(root, text="Download MP3 Playlist", command=download_mp3_playlist, width=20, height=2).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit, width=20, height=2, bg="red", fg="white").pack(pady=10)

# Run the GUI
root.mainloop()
