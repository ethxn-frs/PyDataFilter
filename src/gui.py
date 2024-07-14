# src/gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from data_loader import load_csv, load_json, load_yaml, load_xml
from data_saver import save_csv, save_json, save_yaml, save_xml
from data_stats import calculate_statistics
from data_filter import filter_data
from data_sort import sort_data

class DataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PyDataFilter")
        self.root.geometry("800x600")
        self.data = []
        self.fields = []
        self.file_loaded = False
        self.filename = tk.StringVar(value="No file loaded")

        self.create_widgets()
        self.update_buttons()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=BOTH, expand=True)

        self.file_label = ttk.Label(self.main_frame, textvariable=self.filename, font=("Helvetica", 16))
        self.file_label.pack(pady=10)

        self.load_button = ttk.Button(self.main_frame, text="Load Data", command=self.load_data, bootstyle="primary")
        self.load_button.pack(pady=5, fill=X)

        self.save_button = ttk.Button(self.main_frame, text="Save Data", command=self.save_data, bootstyle="primary")
        self.save_button.pack(pady=5, fill=X)

        self.stats_button = ttk.Button(self.main_frame, text="Show Statistics", command=self.show_statistics_screen, bootstyle="primary")
        self.stats_button.pack(pady=5, fill=X)

        self.filter_button = ttk.Button(self.main_frame, text="Filter Data", command=self.show_filter_screen, bootstyle="primary")
        self.filter_button.pack(pady=5, fill=X)

        self.sort_button = ttk.Button(self.main_frame, text="Sort Data", command=self.show_sort_screen, bootstyle="primary")
        self.sort_button.pack(pady=5, fill=X)

        self.data_display_button = ttk.Button(self.main_frame, text="Show Data", command=self.show_data, bootstyle="primary")
        self.data_display_button.pack(pady=5, fill=X)

    def update_buttons(self):
        state = tk.NORMAL if self.file_loaded else tk.DISABLED
        self.save_button.config(state=state)
        self.stats_button.config(state=state)
        self.filter_button.config(state=state)
        self.sort_button.config(state=state)
        self.data_display_button.config(state=state)

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("YAML files", "*.yaml"), ("XML files", "*.xml")])
        if not file_path:
            return

        try:
            if file_path.endswith('.csv'):
                self.data = load_csv(file_path)
            elif file_path.endswith('.json'):
                self.data = load_json(file_path)
            elif file_path.endswith('.yaml'):
                self.data = load_yaml(file_path)
            elif file_path.endswith('.xml'):
                self.data = load_xml(file_path)
            self.fields = list(self.data[0].keys())
            self.filename.set(f"Loaded: {file_path.split('/')[-1]}")
            self.file_loaded = True
            self.update_buttons()
            messagebox.showinfo("Info", "Data Loaded Successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def save_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("YAML files", "*.yaml"), ("XML files", "*.xml")])
        if not file_path:
            return

        try:
            if file_path.endswith('.csv'):
                save_csv(self.data, file_path)
            elif file_path.endswith('.json'):
                save_json(self.data, file_path)
            elif file_path.endswith('.yaml'):
                save_yaml(self.data, file_path)
            elif file_path.endswith('.xml'):
                save_xml(self.data, file_path)
            messagebox.showinfo("Info", "Data Saved Successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    def show_statistics_screen(self):
        self.main_frame.pack_forget()
        self.stats_frame = ttk.Frame(self.root, padding=10)
        self.stats_frame.pack(fill=BOTH, expand=True)

        ttk.Label(self.stats_frame, text="Statistics", font=("Helvetica", 16)).pack(pady=10)

        stats = calculate_statistics(self.data)
        text = tk.Text(self.stats_frame, wrap="word", font=("Helvetica", 12))
        text.pack(padx=10, pady=10, expand=True, fill=BOTH)
        for key, value in stats.items():
            text.insert(tk.END, f"{key}:\n")
            for stat, val in value.items():
                text.insert(tk.END, f"  {stat}: {val}\n")

        ttk.Button(self.stats_frame, text="Back", command=self.back_to_main, bootstyle="primary").pack(pady=5, fill=X)

    def show_filter_screen(self):
        self.main_frame.pack_forget()
        self.filter_frame = ttk.Frame(self.root, padding=10)
        self.filter_frame.pack(fill=BOTH, expand=True)

        ttk.Label(self.filter_frame, text="Filter Data", font=("Helvetica", 16)).pack(pady=10)

        ttk.Label(self.filter_frame, text="Field:").pack(pady=5)
        self.field_menu = ttk.Combobox(self.filter_frame, values=self.fields)
        self.field_menu.pack(pady=5, fill=X)

        self.condition_label = ttk.Label(self.filter_frame, text="Condition:")
        self.condition_label.pack(pady=5)
        self.condition_menu = ttk.Combobox(self.filter_frame)
        self.condition_menu.pack(pady=5, fill=X)

        self.value_label = ttk.Label(self.filter_frame, text="Value:")
        self.value_label.pack(pady=5)
        self.value_entry = ttk.Entry(self.filter_frame)
        self.value_entry.pack(pady=5, fill=X)

        self.field_menu.bind("<<ComboboxSelected>>", self.update_conditions)

        ttk.Button(self.filter_frame, text="Apply", command=self.apply_filter, bootstyle="success").pack(pady=5, fill=X)
        ttk.Button(self.filter_frame, text="Back", command=self.back_to_main, bootstyle="primary").pack(pady=5, fill=X)

    def update_conditions(self, event):
        field = self.field_menu.get()
        if all(isinstance(item[field], (int, float)) for item in self.data):
            self.condition_menu.config(values=["less_than", "less_than_equals", "equals", "greater_than", "greater_than_equals", "not_equals"])
        elif all(isinstance(item[field], bool) for item in self.data):
            self.condition_menu.config(values=["true", "false"])
        elif all(isinstance(item[field], str) for item in self.data):
            self.condition_menu.config(values=["equals", "not_equals", "contains", "not_contains"])
        else:
            self.condition_menu.config(values=[])

    def apply_filter(self):
        field = self.field_menu.get()
        condition = self.condition_menu.get()
        value = self.value_entry.get()
        if condition in ["less_than", "less_than_equals", "greater_than", "greater_than_equals"]:
            value = float(value) if '.' in value else int(value)
        elif condition in ["true", "false"]:
            value = True if condition == "true" else False
        self.data = filter_data(self.data, field, condition, value)
        messagebox.showinfo("Info", "Data Filtered Successfully")
        self.back_to_main()

    def show_sort_screen(self):
        self.main_frame.pack_forget()
        self.sort_frame = ttk.Frame(self.root, padding=10)
        self.sort_frame.pack(fill=BOTH, expand=True)

        ttk.Label(self.sort_frame, text="Sort Data", font=("Helvetica", 16)).pack(pady=10)

        ttk.Label(self.sort_frame, text="Field:").pack(pady=5)
        self.sort_field_menu = ttk.Combobox(self.sort_frame, values=self.fields)
        self.sort_field_menu.pack(pady=5, fill=X)

        self.order_label = ttk.Label(self.sort_frame, text="Order:")
        self.order_label.pack(pady=5)
        self.order_menu = ttk.Combobox(self.sort_frame)
        self.order_menu.pack(pady=5, fill=X)

        self.sort_field_menu.bind("<<ComboboxSelected>>", self.update_sort_conditions)

        ttk.Button(self.sort_frame, text="Apply", command=self.apply_sort, bootstyle="success").pack(pady=5, fill=X)
        ttk.Button(self.sort_frame, text="Back", command=self.back_to_main, bootstyle="primary").pack(pady=5, fill=X)

    def update_sort_conditions(self, event):
        field = self.sort_field_menu.get()
        if all(isinstance(item[field], (int, float)) for item in self.data):
            self.order_menu.config(values=["ascending", "descending"])
        elif all(isinstance(item[field], bool) for item in self.data):
            self.order_menu.config(values=["false_to_true", "true_to_false"])
        elif all(isinstance(item[field], str) for item in self.data):
            self.order_menu.config(values=["a_to_z", "z_to_a"])
        else:
            self.order_menu.config(values=[])

    def apply_sort(self):
        field = self.sort_field_menu.get()
        order = self.order_menu.get()
        self.data = sort_data(self.data, field, order)
        messagebox.showinfo("Info", "Data Sorted Successfully")
        self.back_to_main()
        self.show_data()

    def show_data(self):
        self.main_frame.pack_forget()
        self.data_frame = ttk.Frame(self.root, padding=10)
        self.data_frame.pack(fill=BOTH, expand=True)

        ttk.Label(self.data_frame, text="Data", font=("Helvetica", 16)).pack(pady=10)

        text = tk.Text(self.data_frame, wrap="word", font=("Helvetica", 12))
        text.pack(padx=10, pady=10, expand=True, fill=BOTH)
        for item in self.data:
            text.insert(tk.END, f"{item}\n")

        ttk.Button(self.data_frame, text="Back", command=self.back_to_main, bootstyle="primary").pack(pady=5, fill=X)

    def back_to_main(self):
        self.stats_frame.pack_forget() if hasattr(self, 'stats_frame') else None
        self.filter_frame.pack_forget() if hasattr(self, 'filter_frame') else None
        self.sort_frame.pack_forget() if hasattr(self, 'sort_frame') else None
        self.data_frame.pack_forget() if hasattr(self, 'data_frame') else None
        self.main_frame.pack(fill=BOTH, expand=True)

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")  # You can change the theme to any other supported by ttkbootstrap
    app = DataApp(root)
    root.mainloop()
