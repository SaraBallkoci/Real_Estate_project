import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re

# Load the dataset
df = pd.read_csv(r"C:\Users\User\Documents\GitHub\Real_Estate_project\tirana_forsale.csv")

# Display basic info about the dataset
def inspect_data(df):
    print("\nData Overview:")
    print(df.info())
    print("\nFirst Few Rows:")
    print(df.head())

# Handle missing data
def clean_data(df):
    print("\nHandling Missing Data...")
    
    # Replace invalid values
    df.replace({'—': np.nan, 'N/A': np.nan, '': np.nan, 'Price upon request': np.nan}, inplace=True)

    # Drop rows with missing essential values (Price, Beds, Baths, SqFt)
    df.dropna(subset=["Price", "Address", "SqFt"], inplace=True)
    
    # Reset index
    df.reset_index(drop=True, inplace=True)
    
    df.drop_duplicates(subset=["Price", "Address", "SqFt"], inplace=True)
    
    print(f"Cleaned Data: {len(df)} rows remaining.")
    return df

def extract_numeric(value):
    """ Extracts numeric values from a string. Handles cases like '1 bed', '2 baths', 'Studio' """
    if isinstance(value, str):
        match = re.search(r'\d+', value)  # Find first numeric value
        return float(match.group()) if match else np.nan  # Convert to float, otherwise NaN
    return np.nan  # Return NaN for non-string values

def convert_columns(df):
    print("Converting Columns...")
    
    # Strip whitespace from all columns
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Convert Price column: Remove "$" and "," then convert to float
    df['Price'] = df['Price'].str.replace('[€,]', '', regex=True).replace('', np.nan).astype(float)
    
    # Convert SqFt column: Replace non-numeric characters, handle empty values
    df['SqFt'] = df['SqFt'].replace(['—', '', 'N/A'], np.nan)  # Handle missing values
    df['SqFt'] = df['SqFt'].str.replace(r'\s*m2', '', regex=True)
    df['SqFt'] = pd.to_numeric(df['SqFt'], errors='coerce')  # Convert to float safely
    
    # Convert Beds & Baths: Extract numbers from text and convert to float
    #df['Beds'] = df['Beds'].apply(extract_numeric)
  
    
    print("Data Cleaning Complete!")
    return df

# Generate summary statistics
def summarize_data(df):
    print("\nSummary Statistics:")
    print(df.describe())

# Plot price distribution
def plot_price_distribution(df):
    plt.figure(figsize=(10,5))
    sns.histplot(df['Price'], bins=30, kde=True)
    plt.xlabel("Price (in euros)")
    plt.ylabel("Count")
    plt.title("Price Distribution of Listings")
    plt.show()

# Analyze Beds/Baths
"""def analyze_beds_baths(df):
    plt.figure(figsize=(10,5))
    sns.countplot(x='Beds', data=df, order=sorted(df['Beds'].dropna().unique()))
    plt.xlabel("Number of Bedrooms")
    plt.ylabel("Count")
    plt.title("Distribution of Bedrooms in Listings")
    plt.show()
    
    plt.figure(figsize=(10,5))
    sns.countplot(x='Baths', data=df, order=sorted(df['Baths'].dropna().unique()))
    plt.xlabel("Number of Bathrooms")
    plt.ylabel("Count")
    plt.title("Distribution of Bathrooms in Listings")
    plt.show()
    """



# Top & Bottom Listings
def show_extreme_listings(df):
    print("\nTop 5 Most Expensive Listings:")
    print(df.nlargest(5, 'Price'))
    print("\nTop 5 Cheapest Listings:")
    print(df.nsmallest(5, 'Price'))

# Run analysis
if __name__ == "__main__":
    inspect_data(df)
    df = clean_data(df)
    df = convert_columns(df)
   # df = handle_missing_geo(df)
    summarize_data(df)
    plot_price_distribution(df)
    #analyze_beds_baths(df)
    show_extreme_listings(df)
    
    # Save the cleaned dataset
    df.to_csv(r"C:\Users\User\Documents\GitHub\Real_Estate_project\tirane_sale_cleaned.csv", index=False)
    print("Cleaned data saved as 'tirane_sale_cleaned.csv'.")
