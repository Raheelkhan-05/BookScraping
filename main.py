import os
import time
import requests
import img2pdf
import re
import shutil
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from upload_to_drive import upload_to_drive  # Import Google Drive uploader

MAIN_PAGE_URL = "https://yazory.com/pdf-books/"
LOG_FILE = "downloaded_books.txt"

# Initialize WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def load_all_books():
    driver.get(MAIN_PAGE_URL)
    time.sleep(5)

    while True:
        try:
            load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "load-more-ajax"))
            )
            driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(3)
            print("--> Loaded more books...")
        except:
            print("----- No more books to load!")
            break

def get_books():
    load_all_books()  # Ensure all books are loaded first

    books = driver.find_elements(By.CSS_SELECTOR, ".btn.button-view")
    book_names = driver.find_elements(By.CSS_SELECTOR, ".text-center.title-journal-sm")

    book_data = {}
    for book, name in zip(books, book_names):
        book_data[book.get_attribute("href")] = name.text.strip()

    return book_data

def extract_ids(iframe_src):
    match = re.search(r"ID=(\d+)_(\d+)", iframe_src)
    if match:
        return match.group(1), match.group(2)
    return None, None

def load_downloaded_books():
    if not os.path.exists(LOG_FILE):
        return set()
    with open(LOG_FILE, "r") as f:
        return set(f.read().splitlines())

def save_downloaded_book(book_url):
    with open(LOG_FILE, "a") as f:
        f.write(book_url + "\n")

# Get list of book URLs and names
books = get_books()
downloaded_books = load_downloaded_books()
new_books = {url: name for url, name in books.items() if url not in downloaded_books}

print(f"Total books found: {len(books)} | New books to download: {len(new_books)}")

# Process new books only
for book_url, book_name in new_books.items():
    try:
        print(f"\n-> Processing book: {book_name}")
        driver.get(book_url)
        time.sleep(5)
        try:
            iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            iframe_src = iframe.get_attribute("src")
            book_id, session_id = extract_ids(iframe_src)
            if not book_id or not session_id:
                raise ValueError("Failed to extract book IDs from iframe source.")
            print(f"Extracted Book ID: {book_id}, Session ID: {session_id}")
            driver.switch_to.frame(iframe)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "flipbook-currentPageNumber"))
            )
            page_info = driver.execute_script("return document.querySelector('.flipbook-currentPageNumber')?.textContent;")

            if page_info:
                total_pages = int(page_info.split("/")[-1].strip())
                print(f"Total pages detected: {total_pages}")
            else:
                raise ValueError("Failed to extract total pages.")

        except Exception as e:
            print(f"Error extracting details: {e}")
            continue  

        cookies = driver.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        headers = {'Referer': book_url}

        sanitized_book_name = re.sub(r'[\\/*?:"<>|]', "_", book_name)
        book_folder = f"{sanitized_book_name}_pages"
        os.makedirs(book_folder, exist_ok=True)

        baseurl = f"https://cdn-view.flipdocs.com/books/{book_id}/{session_id}/zoompage_{{page:04d}}.jpg?r=1"

        for page_num in range(1, total_pages + 1):
            url = baseurl.format(page=page_num)
            response = session.get(url, headers=headers)

            if response.status_code == 200:
                with open(f"{book_folder}/page{page_num:02d}.jpg", 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded page {page_num}")
            else:
                print(f"Failed to download page {page_num}")

        image_files = [os.path.join(book_folder, f) for f in sorted(os.listdir(book_folder)) if f.endswith('.jpg')]
        pdf_filename = f"{sanitized_book_name}.pdf"

        with open(pdf_filename, "wb") as pdf_file:
            pdf_file.write(img2pdf.convert(image_files))

        print(f"PDF created: {pdf_filename}")
        shutil.rmtree(book_folder)
        print(f"Deleted pages folder: {book_folder}")

        save_downloaded_book(book_url)

        # Upload to Google Drive
        GOOGLE_DRIVE_FOLDER_ID = "YOUR_DRIVE_FOLDER_ID"
        upload_to_drive(pdf_filename, GOOGLE_DRIVE_FOLDER_ID)

    except Exception as e:
        print(f"Error processing book {book_name}: {e}")

driver.quit()
print("All new books have been processed!")
