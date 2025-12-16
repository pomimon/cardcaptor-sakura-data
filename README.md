# Card Captor Sakura Data

A data scraping and frontend display project that collects Card Captor Sakura card images and metadata from Fandom and presents them in a clean, readable web interface.

Built as a learning project to practice web scraping, data normalization, and translating structured data into a simple, user-friendly frontend.

---

## Features

- Scrapes card images, names, and descriptions from Fandom
- Normalizes scraped data and stores it in a SQL database
- Displays card data in a static HTML/CSS interface
- Image-forward layout designed for browsing visual datasets
- Consistent formatting across all card entries

---

## Tech Stack

### Frontend

- **HTML**
- **CSS**

### Data & Backend Support

- **Python**
- **BeautifulSoup**
- **SQL**
- **PonyORM**

---

## Limitations & Future Improvements

This project intentionally remains simple. Possible future improvements include:

- Client-side filtering or search functionality
- Pagination or lazy loading for large datasets
- Migration to a dynamic frontend framework (e.g. React) for richer interactions

---

## Running Locally

```bash
git clone https://github.com/pomimon/cardcaptor-sakura-data.git
cd cardcaptor-sakura-data
pip install -r requirements.txt
python scrape.py
```
