import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
from datetime import datetime


class CurrencyConverterApp:
    """
    Real-time currency converter with searchable dropdowns and modern UI.
    Data source: exchangerate-api.com
    Supports 160+ world currencies
    """

    def __init__(self, root):
        self.root = root
        self.root.title("💱 Currency Converter Pro")
        self.root.geometry("700x720")
        self.root.resizable(True, True)
        self.root.minsize(650, 650)
        self.root.configure(bg="#e3f2fd")

        # Style Configuration
        self.setup_styles()

        # API Configuration
        self.api_key = os.getenv('EXCHANGE_RATE_API_KEY', '11e6fc7fc66d1d7884aefb8c')
        self.base_url = f"https://v6.exchangerate-api.com/v6/{self.api_key}"

        # Cache
        self.currency_cache = None

        # Mock Data (fallback for offline mode)
        self.mock_currencies = {
            "result": "success",
            "supported_codes": [
                ["USD", "United States Dollar"], ["EUR", "Euro"],
                ["JPY", "Japanese Yen"], ["GBP", "British Pound Sterling"],
                ["AUD", "Australian Dollar"], ["CAD", "Canadian Dollar"],
                ["CHF", "Swiss Franc"], ["CNY", "Chinese Yuan"],
                ["INR", "Indian Rupee"], ["IQD", "Iraqi Dinar"]
            ]
        }

        # Variables
        self.from_currency = tk.StringVar()
        self.to_currency = tk.StringVar()
        self.amount = tk.StringVar(value="1")
        self.result_text = tk.StringVar(value="Enter amount and click Convert")
        self.rate_text = tk.StringVar(value="")
        self.rate_timestamp = tk.StringVar(value="")
        self.status_text = tk.StringVar(value="")
        self.all_currencies = []

        # Create UI and load currencies
        self.create_widgets()
        self.populate_currencies()

    def setup_styles(self):
        """Configure all UI styles."""
        style = ttk.Style()
        style.theme_use('clam')

        # Labels
        style.configure("TLabel", font=("Segoe UI", 10), background="#e3f2fd")
        style.configure("Title.TLabel", font=("Segoe UI", 17, "bold"), background="#e3f2fd", foreground="#0d47a1")
        style.configure("Subtitle.TLabel", font=("Segoe UI", 11), background="#e3f2fd", foreground="#1565c0")

        # Buttons
        style.configure("Accent.TButton", font=("Segoe UI", 12, "bold"), foreground="white",
                        background="#4caf50", borderwidth=0, padding=18)
        style.map("Accent.TButton", background=[('active', '#43a047'), ('pressed', '#2e7d32')])

        style.configure("Clear.TButton", font=("Segoe UI", 11), foreground="white",
                        background="#ff9800", borderwidth=0, padding=15)
        style.map("Clear.TButton", background=[('active', '#f57c00'), ('pressed', '#e65100')])

        style.configure("Swap.TButton", font=("Segoe UI", 16), foreground="white",
                        background="#9c27b0", borderwidth=0, padding=10)
        style.map("Swap.TButton", background=[('active', '#7b1fa2'), ('pressed', '#6a1b9a')])

        # Entry and Combobox
        style.configure("TEntry", font=("Segoe UI", 11), fieldbackground="white", borderwidth=2)
        style.configure("TCombobox", font=("Segoe UI", 10), fieldbackground="white", borderwidth=1)

        # Frames
        style.configure("TFrame", background="#e3f2fd")
        style.configure("Card.TFrame", background="white", relief="raised", borderwidth=2)

    def create_widgets(self):
        """Create all UI widgets."""
        # Gradient background
        canvas = tk.Canvas(self.root, bg="#e3f2fd", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_rectangle(0, 0, 700, 200, fill="#bbdefb", outline="")
        canvas.create_rectangle(0, 200, 700, 470, fill="#d1e7f7", outline="")
        canvas.create_rectangle(0, 470, 700, 720, fill="#e3f2fd", outline="")

        main_frame = ttk.Frame(canvas, padding="40", style="TFrame")
        canvas.create_window(350, 360, window=main_frame)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_columnconfigure(2, weight=0)

        # Title
        title_label = ttk.Label(main_frame, text="💱 Currency Converter Pro", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 5))

        subtitle_label = ttk.Label(main_frame, text="✨ Real-time Exchange Rates • 160+ Currencies ⚡",
                                   style="Subtitle.TLabel")
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 30))

        # Input Card
        input_card = ttk.Frame(main_frame, style="Card.TFrame", padding="30")
        input_card.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 25), ipadx=10, ipady=10)
        input_card.grid_columnconfigure(1, weight=1)

        # Amount
        ttk.Label(input_card, text="💵 Amount", font=("Segoe UI", 11, "bold"),
                  foreground="#0d47a1").grid(row=0, column=0, sticky="w", padx=(0, 15), pady=(0, 10))

        amount_entry = ttk.Entry(input_card, textvariable=self.amount, font=("Segoe UI", 11), width=25)
        amount_entry.grid(row=0, column=1, columnspan=2, sticky="ew", pady=(0, 20), ipady=8)
        amount_entry.bind('<Return>', lambda e: self.perform_conversion())

        # From Currency
        ttk.Label(input_card, text="🌍 From", font=("Segoe UI", 11, "bold"),
                  foreground="#0d47a1").grid(row=1, column=0, sticky="w", padx=(0, 15), pady=(0, 10))

        self.from_combo = ttk.Combobox(input_card, textvariable=self.from_currency,
                                       font=("Segoe UI", 11), width=25)
        self.from_combo.grid(row=1, column=1, sticky="ew", pady=(0, 20), ipady=6)
        self.from_combo.bind('<KeyRelease>', lambda e: self.filter_currencies('from'))

        # Swap Button
        swap_btn = ttk.Button(input_card, text="🔄", style="Swap.TButton", width=3, command=self.swap_currencies)
        swap_btn.grid(row=1, column=2, padx=(15, 0), pady=(0, 20))

        # To Currency
        ttk.Label(input_card, text="🎯 To", font=("Segoe UI", 11, "bold"),
                  foreground="#0d47a1").grid(row=2, column=0, sticky="w", padx=(0, 15), pady=(0, 10))

        self.to_combo = ttk.Combobox(input_card, textvariable=self.to_currency,
                                     font=("Segoe UI", 11), width=25)
        self.to_combo.grid(row=2, column=1, columnspan=2, sticky="ew", ipady=6)
        self.to_combo.bind('<KeyRelease>', lambda e: self.filter_currencies('to'))

        # Buttons
        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.grid(row=3, column=0, columnspan=3, pady=(0, 25), sticky="ew")
        button_frame.grid_columnconfigure(0, weight=2)
        button_frame.grid_columnconfigure(1, weight=1)

        ttk.Button(button_frame, text="⚡ CONVERT NOW ⚡", style="Accent.TButton",
                   command=self.perform_conversion).grid(row=0, column=0, padx=(0, 15), sticky="ew", ipady=8)

        ttk.Button(button_frame, text="🗑️ Clear", style="Clear.TButton",
                   command=self.clear_fields).grid(row=0, column=1, sticky="ew", ipady=8)

        # Result Card
        result_card = ttk.Frame(main_frame, style="Card.TFrame", padding="35")
        result_card.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(0, 15), ipadx=15, ipady=15)

        tk.Label(result_card, textvariable=self.result_text, font=("Segoe UI", 16, "bold"),
                 wraplength=550, bg="white", fg="#2e7d32", justify="center").pack(pady=(0, 12))

        tk.Label(result_card, textvariable=self.rate_text, font=("Segoe UI", 11),
                 bg="white", fg="#546e7a", justify="center").pack()

        tk.Label(result_card, textvariable=self.rate_timestamp, font=("Segoe UI", 9),
                 bg="white", fg="#95a5a6", justify="center").pack(pady=(5, 0))

        # Status & Info
        ttk.Label(main_frame, textvariable=self.status_text, font=("Segoe UI", 10),
                  foreground="#1976d2", justify="center").grid(row=5, column=0, columnspan=3, pady=(0, 5))

        ttk.Label(main_frame, text="📊 Data source: exchangerate-api.com | Powered by Python & Tkinter",
                  font=("Segoe UI", 8), foreground="#95a5a6").grid(row=6, column=0, columnspan=3)

    def populate_currencies(self):
        """Fetch and populate currency list from API."""
        if self.currency_cache:
            self.from_combo['values'] = self.currency_cache
            self.to_combo['values'] = self.currency_cache
            self.from_combo.set("USD - United States Dollar")
            self.to_combo.set("IQD - Iraqi Dinar")
            return

        try:
            self.status_text.set("Loading currencies...")
            self.root.update()

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
                self.to_combo.set("IQD - Iraqi Dinar")
                self.status_text.set("✅ Ready! 160+ currencies loaded")
            else:
                raise Exception("API returned error")

        except Exception as e:
            self.status_text.set("⚠️ Using offline mode (limited currencies)")
            currencies = [f"{code} - {name}" for code, name in self.mock_currencies['supported_codes']]
            self.currency_cache = currencies
            self.all_currencies = currencies
            self.from_combo['values'] = currencies
            self.to_combo['values'] = currencies
            self.from_combo.set("USD - United States Dollar")
            self.to_combo.set("IQD - Iraqi Dinar")

    def perform_conversion(self):
        """Perform real-time currency conversion via API."""
        try:
            # Input validation
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

            # Same currency check
            if from_code == to_code:
                self.result_text.set(f"{amount_val:.2f} {from_code} = {amount_val:.2f} {to_code}")
                self.rate_text.set("Exchange Rate: 1.00 (same currency)")
                self.status_text.set("")
                return

            self.status_text.set("🔄 Converting...")
            self.root.update()

            # Make API request
            response = requests.get(f"{self.base_url}/pair/{from_code}/{to_code}/{amount_val}", timeout=10)
            response.raise_for_status()
            data = response.json()

            if data['result'] == 'success':
                converted_amount = data['conversion_result']
                exchange_rate = data.get('conversion_rate', converted_amount / amount_val)
            else:
                raise Exception("Conversion failed")

            # Display results
            self.result_text.set(f"{amount_val:.2f} {from_code} = {converted_amount:.2f} {to_code}")
            self.rate_text.set(f"Exchange Rate: 1 {from_code} = {exchange_rate:.4f} {to_code}")
            current_time = datetime.now()
            self.rate_timestamp.set(f"📅 Rate fetched: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            self.status_text.set("✅ Conversion complete!")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            self.status_text.set("❌ Invalid input")
        except requests.exceptions.Timeout:
            messagebox.showerror("Timeout", "Request timed out. Please try again.")
            self.status_text.set("❌ Timeout")
        except Exception as e:
            messagebox.showerror("Error", "Could not complete conversion.\nCheck your internet connection.")
            self.status_text.set("❌ Connection error")

    def swap_currencies(self):
        """Swap the 'from' and 'to' currencies."""
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()

        if from_curr and to_curr:
            self.from_currency.set(to_curr)
            self.to_currency.set(from_curr)
            self.status_text.set("🔄 Currencies swapped!")

    def clear_fields(self):
        """Clear all input and output fields."""
        self.amount.set("1")
        self.result_text.set("Enter amount and click Convert")
        self.rate_text.set("")
        self.rate_timestamp.set("")
        self.status_text.set("✨ Fields cleared!")

    def filter_currencies(self, combo_type):
        """Filter currency dropdown based on user typing (search feature)."""
        combo = self.from_combo if combo_type == 'from' else self.to_combo
        typed = combo.get().upper()

        if not typed or not self.all_currencies:
            combo['values'] = self.all_currencies
            return

        filtered = [c for c in self.all_currencies if typed in c.upper()]
        combo['values'] = filtered if filtered else self.all_currencies


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
