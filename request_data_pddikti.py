import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# Function to log in and create a session
def create_session(username, password):
    login_url = 'https://pddikti.kemdikbud.go.id/login'  # URL untuk halaman login
    session = requests.Session()
    
    # Data login yang akan dikirimkan melalui POST request
    login_data = {
        'username': username,
        'password': password
    }
    
    # Mengirimkan POST request untuk login
    response = session.post(login_url, data=login_data)
    
    if response.status_code == 200 and "Dashboard" in response.text:  # Ganti "Dashboard" dengan string yang sesuai dari halaman login yang berhasil
        return session
    else:
        raise Exception("Failed to log in")

def fetch_institution_data(session, institution_type, province):
    url = f"https://pddikti.kemdikbud.go.id/{institution_type}/{province}"
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Temukan bagian yang berisi data institusi
    institution_list = soup.find_all('div', class_='institution-class')  # Example class name
    
    data = []
    for institution in institution_list:
        name = institution.find('h2').text.strip()  # Example tag
        type_ = institution.find('span', class_='type-class').text.strip()  # Example class for type
        location = institution.find('span', class_='location-class').text.strip()  # Example class for location
        
        data.append({'Name': name, 'Type': type_, 'Location': location})
    
    return data

def fetch_and_save_data():
    institution_type = institution_combobox.get()
    province = province_combobox.get()
    username = username_entry.get()
    password = password_entry.get()

    if not institution_type or not province or not username or not password:
        messagebox.showwarning("Input Error", "Please enter institution type, province, username, and password.")
        return
    
    try:
        session = create_session(username, password)
        data = fetch_institution_data(session, institution_type, province)
        df = pd.DataFrame(data)
        df.to_csv(f'{institution_type}_{province}.csv', index=False)
        messagebox.showinfo("Success", f"Data saved to {institution_type}_{province}.csv")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Set up the GUI
root = tk.Tk()
root.title("Institution Data Fetcher")

# Create and place widgets
tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Institution Type:").grid(row=2, column=0, padx=10, pady=10)
institution_combobox = ttk.Combobox(root, values=["universitas", "politeknik"])
institution_combobox.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Province:").grid(row=3, column=0, padx=10, pady=10)
province_combobox = ttk.Combobox(root, values=["jawabarat", "jawatengah", "jawatimur"])  # Replace with actual provinces
province_combobox.grid(row=3, column=1, padx=10, pady=10)

fetch_button = tk.Button(root, text="Fetch Data", command=fetch_and_save_data)
fetch_button.grid(row=4, column=0, columnspan=2, pady=20)

root.mainloop()
