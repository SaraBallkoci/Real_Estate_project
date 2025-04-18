
## Tirana Real Estate Analysis Dashboard

## Overview
This project scrapes, analyzes, and visualizes real estate data from a website, focusing on properties for sale in Tirana. It includes a web scraper, data cleaning pipeline, and an interactive Streamlit dashboard.

## Features
- Web scraping of websites like Century 21 and Remax property listings
- Data cleaning and preprocessing
- Interactive dashboard with:
  - Price range filtering
  - Square footage filtering
  - Neighborhood selection
  - Top 10 cheapest/most expensive properties view
  - Property distribution visualizations
  - Downloadable filtered data

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Data Collection
Run the scraper to collect property data:
```bash
python scraper.py
```

### 2. Data Cleaning
Process the raw data:
```bash
python analyze.py
```

### 3. Launch Dashboard
Start the Streamlit dashboard:
```bash
streamlit run dashboard.py
```
![Example Image](https://github.com/SaraBallkoci/Real_Estate_project/blob/main/dashboard.PNG)
## Data Structure
The dataset includes the following information for each property:
- Price (in EUR)
- Address
- Square Footage (m²)
- Property Link
- Image URL
- Neighborhood (derived from address)

## Requirements
See requirements.txt for complete list of dependencies.

## Notes
- The scraper includes random delays and user agent rotation to avoid blocking
- Data is cached in the dashboard for better performance
- Filtered data can be downloaded as CSV

## Data Source
All data is sourced from Century 21 Albania and Remax's website.
```
