# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# App title
st.title("Customize your smoothie 🥤")
st.write("Choose the fruits you want in your custom smoothie!")

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# User input
name_on_order = st.text_input("Name of the smoothie:")
st.write("The Name of the smoothie will be:", name_on_order)

# Get fruit options
fruit_df = (
    session
    .table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"))
    .to_pandas()
)

fruit_list = fruit_df["FRUIT_NAME"].tolist()

# Multiselect
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Insert order
if ingredients_list and name_on_order:
    ingredients_string = " ".join(ingredients_list)

    st.write("Your smoothie ingredients:")
    st.write(ingredients_string)

    insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    if st.button("Submit order"):
        session.sql(insert_stmt).collect()
        st.success("Your Smoothie is ordered! ✅")

# External API call
smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)

st.subheader("Smoothiefroot API response")
st.json(smoothiefroot_response.json())
