import json
import os


def formatList(value: list[str]) -> str:
    return " 🥚 ".join(value)

def main():
    cardHtml = ""

    with open('./assets/template.html') as html:
        pageTemplate = html.read()

    with open('./assets/Clow_Cards.json') as jsonfile:
        cards = json.load(jsonfile)

    for card in cards:
        cardInfo = card["info"]

        cardSign = formatList(cardInfo["sign"])
        cardTemperament = formatList(cardInfo.get("temperament", ["n/a"]))
        cardMagicType = formatList(cardInfo.get("magic type", ["n/a"]))

        print(cardMagicType)

        cardHtml += f"""
        <div class="card">
           <div class="card-inner">
                <div class="card-front">
                    <img src="./assets/images/{card["name"]}.png"/>
                </div>
                <div class="card-back">
                    <div>{card["name"]}</div>
                    <div>{cardSign}</div>
                    <div>{card["info"]["hierarchy"]}</div>
                    <div>{cardTemperament}</div>
                    <div>{cardMagicType}</div>
                    <div>{card["info"]["captured (anime)"]}</div>
                    <div>{card["info"]["transformed (anime)"]}</div>
                </div>
            </div>
        </div>
        """

    pageHtml = pageTemplate.replace("{{content}}", cardHtml)

    with open("index.html", mode="w") as f:
        f.write(pageHtml)

if __name__ == "__main__":
    main()
