#!/usr/bin/env python2
import argparse
import os
import getpass
from py.color_common import *

# replaces the original 'cman' script, which was ugly bash

# quick hack to make sure the path is formatted right
COLORS_DIR='/home/{}/dotfiles/colors'.format(getpass.getuser())
USER_COLORS='/home/{}/.colors'.format(getpass.getuser())
USER_COLORSX='/home/{}/.colorsX'.format(getpass.getuser())
I3_CONFIG='/home/{}/.i3/config'.format(getpass.getuser())
I3_CONFIG_TEMPLATE='/home/{}/.i3/config-template'.format(getpass.getuser())

''' 
writes a configuration template for i3 with a bunch of variables for the colors to the correct file
'''
def gen_i3():
    with open(I3_CONFIG_TEMPLATE, 'r') as f:
        contents = f.read()
    with open(USER_COLORSX, 'r') as f:
        colors = ''
        color_dict = read_to_dict(f.read())
        for item in sorted(color_dict.keys()):
            colors += 'set ${c} {h}\n'.format(c=item, h=color_dict[item])
    colors += 'set $color16 #111111\n'
    colors += 'set $color17 #e8dfd6\n'
    with open(I3_CONFIG, 'w') as f:
        f.write(colors)
        f.write(contents)

'''
pretty-print your current terminal colors
'''
def print_colors():
    print 'Current scheme: {}'.format(current_scheme())
    # magic numbers, because the conditional will catch everything else
    correct_sort = lambda x: int(x[0][5:]) if x[0].startswith('color') else -1
    with open(USER_COLORSX, 'r') as f:
        hexvals = read_to_dict(f.read())
    for item, val in sorted(hexvals.iteritems(), key=correct_sort):
        potentially_a_color = item[5:] # again, magic numbers
        if not potentially_a_color.isdigit(): # skip 'background', 'foreground' ...
            continue
        color_num = int(potentially_a_color)
        if  color_num < 8:
            print '\x1b[3{i}mCOLOR{i}  ########  {v}\x1b[39;49m'.format(i=color_num, v=val)
        elif color_num > 14:
            continue # if you somehow defined more than the term allows
        else:
            lo = color_num - 8
            if lo < 2:
                print '\x1b[3{i};1mCOLOR{n}  ########  {v}\x1b[39;49m'.format(i=lo, n=color_num, v=val)
            else:
                print '\x1b[3{i};1mCOLOR{n} ########  {v}\x1b[39;49m'.format(i=lo, n=color_num, v=val)

'''
try to grab the title from dotshare using bs4
if not, return the dot_id
'''
def dotshare_title(dot_id):
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return dot_id
    USER_AGENT = 'https://github.com/delucks X colors manager'
    headers = {'User-Agent': USER_AGENT} 
    baseurl='http://dotshare.it/dots/{dotid}'.format(dotid=dot_id) 
    r = urllib2.Request(baseurl, None, headers)
    soup = BeautifulSoup(urllib2.urlopen(r).read())
    header_full = soup.find('div', 'header').h4.text
    return header_full.split('(')[0].strip()

'''
reformat a file from dotshare.it
'''
def dotshare_grab(dot_id, location):
    import urllib2
    USER_AGENT = 'https://github.com/delucks X colors manager'
    headers = {'User-Agent': USER_AGENT} 
    rawurl='http://dotshare.it/dots/{dotid}/0/raw'.format(dotid=dot_id) 
    r = urllib2.Request(rawurl, None, headers)
    title = dotshare_title(dot_id)
    reformat(urllib2.urlopen(r).read(), location, title)

def read_from_file(file_path, name, location):
    with open(file_path) as f:
      reformat(f.read(), location, name)

'''
remove symlink to old colorscheme, add symlink to new colorscheme
'''
def swap_schemes(new_name, location=COLORS_DIR):
    new_colors = os.path.join(location, new_name + '.colors')
    new_colorsX = os.path.join(location, new_name + '.colorsX')
    try:
        os.unlink(USER_COLORS)
        os.unlink(USER_COLORSX)
    except OSError:
        print 'Failed to remove symlinks to ~/.colors and ~/.colorsX!'
        raise
    try:
        os.symlink(new_colors, USER_COLORS)
        os.symlink(new_colorsX, USER_COLORSX)
    except OSError:
        print 'Failed to create symlinks to ~/.colors and ~/.colorsX for colorscheme {}'.format(new_name)
        raise

'''
print out a list of all available colorschemes and prompt the user to select one
'''
def select_scheme(location=COLORS_DIR):
    import glob
    all_schemes = glob.glob(location + '/*.colorsX')
    # using magic numbers because all of these will end in 8-char '.colorsX'
    colorschemes = [i.split('/')[-1][:-8] for i in all_schemes]
    print 'Available colorschemes:\n'
    for item in colorschemes:
        print item
    choice = raw_input('\nEnter a name: ')
    if not choice in colorschemes:
        print '{}: not a valid colorscheme'.format(choice)
    else:
        swap_schemes(choice)
    os.system('xrdb -merge ~/.Xresources')

'''
reads the symlink and returns the name of the current colorscheme
'''
def current_scheme():
    colors_path = '/home/{}/.colors'.format(getpass.getuser())
    loc = os.path.realpath(colors_path)
    if loc == colors_path:
        raise OSError(1, 'Failed to find current color scheme!', colors_path)
    else:
        return loc.split('/')[-1].split('.')[0]

def main():  
    p = argparse.ArgumentParser(description='manage X11 color palletes')
    p.add_argument('-g', '--generate', help='generate a color scheme from an image')
    p.add_argument('-l', '--location', help='set alternate location for the generated color files', default=COLORS_DIR)
    p.add_argument('-f', '--reformat', help='reformat an existing file as a color scheme', nargs=2)
    p.add_argument('-s', '--select', help='open a selection dialog and pick a colorscheme', action='store_true')
    p.add_argument('-d', '--dotshare', help='download and format a color scheme from dotshare.it')
    p.add_argument('-i', '--generate-i3', help='generate an i3 config file from a template (experimental)', action='store_true')
    p.add_argument('-c', '--current', help='display the currently loaded color scheme', action='store_true')
    args = p.parse_args()
    if args.location:
        if not os.path.isdir(args.location):
            os.mkdir(args.location)
    if args.generate:
        scheme = ImageScheme(image_path=args.generate)
        split_name = args.generate.split('/').pop()
        scheme.generate_xres(args.location, split_name)
    elif args.select:
        select_scheme(location=args.location)
    elif args.dotshare:
        dotshare_grab(args.dotshare, args.location)
    elif args.reformat:
        read_from_file(args.reformat[0], args.reformat[1], args.location)
    elif args.generate_i3:
        gen_i3()
    elif args.current:
        print current_scheme()
    else:
        print_colors()

if (__name__ == '__main__'):
    main()
