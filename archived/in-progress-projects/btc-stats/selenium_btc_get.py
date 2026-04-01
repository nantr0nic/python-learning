from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")

# URL for bitcoin price
url = "https://www.google.com/search?q=bitcoin+price"

# Initialize the Chrome driver
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

try:
    # Wait for the price element to be visible
    price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "pclqee"))
    )
    price = price_element.text
    print(f"Bitcoin price: {price}")
except Exception as e:
    # Handle any exceptions
    print(f"Error: {e}")

# Close the browser
driver.quit()



