import json
import os
import pprint

import requests
from bs4 import BeautifulSoup

URL = "https://ccsakura.fandom.com"

CARDS = [
    "Clow_Cards",
    "Clear_Cards",
]

def buildURL(path: str) -> str:
    return f"{URL}{path}"

def getNodeText(node):
    return node.get_text().strip().lower()

def cleanFieldName(fieldName):
    return fieldName \
        .replace("captured(anime)", "captured (anime)") \
        .replace("captured(manga)", "captured (manga)") \
        .replace("transformed(anime)", "transformed (anime)") \
        .replace("transformed(manga)", "transformed (manga)")

def cleanFieldData(fieldName: str, fieldData: str):
    if fieldName == "temperament":
        if fieldData == "*aggressive; destructive *docile (after capture)":
            return ["aggressive", "destructive", "docile (after capture)"]
        return [item.strip() for item in fieldData.split(";")]

    if fieldName == "sign":
        if fieldData == "sun and moon/star":
            return ["sun", "moon"]
        return [fieldData]

    if fieldName == "magic type":
        if fieldData == "eastern/western magic":
            return ["eastern magic", "western magic"]
        return [fieldData]

    return fieldData

def extractCardUrls(node) -> [str]:
    links = []

    for item in node.find("div", id="gallery-0"):
        for link in item.find_all("a", class_="link-internal"):
            links.append(buildURL(link.get('href')))

    return links

def extractInfoRowClow(row):
    tableCells = row.find_all("td")

    if len(tableCells) != 2:
        return (None, None)

    fieldName = getNodeText(tableCells[0])
    fieldData = getNodeText(tableCells[1])

    cleanName = cleanFieldName(fieldName)
    cleanData = cleanFieldData(cleanName, fieldData)

    return (cleanName, cleanData)

def extractInfoRowClear(row):
    rowNameNode = row.find("b")

    if rowNameNode is None:
        return (None, None)

    rowNameText = getNodeText(rowNameNode)

    if not rowNameText.endswith(":"):
        return (None, None)

    print(rowNameText)

    allRowText = getNodeText(row)
    fieldValue = allRowText.replace(rowNameText, "")

    return (
        rowNameText.rstrip(":"),
        fieldValue.strip(),
    )

def extractInfoRow(row, pageType: str):
    if pageType == "Clow_Cards":
        return extractInfoRowClow(row)

    if pageType == "Clear_Cards":
        return extractInfoRowClear(row)

    return (None, None)

def extractCardImageUrls(node):
    TRUE_FORMS = [
        "ccs ep21 - the loop.png",
        "windy spirit.jpg",
        "ccs ep04 - the wood card's main body.png",
        "120px-sweetclowcard.jpg",
    ]

    images = {}

    for imageNode in node.find_all("img"):
        imageName = imageNode.get('data-image-name').strip().lower()
        imageKey = None

        if "true form" in imageName or imageName in TRUE_FORMS:
            imageKey = "trueform"
        elif "clow" in imageName:
            imageKey = "clow"
        elif "sakura" in imageName:
            imageKey = "sakura"

        if imageKey is None:
            print(f"unknown image type: {imageName}")
        else:
            images[imageKey] = imageNode.parent.get('href')

    return images

def extractCardInfo(cardUrl: str, pageType: str):
    response = requests.get(cardUrl)
    pageNode = BeautifulSoup(response.text, "html.parser")
    infoBoxNode = pageNode.find("table", class_="infobox")

    titleNode = pageNode.find("h1", id="firstHeading")
    titleText = getNodeText(titleNode)

    result = {
        "name": titleText,
        "info": {},
        "images": extractCardImageUrls(infoBoxNode),
    }

    for rowNode in infoBoxNode.find_all("tr"):
        fieldName, fieldData = extractInfoRow(rowNode, pageType)

        if fieldName:
            result["info"][fieldName] = fieldData

    return result

def main():
    for name in CARDS:
        jsonPath = f'./assets/{name}.json'

        print(f"Fetching Cards: {name}")

        if os.path.exists(jsonPath):
            print("skipping existing json file")
            continue

        response = requests.get(buildURL(f"/wiki/{name}"))

        rootNode = BeautifulSoup(response.text, "html.parser")
        cardUrls = extractCardUrls(rootNode)

        allCardInfo = []

        for url in cardUrls:
            print(f"Fetching URL: {url}")
            allCardInfo.append(extractCardInfo(url, name))

        with open(jsonPath, mode="w") as jsonfile:
            json.dump(allCardInfo, jsonfile, ensure_ascii=False, indent=2)

        pprint.pp(allCardInfo)

if __name__ == "__main__":
    main()
