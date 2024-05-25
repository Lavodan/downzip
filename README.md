# downzip
A CLI/GUI tool for downloading and uncompressing weirdly nested archives

### WARNING

Do not use this tool for non archive files, for files in a different format than it is handled for. This program cleans up after itself, which means it deletes files, no guarantee for unexpected behaviour!!
Designed to only handle archive files in the format of archive(folder(archive(content))). Extracts content into specified folder, or the default temporary folder "./temp_down".

## Installation
clone repo
install dependancies (non comprehensive list: PyQt6, requests)
run downzip.py or guihandler.py

OR

download release
unzip
run DownZip.exe

## Usage
### as CLI
`py downzip.py <URL> [path] [-y]`
### as GUI
`py guihandler.py` OR `DownZip.exe`
use buttons
you MAY need to use console to confirm overriting if you do not use Always Yes flag

## Attributions
icon designed by Freepik
7zip is NOT made by me (lol)
