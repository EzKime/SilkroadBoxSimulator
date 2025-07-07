import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import csv

CSV_FILE = 'data.csv'
sorting = 0
def get_drop_rate(item_name):

    try:
        with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get('Item Name (Korean)', '').strip() == item_name.strip():
                    return row.get('Drop Rate', '').strip()
    except Exception:
        return ''
    return ''

def simulate_drops():
    global sorting
    try:
        num_boxes = int(entry.get())
        if num_boxes <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Hatalı Giriş", "Lütfen geçerli bir kutu sayısı girin.")
        return

    total_silk = num_boxes * 15
    total_dollar = total_silk * 0.10
    cost_label.config(text=f"Maliyet: {total_silk} Silk ≈ ${total_dollar:.2f}")

    show_only_legend = legend_var.get()

    items = []
    probabilities = []

    try:
        with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    item_raw = row.get('Item Name (Korean)', '').strip()
                    qty_raw = row.get('Qty', '').strip()
                    drop_raw = row.get('Drop Rate', '').strip().replace('%', '')

                    if not item_raw or not qty_raw or not drop_raw:
                        continue

                    item = item_raw
                    quantity = int(qty_raw)
                    drop_rate_percent = float(drop_raw)

                    items.append((item, quantity))
                    probabilities.append(drop_rate_percent / 100)
                except Exception:
                    continue
    except FileNotFoundError:
        messagebox.showerror("Dosya Bulunamadı", f"{CSV_FILE} dosyası bulunamadı.")
        return

    if not items:
        messagebox.showerror("Veri Hatası", "CSV'den geçerli öğe alınamadı.")
        return

    results = []
    for _ in range(num_boxes):
        selected = random.choices(items, weights=probabilities, k=1)[0]
        results.append(selected)

    summary = {}
    for item, qty in results:
        summary[(item, qty)] = summary.get((item, qty), 0) + 1

    sorted_summary = sorted(summary.items(), key=lambda x: x[1], reverse=True)

    output_lines = [f"{num_boxes} kutu açılıyor...\n"]

    if show_only_legend:
        output_lines.append("🔹 Sadece Legend (0.00030%) itemleri listeleniyor:\n")
        for (item, qty), count in sorted_summary:
            
            if '0.00030%' in get_drop_rate(item):
                sorting += 1
                percent = (count / num_boxes) * 100
                output_lines.append(f"{sorting} - {item} x{qty}: {count} kez ({percent:.4f}%)")
    else:
        for (item, qty), count in sorted_summary:
            percent = (count / num_boxes) * 100
            output_lines.append(f"{item} x{qty}: {count} kez ({percent:.4f}%)")

    text_area.delete(1.0, tk.END)
    for line in output_lines:
        text_area.insert(tk.END, line + "\n")
    sorting = 0
# GUI Kurulumu
root = tk.Tk()
root.title("Silkroad Kutu Açma Simülatörü")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Kutu Sayısı:").grid(row=0, column=0, padx=5)
entry = tk.Entry(frame, width=10)
entry.insert(0, "99999")
entry.grid(row=0, column=1, padx=5)

simulate_button = tk.Button(frame, text="Simüle Et", command=simulate_drops)
simulate_button.grid(row=0, column=2, padx=5)

cost_label = tk.Label(frame, text="Maliyet: 0 Silk ≈ $0.00", fg="blue", font=("Arial", 10, "bold"))
cost_label.grid(row=0, column=3, padx=10, pady=5)

legend_var = tk.BooleanVar()
legend_checkbox = tk.Checkbutton(root, text="Sadece Legend (0.00030%) itemleri göster", variable=legend_var)
legend_checkbox.pack()

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=25)
text_area.pack(padx=10, pady=10)

root.mainloop()
