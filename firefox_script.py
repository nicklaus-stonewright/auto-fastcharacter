from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import base64
import time
import os


def save_first_two_pages_as_pdf(driver, file_path):
    # Ensure the page is fully loaded
    time.sleep(2)

    # Chrome DevTools printToPDF command
    pdf = driver.execute_cdp_cmd(
        "Page.printToPDF",
        {"landscape": False, "printBackground": True, "pageRanges": "1-2"},
    )

    # Write the base64-encoded PDF to a file
    with open(file_path, "wb") as f:
        f.write(base64.b64decode(pdf["data"]))


# Output directory for PDFs
output_dir = os.path.abspath("character_pdfs")
os.makedirs(output_dir, exist_ok=True)

# Set up Firefox
options = webdriver.FirefoxOptions()
options.add_argument("-devtools")  # Optional: open DevTools
driver = webdriver.Firefox(options=options)

driver.install_addon("adblock_for_firefox-6.20.0.xpi", temporary=True)
time.sleep(5)

# Load the site in the first tab to get the class options
driver.get("https://fastcharacter.com/")
time.sleep(5)

# Get all class <option> values except the unwanted ones
class_select = Select(driver.find_element(By.NAME, "pcclass"))
class_values = [
    opt.get_attribute("value")
    for opt in class_select.options
    if opt.get_attribute("value") not in ["0", "", "randphb"]
]

# Store the main/original tab for reference
main_tab = driver.current_window_handle

# Loop through each class and create a new tab for it
for class_value in class_values:
    # Open a new tab
    driver.execute_script("window.open('about:blank', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab
    driver.get("https://fastcharacter.com/")
    time.sleep(3)

    # Set character options
    level_number = "4"
    level_text = "lvl" + level_number

    Select(driver.find_element(By.NAME, "pclevel")).select_by_value(level_number)
    Select(driver.find_element(By.NAME, "pcbkgrd")).select_by_value("0")
    Select(driver.find_element(By.NAME, "pcrace")).select_by_value("0")
    Select(driver.find_element(By.NAME, "pointBuy")).select_by_value("15x14x13x12x10x8")
    Select(driver.find_element(By.NAME, "pcgender")).select_by_value("they")
    Select(driver.find_element(By.NAME, "pcclass")).select_by_value(class_value)

    # Checkboxes (optional rules)
    for cid in ["pcrulescrib", "pcidealbondflaw"]:
        checkbox = driver.find_element(By.ID, cid)
        if not checkbox.is_selected():
            checkbox.click()

    # Submit the form
    driver.find_element(By.CSS_SELECTOR, "input.subbtn[type='submit']").click()
    print(f"Generated character for class: {class_value}")
    save_first_two_pages_as_pdf(driver, f"character_{level_text}_{class_value}.pdf")


# All tabs now open with submitted characters
print("All class pages generated and open.")

# driver.quit()  # You can manually close after review, or uncomment to auto-close
