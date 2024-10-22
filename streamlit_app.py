# streamlit_app.py

import streamlit as st
from scripts import utils

st.set_page_config(page_title="E-commerce Collection Generator", layout="wide")

# Sidebar for inputs
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("Entrez votre clé API OpenAI", type="password")
store_thematic = st.sidebar.text_input("Entrez la thématique de la boutique")
products_input = st.sidebar.text_area("Entrez les produits (séparés par des virgules)")

# Bouton pour exécuter tout le processus en un seul clic
if st.sidebar.button("Créer et catégoriser"):
    if not api_key or not store_thematic or not products_input:
        st.error("Merci de fournir tous les champs requis !")
    else:
        # Configure la clé API OpenAI
        utils.set_api_key(api_key)
        
        # Préparer la liste de produits
        product_list = [p.strip() for p in products_input.split(",")]
        
        # Générer les collections avec GPT
        collections = utils.create_collections_from_gpt(store_thematic, product_list)
        
        # Vérifier si des collections ont été générées
        if not collections:
            st.warning("Aucune collection générée. Merci de réessayer.")
        else:
            # Afficher le tableau des collections générées
            st.subheader("Collections générées")
            collections_table = [{"Collection": c} for c in collections]
            st.table(collections_table)
            
            # Catégoriser les produits dans les collections générées
            categorized_products = utils.categorize_products_with_collections(product_list, collections)
            
            # Préparer les données pour l'affichage des résultats de la catégorisation
            categorized_table = [
                {
                    "Produit": product,
                    "Collections": ", ".join(categories)  # Joindre sans accents
                }
                for product, categories in categorized_products.items()
            ]
            
            # Afficher le tableau de produits catégorisés
            st.subheader("Produits catégorisés")
            st.table(categorized_table)
