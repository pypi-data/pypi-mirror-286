# Dracula

This script updates MP3 metadata based on predefined track lists.

Source of the track list: https://gall.dcinside.com/mini/board/view/?id=musicalplay&no=216401&page=1

## Installation

You can install the package using pip:

``` shell
pip install git+https://github.com/yourusername/metadata_updater.git
```

## Usage
Before use,
- The file structure should look like this:
    <album folder>.
    --- CD1
    --- CD2
    --- CD3
- Please keep the file names as they are ripped:
    <track number> track <track number>.mp3

``` shell
dracula <folder_path> [image_path]
```
- folder_path: Path to the folder containing folders named CD1~CD3
- [image_path]: (Optional) Path to the album cover image.
