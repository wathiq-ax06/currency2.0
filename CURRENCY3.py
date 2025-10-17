def currency_converter():
    """
    A comprehensive currency converter program.
    Rates are illustrative and not live data.
    Base currency for rates is United States Dollar (USD).
    """
    # A dictionary of world currencies {CODE: {'name': 'Full Name', 'rate': Units per 1 USD}}
    # NOTE: These rates are for demonstration purposes only and are not real-time.
    CURRENCIES = {
        'USD': {'name': 'United States Dollar', 'rate': 1.0},
        'EUR': {'name': 'Euro', 'rate': 0.93},
        'JPY': {'name': 'Japanese Yen', 'rate': 157.53},
        'GBP': {'name': 'British Pound', 'rate': 0.79},
        'AUD': {'name': 'Australian Dollar', 'rate': 1.51},
        'CAD': {'name': 'Canadian Dollar', 'rate': 1.37},
        'CHF': {'name': 'Swiss Franc', 'rate': 0.91},
        'CNY': {'name': 'Chinese Yuan', 'rate': 7.24},
        'INR': {'name': 'Indian Rupee', 'rate': 83.51},
        'BRL': {'name': 'Brazilian Real', 'rate': 5.25},
        'RUB': {'name': 'Russian Ruble', 'rate': 88.20},
        'ZAR': {'name': 'South African Rand', 'rate': 18.78},
        'MXN': {'name': 'Mexican Peso', 'rate': 18.38},
        'SGD': {'name': 'Singapore Dollar', 'rate': 1.35},
        'NZD': {'name': 'New Zealand Dollar', 'rate': 1.63},
        'IQD': {'name': 'Iraqi Dinar', 'rate': 1310.0},
        'SAR': {'name': 'Saudi Riyal', 'rate': 3.75},
        'AED': {'name': 'UAE Dirham', 'rate': 3.67},
        'EGP': {'name': 'Egyptian Pound', 'rate': 47.65},
        'TRY': {'name': 'Turkish Lira', 'rate': 32.27},
        'KRW': {'name': 'South Korean Won', 'rate': 1380.55},
        'SEK': {'name': 'Swedish Krona', 'rate': 10.52},
        'NOK': {'name': 'Norwegian Krone', 'rate': 10.60},
        'HKD': {'name': 'Hong Kong Dollar', 'rate': 7.81},
        'IDR': {'name': 'Indonesian Rupiah', 'rate': 16255.0},
        'MYR': {'name': 'Malaysian Ringgit', 'rate': 4.71},
        'PHP': {'name': 'Philippine Peso', 'rate': 58.75},
        'THB': {'name': 'Thai Baht', 'rate': 36.72},
        'VND': {'name': 'Vietnamese Dong', 'rate': 25450.0},
        'PLN': {'name': 'Polish Zloty', 'rate': 3.96},
        'ARS': {'name': 'Argentine Peso', 'rate': 897.25},
        'CLP': {'name': 'Chilean Peso', 'rate': 924.50},
        'COP': {'name': 'Colombian Peso', 'rate': 3925.0},
        # You can continue to add more currencies here...
    }

    # --- Welcome Message ---
    print("=============================================")
    print("      Welcome to the Currency Converter")
    print("=============================================")
    print("Disclaimer: Exchange rates are not live and are for demonstration only.")
    print("Please use standard 3-letter currency codes (e.g., USD, EUR, JPY).")
    print("---------------------------------------------")

    # --- Step 1: Get Amount from User ---
    while True:
        try:
            amount = float(input("Enter the amount to convert: "))
            if amount < 0:
                print("Amount cannot be negative. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # --- Step 2: Get Source Currency ---
    while True:
        from_currency = input("Enter the source currency code (e.g., USD): ").upper()
        if from_currency in CURRENCIES:
            break
        else:
            print(f"Error: '{from_currency}' is not a valid currency code. Please try again.")

    # --- Step 3: Get Target Currency ---
    while True:
        to_currency = input(f"Enter the target currency code (e.g., IQD): ").upper()
        if to_currency in CURRENCIES:
            break
        else:
            print(f"Error: '{to_currency}' is not a valid currency code. Please try again.")

    # --- Conversion Logic ---
    # First, convert the source amount to the base currency (USD)
    # The rate is 'units per 1 USD', so we divide to get the USD value.
    amount_in_usd = amount / CURRENCIES[from_currency]['rate']

    # Second, convert the USD amount to the target currency
    # We multiply by the target currency's rate.
    converted_amount = amount_in_usd * CURRENCIES[to_currency]['rate']

    # --- Display Result ---
    from_name = CURRENCIES[from_currency]['name']
    to_name = CURRENCIES[to_currency]['name']

    print("\n------------------ Result -------------------")
    print(f"{amount:,.2f} {from_name} ({from_currency})")
    print("                is equal to")
    print(f"{converted_amount:,.2f} {to_name} ({to_currency})")
    print("---------------------------------------------")


# Run the converter
if __name__ == "__main__":
    currency_converter()