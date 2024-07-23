# src/gui.py
import ast
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from data_filter import filter_data
from data_loader import load_csv, load_json, load_yaml, load_xml
from data_saver import save_csv, save_json, save_yaml, save_xml
from data_sort import sort_data
from data_stats import calculate_statistics


class DataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PyDataFilter")
        self.root.geometry("800x600")
        self.data = []
        self.fields = []
        self.file_loaded = False
        self.filename = tk.StringVar(value="No file loaded")
        self.history = []

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

        self.stats_button = ttk.Button(self.main_frame, text="Show Statistics", command=self.show_statistics_screen,
                                       bootstyle="primary")
        self.stats_button.pack(pady=5, fill=X)

        self.filter_button = ttk.Button(self.main_frame, text="Filter Data", command=self.show_filter_screen,
                                        bootstyle="primary")
        self.filter_button.pack(pady=5, fill=X)

        self.sort_button = ttk.Button(self.main_frame, text="Sort Data", command=self.show_sort_screen,
                                      bootstyle="primary")
        self.sort_button.pack(pady=5, fill=X)

        self.data_display_button = ttk.Button(self.main_frame, text="Show Data", command=self.show_data,
                                              bootstyle="primary")
        self.data_display_button.pack(pady=5, fill=X)

        self.reset_button = ttk.Button(self.main_frame, text="Reset Data", command=self.reset_data, bootstyle="warning")
        self.reset_button.pack(pady=5, fill=X)

        self.history_button = ttk.Button(self.main_frame, text="Show History", command=self.show_history_screen,
                                         bootstyle="secondary")
        self.history_button.pack(pady=5, fill=X)

    def update_buttons(self):
        state = tk.NORMAL if self.file_loaded else tk.DISABLED
        self.save_button.config(state=state)
        self.stats_button.config(state=state)
        self.filter_button.config(state=state)
        self.sort_button.config(state=state)
        self.data_display_button.config(state=state)
        self.reset_button.config(state=state)
        self.history_button.config(state=state)

    def load_data(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("YAML files", "*.yaml"),
                       ("XML files", "*.xml")])
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
            self.original_data = self.data.copy()
            self.fields = list(self.data[0].keys())
            self.filename.set(f"Loaded: {file_path.split('/')[-1]}")
            self.file_loaded = True
            self.update_buttons()
            messagebox.showinfo("Info", "Data Loaded Successfully")
            self.add_to_history("Load Data", f"Loaded {file_path.split('/')[-1]}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def save_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"),
                                                            ("YAML files", "*.yaml"), ("XML files", "*.xml")])
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
            if 'true_percentage' in value and 'false_percentage' in value:
                text.insert(tk.END, f"  true: {value['true_percentage']:.2f}%\n")
                text.insert(tk.END, f"  false: {value['false_percentage']:.2f}%\n")
            else:
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

        self.filtered_out_label = ttk.Label(self.filter_frame, text="Filtered Out Rows:", font=("Helvetica", 14))
        self.filtered_out_label.pack(pady=10)

        self.filtered_out_text = tk.Text(self.filter_frame, wrap="word", font=("Helvetica", 12), height=10)
        self.filtered_out_text.pack(pady=10, padx=10, fill=BOTH)

        ttk.Button(self.filter_frame, text="Apply", command=self.apply_filter, bootstyle="success").pack(pady=5, fill=X)
        ttk.Button(self.filter_frame, text="Back", command=self.back_to_main, bootstyle="primary").pack(pady=5, fill=X)

    def update_conditions(self, event):
        field = self.field_menu.get()

        # Convertir les chaînes "true"/"false" en booléens et les listes sous forme de chaînes en listes réelles
        for item in self.data:
            if isinstance(item[field], str):
                if item[field].lower() == "true":
                    item[field] = True
                elif item[field].lower() == "false":
                    item[field] = False
                elif item[field].startswith("[") and item[field].endswith("]"):
                    item[field] = ast.literal_eval(item[field])

        if all(isinstance(item[field], list) for item in self.data):
            self.condition_menu.config(
                values=["exact_length", "min_length", "max_length", "average_equals", "average_greater",
                        "average_less"])
        elif all(isinstance(item[field], bool) for item in self.data):
            self.condition_menu.config(values=["true", "false"])
        elif all(isinstance(item[field], (int, float)) for item in self.data):
            self.condition_menu.config(
                values=["less_than", "less_than_equals", "equals", "greater_than", "greater_than_equals", "not_equals"])
        elif all(isinstance(item[field], str) for item in self.data):
            self.condition_menu.config(
                values=["equals", "not_equals", "contains", "not_contains", "lexicographically_less_than",
                        "lexicographically_greater_than", "starts_with", "ends_with", "lexicographically_less_than_field", "lexicographically_greater_than_field"])
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

        filtered_out_data = filter_data(self.data, field, condition, value)
        self.filtered_out_text.delete(1.0, tk.END)
        for item in filtered_out_data:
            self.filtered_out_text.insert(tk.END, f"{item}\n")

        # Mettre à jour les données filtrées après la confirmation
        confirm = messagebox.askyesno("Confirm Filter", "Do you want to apply this filter?")
        if confirm:
            self.data = filtered_out_data
            messagebox.showinfo("Info", "Data Filtered Successfully")
            self.add_to_history("Filter Data", f"Filtered by {field} {condition} {value}")
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

        self.sorted_data_label = ttk.Label(self.sort_frame, text="Sorted Data:", font=("Helvetica", 14))
        self.sorted_data_label.pack(pady=10)

        self.sorted_data_text = tk.Text(self.sort_frame, wrap="word", font=("Helvetica", 12), height=10)
        self.sorted_data_text.pack(pady=10, padx=10, fill=BOTH)

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
        sorted_data = sort_data(self.data, field, order)

        self.sorted_data_text.delete(1.0, tk.END)
        for item in sorted_data:
            self.sorted_data_text.insert(tk.END, f"{item}\n")

        # Mettre à jour les données triées après la confirmation
        confirm = messagebox.askyesno("Confirm Sort", "Do you want to apply this sort?")
        if confirm:
            self.data = sorted_data
            messagebox.showinfo("Info", "Data Sorted Successfully")
            self.add_to_history("Sort Data", f"Sorted by {field} in {order} order")
            self.back_to_main()

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
        self.history_frame.pack_forget() if hasattr(self, 'history_frame') else None
        self.main_frame.pack(fill=BOTH, expand=True)

    def add_to_history(self, action, result):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"{timestamp} - {action}: {result}")

    def show_history_screen(self):
        self.main_frame.pack_forget()
        self.history_frame = ttk.Frame(self.root, padding=10)
        self.history_frame.pack(fill=BOTH, expand=True)

        ttk.Label(self.history_frame, text="History", font=("Helvetica", 16)).pack(pady=10)

        for idx, entry in enumerate(self.history):
            frame = ttk.Frame(self.history_frame)
            frame.pack(fill=X, pady=2)

            ttk.Label(frame, text=entry, font=("Helvetica", 12)).pack(side=LEFT, padx=10, pady=5)

            if "Load Data" not in entry:  # Ne pas ajouter de bouton "Annuler" pour le chargement de fichier
                action = entry.split(" - ")[1].split(": ")[0]
                details = entry.split(": ")[1]
                if action == "Filter Data":
                    ttk.Button(frame, text="Undo", command=lambda d=details: self.undo_filter(d),
                               bootstyle="danger").pack(side=RIGHT, padx=10)
                elif action == "Sort Data":
                    ttk.Button(frame, text="Undo", command=lambda d=details: self.undo_sort(d),
                               bootstyle="danger").pack(side=RIGHT, padx=10)
                elif action == "Reset Data":
                    ttk.Button(frame, text="Undo", command=self.undo_reset, bootstyle="danger").pack(side=RIGHT,
                                                                                                     padx=10)

        ttk.Button(self.history_frame, text="Back", command=self.back_to_main, bootstyle="primary").pack(pady=5, fill=X)

    def undo_filter(self, action_details):
        # Restaurer les données originales avant le filtre
        self.data = self.original_data.copy()
        for previous_action in self.history:
            if "Filter Data" in previous_action:
                self.apply_undo_filter(previous_action.split(": ")[1])
        messagebox.showinfo("Info", "Filter undone successfully")
        self.show_data()

    def apply_undo_filter(self, details):
        field, condition, value = details.split(" ")
        if condition in ["less_than", "less_than_equals", "greater_than", "greater_than_equals"]:
            value = float(value) if '.' in value else int(value)
        elif condition in ["true", "false"]:
            value = True if condition == "true" else False
        self.data = filter_data(self.data, field, condition, value)

    def undo_sort(self, action_details):
        # Restaurer les données originales avant le tri
        self.data = self.original_data.copy()
        for previous_action in self.history:
            if "Sort Data" in previous_action:
                self.apply_undo_sort(previous_action.split(": ")[1])
        messagebox.showinfo("Info", "Sort undone successfully")
        self.show_data()

    def apply_undo_sort(self, details):
        field, order = details.split(" by ")[1].split(" in ")
        self.data = sort_data(self.data, field, order)

    def undo_reset(self):
        # Réinitialiser les données à leur état original
        self.data = self.original_data.copy()
        messagebox.showinfo("Info", "Reset undone successfully")
        self.show_data()

    def reset_data(self):
        confirm = messagebox.askyesno("Confirm Reset", "Do you want to reset the data to its original state?")
        if confirm:
            self.data = self.original_data.copy()
            messagebox.showinfo("Info", "Data has been reset to its original state.")
            self.add_to_history("Reset Data", "Data reset to original state")
            self.back_to_main()


if __name__ == "__main__":
    root = ttk.Window(themename="darkly")  # You can change the theme to any other supported by ttkbootstrap
    app = DataApp(root)
    root.mainloop()
