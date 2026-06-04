import requests
import csv
from bs4 import BeautifulSoup


def get_cars_data(car: str) -> list[dict]:
    """Scrape car price data from PakWheels for a given brand."""

    url = f'https://www.pakwheels.com/new-cars/pricelist/{car}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/121.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # raises an error for 4xx/5xx responses
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

    cars = []
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')

    if not tables:
        print(f"No tables found for '{car}'.")
        return []

    for table in tables:
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) >= 2:
                name  = cols[0].get_text(strip=True)
                price = cols[1].get_text(strip=True)
                if name and price:          # skip empty rows
                    cars.append({'name': name, 'price': price})

    return cars


def scrapper(brands: list[str]) -> list[dict]:
    """Scrape car data for multiple brands and return combined results."""

    all_cars = []
    for brand in brands:
        print(f"Scraping: {brand}...")
        data = get_cars_data(brand)
        if data:
            all_cars.extend(data)
            print(f"  Found {len(data)} entries.")
        else:
            print(f"  No data found for '{brand}'.")

    return all_cars


def save_to_file(data: list[dict], filename: str) -> None:
    """Save scraped car data to a CSV file."""

    if not data:
        print("No data to save.")
        return

    if not filename.endswith('.csv'):
        filename += '.csv'

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'price'])
        writer.writeheader()
        writer.writerows(data)

    print(f"Data saved to '{filename}' ({len(data)} rows).")


# --- usage ---
if __name__ == '__main__':
    brands = ['toyota', 'honda', 'suzuki']
    cars   = scrapper(brands)
    save_to_file(cars, 'pakwheels_prices.csv')