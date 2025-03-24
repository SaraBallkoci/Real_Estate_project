import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import folium
from streamlit_folium import st_folium
import numpy as np

# Load Data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(r"C:\Users\User\Desktop\datapipeline\tirane_sale_cleaned.csv")
        print(df)
        df.columns = df.columns.str.strip()

        # ✅ Convert numeric values correctly
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
        df["SqFt"] = pd.to_numeric(df["SqFt"], errors="coerce")

        return df
    except Exception as e:
        st.error(f"⚠️ Error loading data: {str(e)}")
        return pd.DataFrame()  # Return an empty DataFrame if error occurs
  

df = load_data()

# Streamlit UI
st.title("🏡 Tirana Real Estate Dashboard")
st.write("Analyze real estate trends in Tirana using interactive visualizations.")

# Sidebar Filters
st.sidebar.header("🔍 Filter Listings")

# Show all properties button
show_all = st.sidebar.checkbox("Show All Properties", value=False)

if show_all:
    filtered_df = df  # Show all properties
else:
    # Determine the max price dynamically and round up to the next 1 million
    min_price_value = max(5, df["Price"].min())  # Ensure minimum is at least 1,000
    max_price_value = np.ceil(df["Price"].max() / 1_000_000) * 1_000_000  # Round up to next 1M

    # Price Slider
    min_price, max_price = st.sidebar.slider(
        "Select Price Range (€)", 
        min_value=int(min_price_value), 
        max_value=int(max_price_value), 
        value=(int(min_price_value), int(max_price_value)),
        format="%d€"
    )

    # Bedrooms: Round up to the next multiple of 5
    #min_beds = 1
    #max_beds = int(np.ceil(df["Beds"].max() / 5) * 5)

    # Square Footage: Ensure a sensible range
    min_sqft = 50
    max_sqft = int(np.ceil(df["SqFt"].max() / 10_000) * 10_000)

    # Filters
    #selected_beds = st.sidebar.slider("Bedrooms", min_beds, max_beds, (1, 5))
    selected_sqft = st.sidebar.slider("Square Footage", min_sqft, max_sqft, (50, 5000))

    # Apply Filters
    filtered_df = df[
        (df["Price"] >= min_price) & (df["Price"] <= max_price) &
       # (df["Beds"] >= selected_beds[0]) & (df["Beds"] <= selected_beds[1]) &
        (df["SqFt"] >= selected_sqft[0]) & (df["SqFt"] <= selected_sqft[1])
        
    ]
    show_top_5_cheap = st.sidebar.checkbox("Show Top 10 Cheapest", value=False)
    if show_top_5_cheap:
        filtered_df = df.nsmallest(10, 'Price')
        
    show_top_5_expensive = st.sidebar.checkbox("Show Top 10 Most Expensive", value=False)
    if show_top_5_expensive:
        filtered_df = df.nlargest(10, 'Price')


# Display Data Table with Interactive Selection
st.subheader(f"📊 {len(filtered_df)} Listings Found")

# Create an interactive table where users can select a row
selected_rows = st.data_editor(
    filtered_df[["Price", "Address","SqFt","Link"]]	
    .sort_values(by="Price", ascending=False)
    .reset_index(drop=True),
    use_container_width=True,  # Makes the table responsive
    height=400,
    num_rows="dynamic",
    hide_index=True,  # Hides the index column
    column_config={"Link": st.column_config.LinkColumn()},  # Make links clickable
    key="table_selection"
)

# Get selected address (if any)
selected_address = selected_rows.iloc[0]["Address"] if not selected_rows.empty else None

# Price Distribution
st.subheader("💰 Price Distribution")
with st.container():
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Plot histogram
    sns.histplot(filtered_df["Price"], bins=30, kde=True, ax=ax)

    # Format x-axis: Convert to millions and append "M"
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'€{x/100_000:.0f}00000'))

    ax.set_xlabel("Price (€)")
    ax.set_ylabel("Count")
    st.pyplot(fig)

# Beds/Baths Analysis
#st.subheader("🛏️ Bedrooms & 🛁 Bathrooms Distribution")
#with st.container():
   # fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    #sns.countplot(x="Beds", data=filtered_df, ax=ax[0], hue="Beds", palette="Blues", legend=False)
    #ax[0].set_title("Number of Bedrooms")
   # ax[0].set_xlabel("Beds")

  #  sns.countplot(x="Baths", data=filtered_df, ax=ax[1], hue="Baths", palette="Reds", legend=False)
 #   ax[1].set_title("Number of Bathrooms")
#    ax[1].set_xlabel("Baths")

#    st.pyplot(fig)


st.write("Data Source: Century 21")