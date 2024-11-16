from playwright.sync_api import sync_playwright
import pandas as pd
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

def scrape_sales_data(url):
    """Scrape dynamic sales data using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # Wait for the table or data to load
        page.wait_for_selector('table.sales-data')

        # Extract the rows of the table
        table_rows = page.locator('table.sales-data tr').all_text_contents()
        
        # Process the data into structured format
        sales_data = []
        for row in table_rows:
            cols = row.split('\n')
            if len(cols) == 3:
                sales_data.append({
                    'date': cols[0].strip(),
                    'product': cols[1].strip(),
                    'sales': float(cols[2].strip())
                })
        
        browser.close()

    return pd.DataFrame(sales_data)
