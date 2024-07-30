import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

def fetch_anime_data(season, year):
    url = f"https://myanimelist.net/anime/season/{year}/{season}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Temukan bagian yang berisi data anime
    anime_list = soup.find_all('div', class_='seasonal-anime')
    
    data = []
    for anime in anime_list:
        title = anime.find('a', class_='link-title').text.strip()
        genres = [genre.text.strip() for genre in anime.find_all('span', class_='genre')]
        data.append({'Title': title, 'Genres': ', '.join(genres)})
    
    return data

def fetch_and_save_data():
    season = season_combobox.get()
    year = year_entry.get()

    if not season or not year:
        messagebox.showwarning("Input Error", "Please enter both season and year.")
        return
    
    try:
        data = fetch_anime_data(season, year)
        df = pd.DataFrame(data)
        df.to_csv(f'anime_{season}_{year}.csv', index=False)
        messagebox.showinfo("Success", f"Data saved to anime_{season}_{year}.csv")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Set up the GUI
root = tk.Tk()
root.title("Anime Data Fetcher")

# Create and place widgets
tk.Label(root, text="Season:").grid(row=0, column=0, padx=10, pady=10)
season_combobox = ttk.Combobox(root, values=["winter", "spring", "summer", "fall"])
season_combobox.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Year:").grid(row=1, column=0, padx=10, pady=10)
year_entry = tk.Entry(root)
year_entry.grid(row=1, column=1, padx=10, pady=10)

fetch_button = tk.Button(root, text="Fetch Data", command=fetch_and_save_data)
fetch_button.grid(row=2, column=0, columnspan=2, pady=20)

root.mainloop()
