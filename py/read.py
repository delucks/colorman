from color_common import reformat
import argparse
import getpass

# quick hack to make sure the path is formatted right
COLORS_DIR="/home/{user}/dotfiles/colors".format(user=getpass.getuser())

p = argparse.ArgumentParser(description="read in a file from the filesystem, reformat it and put it in the color dir")
p.add_argument("xres", help="the file you want to read in")
p.add_argument("name", help="what you want to name the color scheme")
p.add_argument("-l","--location",help="set alternate location for the downloaded/processed dot",default=COLORS_DIR)
args = p.parse_args()

with open(args.xres) as f:
  reformat(f.read(),args.location,args.name)
