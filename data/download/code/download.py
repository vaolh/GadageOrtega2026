#!/usr/bin/env python3
"""
Bolivia INE - Encuesta de Hogares Selenium Downloader
Downloads Encuesta de Hogares data from 2005-2018
"""

import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Survey data - mapping years to their dropdown values and expected filenames
SURVEYS = {
    2018: {"value": "45;43", "name": "Encuesta de Hogares 2018"},
    2017: {"value": "43;41", "name": "Encuesta de Hogares 2017"},
    2016: {"value": "41;39", "name": "Encuesta de Hogares 2016"},
    2015: {"value": "35;35", "name": "Encuesta de Hogares 2015"},
    2014: {"value": "34;34", "name": "Encuesta de Hogares 2014 (Factor de Expansión 2014)"},
    2013: {"value": "33;33", "name": "Encuesta de Hogares 2013 (Factor de Expansión 2014)"},
    2012: {"value": "32;32", "name": "Encuesta de Hogares 2012 (Factor de Expansión 2014)"},
    2011: {"value": "31;31", "name": "Encuesta de Hogares 2011 (Factor de Expansión 2014)"},
    2009: {"value": "24;24", "name": "Encuesta de Hogares 2009 (Factor de Expansión 2001)"},
    2008: {"value": "23;23", "name": "Encuesta de Hogares 2008 (Factor de Expansión 2001)"},
    2007: {"value": "26;26", "name": "Encuesta de Hogares 2007 (Factor de Expansión 2001)"},
    2006: {"value": "25;25", "name": "Encuesta de Hogares 2006 (Factor de Expansión 2001)"},
    2005: {"value": "22;22", "name": "Encuesta de Hogares 2005 (Factor de Expansión 2001)"},
}

BASE_URL = "https://www.ine.gob.bo/index.php/censos-y-banco-de-datos/censos/bases-de-datos-encuestas-sociales/"

def setup_driver(download_dir):
    """Setup headless Chrome driver with download preferences"""
    chrome_options = Options()
    
    # Headless mode
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Download preferences
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def wait_for_download(download_dir, timeout=600):
    """Wait for download to complete (max 10 min)"""
    seconds = 0
    while seconds < timeout:
        time.sleep(1)
        files = list(Path(download_dir).glob("*"))
        if files:
            if not any(str(f).endswith(('.crdownload', '.tmp')) for f in files):
                return True
        seconds += 1
    return False

def download_survey(driver, year, survey_data, download_dir):
    """Download a specific survey year"""
    print(f"\n{'='*60}")
    print(f"Downloading: {survey_data['name']}")
    print(f"{'='*60}")
    
    try:
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 60)
        
        dropdown = wait.until(EC.presence_of_element_located((By.ID, "proyecto")))
        select = Select(dropdown)
        select.select_by_value(survey_data["value"])
        print(f"Selected survey: {survey_data['name']}")
        
        download_button = wait.until(EC.element_to_be_clickable((By.ID, "btn_ajax")))
        
        files_before = set(Path(download_dir).glob("*"))
        download_button.click()
        print("Clicked download button, waiting for download to start...")
        time.sleep(3)
        
        if wait_for_download(download_dir, timeout=600):
            files_after = set(Path(download_dir).glob("*"))
            new_files = files_after - files_before
            if new_files:
                downloaded_file = list(new_files)[0]
                new_name = f"eh_{year}.zip"
                new_path = downloaded_file.parent / new_name
                if not new_path.exists():
                    downloaded_file.rename(new_path)
                print(f"✓ Downloaded: {new_name}")
                return True
            else:
                print("✗ No new file detected")
                return False
        else:
            print("✗ Download timeout")
            return False
            
    except Exception as e:
        print(f"✗ Error downloading {year}: {e}")
        return False

def main():
    output_dir = Path("../output").resolve()
    output_dir.mkdir(exist_ok=True, parents=True)
    print(f"Download directory: {output_dir}")
    print(f"Total surveys to download: {len(SURVEYS)}")
    
    driver = setup_driver(str(output_dir))
    
    try:
        successful = 0
        failed = 0
        for year in sorted(SURVEYS.keys(), reverse=True):
            if download_survey(driver, year, SURVEYS[year], str(output_dir)):
                successful += 1
            else:
                failed += 1
            time.sleep(2)
        print(f"\n{'='*60}\nDOWNLOAD SUMMARY\n{'='*60}")
        print(f"Successful: {successful}\nFailed: {failed}\nTotal: {len(SURVEYS)}\n{'='*60}\n")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
