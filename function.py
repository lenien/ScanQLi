import requests
from BeautifulSoup import BeautifulSoup
import config
import time
import urlparse
import progressbar
from termcolor import colored

reponsetime = None
currenttested = None
cookies = None
verbose = False
vulnscanstrated = False

def GetHref(html):
    soup = BeautifulSoup(html)
    hreflist = []
    for link in soup.findAll('a'):
        href = link.get('href')
        if href:
            hreflist.append(href)
    return set(hreflist)

def GetCurrentDir(url):
    urllen = len(url)
    for i in range(1, urllen):
        if "/" in url[-i:]:
            return url[:urllen - i + 1]
        elif "." in url[-i:]:
            while "/" not in url[-i:]:
                i += 1
            return url[:urllen - i + 1]
    return False

def CraftURL(url, href):
    href = href.replace("./", "")
    urlsplited = urlparse.urlsplit(url)
    if href[:1] == "/":
        return urlsplited.scheme + "://" + urlsplited.netloc + href
    else:
        return GetCurrentDir(urlsplited.scheme + "://" + urlsplited.netloc + urlsplited.path) + href

def GetLinks(url, html):
    hrefset = GetHref(html)
    links = []
    urlsplited = urlparse.urlsplit(url)
    baseurl = urlsplited.scheme + "://" + urlsplited.netloc
    for href in hrefset:
        if href[:7] != "http://" and href[:8] != "https://":
            links.append(CraftURL(url, href))
        elif href[:len(baseurl)] == baseurl:
            links.append(href)
    # print(links)
    return set(links)

def CheckBlackListURLs(url):
    for ban in config.BannedURLs:
        if ban in url or ban == url:
            return True
    return False

def GetHTML(url):
    global reponsetime
    global cookies
    global verbose
    global vulnscanstrated
    
    try:
        if not CheckBlackListURLs(url):
            if verbose and vulnscanstrated:
                bar.printabove("[GET] " + url)
            starttime = time.time()
            # print(cookies)
            r = requests.get(url, cookies=cookies)
            endtime = time.time()
            if reponsetime and (reponsetime * 3 > endtime - starttime):
                reponsetime = (reponsetime + (endtime - starttime)) / 2    
            elif reponsetime == None:
                reponsetime = endtime - starttime
        else:
            return ""
    except requests.ConnectionError as error:
        print(error)
        exit()
    return r.text

def PostData(url, data):
    global reponsetime
    global cookies
    global verbose
    global vulnscanstrated
    
    if url not in config.BannedURLs:
        if verbose and vulnscanstrated:
                bar.printabove("[POST] " + url + " [PARAM] " + str(data))
        starttime = time.time()
        r = requests.post(url, data=data, cookies=cookies)
        endtime = time.time()

        if reponsetime and ((reponsetime * 2) > (endtime - starttime)):
            reponsetime = (reponsetime + (endtime - starttime)) / 2    
        elif reponsetime == None:
            reponsetime = endtime - starttime
        return r.text
    else:
        return ""

def GetParams(url):
    result = []
    i = 1
    buffer = 0
    while "?" not in url[:-buffer + 1][-i:] and "/" not in url[-i:]:
        if buffer == 0 and "&" in url[-i:]:
            result.append(url[-i + 1:])
            buffer += i + 1
            i = 1
        elif "&" in url[:-buffer][-i:]:
            result.append(url[:-buffer + 1][-i:])
            buffer += i + 1
            i = 0
        elif "?" in url[:-buffer][-i:]:
            result.append(url[:-buffer + 1][-i:])
            break
        i += 1
    result.reverse()
    return result

def ConcatURLParams(url, params):
    result = {url}
    buffer = url + "?"
    firstloop = True
    for param in params:
        if firstloop:
            buffer += param
            firstloop = False
        else:
            buffer += "&" + param
        result.add(buffer)
    return result

def GetAllURLsParams(url):
    urlparsed = urlparse.urlparse(url)
    base = urlparsed.scheme + "://" + urlparsed.netloc + urlparsed.path
    return ConcatURLParams(base, GetParams(url))

