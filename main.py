#!/usr/bin/python

import function
import requests
import time
import config
from termcolor import colored
import optparse_mooi
import optparse
import validators
import progressbar
import json
from operator import is_not
from functools import partial
import logo


# url = "http://challenge01.root-me.org/web-serveur/ch18/"
# url = "http://challenge01.root-me.org/web-serveur/ch9/"
# url = "http://challenge01.root-me.org/web-serveur/ch19/"
# url = "http://challenge01.root-me.org/web-serveur/ch49/"
# url = "http://challenge01.root-me.org/web-serveur/ch34/"
# url = "http://challenge01.root-me.org/realiste/ch9/" # Web TV
# url = "http://challenge01.root-me.org/web-serveur/ch10/"
# url = "http://challenge01.root-me.org/web-serveur/ch31/" # File reading
# url = "http://styleshit.altervista.org/lvl1.php?id=1"
# url = "http://challenge01.root-me.org/web-serveur/ch40/" # Time base
# url = "http://challenge01.root-me.org/realiste/ch8/" # MALab SQL Blind *

# url = "http://challenge01.root-me.org/web-serveur/ch42/" # GBK *
# url = "http://challenge01.root-me.org/web-serveur/ch30/" # filter
# url = "http://challenge01.root-me.org/web-serveur/ch33/" # Insert *
# url = "http://challenge01.root-me.org/realiste/ch4/index.php"
# url = "http://challenge01.root-me.org/realiste/ch14/?p=news"
# url = "http://challenge01.root-me.org/realiste/ch1/" # False positive

# Define parser
examples_message = """\nExamples:
  scanqli.py -u 'http://127.0.0.1/test/?p=news' -o output.log\n  scanqli.py -u 'https://127.0.0.1/test/' -r -c '{"PHPSESSID":"4bn7uro8qq62ol4o667bejbqo3" , "Session":"Mzo6YWMwZGRmOWU2NWQ1N2I2YTU2YjI0NTMzODZjZDVkYjU="}'\n"""
logo_message = logo.chooselogo()

parser = optparse.OptionParser(description=logo_message, usage = "scanqli.py -u [url] [options]", epilog = examples_message, formatter=optparse_mooi.CompactHelpFormatter(align_long_opts=True, metavar_column=20))
groupscan = optparse.OptionGroup(parser, "Scanning")
groupoutput = optparse.OptionGroup(parser, "Output")

groupscan.add_option('-u', "--url", action="store", dest="url", help="URL to scan", default=None)
groupscan.add_option('-U', "--urllist", action="store", metavar="file", dest="urllist", help="URL list to scan (one line by url)", default=None)
groupscan.add_option('-i', "--ignore", action="append", metavar="url", dest="iurl", help="Ignore given URLs during scan", default=None)
groupscan.add_option('-I', "--ignorelist", action="store", metavar="file", dest="iurllist", help="Ignore given URLs list (one line by url)", default=None)
groupscan.add_option('-c', "--cookies", action="store", metavar="cookies", dest="cookies", help="Scan with given cookies", default=None, type=str)
groupscan.add_option('-q', "--quick", action="store_true", dest="quick", help="Check only very basic vulns", default=None)
groupscan.add_option('-r', "--recursive", action="store_true", dest="recursive", help="Recursive URL scan (will follow each href)", default=False)
groupoutput.add_option('-v', "--verbose", action="store_true", dest="verbose", help="Display all tested URLs", default=False)
groupoutput.add_option('-o', "--output", action="store", metavar="file", dest="output", help="Write outputs in file", default=None)
parser.add_option_group(groupscan)
parser.add_option_group(groupoutput)

options, args = parser.parse_args()

# Check requiered arg
if not options.url and not options.urllist:
    parser.print_help()
    exit(0)
elif options.url and validators.url(options.url):
    url = [options.url]
elif options.urllist:
    text_file = open(options.urllist, "r")
    url = text_file.read().split('\n')
    url = filter(partial(is_not, ""), url)
    for infile in url:
        if not validators.url(infile):
            # parser.print_help()
            function.PrintError("-u " + infile, "Malformed URL. Please given a valid URL")
            exit(0)
    # print(ur
    # exit(0)
else:
    function.PrintError("-u " + options.url, "Malformed URL. Please given a valid URL")
    exit(0)

# Check verbose args
function.verbose = options.verbose

# Check log file write perm
if options.output:
    if function.CheckFilePerm(options.output):
        progressbar.logfile = options.output
    else:
        function.PrintError("-o " + options.output, "No write permission for output file")
        exit(0)

# Check Banned URLs
if options.iurl:
    for bannedurl in options.iurl:
        if validators.url(bannedurl):
            config.BannedURLs.append(bannedurl)
        else:
            function.PrintError("-i " + bannedurl, "Malformed URL. Please given a valid URL")
            exit(0)

if options.iurllist:
    try:
        filelist = open(options.iurllist, "r")
        for iurl in filelist:
            if validators.url(iurl):
                config.BannedURLs.append(iurl.replace("\n", ""))
            else:
                function.PrintError("-I " + options.iurllist + " : " + iurl, "Malformed URL. Please given a valid URL")
                exit(0)
    except IOError:
        function.PrintError("-I " + options.iurllist, "Unable to read the given file")
        exit(0)

# Cookies
# function.cookies = {"PHPSESSID":"4bn7uro8qq62ol4o667bejbqo3" , "Session":"Mzo6YWMwZGRmOWU2NWQ1N2I2YTU2YjI0NTMzODZjZDVkYjU="}
if options.cookies:
    function.cookies = json.loads(options.cookies)

# Quick scan
if options.quick:
    config.scantype = "quick"

# init config
config.init()

# Start
starttime = time.time()

print(logo.chooselogo() + "\n")

if options.recursive:
    baseurl = []
    for uniturl in url:
        baseurl.append(uniturl)
        print("Base URL = " + uniturl)
    pageset = function.GetAllPages(baseurl)
    print(str(len(pageset)) + " URLs founds")
else:
    pageset = {None:None}
    for uniturl in url:
        print("URL = " + uniturl)
        pageset.update({uniturl:function.GetHTML(uniturl)})
    pageset.pop(None)

print("----------------------------")
function.vulnscanstrated = True
result = function.CheckPageListAllVulns(pageset)

print("----------------------------")
if len(result) <= 1:
    print(colored(str(len(result)) + " vulnerability ", attrs=["bold"])  + "found in " + str(round(time.time() - starttime, 2)) + " seconds!")
    # colored("[GET] ", "green", attrs=["bold"])
else:
    print(colored(str(len(result)) + " vulnerabilities ", attrs=["bold"])  + "founds in " + str(round(time.time() - starttime, 2)) + " seconds!")