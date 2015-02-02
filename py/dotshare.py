import argparse
import requests
import re

# grab a termcolors dot from dotshare.it, reformat and add to your colors dir
# usage: python2 dotshare.py {dotID}

p = argparse.ArgumentParser(description="grab a dot from http://dotshare.it/category/terms/colors/, put it in your colors dir")
p.add_argument("dot", help="the dotshare ID of the file you want. e.g. http://dotshare.it/dots/87/ would be 87")
p.add_argument("-l","--location",help="set alternate location for the downloaded/processed dot",default="/home/jamie/dotfiles/colors")
args = p.parse_args()

COLORS = "{dst}/{fn}.colors".format(dst=args.location,fn=args.dot)
XRESOURCES = "{dst}/{fn}.colorsX".format(dst=args.location,fn=args.dot) 
USER_AGENT = "https://github.com/delucks X colors manager"
headers = {'User-Agent': USER_AGENT} 
baseurl="http://dotshare.it/dots/{dotid}/0/raw".format(dotid=args.dot) 
RE_COLORS = re.compile(".*(color[0-9]{1,2})(?:[\t\ ]*):(?:[\t\ ]*)(?:\[[0-9]{1,3}\])?(#[a-zA-Z0-9]{3,6})",re.IGNORECASE)
BG_COLORS = re.compile(".*(foreground|background)(?:[\t\ ]*):(?:[\t\ ]*)(?:\[[0-9]{1,3}\])?(#[a-zA-Z0-9]{3,6})",re.IGNORECASE) 
colors = {}
xres = ''
cols = ''

r = requests.get(baseurl,headers=headers)

# read line by line and attempt to match the colors
for line in re.finditer('.*?\n',r.text):
    l = line.group(0).strip()
    if len(l) is 0:
      continue
    if l[0] not in '!':
      m = RE_COLORS.match(l)
      if m is not None:
        colors[m.group(1)] = m.group(2)
      else:
        b = BG_COLORS.match(l)
        if b is not None:
          colors[b.group(1)] = b.group(2)

for item in sorted(colors.keys()):
  xres += "*{color}: {hexval}\n".format(color=item,hexval=colors[item])
  cols += "export {color}=\"{hexval}\"\n".format(color=item.upper(),hexval=colors[item])

with open(XRESOURCES, 'w+') as f:
  f.write(xres)
with open(COLORS, 'w+') as f:
  f.write(cols)
