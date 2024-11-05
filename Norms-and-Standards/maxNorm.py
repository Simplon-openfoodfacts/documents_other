import tkinter as tk
from tkinter import messagebox
import json
import numpy as np  # Importing numpy to use NaN

# Maximum nutritional values
nutritional_values_max = {
    'energy-kcal_100g': 600,
    'fat_100g': 20,
    'saturated-fat_100g': 10,
    'cholesterol_100g': 300,
    'carbohydrates_100g': 50,
    'sugars_100g': 22.5,
    'fiber_100g': 35,  # Not specified
    'proteins_100g': 20,
    'salt_100g': 3,
    'sodium_100g': 1200,
    'vitamin-c_100g': 80,
    'potassium_100g': 2000,
    'calcium_100g': 1200,
    'iron_100g': 15,
    'magnesium_100g': 350,
    'zinc_100g': 10
}

class NutritionalInputApp:
    def __init__(self, master):
        self.master = master
        master.title("Input Nutritional Values")

        # Product name input field
        self.product_label = tk.Label(master, text="Product Name:")
        self.product_label.pack()
        self.product_entry = tk.Entry(master)
        self.product_entry.pack()

        # Nutritional values input fields
        self.entries = {}
        for nutrient in nutritional_values_max.keys():
            label = tk.Label(master, text=nutrient)
            label.pack()

            entry = tk.Entry(master)
            entry.pack()
            self.entries[nutrient] = entry

        self.submit_button = tk.Button(master, text="Submit", command=self.validate_input)
        self.submit_button.pack()

    def validate_input(self):
        # Check product name
        product_name = self.product_entry.get()
        if not product_name.strip():
            messagebox.showerror("Input Error", "Product name cannot be empty.")
            return
        
        # Dictionary to store results
        nutritional_values = {"product_name": product_name}

        for nutrient, entry in self.entries.items():
            value = entry.get()
            max_value = nutritional_values_max[nutrient]

            # Skip empty values
            if not value:
                nutritional_values[nutrient] = np.nan  # Record NaN for empty value
                continue

            # Check if maximum value is "N/A"
            if max_value == 'N/A':
                nutritional_values[nutrient] = value  # Store as is
                continue
            
            try:
                value = float(value)
                if value < 0 or value > max_value:
                    messagebox.showerror("Input Error", f"{nutrient} must be between 0 and {max_value}.")
                    return
                nutritional_values[nutrient] = value
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid input for {nutrient}. Please enter a number.")
                return

        # Write data to JSON file
        with open("nutritional_values.json", "w") as json_file:
            json.dump(nutritional_values, json_file, indent=4, default=str)  # Use default=str for NaN
        
        messagebox.showinfo("Success", "All values are valid and saved to nutritional_values.json!")

if __name__ == "__main__":
    root = tk.Tk()
    app = NutritionalInputApp(root)
    root.mainloop()
