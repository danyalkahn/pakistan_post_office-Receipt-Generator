import os
import csv
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
import datetime
import sqlite3

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

script_directory = os.path.dirname(os.path.abspath(__file__))
# os.chdir(script_directory) # Remove this line, this was wrong to do

#DATABASE_FILE = resource_path("customer_data.db") #  Do not call resource path here.
DATABASE_FILE = "customer_data.db"  # Database will always be in the same directory
PAKISTAN_POST_LOGO = resource_path("pakistan_post_logo.png")
TEXT_IMAGE = resource_path("text.jpg")

TABLE_NAME = "customer_data"

# Data storage (no longer directly used; data is in the database)
data_list = []

def create_table():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            city TEXT,
            phone TEXT,
            price TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def load_data():
    global data_list
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(f"SELECT name, address, city, phone, price, timestamp FROM {TABLE_NAME}")
        loaded_data = cursor.fetchall()
        data_list = list(map(list, loaded_data))
        print(f"Loaded {len(data_list)} records from {DATABASE_FILE}")
        update_table()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Error loading data: {e}")
        data_list = []
        update_table()

def save_data():
    try:
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not filepath:
            return

        with open(filepath, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data_list)
        print(f"save_data: Saving to filepath = {filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving data: {e}")

def import_data():
    global data_list  # Place the global declaration at the beginning
    try:
        filepath = filedialog.askopenfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not filepath:
            return

        print(f"Attempting to load data from filepath: {filepath}")  # Debug

        with open(filepath, "r", newline="", encoding="utf-8") as file:  # Try utf-8 (1)
            reader = csv.reader(file)  # You can add delimiter=";" here if needed (5)

            new_data = [] # start with a blank list

            for row in reader:
                print("Raw CSV Row:", row)  # Debug: Print the raw row

                if row:  # Skip empty rows (3)
                    new_data.append(row)
                else:
                    print("Skipping empty row")

            print(f"Successfully loaded {len(new_data)} records from {filepath}")

            # Add the imported data to the database
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            for row in new_data:
                if len(row) >= 5:  # Ensure at least 5 values
                    cursor.execute(
                        f"""
                        INSERT INTO {TABLE_NAME} (name, address, city, phone, price)
                        VALUES (?, ?, ?, ?, ?)
                    """,
                        row[:5],  # Insert the first 5 values
                    )
            conn.commit()
            conn.close()

            # Reload data from the database to update the table
            load_data()

            print(f"Data list after loading: {data_list}")
            update_table()

    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {filepath}")  # GUI error message
        print(f"File {filepath} not found.")
        data_list = []
        update_table()
    except Exception as e:
        messagebox.showerror("Error", f"Error loading data: {e}")  # GUI error message
        print(f"Error loading data: {e}")
        data_list = []
        update_table()

def add_data():
    name = entry_name.get()
    address = entry_address.get()
    city = entry_city.get()
    phone = entry_phone.get()
    price = entry_price.get()

    if not (name and address and city and phone and price):
        messagebox.showwarning("Warning", "Please fill all fields!")
        return

    timestamp = datetime.datetime.now().isoformat()
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO {TABLE_NAME} (name, address, city, phone, price, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (name, address, city, phone, price, timestamp),
        )
        conn.commit()
        conn.close()
        load_data()
    except Exception as e:
        messagebox.showerror("Error", f"Error adding data to database: {e}")

    update_table()
    clear_fields()


def update_table():
    print("Updating the table...")
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(f"SELECT name, address, city, phone, price, timestamp FROM {TABLE_NAME}")
        data_list = [list(row) for row in cursor.fetchall()]  # Fetch data from the database
        conn.close()
        for i, data in enumerate(data_list):
            if len(data) > 5:
                print(f"Inserting data: {data[:5]}")
                tree.insert("", "end", values=(i + 1, *data[:5]))
        print("Table update complete.")
    except Exception as e:
        messagebox.showerror("Error", f"Error updating table: {e}")


def clear_fields():
    entry_name.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_city.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_price.delete(0, tk.END)


def generate_pdf_selected():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "No entries selected!")
        return
    selected_data = []
    for item in selected_items:
        index = int(tree.item(item, "values")[0]) - 1
        selected_data.append(data_list[index])

    filename = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    if filename:
        generate_pdf(selected_data, filename)


def generate_pdf_all():
    if not data_list:
        messagebox.showwarning("Warning", "No data to generate PDF!")
        return

    filename = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    if filename:
        generate_pdf(data_list, filename)


def generate_pdf_today():
    today = datetime.date.today()
    today_data = []
    for data in data_list:
        if len(data) > 5:
            date_str = data[5]
            if date_str:  # Check if date_str is not None or empty
                try:
                    date_str = str(date_str) # added fix
                    date_str = data[5].split('T')[0]

                    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                    if date == today:
                        today_data.append(data)
                except ValueError:
                    print(f"Invalid date format: {data[5]}")
            else:
                print("Skipping entry with missing date")  # Track data, add a statement here

    if not today_data:
        messagebox.showwarning("Warning", "No data for today to generate PDF!")
        return

    filename = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    if filename:
        generate_pdf(today_data, filename)


