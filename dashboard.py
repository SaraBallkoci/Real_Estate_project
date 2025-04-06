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
        df = pd.read_csv("tirane_sale_cleaned.csv")
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
df["Neighborhood"] = df["Address"].str.split(",").str[0].str.strip()

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
    min_price_value = int(df["Price"].min())  # e.g., 25,000
    max_price_value = int(df["Price"].max())  # e.g., 2,000,000

    min_price, max_price = st.sidebar.slider(
        "Select Price Range (€)",
        min_value=min_price_value,
        max_value=max_price_value,
        value=(min_price_value, max_price_value),
        step=5000,  # Adjust as needed
        format="%d€"
    )
    # Bedrooms: Round up to the next multiple of 5
    #min_beds = 1
    #max_beds = int(np.ceil(df["Beds"].max() / 5) * 5)

    # Square Footage: Ensure a sensible range
    min_sqft = int(df["SqFt"].min())
    max_sqft = int(df["SqFt"].max())  # 565

    selected_sqft = st.sidebar.slider(
    "Square Footage (m²)",
    min_value=min_sqft,
    max_value=max_sqft,
    value=(min_sqft, max_sqft),
    step=10
)

    show_top_5_cheap = st.sidebar.checkbox("Show Top 10 Cheapest", value=False)
    if show_top_5_cheap:
            filtered_df = df.nsmallest(10, 'Price')

    show_top_5_expensive = st.sidebar.checkbox("Show Top 10 Most Expensive", value=False)
    if show_top_5_expensive:
        filtered_df = df.nlargest(10, 'Price')

    neighborhoods = ["All"] + sorted(df["Neighborhood"].dropna().unique().tolist())
    selected_neighborhood = st.sidebar.selectbox("Select Neighborhood", ["All"] + sorted(df["Neighborhood"].unique().tolist()))

    # Apply Filters
    filtered_df = df[
        (df["Price"] >= min_price) & (df["Price"] <= max_price) &
       # (df["Beds"] >= selected_beds[0]) & (df["Beds"] <= selected_beds[1]) &
        (df["SqFt"] >= selected_sqft[0]) & (df["SqFt"] <= selected_sqft[1])

    ]

    if selected_neighborhood != "All":
        filtered_df = filtered_df[filtered_df["Neighborhood"] == selected_neighborhood]




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


st.subheader("🏘️ Listings by Neighborhood")

top_neighborhoods = (
    filtered_df["Neighborhood"]
    .value_counts()
    .head(10)  # top 10 areas
    .sort_values(ascending=True)
)

fig, ax = plt.subplots(figsize=(8, 5))
top_neighborhoods.plot(kind="barh", ax=ax, color="skyblue")
ax.set_xlabel("Number of Listings")
ax.set_title("Top Neighborhoods in Tirana")
st.pyplot(fig)

# Price Distribution
st.subheader("💰 Price Distribution")
with st.container():
    fig, ax = plt.subplots(figsize=(8, 4))

    # Plot histogram
    sns.histplot(filtered_df["Price"], bins=30, kde=True, ax=ax)

    ax.xaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))

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

# 📥 Download filtered data
st.subheader("⬇️ Download Listings")
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="tirana_filtered_listings.csv",
    mime="text/csv"
)

st.write("Data Source: Century 21")
