# BookScraping

BookScraping is an automated Python tool for scraping book pages from [yazory.com/pdf-books/](https://yazory.com/pdf-books/), converting them into PDF files, and optionally uploading them directly to Google Drive.  
It leverages Selenium for web navigation, requests for image downloading, img2pdf for PDF conversion, and Google Drive API for cloud uploads.  
This project was created to practice and demonstrate web scraping, automation, and integration with cloud storage.

---

## 🚀 Features

- **Automated Book Discovery:**  
  Loads all available books by clicking "Load More" until all items are visible.
- **Book Downloading:**  
  - Navigates to each book page.
  - Extracts the total number of pages and relevant book/session IDs from embedded iframes.
  - Downloads all book pages as images.
- **PDF Creation:**  
  - Combines downloaded images into a single PDF file for each book.
  - Handles naming and folder structure automatically.
- **Duplicate Avoidance:**  
  - Maintains a log of already-downloaded books to avoid redundant downloads.
- **Google Drive Integration:**  
  - Uploads resulting PDFs to a specified Google Drive folder using service account credentials (optional).
- **Robust Error Handling:**  
  Prints clear error messages for failed downloads or uploads.

---

## 🛠️ Technologies Used

- **Python 3**
- **Selenium** (browser automation)
- **Requests** (HTTP requests)
- **img2pdf** (image-to-PDF conversion)
- **Google Drive API** (`googleapiclient`, `google.oauth2`)
- **Regular Expressions, OS, JSON, Shutil** (standard Python modules)

---

## 📁 Project Structure

```
BookScraping/
│
├── main.py                # Main automation & scraping logic
├── upload_to_drive.py     # Google Drive uploader
├── requirements.txt       # Python dependencies (not present, but recommended)
├── downloaded_books.txt   # Log of processed books
└── [generated PDFs, image folders]
```

---

## ⚙️ Setup & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/Raheelkhan-05/BookScraping.git
cd BookScraping
```

### 2. Install Dependencies

Recommended packages (add to `requirements.txt` for convenience):

```bash
pip install selenium requests img2pdf google-api-python-client google-auth-httplib2 google-auth-oauthlib webdriver-manager
```

### 3. Obtain Google Credentials (Optional)

- Create a Google Cloud project and enable the Drive API.
- Download your service account JSON and set it as an environment variable:
  ```bash
  export GOOGLE_CREDENTIALS_JSON='{"type": ...}'  # Paste your JSON inline or use a file and load it in code
  ```
- Set your Drive folder ID in `main.py` or pass it via command line to `upload_to_drive.py`.

### 4. Run the Scraper

```bash
python main.py
```

- The script will:
  - Load all books on `yazory.com/pdf-books/`
  - Process new books (skipping already-downloaded ones)
  - Download each page, create a PDF, upload to Google Drive (if configured)
  - Clean up temporary files

### 5. Upload PDFs Manually (if needed)

```bash
python upload_to_drive.py <filename.pdf> <drive_folder_id>
```

---

## 🔑 Customization

- **Change Target Website:**  
  Modify `MAIN_PAGE_URL` in `main.py`.
- **Change Output Location:**  
  Edit folder/PDF naming logic as needed.
- **Disable Google Drive Upload:**  
  Comment out or remove the `upload_to_drive()` call.

---

## ⚠️ Disclaimer

- This tool is for educational purposes only.  
- Please respect copyright and terms of use of the source website.
- Use responsibly and only for legitimate personal/research uses.

---

## 📬 Contact

Made by [Raheelkhan Lohani](https://github.com/Raheelkhan-05)  
Feel free to connect for questions, feedback, or contributions!