def generate_pdf(data_to_print, filename):
    if not data_to_print:
        messagebox.showwarning("Warning", "No data to generate PDF!")
        return

    print(f"generate_pdf: Generating PDF to pdf_file = {filename}")  # Add this line for debugging
    try:
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        # NEW BOX dimensions:
        new_box_height = 20  # Height in points
        new_box_width = 4 * 72
        start_x = 50
        start_y = height - 100
        logo_top_padding = 20
        start_y += logo_top_padding
        line_height = 14
        box_width = 250
        box_height = 110
        text_vertical_offset = 35
        box_spacing = 20

        to_x = start_x + 10
        from_x = start_x + box_width + box_spacing + 10
        from reportlab.lib.units import inch
        for data in data_to_print:
            current_y = start_y  # Initialize current_y for each entry

            # Draw Pakistan Post logo
            c.drawImage(PAKISTAN_POST_LOGO, start_x, current_y, width=500, height=50)  # Correct the path

            # V.P.L Price
            c.setFont("Helvetica-Bold", 12)
            c.drawString(start_x + 5, current_y - 18, f"V.P.L Rs: {data[4]}")  # Removed 20

            # --- Draw Boxes ---
            c.setStrokeColor(colors.black)

            box_y = current_y - 35 - box_height

            # NEW BOX: Draw the new box ABOVE the "To" Section
            new_box_y = box_y + box_height + 10  # Position it above, add a 10-point gap. Adjust as needed

            c.rect(start_x, new_box_y, new_box_width, new_box_height)  # NEW BOX

            c.rect(start_x, box_y, box_width, box_height)  # "To" Box
            c.rect(start_x + box_width + box_spacing, box_y, box_width, box_height)  # "From" Box

            # --- "To" Section ---
            c.setFont("Helvetica", 10)
            to_x = start_x + 10  # X position for "To:" label
            c.drawString(to_x, box_y + box_height - text_vertical_offset, "To:")
            c.drawString(to_x, box_y + box_height - text_vertical_offset - line_height, f"Name: {data[0]}")
            c.drawString(to_x, box_y + box_height - text_vertical_offset - 2 * line_height, f"Address: {data[1]}")
            c.drawString(to_x, box_y + box_height - text_vertical_offset - 3 * line_height, f"City: {data[2]}")
            c.drawString(to_x, box_y + box_height - text_vertical_offset - 4 * line_height, f"Phone: {data[3]}")

            # --- "From" Section (WALI TRADER) ---
            from_x = start_x + box_width + box_spacing + 10  # X position for "From:" label
            from_y = box_y + box_height - text_vertical_offset
            c.setFont("Helvetica-Bold", 10)
            c.drawString(from_x, from_y, "From: WALI TRADER")
            c.setFont("Helvetica", 8)
            c.drawString(from_x, from_y - line_height, "CENTER HAYATABAD")
            c.drawString(from_x, from_y - 2 * line_height, "All Pakistan Online Cosmetic Delivery")
            c.drawString(from_x, from_y - 3 * line_height, "P/O Code: 25100")
            c.drawString(from_x, from_y - 4 * line_height, "Phone: 0307-7199782")

            # --- Replace Urdu Text with Image ---
            image_path = TEXT_IMAGE  # Path to your image file

            # Approach 1: Specify Width in Inches
            image_width_inches = 3  # adjust the number of inches that you want
            image_width = image_width_inches * 72  # Convert inches to points
            image_height = image_width / 8.56  # Maintain aspect ratio
            image_x = (width - image_width) / 2  # Center image horizontally
            image_y = box_y - 50  # Adjust y position as needed.  Box_y - 20 in original, reduced to 50 to move down
            c.drawImage(image_path, image_x, image_y, width=image_width, height=image_height, mask='auto')

            # --- Update start_y for the next entry ---
            start_y -= box_height + 30 + 100  # Move down for the next entry
            if start_y < 100:
                c.showPage()
                start_y = height - 50

        c.save()
        messagebox.showinfo("Success", "PDF Created Successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error generating PDF: {e}")

# GUI Setup
root = tk.Tk()
root.title("Customer Data Entry")

# try: #Add icon code.
#     root.iconbitmap(resource_path("myicon.ico"))
# except:
#     pass
# Labels and Entry Fields
ttk.Label(root, text="Name").grid(row=0, column=0)
entry_name = ttk.Entry(root)
entry_name.grid(row=0, column=1)

ttk.Label(root, text="Address").grid(row=1, column=0)
entry_address = ttk.Entry(root)
entry_address.grid(row=1, column=1)

ttk.Label(root, text="City").grid(row=2, column=0)
entry_city = ttk.Entry(root)
entry_city.grid(row=2, column=1)

ttk.Label(root, text="Phone").grid(row=3, column=0)
entry_phone = ttk.Entry(root)
entry_phone.grid(row=3, column=1)

ttk.Label(root, text="Price").grid(row=4, column=0)
entry_price = ttk.Entry(root)
entry_price.grid(row=4, column=1)

# Buttons
ttk.Button(root, text="Add Data", command=add_data).grid(row=5, column=0)
ttk.Button(root, text="Generate PDF (Selected)", command=generate_pdf_selected).grid(row=5, column=1)
ttk.Button(root, text="Generate PDF (All Data)", command=generate_pdf_all).grid(row=5, column=2)
ttk.Button(root, text="Generate PDF (Today's Data)", command=generate_pdf_today).grid(row=5, column=3)
ttk.Button(root, text="Import Data", command=import_data).grid(row=5, column=4)
ttk.Button(root, text="Export Data", command=save_data).grid(row=5, column=5)

# Table
columns = ("#", "Name", "Address", "City", "Phone", "Price")
tree = ttk.Treeview(root, columns=columns, show="headings", selectmode="extended")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.grid(row=6, column=0, columnspan=6)

# Create the table if it doesn't exist
create_table()

# Load data on startup
print("Calling load_data() on startup...")
load_data()
print("load_data() call complete.")

root.mainloop()


