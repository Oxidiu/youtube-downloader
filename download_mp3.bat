@echo off
setlocal

set "FFMPEG_PATH=%~dp0ffmpeg"
set "PATH=%FFMPEG_PATH%;%PATH%"

youtube-dl.exe --geo-bypass --yes-playlist --abort-on-unavailable-fragment --add-metadata --embed-thumbnail -x --audio-format mp3 -w -c -a "download_list.txt" --output "downloads\%%(title)s.%%(ext)s" --download-archive "archive.txt"

@REM --geo-bypass                          Bypass geographic restriction via faking X-Forwarded-For HTTP header
@REM --yes-playlist                        Download the playlist, if the URL refers to a video and a playlist.
@REM --abort-on-unavailable-fragment       Abort downloading when some fragment is not available
@REM --newline
@REM --write-all-thumbnails                Write all thumbnail image formats to disk
@REM -x                                    Convert video files to audio-only files (requires ffmpeg/avconv and ffprobe/avprobe) "flac", "mp3", "m4a", "opus", "vorbis", or "wav"; "best" by default; No effect without -x
@REM -v, --verbose                         Print various debugging information
@REM -w, --no-overwrites                   Do not overwrite files
@REM -c, --continue                        Force resume of partially downloaded files. By default, youtube-dl will resume downloads if possible.
@REM --format                              Video format code, see the "FORMAT SELECTION" for all the info
@REM -a, --batch-file FILE                 File containing URLs to download ('-' for stdin), one URL per line. Lines starting with '#', ';' or ']' are considered as comments and ignored. Use only video ID in file name
@REM --add-metadata                        Write metadata to the video file
@REM --embed-thumbnail                    Embed thumbnail in the audio as cover

echo.
echo Download complete. Press any key to exit...
pause >nul
