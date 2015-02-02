# wp

This script downloads and manipulates color palletes for X11 based Linux systems. It includes functionality to download color palletes from the site [dotshare.it](http://dotshare.it), and generate color palletes from image files (wallpapers).

I've forked this from https://github.com/everett1992/wp, and included a bunch of extra functionality.

The color extraction scripts were taken from [this blog post](http://charlesleifer.com/blog/using-python-and-k-means-to-find-the-dominant-colors-in-images/)
 with normalization reddit user radiosilence.

## Dependencies

* PIL, the python image library. Ususally this can be gotten by `pip install Pillow`
* python2-requests, if you want to use the dotshare.it functionality
* dmenu, if you want to use the 'colorselect' functionality

## Setup

All color files will be downloaded to ~/dotfiles/colors, unless you specify a different $COLORS_DIR by editing `wp`. Make sure this directory exists, or change it in the file.

The current colorscheme will be symlinked to ~/.colors, and ~/.colorsX for sourcing by bash scripts and xrdb respectively. As such, you should include the following line in your ~/.Xresources file:

```
#include "/home/username/.colorsX"
```

This script only works on the color pallete, all other xrdb tweaks (fonts, mouse colors, cursors, transparency) should be made in ~/.Xresources.

## Usage

```
$ wp generate [file]
```

Generates color files [file].colors and [file].colorsX which can be sourced by shell scripts and xrdb respectivly. The color files are added to the $COLORS_DIR directory, which defaults to ~/dotfiles/colors/.

```
$ wp colorselect
```

Pipes a list of all the colorschemes in $COLORS_DIR into dmenu, then links the selected one and merges xrdb.
Dependencies: dmenu

```
$ wp dotshare [dot-id]
```

Fetches a set of terminal colors from dotshare.it, a social dotfiles sharing site, reformats them, and puts them into $COLORS_DIR. By dot-id, I mean the end of a colorscheme's url, for example http://dotshare.it/dots/87/'s dot-id would be 87. Make sure that the colorscheme is from the set in http://dotshare.it/category/terms/colors/.
Dependencies: python2-requests

```
$ wp colors
```

Displays a pretty-printed color pallete in your terminal!
