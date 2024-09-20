from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from loguru import logger
import os
import time

def render(rootdir, relpath, soup, selector):
    # Check if plotly div exists, if not return to avoid starting webdriver
    if soup.find('div', class_='plotly') is None and soup.find('div', class_='plotly-graph-div') is None:
        return

    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)

    driver.get("file://" + os.path.abspath(rootdir))

    # Wait for page to completely load
    try:
        WebDriverWait(driver, 30).until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
        )
    except TimeoutException as err:
        raise TimeoutError("Page not loaded") from err

    for el in driver.find_elements(By.CLASS_NAME, 'js-plotly-plot'):
        viz_id = el.get_attribute('id')
        viz = soup.find(id=viz_id)
        script = viz.find_next_sibling('script')
        logger.info(f"Found plotly viz {viz} with id {viz_id}")

        # Scroll to element and pause for lazy loading
        SCROLL_PAUSE_TIME = 1
        driver.execute_script("arguments[0].scrollIntoView();", el)
        time.sleep(SCROLL_PAUSE_TIME)

        png_name = viz_id + ".png"
        png_path = os.path.join(os.path.join(os.path.dirname(rootdir), relpath), png_name)
                
        # Replace plotly elements with img
        if script is None:
                logger.error(f"No data found for plotly viz with id {viz_id}")
                continue

        new_img = soup.new_tag("img", src=f"{os.path.join(relpath,png_name)}")
        viz.insert_after(new_img)

        viz.decompose()
        script.decompose()

        if os.path.exists(png_path):
            logger.error(f"Existing png path! {png_path}")
            continue

        os.makedirs(os.path.dirname(png_path),exist_ok=True)
        el.screenshot(png_path)

    driver.quit()