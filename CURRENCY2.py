import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
from datetime import datetime


class CurrencyConverterApp:
    """
    A real-time currency converter desktop application built with Python and Tkinter.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("💱 Currency Converter Pro")
        self.root.geometry("700x700")
        self.root.resizable(True, True)
        self.root.minsize(650, 600)

        # Set vibrant gradient background
        self.root.configure(bg="#e3f2fd")

        # --- Style Configuration ---
        style = ttk.Style()
        style.theme_use('clam')

        # Configure Labels with vibrant colors
        style.configure("TLabel", font=("Segoe UI", 10), background="#e3f2fd")
        style.configure("Title.TLabel", font=("Segoe UI", 17, "bold"), background="#e3f2fd", foreground="#0d47a1")
        style.configure("Subtitle.TLabel", font=("Segoe UI", 11), background="#e3f2fd", foreground="#1565c0")

        # Configure Buttons with lively colors
        style.configure("TButton", font=("Segoe UI", 11, "bold"), foreground="white", background="#2196f3",
                        borderwidth=0, padding=15)
        style.map("TButton", background=[('active', '#1976d2'), ('pressed', '#0d47a1')])

        # Big vibrant green convert button
        style.configure("Accent.TButton", font=("Segoe UI", 12, "bold"), foreground="white", background="#4caf50",
                        borderwidth=0, padding=18)
        style.map("Accent.TButton", background=[('active', '#43a047'), ('pressed', '#2e7d32')])

        # Orange clear button
        style.configure("Clear.TButton", font=("Segoe UI", 11), foreground="white", background="#ff9800", borderwidth=0,
                        padding=15)
        style.map("Clear.TButton", background=[('active', '#f57c00'), ('pressed', '#e65100')])

        # Purple swap button
        style.configure("Swap.TButton", font=("Segoe UI", 16), foreground="white", background="#9c27b0", borderwidth=0,
                        padding=10)
        style.map("Swap.TButton", background=[('active', '#7b1fa2'), ('pressed', '#6a1b9a')])

        # Configure Entry and Combobox
        style.configure("TEntry", font=("Segoe UI", 11), fieldbackground="white", borderwidth=2, relief="solid")
        style.configure("TCombobox", font=("Segoe UI", 10), fieldbackground="white", borderwidth=1)

        # Configure Frame with gradient background
        style.configure("TFrame", background="#e3f2fd")
        style.configure("Card.TFrame", background="white", relief="raised", borderwidth=2)

        # --- API Configuration ---
        self.api_key = os.getenv('EXCHANGE_RATE_API_KEY', '11e6fc7fc66d1d7884aefb8c')
        self.base_url = f"https://v6.exchangerate-api.com/v6/{self.api_key}"

        # --- Cache for API responses ---
        self.currency_cache = None
        self.last_update = None

        # --- Mock Data for Demonstration ---
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
        self.amount = tk.StringVar(value="1")
        self.result_text = tk.StringVar(value="Enter amount and click Convert")
        self.rate_text = tk.StringVar(value="")
        self.conversion_history = []
        self.all_currencies = []

        self.create_widgets()
        self.populate_currencies()

    def create_widgets(self):
        """Creates and places all the GUI widgets in the main window."""
        canvas = tk.Canvas(self.root, bg="#e3f2fd", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        canvas.create_rectangle(0, 0, 700, 200, fill="#bbdefb", outline="")
        canvas.create_rectangle(0, 200, 700, 450, fill="#d1e7f7", outline="")
        canvas.create_rectangle(0, 450, 700, 700, fill="#e3f2fd", outline="")

        main_frame = ttk.Frame(canvas, padding="40", style="TFrame")
        canvas.create_window(350, 350, window=main_frame)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_columnconfigure(2, weight=0)

        title_label = ttk.Label(main_frame, text="💱 Currency Converter Pro", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 5))

        subtitle_label = ttk.Label(main_frame, text="✨ Real-time Exchange Rates • Fast & Accurate ⚡",
                                   style="Subtitle.TLabel")
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 30))

        input_card = ttk.Frame(main_frame, style="Card.TFrame", padding="30")
        input_card.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 25), ipadx=10, ipady=10)
        input_card.grid_columnconfigure(1, weight=1)

        amount_label = ttk.Label(input_card, text="💵 Amount", font=("Segoe UI", 11, "bold"), foreground="#0d47a1")
        amount_label.grid(row=0, column=0, sticky="w", padx=(0, 15), pady=(0, 10))

        amount_entry = ttk.Entry(input_card, textvariable=self.amount, font=("Segoe UI", 11), width=25)
        amount_entry.grid(row=0, column=1, columnspan=2, sticky="ew", pady=(0, 20), ipady=8)
        amount_entry.bind('<Return>', lambda e: self.perform_conversion())

        from_label = ttk.Label(input_card, text="🌍 From", font=("Segoe UI", 11, "bold"), foreground="#0d47a1")
        from_label.grid(row=1, column=0, sticky="w", padx=(0, 15), pady=(0, 10))

        self.from_combo = ttk.Combobox(input_card, textvariable=self.from_currency,
                                       font=("Segoe UI", 11), width=25)
        self.from_combo.grid(row=1, column=1, sticky="ew", pady=(0, 20), ipady=6)
        self.from_combo.bind('<KeyRelease>', lambda e: self.filter_from())

        swap_button = ttk.Button(input_card, text="🔄", style="Swap.TButton", width=3, command=self.swap_currencies)
        swap_button.grid(row=1, column=2, padx=(15, 0), pady=(0, 20))

        to_label = ttk.Label(input_card, text="🎯 To", font=("Segoe UI", 11, "bold"), foreground="#0d47a1")
        to_label.grid(row=2, column=0, sticky="w", padx=(0, 15), pady=(0, 10))

        self.to_combo = ttk.Combobox(input_card, textvariable=self.to_currency,
                                     font=("Segoe UI", 11), width=25)
        self.to_combo.grid(row=2, column=1, columnspan=2, sticky="ew", pady=(0, 0), ipady=6)
        self.to_combo.bind('<KeyRelease>', lambda e: self.filter_to())

        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.grid(row=3, column=0, columnspan=3, pady=(0, 25), sticky="ew")
        button_frame.grid_columnconfigure(0, weight=2)
        button_frame.grid_columnconfigure(1, weight=1)

        convert_button = ttk.Button(button_frame, text="⚡ CONVERT NOW ⚡", style="Accent.TButton",
                                    command=self.perform_conversion)
        convert_button.grid(row=0, column=0, padx=(0, 15), sticky="ew", ipady=8)

        clear_button = ttk.Button(button_frame, text="🗑️ Clear", style="Clear.TButton", command=self.clear_fields)
        clear_button.grid(row=0, column=1, sticky="ew", ipady=8)

        result_card = ttk.Frame(main_frame, style="Card.TFrame", padding="35")
        result_card.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(0, 20), ipadx=15, ipady=15)

        result_label = tk.Label(result_card, textvariable=self.result_text, font=("Segoe UI", 16, "bold"),
                                wraplength=550, bg="white", fg="#2e7d32", justify="center")
        result_label.pack(pady=(0, 12))

        rate_label = tk.Label(result_card, textvariable=self.rate_text, font=("Segoe UI", 11),
                              bg="white", fg="#546e7a", justify="center")
        rate_label.pack()

        self.status_text = tk.StringVar(value="")
        status_label = ttk.Label(main_frame, textvariable=self.status_text, font=("Segoe UI", 10),
                                 foreground="#1976d2", justify="center")
        status_label.grid(row=5, column=0, columnspan=3, pady=(0, 10))

    def populate_currencies(self):
        """Fetches the list of supported currencies and populates the dropdowns."""
        if self.currency_cache:
            currencies = self.currency_cache
            self.from_combo['values'] = currencies
            self.to_combo['values'] = currencies
            self.from_combo.set("USD - United States Dollar")
            self.to_combo.set("EUR - Euro")
            return

        try:
            self.status_text.set("Loading currencies...")
            self.root.update()

            if self.api_key == 'YOUR_API_KEY':
                data = self.mock_currencies
            else:
                response = requests.get(f"{self.base_url}/codes", timeout=10)
                response.raise_for_status()
                data = response.json()

            if data['result'] == 'success':
                currencies = [f"{code} - {name}" for code, name in data['supported_codes']]
                self.currency_cache = currencies
                self.all_currencies = currencies
                self.from_combo['values'] = currencies
                self.to_combo['values'] = currencies
                self.from_combo.set("USD - United States Dollar")
                self.to_combo.set("EUR - Euro")
                self.status_text.set("✅ Ready to convert!")
            else:
                self.status_text.set("Error loading currencies")
                messagebox.showerror("Error", "Could not load currency list.")

        except requests.exceptions.RequestException as e:
            self.status_text.set("Using offline mode")
            messagebox.showwarning("Network Error", f"Could not connect to API.\nUsing limited currency list.")
            currencies = [f"{code} - {name}" for code, name in self.mock_currencies['supported_codes']]
            self.currency_cache = currencies
            self.all_currencies = currencies
            self.from_combo['values'] = currencies
            self.to_combo['values'] = currencies
            self.from_combo.set("USD - United States Dollar")
            self.to_combo.set("EUR - Euro")

    def perform_conversion(self):
        """Handles the currency conversion logic."""
        try:
            if not self.amount.get().strip():
                messagebox.showwarning("Input Required", "Please enter an amount.")
                return

            if not self.from_currency.get() or not self.to_currency.get():
                messagebox.showwarning("Selection Required", "Please select both currencies.")
                return

            amount_val = float(self.amount.get())

            if amount_val <= 0:
                messagebox.showwarning("Invalid Amount", "Please enter a positive amount.")
                return

            from_code = self.from_currency.get().split(" - ")[0]
            to_code = self.to_currency.get().split(" - ")[0]

            if from_code == to_code:
                self.result_text.set(f"{amount_val:.2f} {from_code} = {amount_val:.2f} {to_code}")
                self.rate_text.set("1.00 (same currency)")
                self.status_text.set("")
                return

            self.status_text.set("Converting...")
            self.root.update()

            if self.api_key == 'YOUR_API_KEY':
                rates = self.mock_rates['conversion_rates']
                base_rate = rates.get(from_code, 1.0)
                target_rate = rates.get(to_code, 0.0)
                converted_amount = (amount_val / base_rate) * target_rate
                exchange_rate = target_rate / base_rate
            else:
                response = requests.get(f"{self.base_url}/pair/{from_code}/{to_code}/{amount_val}", timeout=10)
                response.raise_for_status()
                data = response.json()

                if data['result'] == 'success':
                    converted_amount = data['conversion_result']
                    exchange_rate = data.get('conversion_rate', converted_amount / amount_val)
                else:
                    self.result_text.set("Error: Could not perform conversion.")
                    self.status_text.set("Conversion failed")
                    return

            self.result_text.set(f"{amount_val:.2f} {from_code} = {converted_amount:.2f} {to_code}")
            self.rate_text.set(f"Exchange Rate: 1 {from_code} = {exchange_rate:.4f} {to_code}")
            self.status_text.set(f"Updated: {datetime.now().strftime('%H:%M:%S')}")

            self.conversion_history.append({
                'time': datetime.now(),
                'from': from_code,
                'to': to_code,
                'amount': amount_val,
                'result': converted_amount
            })

            if len(self.conversion_history) > 10:
                self.conversion_history.pop(0)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the amount.")
            self.status_text.set("Error: Invalid input")
        except requests.exceptions.Timeout:
            messagebox.showerror("Timeout", "Request timed out. Please try again.")
            self.status_text.set("Error: Timeout")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"Failed to get exchange rates.\nPlease check your connection.")
            self.status_text.set("Error: Network issue")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            self.status_text.set("Error occurred")

    def swap_currencies(self):
        """Swaps the from and to currencies."""
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()

        if from_curr and to_curr:
            self.from_currency.set(to_curr)
            self.to_currency.set(from_curr)
            self.status_text.set("🔄 Currencies swapped successfully!")

    def clear_fields(self):
        """Clears all input and output fields."""
        self.amount.set("1")
        self.result_text.set("Enter amount and click Convert")
        self.rate_text.set("")
        self.status_text.set("✨ Fields cleared - Ready to convert!")

    def filter_from(self):
        """Filter 'From' currency dropdown based on typed text."""
        typed = self.from_combo.get().upper()
        if not typed or not self.all_currencies:
            self.from_combo['values'] = self.all_currencies
            return
        filtered = [c for c in self.all_currencies if typed in c.upper()]
        self.from_combo['values'] = filtered if filtered else self.all_currencies

    def filter_to(self):
        """Filter 'To' currency dropdown based on typed text."""
        typed = self.to_combo.get().upper()
        if not typed or not self.all_currencies:
            self.to_combo['values'] = self.all_currencies
            return
        filtered = [c for c in self.all_currencies if typed in c.upper()]
        self.to_combo['values'] = filtered if filtered else self.all_currencies


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
