# colorman X11 Color Manager

This script downloads and manipulates color palettes for X11 based Linux systems. It includes functionality to download color palettes from the site [dotshare.it](http://dotshare.it), and generate color palettes from image files (wallpapers).

I've forked this from https://github.com/everett1992/wp, rewrote most of it in python, and included a bunch of extra functionality.

The color extraction scripts were taken from [this blog post](http://charlesleifer.com/blog/using-python-and-k-means-to-find-the-dominant-colors-in-images/)
 with normalization reddit user radiosilence.

## Dependencies

* PIL, the python image library. Ususally this can be gotten by `pip install Pillow`

## Setup

All color files will be downloaded to ~/dotfiles/colors, unless you specify a different directory with the '-l' flag. If the directory does not exist, it will be created for you.

The current colorscheme will be symlinked to ~/.colors, and ~/.colorsX for sourcing by bash scripts and xrdb respectively. As such, you should include the following line in your ~/.Xresources file:

```
#include "/home/username/.colorsX"
```

This script only works on the color palette, all other xrdb tweaks (fonts, mouse colors, cursors, transparency) should be made in ~/.Xresources.

## Usage

```
cman.py
```

With no arguments, displays a pretty-printed color palette of your current scheme in your terminal!

```
cman.py -g [image file]
```

Generates color files [image file].colors and [image file].colorsX which can be sourced by shell scripts and xrdb respectivly. The color files are added to the colorscheme directory, which defaults to ~/dotfiles/colors/. You can specify this with:

```
cman.py -g [image file] -l [alternate location]
```

This flag works for all subsequent options involving manipulating color schemes.

```
cman.py -d [dot-id]
```

Fetches a set of terminal colors from dotshare.it, a social dotfiles sharing site, reformats them, and puts them into the colorscheme directory. By dot-id, I mean the end of a colorscheme's url, for example http://dotshare.it/dots/87/ 's dot-id would be 87. Make sure that the colorscheme is from the set in http://dotshare.it/category/terms/colors/.

```
cman.py -f [file] [name]
```

Format a ~/.Xresources style file, generate a color palette from it, put it into the colorscheme directory. [name] indicates the name of the generated color scheme.

```
cman.py -i
```

Currently experimental functionality to generate templated i3 config file from your current color scheme.