def GetAllPages(urllist):

    # print(urllist)

    links = {None:None}
    templinks = {None}
    linksfollowed = {None}
    newlinks = {None}

    for url in urllist:
        # print(url)
        html = GetHTML(url)
        links.update({url:html})
        templinks.update(GetLinks(url, html))
        templinks.update(GetAllURLsParams(url))
        linksfollowed.update(url)
        newlinks.update(url)

    links.pop(None)
    templinks.remove(None)
    linksfollowed.remove(None)
    newlinks.remove(None)

    bar = progressbar.progressbar("count", "Get URLs")
    while templinks:
        bar.progress(len(templinks))
        for link in templinks:
            html = GetHTML(link)
            links.update({link:html})
            newlinks.update(GetLinks(link, html))
            newlinks.update(GetAllURLsParams(link))
            linksfollowed.update({link})
        templinks = newlinks.difference(linksfollowed)
    bar.delbar()

    result = {}
    for link in links:
        if not CheckBlackListURLs(link):
            result.update({link:links[link]})

    return result


# def GetAllPages(url):
#     html = GetHTML(url)
#     links = {url:html}
#     templinks = GetLinks(url, html)
#     templinks.update(GetAllURLsParams(url))
#     print(templinks)
#     exit(0)
#     linksfollowed = {url}
#     newlinks = {url}
#     bar = progressbar.progressbar("count", "Get URLs")
#     while templinks:
#         bar.progress(len(templinks))
#         for link in templinks:
#             html = GetHTML(link)
#             links.update({link:html})
#             newlinks.update(GetLinks(link, html))
#             newlinks.update(GetAllURLsParams(link))
#             linksfollowed.update({link})
#         templinks = newlinks.difference(linksfollowed)
#     bar.delbar()

#     result = {}
#     for link in links:
#         if not CheckBlackListURLs(link):
#             result.update({link:links[link]})

#     return result

def CheckValidProof(html):
    validproof = []
    for ivulnproof in config.vulnproof:
        if ivulnproof not in html:
            validproof.append(ivulnproof)
    return set(validproof)

def CheckGetBlind(url, blindlist, html):
    blindtrue = GetHTML(url + blindlist[0])
    blindfalse = GetHTML(url + blindlist[1])

    if (blindtrue == html) and (blindtrue != blindfalse):
        bar.printabove(colored("[GET] ", "yellow", attrs=["bold"]) + colored(url, "yellow") + colored(blindlist[1], "red", attrs=["bold"]))
        return url + blindlist[1]
    else:
        return False

def CheckGetVuln(url, vuln, html):
    global currenttested
    global reponsetime
    
    if currenttested == "blind":
        return CheckGetBlind(url, vuln, html)
    
    validproof = CheckValidProof(html)
    payloadedurl = url + vuln
    
    while True:
        starttime = time.time()
        page = GetHTML(payloadedurl)
        endtime = time.time()
        if (currenttested != "timebase") or (reponsetime * 3 + 2 > endtime - starttime):
            break

    for ivalidproof in validproof:
        if (ivalidproof in page) or (currenttested == "timebase" and (endtime - starttime) >= (reponsetime + 2)):
            bar.printabove(colored("[GET] ", "green", attrs=["bold"]) + colored(url, "green") + colored(vuln, "red", attrs=["bold"]))
            return payloadedurl
    return False

def CheckPostBlind(url, blindlist, fields, html):
    # blindtrue = GetHTML(url + blindlist[0])
    # blindfalse = GetHTML(url + blindlist[1])

    datatrue = {}
    datafalse = {}
    
    for field in fields:
        datatrue.update({field:blindlist[0]})
    for field in fields:
        datafalse.update({field:blindlist[1]})

    blindtrue = PostData(url, datatrue)
    blindfalse = PostData(url, datafalse)

    if (blindtrue == html) and (blindtrue != blindfalse):
        printpayload = colored("{", "yellow")
        icomma = 1
        for field in fields:
            printpayload = printpayload + colored(field + ":", "yellow") + colored(blindlist[1], "red", attrs=["bold"])
            if icomma != len(fields):
                printpayload = printpayload + colored(", ", "yellow")
            icomma += 1
        printpayload = printpayload + colored("}", "yellow")
        bar.printabove(colored("[POST] ", "yellow", attrs=["bold"]) + colored(url, "yellow") + colored(" [PARAM] ", "yellow", attrs=["bold"]) + printpayload)
        return [url, blindfalse]
    else:
        return False

