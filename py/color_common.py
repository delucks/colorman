import re

def reformat(text,location,name):
  colors = {}
  COLORS = "{dst}/{fn}.colors".format(dst=location,fn=name)
  XRESOURCES = "{dst}/{fn}.colorsX".format(dst=location,fn=name) 
  xres = ''
  cols = ''
  RE_COLORS = re.compile(".*(color[0-9]{1,2})(?:[\t\ ]*):(?:[\t\ ]*)(?:\[[0-9]{1,3}\])?(#[a-zA-Z0-9]{3,6})",re.IGNORECASE)
  BG_COLORS = re.compile(".*(foreground|background)(?:[\t\ ]*):(?:[\t\ ]*)(?:\[[0-9]{1,3}\])?(#[a-zA-Z0-9]{3,6})",re.IGNORECASE) 
  # read line by line and attempt to match the colors
  for line in re.finditer('.*?\n',text):
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
