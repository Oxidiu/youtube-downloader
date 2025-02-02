# FORMAT SELECTION

The general syntax for format selection is --format FORMAT or shorter -f FORMAT where FORMAT is a selector expression, i.e. an expression that describes format or formats you would like to download.

You can also use a file extension (currently 3gp, aac, flv, m4a, mp3, mp4, ogg, wav, webm are supported) to download the best quality format of a particular file extension served as a single file, e.g. -f webm will download the best quality format with the webm extension served as a single file.

## Format selection examples
Note that on Windows you may need to use double quotes instead of single.
```
# Download best mp4 format available or any other best if no mp4 available
$ youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

# Download best format available but no better than 480p
$ youtube-dl -f 'bestvideo[height<=480]+bestaudio/best[height<=480]'

# Download best video only format but no bigger than 50 MB
$ youtube-dl -f 'best[filesize<50M]'

# Download best format available via direct link over HTTP/HTTPS protocol
$ youtube-dl -f '(bestvideo+bestaudio/best)[protocol^=http]'

# Download the best video format and the best audio format without merging them
$ youtube-dl -f 'bestvideo,bestaudio' -o '%(title)s.f%(format_id)s.%(ext)s'
```
