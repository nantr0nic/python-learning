import requests  # Helps track web requests
from bs4 import BeautifulSoup  # Helps scrape / find / etc. html/xml/etc. things

# win10toast didn't work last time I tried...
from win10toast import ToastNotifier  # Makes windows notifications

# weather for Portland, OR
url = "https://forecast.weather.gov/MapClick.php?lat=45.5118&lon=-122.6756"

# Make a request to the webpage
response = requests.get(url)

# ToastNotifier object...
toaster = ToastNotifier()

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the div with the class "myforecast-current-lrg"
    temp_div = soup.find("p", class_="myforecast-current-lrg")

    if temp_div:
        # Extract and print the text content of the div
        temperature_text = temp_div.text.strip()
        print(f"The current temperature is: {temperature_text}")
        # This creates the Winblow$ notification
        toaster.show_toast(
            "Weather", f"Current temperature is: " + temperature_text, duration=5
        )
    else:
        print("Div with specified class not found.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
