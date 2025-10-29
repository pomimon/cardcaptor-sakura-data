import json
from pony.orm import set_sql_debug
from pony.orm import Database
from pony.orm import Optional
from pony.orm import Required
from pony.orm import db_session
from pony.orm import commit
from pony.orm import Set

SRC_PATH = "./assets/Clow_Cards.json"
DST_PATH = "./cards.sqlite"

db = Database()

# prints out sql statements as they are executed
set_sql_debug(True)

class Card(db.Entity):
  Images = Set("Image")
  Signs = Set("Sign")
  MagicTypes = Set("MagicType")
  Temperaments = Set("Temperament")

  Name = Required(str, unique=True)
  Kanji = Optional(str)
  Katakana = Optional(str)
  Captured_Anime = Optional(str)
  Captured_Manga = Optional(str)
  Transformed_Anime = Optional(str)
  Transformed_Manga = Optional(str)
  Hierarchy = Optional(str)

class Image(db.Entity):
  card = Required(Card)
  type = Required(str)
  url = Required(str)

class Sign(db.Entity):
  card = Required(Card)
  name = Required(str)

class MagicType(db.Entity):
  card = Required(Card)
  name = Required(str)

class Temperament(db.Entity):
  card = Required(Card)
  name = Required(str)

# setting up connection to database
db.bind(provider='sqlite', filename=DST_PATH, create_db=True)
db.generate_mapping(check_tables=False, create_tables=True)
db.drop_all_tables(with_all_data=True)
db.create_tables()

@db_session
def main():
    with open(SRC_PATH) as jsonfile:
        cards = json.load(jsonfile)

    for card in cards:
      entity = Card(
        Name=card["name"],
        Kanji=card["info"].get("kanji", ""),
        Katakana=card["info"].get("katakana", ""),
        Captured_Anime=card["info"].get("captured (anime)", ""),
        Captured_Manga=card["info"].get("captured (manga)", ""),
        Transformed_Anime=card["info"].get("transformed (anime)", ""),
        Transformed_Manga=card["info"].get("transformed (manga)", ""),
        Hierarchy=card["info"].get("hierarchy", ""),
      )

      for type, url in card["images"].items():
        Image(card=entity, type=type, url=url)

      for sign in card["info"].get("sign", []):
        Sign(card=entity, name=sign)

      for sign in card["info"].get("magic type", []):
        MagicType(card=entity, name=sign)

      for sign in card["info"].get("temperament", []):
        Temperament(card=entity, name=sign)

    commit()

    print(db)

if __name__ == "__main__":
    main()
