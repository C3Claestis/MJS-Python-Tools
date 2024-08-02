from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import time

def fetch_movie_data(year):
    # Setup the ChromeDriver using WebDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    url = f"https://www.vidio.com/film?year={year}"
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    # Find the movie elements
    movies = driver.find_elements(By.CLASS_NAME, 'movie-card')  # Adjust class name as needed
    data = []
    for movie in movies:
        title = movie.find_element(By.TAG_NAME, 'h3').text.strip()  # Adjust tag as needed
        genre = movie.find_element(By.CLASS_NAME, 'genre').text.strip()  # Adjust class name as needed
        movie_type = movie.find_element(By.CLASS_NAME, 'type').text.strip()  # Adjust class name as needed
        
        data.append({'Title': title, 'Genre': genre, 'Type': movie_type, 'Year': year})

    driver.quit()
    return data

def fetch_and_save_data():
    year = year_combobox.get()

    if not year:
        messagebox.showwarning("Input Error", "Please select a year.")
        return

    try:
        data = fetch_movie_data(year)
        df = pd.DataFrame(data)
        df.to_csv(f'movies_{year}.csv', index=False)
        messagebox.showinfo("Success", f"Data saved to movies_{year}.csv")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Set up the GUI
root = tk.Tk()
root.title("Vidio Movie Data Fetcher")

# Create and place widgets
tk.Label(root, text="Year:").grid(row=0, column=0, padx=10, pady=10)
year_combobox = ttk.Combobox(root, values=[str(year) for year in range(2000, 2024)])  # Replace with the actual range of years
year_combobox.grid(row=0, column=1, padx=10, pady=10)

fetch_button = tk.Button(root, text="Fetch Data", command=fetch_and_save_data)
fetch_button.grid(row=1, column=0, columnspan=2, pady=20)

root.mainloop()
