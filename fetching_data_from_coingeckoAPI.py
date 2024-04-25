import requests
import pandas as pd

def fetch_opening_price_data(coin_id):
    # Define the CoinGecko API endpoint for historical price data
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    
    # Define the parameters for fetching 5 years of data
    params = {
        "vs_currency": "inr",  # You can change the currency here if needed
        "days": 1800,  # 5 years (365 days * 5)
        "interval": "daily"  # Daily interval
    }
    
    # Fetch data from the CoinGecko API
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        opening_prices = [entry[1] for entry in data["prices"]]
        timestamps = [entry[0] for entry in data["prices"]]
        df = pd.DataFrame({"Timestamp": timestamps, "Opening Price (USD)": opening_prices})
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="ms")  # Convert timestamp to datetime
        return df
    else:
        print("Failed to fetch data")
        return None

# Fetch opening price data for a particular cryptocurrency (e.g., Bitcoin)
coin_id = "shiba-inu"
opening_price_data = fetch_opening_price_data(coin_id)

# Check if data is fetched successfully
if opening_price_data is not None:
    # Define the path to save the Excel file
    excel_file_path = f"{coin_id}_opening_price_data_new1.xlsx"

    # Save data to Excel file
    opening_price_data.to_excel(excel_file_path, index=False)
    print("Opening price data saved to:", excel_file_path)
else:
    print("No data fetched. Exiting...")