def CheckPostVuln(url, vuln, fields, html):
    global currenttested
    global reponsetime

    if currenttested == "blind":
        return CheckPostBlind(url, vuln, fields, html)

    validproof = CheckValidProof(url)
    payloadeddata = {}
    
    for field in fields:
        payloadeddata.update({field:vuln})
    
    while True:
        starttime = time.time()
        page = PostData(url, payloadeddata)
        endtime = time.time()
        if (currenttested != "timebase") or (reponsetime * 3 + 2 > endtime - starttime):
            break
    
    for ivalidproof in validproof:
        if (ivalidproof in page) or (currenttested == "timebase" and (endtime - starttime) >= (reponsetime + 2)):
            printpayload = colored("{", "green")
            icomma = 1
            for field in fields:
                printpayload = printpayload + colored(field + ":", "green") + colored(vuln, "red", attrs=["bold"])
                if icomma != len(fields):
                    printpayload = printpayload + colored(", ", "green")
                icomma += 1
            printpayload = printpayload + colored("}", "green")
            bar.printabove(colored("[POST] ", "green", attrs=["bold"]) + colored(url, "green") + colored(" [PARAM] ", "green", attrs=["bold"]) + printpayload)
            return [url, payloadeddata]
    
    return False

def CheckURLQuery(url):
    urlsplited = urlparse.urlsplit(url)
    if urlsplited.query:
        return True
    else:
        return False

def CheckPageVuln(url, vuln, html = None):
    # print(url)
    if html:
        fields = {}
        soup = BeautifulSoup(html)
        for link in soup.findAll('input'):
            field = link.get('name')
            if field:
                fields.update({field:"0"})
        if fields:
            postresult = CheckPostVuln(url, vuln, fields, html)
            if postresult:
                return postresult
    if CheckURLQuery(url):
        return CheckGetVuln(url, vuln, html)

def CheckPageListVuln(pageset, vuln):
    result = []
    for url in pageset:
        payload = CheckPageVuln(url, vuln, pageset[url])
        if payload:
            result.append(payload)
    return result

def CheckPageListAllVulns(pageset):
    result = []
    checkbreak = False

    global bar
    global currenttested

    bar = progressbar.progressbar("bar", "Search vulns")
    bar.totalcount = len(config.vulncheck)
    bar.count = 0

    for vulnlist in config.vulncheck:
        if checkbreak:
            break
        bar.total = len(vulnlist[0])
        bar.value = 0
        bar.count += 1
        currenttested = vulnlist[1]
        for vuln in vulnlist[0]:
            # bar.printabove("total = " + str(bar.total))
            # bar.printabove("value = " + str(bar.value))
            bar.progress(1)
            payload = CheckPageListVuln(pageset, vuln)
            if payload:
                result.append(payload)
                checkbreak = True
                break
        # bar.delbar()
        # print("")
    
    bar.delbar()
    return payload

def CheckFilePerm(filename):
    try:
        output = open(filename,"a+")
        output.close()
    except:
        return 0
    return 1

def PrintError(command, errormsg):
    print(colored("ERROR: ", "red", attrs=["bold"]) + colored(command, attrs=["bold"]) + " : " + errormsg)

# print(PostData("http://challenge01.root-me.org/web-serveur/ch9/", {"login":" '", "password":" '"}))
# print(CheckURLQuery("http://challenge01.root-me.org/web-serveur/ch9/?action=news&news_id=2"))
# print(CheckPageVuln("http://challenge01.root-me.org/web-serveur/ch18/?action=news&news_id=2", "'"))