# streamlit_app.py

import streamlit as st
from scripts.utils import create_collections_from_gpt, categorize_products_with_collections

st.set_page_config(page_title="E-commerce Collection Generator", layout="wide")

st.sidebar.title("E-commerce App")
st.sidebar.header("Settings")

# Input fields on the sidebar
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
store_thematic = st.sidebar.text_input("Enter Store Theme")
products_input = st.sidebar.text_area("Enter Products (comma-separated)")

# Generate collections button
if st.sidebar.button("Generate Collections"):
    if not api_key or not store_thematic or not products_input:
        st.error("Please provide all inputs!")
    else:
        # Set OpenAI API Key
        create_collections_from_gpt(api_key)
        
        # Process the input
        product_list = [p.strip() for p in products_input.split(",")]
        
        # Generate collections
        collections = create_collections_from_gpt(store_thematic, product_list)
        
        if not collections:
            st.warning("No collections generated. Please try again.")
        else:
            st.subheader("Generated Collections")
            st.write("\n".join(collections))

            # Categorize products
            categorized_products = categorize_products_with_collections(product_list, collections)

            st.subheader("Categorized Products")
            for product, categories in categorized_products.items():
                st.write(f"{product}: {', '.join(categories)}")
