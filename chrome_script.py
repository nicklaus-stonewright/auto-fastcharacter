from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import base64
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def save_first_two_pages_as_pdf(driver, file_path):
    # Wait for the page to be fully loaded
    time.sleep(2)

    # Use Chrome DevTools Protocol to print to PDF
    pdf = driver.execute_cdp_cmd(
        "Page.printToPDF",
        {"landscape": False, "printBackground": True, "pageRanges": "1-2"},
    )

    # Save the PDF to file
    with open(file_path, "wb") as f:
        f.write(base64.b64decode(pdf["data"]))


level_number = "3"
level_text = "lvl" + level_number
output_dir = os.path.abspath(f"character_pdfs\{level_text}")
os.makedirs(output_dir, exist_ok=True)

# Set up Chrome in headless mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension("adblock_for_chrome-6.20.1_0.crx")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=chrome_options)

# Load the site in the first tab to get the class options
driver.get("https://fastcharacter.com/")
time.sleep(3)

# Wait for and click the "Consent" button if it appears
try:
    consent_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-button.fc-cta-consent"))
    )
    consent_button.click()
    print("Clicked consent button.")
except:
    print("Consent button not found or already accepted.")

# Get all class <option> values except the unwanted ones
class_select = Select(driver.find_element(By.NAME, "pcclass"))
class_values = [
    opt.get_attribute("value")
    for opt in class_select.options
    if opt.get_attribute("value") not in ["0", "", "randphb"]
]

# Store the main tab
main_tab = driver.current_window_handle

# Loop through each class and create new characters
for class_value in class_values:
    driver.execute_script("window.open('about:blank', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get("https://fastcharacter.com/")
    time.sleep(3)

    Select(driver.find_element(By.NAME, "pclevel")).select_by_value(level_number)
    Select(driver.find_element(By.NAME, "pcbkgrd")).select_by_value("0")
    Select(driver.find_element(By.NAME, "pcrace")).select_by_value("0")
    Select(driver.find_element(By.NAME, "pointBuy")).select_by_value("15x14x13x12x10x8")
    Select(driver.find_element(By.NAME, "pcgender")).select_by_value("they")
    Select(driver.find_element(By.NAME, "pcclass")).select_by_value(class_value)

    # Optional checkboxes
    for cid in ["pcrulescrib", "pcidealbondflaw"]:
        checkbox = driver.find_element(By.ID, cid)
        if not checkbox.is_selected():
            checkbox.click()

    # Submit
    driver.find_element(By.CSS_SELECTOR, "input.subbtn[type='submit']").click()
    print(f"Generated character for class: {class_value}")

    # Save PDF
    save_first_two_pages_as_pdf(
        driver, os.path.join(output_dir, f"character_{level_text}_{class_value}.pdf")
    )

    driver.close()
    driver.switch_to.window(main_tab)

print("All class pages generated and saved as PDFs.")
