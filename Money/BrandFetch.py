import requests
import csv
import io

# --- Paste your BrandFetch API key here ---
# Get your free key from https://brandfetch.com/
API_KEY = "NYLCgMd6CD/gur1N62/QehLDC6KW8whx/bf/pn9TcAY=" 

# The transaction data you provided
csv_data = """Type,Product,Started Date,Completed Date,Description,Amount,Fee,Currency,State,Balance
Card Payment,Current,2024-12-30 16:16:02,2025-01-01 06:56:56,McDonald's,-11.80,0.00,EUR,COMPLETED,1467.83
Card Payment,Current,2024-12-31 19:55:30,2025-01-01 14:03:07,Coccinelle Supermarché,-12.75,0.00,EUR,COMPLETED,1455.08
Card Payment,Current,2025-01-01 20:21:51,2025-01-02 06:48:57,Evry Mini market,-3.98,0.00,EUR,COMPLETED,1451.10
Deposit,Current,2025-01-03 03:00:47,2025-01-03 03:00:48,Payment from UNIVERSITAT SIEGEN KOR,1400.00,0.00,EUR,COMPLETED,2851.10
Card Payment,Current,2025-01-03 21:50:51,2025-01-04 10:21:32,L'epicerie Du Po,-3.70,0.00,EUR,COMPLETED,2847.40
Card Payment,Current,2025-01-03 11:06:24,2025-01-04 10:38:52,Evry Mini market,-8.32,0.00,EUR,COMPLETED,2839.08
"""

def get_brand_category(description):
    """
    Searches for a brand using the BrandFetch API and returns its category.
    """
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        return "API Key not set"

    # The BrandFetch search endpoint
    url = f"https://api.brandfetch.io/v2/search/{description}"
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)
        
        data = response.json()
        
        # Check if the search returned any results
        if data and isinstance(data, list) and len(data) > 0:
            # Use the first result
            brand_info = data[0]
            # The 'tags' field is a good source for a category
            if brand_info.get('tags') and len(brand_info['tags']) > 0:
                # Capitalize the first tag to make it look nice
                return brand_info['tags'][0].capitalize()
            else:
                return "Uncategorized"
        else:
            return "Not Found"
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the API request: {e}")
        return "API Error"
    except (KeyError, IndexError):
        # Handle cases where the response format is unexpected
        return "Invalid Response"

# Use io.StringIO to treat the string data as a file
data_file = io.StringIO(csv_data)

# Read the CSV data
csv_reader = csv.reader(data_file)

# Get the header row to find the 'Description' column index
header = next(csv_reader)
try:
    description_index = header.index('Description')
except ValueError:
    print("Error: 'Description' column not found in the data.")
    exit()

print(f"{'Description':<40} | {'Category'}")
print("-" * 60)

# Process each transaction
for row in csv_reader:
    description = row[description_index]
    category = get_brand_category(description)
    print(f"{description:<40} | {category}")