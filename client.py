import tkinter as tk
from tkinter import messagebox, simpledialog
import requests

API = 'http://127.0.0.1:5000'

# Funkcija za refresh liste troškova
def load_troskovi():
    troskovi_list.delete(0, tk.END)
    r = requests.get(f"{API}/troskovi")
    for t in r.json():
        troskovi_list.insert(tk.END, f"{t[0]} | {t[1]} | {t[2]} | {t[3]} | {t[4]} | {t[5]}")

def dodaj_trosak():
    data = {
        'naziv': naziv_var.get(),
        'iznos': iznos_var.get(),
        'tip': tip_var.get(),
        'namena': namena_var.get(),
        'lokacija': lokacija_var.get()
    }
    r = requests.post(f"{API}/troskovi", json=data)
    load_troskovi()

def obrisi_trosak():
    try:
        sel = troskovi_list.curselection()[0]
        trosak_id = int(troskovi_list.get(sel).split('|')[0])
        requests.delete(f"{API}/troskovi/{trosak_id}")
        load_troskovi()
    except:
        messagebox.showerror("Greška", "Izaberite trosak za brisanje")

def izmeni_trosak():
    try:
        sel = troskovi_list.curselection()[0]
        trosak_id = int(troskovi_list.get(sel).split('|')[0])
        data = {
            'naziv': naziv_var.get(),
            'iznos': iznos_var.get(),
            'tip': tip_var.get(),
            'namena': namena_var.get(),
            'lokacija': lokacija_var.get()
        }
        requests.put(f"{API}/troskovi/{trosak_id}", json=data)
        load_troskovi()
    except:
        messagebox.showerror("Greška", "Izaberite trosak za izmenu")

# GUI setup
root = tk.Tk()
root.title("Menadžment Troškova")

naziv_var = tk.StringVar()
iznos_var = tk.StringVar()
tip_var = tk.StringVar(value="put")
namena_var = tk.StringVar()
lokacija_var = tk.StringVar()

tk.Label(root, text="Naziv:").pack()
tk.Entry(root, textvariable=naziv_var).pack()
tk.Label(root, text="Iznos:").pack()
tk.Entry(root, textvariable=iznos_var).pack()
tk.Label(root, text="Tip:").pack()
for t in ["put", "rekreacija", "drugo"]:
    tk.Radiobutton(root, text=t, variable=tip_var, value=t).pack()
tk.Label(root, text="Namena:").pack()
tk.Entry(root, textvariable=namena_var).pack()
tk.Label(root, text="Lokacija:").pack()
tk.Entry(root, textvariable=lokacija_var).pack()

tk.Button(root, text="Dodaj trošak", command=dodaj_trosak).pack()
tk.Button(root, text="Izmeni trošak", command=izmeni_trosak).pack()
tk.Button(root, text="Obriši trošak", command=obrisi_trosak).pack()

troskovi_list = tk.Listbox(root, width=80)
troskovi_list.pack()

tk.Button(root, text="Refresh lista troškova", command=load_troskovi).pack()

root.after(1000, load_troskovi)
root.mainloop()
