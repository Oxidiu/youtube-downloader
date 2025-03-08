@echo off
setlocal

set "FFMPEG_PATH=%~dp0ffmpeg"
set "PATH=%FFMPEG_PATH%;%PATH%"

.\yt-dlp.exe -U -i --geo-bypass -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" -w -c -a "download.txt" --output "downloads\%%(title)s.%%(ext)s" --download-archive "archive.txt"

@REM -i or --ignore-errors: Skips unavailable videos instead of stopping.
@REM --geo-bypass                          Bypass geographic restriction via faking X-Forwarded-For HTTP header
@REM --yes-playlist                        Download the playlist, if the URL refers to a video and a playlist.
@REM --abort-on-unavailable-fragment       Abort downloading when some fragment is not available
@REM -w, --no-overwrites                   Do not overwrite files
@REM -c, --continue                        Force resume of partially downloaded files
@REM -a, --batch-file FILE                 File containing URLs to download
@REM --format (-f)                         Selects the best MP4 video and M4A audio format and merges them

echo.
echo Download complete. Press any key to exit...
pause >nul
