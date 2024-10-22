# streamlit_app.py

import streamlit as st
from scripts import utils

st.set_page_config(page_title="E-commerce Collection Generator", layout="wide")

# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox(
    "Choose an operation:",
    ("Select", "Generate Collections", "Categorize Products")
)

if option == "Generate Collections":
    st.title("Generate Collections")
    
    # User inputs for this section
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    store_thematic = st.text_input("Enter Store Theme")
    products_input = st.text_area("Enter Products (comma-separated)")
    
    if st.button("Generate"):
        if not api_key or not store_thematic or not products_input:
            st.error("Please provide all inputs!")
        else:
            # Set OpenAI API Key
            utils.get_api_key(api_key)
            
            # Prepare product list
            product_list = [p.strip() for p in products_input.split(",")]
            
            # Generate collections
            collections = utils.create_collections_from_gpt(store_thematic, product_list)
            
            if not collections:
                st.warning("No collections generated. Please try again.")
            else:
                st.subheader("Generated Collections")
                st.write("\n".join(collections))

elif option == "Categorize Products":
    st.title("Categorize Products")
    
    # User inputs for this section
    products_input = st.text_area("Enter Products (comma-separated)")
    collections_input = st.text_area("Enter Collections (comma-separated)")
    
    if st.button("Categorize"):
        if not products_input or not collections_input:
            st.error("Please provide all inputs!")
        else:
            # Prepare lists
            product_list = [p.strip() for p in products_input.split(",")]
            collections = [c.strip() for c in collections_input.split(",")]
            
            # Categorize products
            categorized_products = utils.categorize_products_with_collections(product_list, collections)
            
            st.subheader("Categorized Products")
            for product, categories in categorized_products.items():
                st.write(f"{product}: {', '.join(categories)}")
else:
    st.write("Please select an option from the sidebar to begin.")

