import json
import requests
import os

def main():
    with open('./assets/Clow_Cards.json') as jsonfile:
        cards = json.load(jsonfile)

    for card in cards:
        cardName = card["name"]
        cardPath = f'./assets/images/{cardName}.png'

        print(f"Fetching Image for {cardName}")

        if os.path.exists(cardPath):
            continue

        getCard = requests.get(card['images']["clow"])

        with open(cardPath, mode="wb") as f:
            f.write(getCard.content)

if __name__ == "__main__":
    main()
