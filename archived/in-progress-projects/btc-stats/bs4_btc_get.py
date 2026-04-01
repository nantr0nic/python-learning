from bs4 import BeautifulSoup
import requests

# URL for bitcoin price
url = "https://www.google.com/search?q=bitcoin+price"

# Add headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Make a request to the webpage
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    # Find the span element with the class "pclqee" <-- BTC price
    price_element = soup.find("span", class_="pclqee")

    if price_element:
        price_text = price_element.text.strip()
        print(f"The current price is: {price_text}")

    else:
        print("The web element was not found.")
else:
    print("Failed to retrieve the webpage.")
