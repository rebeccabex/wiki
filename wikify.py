from pathlib import Path
import json
import os

filepath = os.getcwd()

links = {
  "The Millennium Empire_novel": "The Millennium Empire",
  "The Millennium Empire_place": "Eldanan Empire",
  "Helvina": "Helvina",
  "Farida": "Farida",
  "Hegedar": "Hegedar",
  "Egafsir": "Egafsir",
  "Eldana": "Eldanan Empire"
}

def makeLink(tag):
    return "<a href=\"%s.html\">%s</a>" % (links.get(tag, tag), tag if tag.find("_") == -1 else tag[:tag.find("_")])

def convertLinks(page):
    convertedPage = ""
    pageLines = page.split("\n")
    for line in pageLines:
        tagStart = 0
        convertedLine = ""
        lastMark = 0
        while tagStart != -1:
            tagStart = line.find("<", lastMark)
            tagEnd = line.find(">", tagStart)
            if tagStart == -1:
                if lastMark == 0:
                    convertedLine = line
                else:
                    convertedLine = convertedLine + line[lastMark+1:]
            else:
                if lastMark == 0:
                    convertedLine = convertedLine + line[:tagStart] + makeLink(line[tagStart+1:tagEnd])
                else:
                    convertedLine = convertedLine + line[lastMark+1:tagStart] + makeLink(line[tagStart+1:tagEnd])
            lastMark = tagEnd
        convertedPage = convertedPage + convertedLine + "\n"
    return convertedPage

def splitPage(page):
    return page.split("########")

def parseHeader(header):
    headerData = {}
    headerLines = header.split("\n")
    for line in headerLines:
        if (line.find("=") != -1):
            parameterAndValue = line.split("=")
            parameter = parameterAndValue[0]
            value = parameterAndValue[1]
            if (value.find("[") != -1):
                valueList = value[1:-1].split(",")
            if parameter == "Title":
                headerData["Title"] = value
            elif parameter == "Tags":
                headerData["Tags"] = valueList
            elif parameter == "Categories":
                headerData["Categories"] = valueList
    return headerData

def parseBody(body):
    return convertLinks(body)

def parsePage(page):
    htmlFile = "<!DOCTYPE html>\n<html>\n<head>\n<title>"
    headerBody = splitPage(page)
    header = headerBody[0]
    body = headerBody[1]
    headerData = parseHeader(header)
    htmlFile += headerData.get("Title", "")
    htmlFile += "</title>\n</head>\n<body>\n"
    htmlFile += parseBody(body)
    htmlFile += "\n</body>\n</html>"
    return htmlFile

pageTitles = [
    "Helvina",
    "Eldanan Empire"
]

def getLinks(filename):
    with open(filename, "r") as linksPage:
        return json.load(linksPage)

def writeLinks(linksDict, filename):
    with open(filename, "w") as linksPage:
        json.dump(linksDict, linksPage, indent=4, sort_keys=True)

if __name__ == "__main__":
    linksDict = getLinks(filepath + "/links.json")

    for pageTitle in pageTitles:
        f = open(filepath + "/" + pageTitle + ".txt")

        textPage = f.read()

        wikiPage = open(filepath + "/" + pageTitle + ".html", "w")
        htmlPage = parsePage(textPage)
        wikiPage.write(htmlPage)
        wikiPage.close()

    writeLinks(linksDict, filepath + "/links.json")

