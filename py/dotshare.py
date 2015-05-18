import urllib2
import getpass
from color_common import reformat

# grab a termcolors dot from dotshare.it, reformat and add to your colors dir
# usage: python2 dotshare.py {dotID}

def dotgrab(dot_id, location):
    USER_AGENT = "https://github.com/delucks X colors manager"
    headers = {'User-Agent': USER_AGENT} 
    baseurl="http://dotshare.it/dots/{dotid}/0/raw".format(dotid=dot_id) 
    r = urllib2.Request(baseurl, None, headers)
    reformat(urllib2.urlopen(r).read(),location,dot_id)

if (__name__ == '__main__'):
    import argparse
    p = argparse.ArgumentParser(description="grab a dot from http://dotshare.it/category/terms/colors/, put it in your colors dir")
    p.add_argument("dot", help="the dotshare ID of the file you want. e.g. http://dotshare.it/dots/87/ would be 87")
    p.add_argument("-l","--location",help="set alternate location for the downloaded/processed dot",default=COLORS_DIR)
    args = p.parse_args()
    dotgrab(args.dot, args.location)
