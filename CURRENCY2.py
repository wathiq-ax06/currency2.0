import tkinter as tk
from tkinter import ttk, messagebox
import requests


class CurrencyConverterApp:
    """
    A real-time currency converter desktop application built with Python and Tkinter.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Currency Converter")
        self.root.geometry("450x300")
        self.root.resizable(False, False)

        # --- Style Configuration ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"), foreground="white", background="#007BFF")
        style.configure("TEntry", font=("Arial", 10))
        style.configure("TCombobox", font=("Arial", 10))
        style.map("TButton", background=[('active', '#0056b3')])

        # --- API Configuration ---
        # IMPORTANT: Replace 'YOUR_API_KEY' with a free key from https://www.exchangerate-api.com
        self.api_key = '11e6fc7fc66d1d7884aefb8c'
        self.base_url = f"https://v6.exchangerate-api.com/v6/{self.api_key}"

        # --- Mock Data for Demonstration (if API key is missing) ---
        self.mock_currencies = {"result": "success",
                                "supported_codes": [["USD", "United States Dollar"], ["EUR", "Euro"],
                                                    ["JPY", "Japanese Yen"], ["GBP", "British Pound Sterling"],
                                                    ["AUD", "Australian Dollar"], ["CAD", "Canadian Dollar"],
                                                    ["CHF", "Swiss Franc"], ["CNY", "Chinese Yuan"],
                                                    ["INR", "Indian Rupee"]]}
        self.mock_rates = {"result": "success",
                           "conversion_rates": {"USD": 1.0, "EUR": 0.93, "JPY": 154.6, "GBP": 0.8, "AUD": 1.52,
                                                "CAD": 1.37, "CHF": 0.91, "CNY": 7.24, "INR": 83.51}}

        # --- Variables ---
        self.from_currency = tk.StringVar()
        self.to_currency = tk.StringVar()
        self.amount = tk.StringVar()
        self.result_text = tk.StringVar(value="Result will be shown here.")

        self.create_widgets()
        self.populate_currencies()

    def create_widgets(self):
        """Creates and places all the GUI widgets in the main window."""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="Python Currency Converter", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Amount Entry
        ttk.Label(main_frame, text="Amount:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        amount_entry = ttk.Entry(main_frame, textvariable=self.amount, width=20)
        amount_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        # From Currency
        ttk.Label(main_frame, text="From:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.from_combo = ttk.Combobox(main_frame, textvariable=self.from_currency, state='readonly')
        self.from_combo.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        # To Currency
        ttk.Label(main_frame, text="To:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.to_combo = ttk.Combobox(main_frame, textvariable=self.to_currency, state='readonly')
        self.to_combo.grid(row=3, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        # Convert Button
        convert_button = ttk.Button(main_frame, text="Convert", command=self.perform_conversion)
        convert_button.grid(row=4, column=0, columnspan=3, pady=20, sticky="ew")

        # Result Label
        result_label = ttk.Label(main_frame, textvariable=self.result_text, font=("Arial", 12, "bold"), wraplength=400)
        result_label.grid(row=5, column=0, columnspan=3, pady=(0, 10))

    def populate_currencies(self):
        """Fetches the list of supported currencies and populates the dropdowns."""
        try:
            if self.api_key == 'YOUR_API_KEY':
                print("API key not found. Using mock currency data.")
                data = self.mock_currencies
            else:
                response = requests.get(f"{self.base_url}/codes")
                response.raise_for_status()  # Raise an exception for bad status codes
                data = response.json()

            if data['result'] == 'success':
                currencies = [f"{code} - {name}" for code, name in data['supported_codes']]
                self.from_combo['values'] = currencies
                self.to_combo['values'] = currencies
                self.from_combo.set("USD - United States Dollar")
                self.to_combo.set("EUR - Euro")
            else:
                messagebox.showerror("Error", "Could not load currency list.")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"Could not connect to API: {e}\nUsing mock data.")
            currencies = [f"{code} - {name}" for code, name in self.mock_currencies['supported_codes']]
            self.from_combo['values'] = currencies
            self.to_combo['values'] = currencies
            self.from_combo.set("USD - United States Dollar")
            self.to_combo.set("EUR - Euro")

    def perform_conversion(self):
        """Handles the currency conversion logic."""
        try:
            amount_val = float(self.amount.get())
            from_code = self.from_currency.get().split(" - ")[0]
            to_code = self.to_currency.get().split(" - ")[0]

            if self.api_key == 'YOUR_API_KEY':
                print("API key not found. Using mock rate data for conversion.")
                rates = self.mock_rates['conversion_rates']
                base_rate = rates.get(from_code, 1.0)
                target_rate = rates.get(to_code, 0.0)
                converted_amount = (amount_val / base_rate) * target_rate
            else:
                response = requests.get(f"{self.base_url}/pair/{from_code}/{to_code}/{amount_val}")
                response.raise_for_status()
                data = response.json()

                if data['result'] == 'success':
                    converted_amount = data['conversion_result']
                else:
                    self.result_text.set("Error: Could not perform conversion.")
                    return

            self.result_text.set(f"{amount_val:.2f} {from_code} = {converted_amount:.2f} {to_code}")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the amount.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"Failed to get exchange rates: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # You may need to install the 'requests' library first:
    # pip install requests

    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()

