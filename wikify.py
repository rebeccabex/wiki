from pathlib import Path


wikiRoot = Path("C:/Users/user/Documents/Other/Lit/Wikis")

# print(wikiRoot)
# wikiToUse = Path / "TME Wiki/Pages"
# fileToOpen = wikiToUse / "Helvina"

filepath = "C:/Users/user/Documents/Other/Lit/Wikis/TME Wiki/Pages/"

pageTitle = "Helvina"
pageTitle = "Eldanan Empire"

f = open(filepath + pageTitle + ".txt")

links =	{
  "The Millennium Empire_novel": "The Millennium Empire",
  "The Millennium Empire_novel": "The Millennium Empire",
  "Helvina": "Helvina",
  "Farida": "Farida",
  "Hegedar": "Hegedar",
  "Egafsir": "Egafsir",
  "Eldana": "Eldanan Empire"
}

def makeLink(tag):
	return "<a href=\"%s.html\">%s</a>" % (links.get(tag, tag), tag if tag.find("_") == -1 else tag[:tag.find("_")])

h = f.read()

def convertLinks(page):
	convertedPage = ""
	pageLines = page.split("\n")
	for line in pageLines:
		tagStart = 0
		convertedLine = ""
		lastMark = 0
		while tagStart != -1:
			tagStart = line.find("[", lastMark)
			tagEnd = line.find("]", tagStart)
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

g = open(filepath + pageTitle + ".html", "w")


g.write("<!DOCTYPE html>")
g.write("\n<html>")
g.write("\n<head>")
g.write("\n</head>")
g.write("\n<body>")
g.write("\n" + convertLinks(h))
g.write("\n</body>")
g.write("\n</html>")


