# EstateParser

📊 **EstateParser** – A Python-based web scraper that extracts apartment listings and detailed property information from [MyHome.ge](https://www.myhome.ge), [Korter.ge](https://korter.ge), and [home.ss.ge](https://home.ss.ge). This script uses **CloudScraper**, **Requests**, and **JSON parsing** to collect data and present it in a formatted text output.

⚠️ **This project is for educational purposes only.**  
🚫 **Commercial use is strictly prohibited.**

## Features 🚀
- **Extracts apartment details** (address, price, area, rooms, amenities, etc.)
- **Supports three Georgian real estate platforms** (MyHome.ge, Korter.ge, home.ss.ge)
- **Bypasses Cloudflare protection** with CloudScraper
- **User-friendly formatted output** with emojis for readability
- **Handles JSON extraction** from complex HTML structures
- **Error handling** for robust operation

## Installation 🛠️

### Prerequisites:
- Python 3.x

### Download the Project:
Clone the repository using:
```sh
git clone https://github.com/adleyba/EstateParser.git
```

### Install required dependencies:
```sh
pip install -r requirements.txt
```

### Requirements File (`requirements.txt`):
```
requests
cloudscraper
```

## Usage 📖
Run the script with:
```sh
python EstateParser.py
```

The script will prompt you to enter a URL from one of the supported websites (MyHome.ge, Korter.ge, or home.ss.ge). It will then process the listing and display the extracted data.

### Example Run:
```
Please enter your URL from MyHome.ge, Korter.ge, or home.ss.ge:
https://www.myhome.ge/en/pr/12345678
```

The script will output formatted property details like:
```
🏠 Apartment for Sale in Batumi  
📍 Address: 26 May Street  
🏢 Property Type: Apartment (Studio)  
🏷 Condition: Newly renovated  
📏 Area: 45 m²  
...
```

## How It Works 🔍
1. **Accepts a URL** from the user for a specific listing.
2. **Detects the website** based on the URL domain.
3. **Fetches the page content** using Requests or CloudScraper (for Cloudflare-protected sites).
4. **Extracts JSON data** embedded in the HTML using string splitting and regex.
5. **Parses the JSON** and formats the property details into a readable output.
6. **Handles errors gracefully**, informing the user of any issues.

## Technologies Used 🛠️
- **[Requests](https://requests.readthedocs.io/en/latest/)** – For making HTTP requests
- **[CloudScraper](https://pypi.org/project/cloudscraper/)** – To bypass Cloudflare protection
- **[JSON](https://docs.python.org/3/library/json.html)** – For parsing extracted data
- **[Regular Expressions (re)](https://docs.python.org/3/library/re.html)** – For precise JSON extraction

## Disclaimer ⚠️
This project is intended for **educational and research purposes only**. **Scraping websites without permission may violate their terms of service.** Please ensure compliance with the terms of [MyHome.ge](https://www.myhome.ge/), [Korter.ge](https://korter.ge/), and [home.ss.ge](https://home.ss.ge/) before using this script.

## License 📜
**Apache License 2.0**

---
Made with ❤️ for educational purposes.
---
