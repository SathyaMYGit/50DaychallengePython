import platform
import asyncio

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

st.set_page_config(page_title="Headphone Price Comparator", page_icon="🛒")
st.title("🛒 Headphone Price Comparator")

product = st.text_input("Enter product name", "headphones")

def search_amazon(page, product):
    try:
        print("🔍 Searching on Amazon...")
        page.goto("https://www.amazon.in", timeout=20000)
        page.fill("input[name='field-keywords']", product)
        page.press("input[name='field-keywords']", "Enter")
        page.wait_for_selector(".s-title-instructions-style", timeout=15000)
        titles = page.locator(".s-title-instructions-style").all_text_contents()
        prices = page.locator(".a-price-whole").all_text_contents()
        print("✅ Amazon search complete")
        return {
            "site": "Amazon",
            "title": titles[0] if titles else "No product found",
            "price": prices[0] if prices else "N/A"
        }
    except PlaywrightTimeout:
        print("❌ Amazon: Timeout Error")
        return {"site": "Amazon", "title": "Timeout Error", "price": "N/A"}
    except Exception as e:
        print(f"❌ Amazon: {e}")
        return {"site": "Amazon", "title": "Error", "price": "N/A"}

def search_flipkart(page, product):
    try:
        print("🔍 Searching on Flipkart...")
        page.goto("https://www.flipkart.com", timeout=20000)
        try:
            page.click("button._2KpZ6l._2doB4z", timeout=5000)  # Close login popup
        except:
            pass
        page.fill("input[name='q']", product)
        page.press("input[name='q']", "Enter")
        page.wait_for_selector("._1YokD2 ._4rR01T", timeout=15000)
        titles = page.locator("._4rR01T").all_text_contents()
        prices = page.locator("._30jeq3").all_text_contents()
        print("✅ Flipkart search complete")
        return {
            "site": "Flipkart",
            "title": titles[0] if titles else "No product found",
            "price": prices[0] if prices else "N/A"
        }
    except PlaywrightTimeout:
        print("❌ Flipkart: Timeout Error")
        return {"site": "Flipkart", "title": "Timeout Error", "price": "N/A"}
    except Exception as e:
        print(f"❌ Flipkart: {e}")
        return {"site": "Flipkart", "title": "Error", "price": "N/A"}

def search_meesho(page, product):
    try:
        print("🔍 Searching on Meesho...")
        page.goto("https://www.meesho.com", timeout=20000, wait_until="load")
        page.wait_for_selector("input[type='search']", timeout=15000)
        page.fill("input[type='search']", product)
        page.press("input[type='search']", "Enter")
        page.wait_for_timeout(5000)  # wait for results
        titles = page.locator("p.pv-z").all_text_contents()
        prices = page.locator("h5.pw-dt").all_text_contents()
        print("✅ Meesho search complete")
        return {
            "site": "Meesho",
            "title": titles[0] if titles else "No product found",
            "price": prices[0] if prices else "N/A"
        }
    except PlaywrightTimeout:
        print("❌ Meesho: Timeout Error")
        return {"site": "Meesho", "title": "Timeout Error", "price": "N/A"}
    except Exception as e:
        print(f"❌ Meesho: {e}")
        return {"site": "Meesho", "title": "Error", "price": "N/A"}

def fetch_prices(product):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        results = [
            search_amazon(page, product),
            search_flipkart(page, product),
            search_meesho(page, product)
        ]
        browser.close()
        return results

if st.button("Compare Prices"):
    with st.spinner("Searching... Please wait"):
        results = fetch_prices(product)
        st.success("Comparison Complete!")
        st.write("### 🧾 Price Comparison Results")
        for result in results:
            st.markdown(f"**{result['site']}**  
                        - 🛍️ Product: `{result['title']}`  
                        - 💰 Price: `{result['price']}`")
