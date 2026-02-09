from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import base64
import time
import os

# --- CONFIGURATION ---
TARGET_LEVELS = ["3", "4", "5", "6", "7"] 
ADBLOCK_PATH = "adblock_for_firefox-6.33.6.xpi" # Ensure this file is in your folder

def save_first_page_as_pdf(driver, file_name):
    params = {
        "pageRanges": ["1"],
        "orientation": "portrait",
        "printBackground": True
    }
    # Direct execution to bypass version-specific PrintOptions
    pdf_data = driver.execute("printPage", {"options": params})['value']
    
    target_path = os.path.join(output_dir, file_name)
    with open(target_path, "wb") as f:
        f.write(base64.b64decode(pdf_data))

# Output directory setup
output_dir = os.path.abspath("character_pdfs")
os.makedirs(output_dir, exist_ok=True)

# --- FIREFOX SETUP ---
options = webdriver.FirefoxOptions()
options.add_argument("-headless") 
driver = webdriver.Firefox(options=options)

# Re-installing the Add-on
if os.path.exists(ADBLOCK_PATH):
    driver.install_addon(ADBLOCK_PATH, temporary=True)
    print("Adblocker installed.")
    time.sleep(5)
else:
    print(f"Warning: {ADBLOCK_PATH} not found. Proceeding without it.")

# Initial load to get class list
driver.get("https://fastcharacter.com/")
time.sleep(5)

class_select = Select(driver.find_element(By.NAME, "pcclass"))
raw_class_values = [
    opt.get_attribute("value")
    for opt in class_select.options
    if opt.get_attribute("value") not in ["0", "", "randphb"]
]

# Deduplication logic (First 4 chars, max 2 of each)
class_values = []
prefix_counts = {}
for val in raw_class_values:
    prefix = val[:4]
    if prefix not in prefix_counts:
        prefix_counts[prefix] = 0
    if prefix_counts[prefix] < 2:
        class_values.append(val)
        prefix_counts[prefix] += 1

print(f"Found {len(class_values)} classes to process per level.")

# --- NESTED LOOP FOR LEVELS ---
for level in TARGET_LEVELS:
    print(f"\n--- Starting Level {level} ---")
    
    for class_value in class_values:
        # Open new tab
        driver.execute_script("window.open('about:blank', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get("https://fastcharacter.com/")
        time.sleep(3) 

        # --- SHIELD: Remove blocking overlays via JS ---
        driver.execute_script("""
            var overlays = document.querySelectorAll('.fc-dialog-overlay, .fc-consent-root, .fc-dialog-container');
            for (var i = 0; i < overlays.length; i++) { overlays[i].remove(); }
            document.body.style.overflow = 'auto';
        """)

        # Set dropdowns
        Select(driver.find_element(By.NAME, "pclevel")).select_by_value(level)
        Select(driver.find_element(By.NAME, "pcbkgrd")).select_by_value("0")
        Select(driver.find_element(By.NAME, "pcrace")).select_by_value("0")
        Select(driver.find_element(By.NAME, "pointBuy")).select_by_value("15x14x13x12x10x8")
        Select(driver.find_element(By.NAME, "pcgender")).select_by_value("they")
        Select(driver.find_element(By.NAME, "pcclass")).select_by_value(class_value)

        # Checkboxes - using JS click to bypass "ElementClickIntercepted"
        for cid in ["pcrulescrib", "pcidealbondflaw"]:
            cb = driver.find_element(By.ID, cid)
            if not cb.is_selected():
                driver.execute_script("arguments[0].click();", cb)

        # Submit - using JS click for reliability
        submit_btn = driver.find_element(By.CSS_SELECTOR, "input.subbtn[type='submit']")
        driver.execute_script("arguments[0].click();", submit_btn)
        
        # Save PDF
        filename = f"{level}/character-lvl{level}-{class_value.replace(' ', '-')}.pdf"
        save_first_page_as_pdf(driver, filename)
        print(f"Saved: {filename}")

        # Memory Cleanup
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

print("\nTask complete.")
driver.quit()