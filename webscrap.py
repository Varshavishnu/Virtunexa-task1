import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import pandas as pd
import ttkbootstrap as tb

# Function to scrape data
def scrape_data():
    url = url_entry.get()
    tag = tag_entry.get()
    
    if not url or not tag:
        messagebox.showerror("Error", "Please enter both URL and HTML tag!")
        return

    status_label.config(text="Scraping in progress...", foreground="yellow")
    root.update_idletasks()

    try:
        # Fetch page content
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract content based on tag
        elements = soup.find_all(tag)
        data = [elem.get_text(strip=True) for elem in elements]

        if not data:
            messagebox.showinfo("No Data", f"No '{tag}' tags found on the page.")
            status_label.config(text="No data found.", foreground="red")
            return

        # Display in GUI
        text_output.config(state="normal")
        text_output.delete(1.0, tk.END)
        for item in data:
            text_output.insert(tk.END, item + "\n\n")
        text_output.config(state="disabled")

        # Store scraped data in global variable for saving
        global scraped_data
        scraped_data = data

        status_label.config(text=f"Scraped {len(data)} items successfully!", foreground="green")
        messagebox.showinfo("Success", f"Scraped {len(data)} items successfully!")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch page: {e}")
        status_label.config(text="Scraping failed.", foreground="red")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")
        status_label.config(text="An error occurred.", foreground="red")

# Function to save data as CSV
def save_to_csv():
    if not scraped_data:
        messagebox.showerror("Error", "No data to save. Scrape first!")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    # Save to CSV
    df = pd.DataFrame(scraped_data, columns=["Extracted Data"])
    df.to_csv(file_path, index=False)
    
    messagebox.showinfo("Saved", f"Data saved to {file_path}")
    status_label.config(text="Data saved successfully!", foreground="green")

# GUI Setup
root = tb.Window(themename="darkly")  # Dark theme for modern UI
root.title("Web Scraper")
root.geometry("550x550")

# Header Label
header_label = tb.Label(root, text="Web Scraper", font=("Arial", 18, "bold"), bootstyle="primary")
header_label.pack(pady=10)

# URL Input
url_frame = tb.Frame(root)
url_frame.pack(pady=5)
tb.Label(url_frame, text="Enter URL:", font=("Arial", 12)).pack(side="left", padx=5)
url_entry = tb.Entry(url_frame, width=40, font=("Arial", 12))
url_entry.pack(side="left", padx=5)

# HTML Tag Input
tag_frame = tb.Frame(root)
tag_frame.pack(pady=5)
tb.Label(tag_frame, text="Enter HTML Tag:", font=("Arial", 12)).pack(side="left", padx=5)
tag_entry = tb.Entry(tag_frame, width=20, font=("Arial", 12))
tag_entry.pack(side="left", padx=5)

# Scrape Button
scrape_button = tb.Button(root, text="Scrape", bootstyle="primary", command=scrape_data)
scrape_button.pack(pady=10)

# Output Text Box (Scrollable)
output_frame = tb.Frame(root)
output_frame.pack(pady=5, fill="both", expand=True)

text_output = tk.Text(output_frame, height=10, width=60, font=("Arial", 12), state="disabled", wrap="word", bg="#1e1e1e", fg="white")
text_output.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(output_frame, command=text_output.yview)
scrollbar.pack(side="right", fill="y")
text_output.config(yscrollcommand=scrollbar.set)

# Save & Exit Buttons
button_frame = tb.Frame(root)
button_frame.pack(pady=10)

save_button = tb.Button(button_frame, text="Save as CSV", bootstyle="success", command=save_to_csv)
save_button.pack(side="left", padx=10)

exit_button = tb.Button(button_frame, text="Exit", bootstyle="danger", command=root.quit)
exit_button.pack(side="left", padx=10)

# Status Label
status_label = tb.Label(root, text="Ready", font=("Arial", 10, "italic"), bootstyle="secondary")
status_label.pack(pady=5)

# Initialize empty scraped data
scraped_data = []

root.mainloop()
