# Customer Data Entry and PDF Generator

Disclaimer Must Read : This code is generated with AI.

## Overview

This Python script provides a simple GUI application for managing customer data and generating PDF documents.  It allows you to:

*   Enter and store customer information (Name, Address, City, Phone, Price).
*   Save customer data to a SQLite database.
*   Load customer data from the SQLite database on startup.
*   Import customer data from CSV files.
*   Export customer data to CSV files.
*   Generate PDF reports for selected entries, all entries, or entries from the current day.

The script is built using Tkinter for the GUI and reportlab for PDF generation.  It also uses the `sqlite3` module to interact with a database file.

## Features

*   **User-Friendly Interface:**  A simple Tkinter-based GUI for easy data entry and management.
*   **Data Persistence:** Stores customer data in a SQLite database for persistent storage.
*   **CSV Import/Export:**  Allows importing and exporting data in CSV format for compatibility with other applications.
*   **PDF Generation:** Generates PDF reports with customer information, including a Pakistan Post logo and a "From" section with WALI TRADER details.
*   **PDF Generation Options:**
    *   Generate a PDF for selected entries in the table.
    *   Generate a PDF for all entries in the table.
    *   Generate a PDF for entries added on the current day.
*   **Error Handling:** Includes basic error handling and user feedback through message boxes.
*   **Cross-Platform Compatibility:** Should run on any platform that supports Python and its dependencies.
*   **Automatic Path Handling:** Uses `resource_path` to correctly locate supporting files (logo, text image, database) whether running as a script or a PyInstaller executable.

## Requirements

*   Python 3.x
*   The following Python libraries:
    *   `tkinter` (usually comes with Python)
    *   `reportlab`
    *   `csv`
    *   `sqlite3`
    *   `datetime`
*   Image Files
    * `pakistan_post_logo.png`
    * `text.jpg`
    * `customer_data.db` (This will be created automatically if it doesn't exist, but including an empty one helps)

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/danyalkahn/pakistan_post_office-Receipt-Generator
    cd pakistan_post_office-Receipt-Generator
    ```

2.  **Install the required libraries:**

    ```bash
    pip install reportlab
    ```
3.  **Place Image and Database Files:** Ensure that `pakistan_post_logo.png`, `text.jpg`, and `customer_data.db` (even if it's an empty database file) are in the same directory as the Python script. These files are essential for the script to function correctly.  You can include an empty `customer_data.db` in the repository, which will be automatically populated by the script.

## Usage

1.  **Run the script:**

    ```bash
    python your_script_name.py  # Replace your_script_name.py with the name of your script
    ```

2.  **Using the GUI:**

    *   Enter customer data in the provided fields (Name, Address, City, Phone, Price).
    *   Click "Add Data" to save the entry to the SQLite database and update the table displayed in the GUI.  A timestamp will be automatically generated for each entry.
    *   **Generating PDFs:**
        *   **Selected Entries:** Select one or more rows in the table by clicking on them. Then, click "Generate PDF (Selected)" to create a PDF report containing only the information from the selected rows.
        *   **All Entries:**  Click "Generate PDF (All Data)" to create a PDF report containing all entries currently stored in the SQLite database and displayed in the table.
        *   **Today's Entries:** Click "Generate PDF (Today's Data)" to create a PDF report containing only the entries that were added on the current day.  The script uses the timestamp to determine the date.
    *   **Importing Data:** Click "Import Data" to load customer data from a CSV file.  The CSV file should have the following format (comma-separated values):  `Name,Address,City,Phone,Price`.  The existing data in the database will *not* be overwritten, the imported data will be added.
    *   **Exporting Data:** Click "Export Data" to save the customer data currently stored in the SQLite database and displayed in the table to a CSV file.  The CSV file will be created in the same format as described above.

## File Structure

## Configuration

*   **Image and Database Paths:** The script uses relative paths for the `pakistan_post_logo.png`, `text.jpg`, and `customer_data.db` files.  This means they must be located in the same directory as the Python script.  If you want to use different locations, you can modify the `resource_path` function and the variables `DATABASE_FILE`, `PAKISTAN_POST_LOGO`, and `TEXT_IMAGE` in the script.  However, for ease of use, keeping them in the same directory is recommended.
*   **PDF Styling:** The PDF generation logic is within the `generate_pdf` function. You can customize the appearance of the PDF reports by modifying the code in this function, such as:
    *   Fonts (size, family)
    *   Colors
    *   Layout (positioning of elements)
    *   Content (adding or removing information)
*   **Database Table Name:** The `TABLE_NAME` variable defines the name of the table used in the SQLite database.  You can change this if necessary.

## Notes

*   **`resource_path` Function:** This function is crucial for ensuring that the script can locate the necessary files (images, database) even when it's packaged as a standalone executable using tools like PyInstaller.  It handles the different ways file paths are resolved in development versus when running from a packaged executable.
*   **Error Handling:** The script includes basic error handling using `try...except` blocks and message boxes to inform the user of potential issues.  For a production environment, consider implementing more robust error handling and logging to better diagnose and resolve problems.
*   **CSV Format:** The CSV import and export functionality assumes that the CSV files have the exact same structure as the data stored in the SQLite database: `Name,Address,City,Phone,Price`. Ensure that your CSV files adhere to this format to avoid errors during import.
*   **Database Initialization:** The script automatically creates the `customer_data.db` file and the `customer_data` table if they don't already exist. You don't need to manually create these before running the script.  However, including an empty `customer_data.db` file in the repository provides clarity and avoids potential confusion.
*   **Dependencies:** While `tkinter` usually comes pre-installed with Python, you might need to install `reportlab` using `pip install reportlab`.

## Contributing

Contributions are welcome! Please submit pull requests with bug fixes, new features, or improvements to the documentation. Before submitting a pull request, please ensure that:

*   The code is well-documented.
*   The code follows PEP 8 style guidelines.
*   Any new features are accompanied by appropriate tests.

## License

MIT License

Copyright (c) 2025 Danyal Khan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
