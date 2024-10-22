# streamlit_app.py

import streamlit as st
from scripts import utils

# Configurer Streamlit
st.set_page_config(page_title="E-commerce App", layout="wide")

# Sidebar avec menu déroulant pour la navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox(
    "Choisissez une opération:",
    ("Sélectionnez", "Créer et catégoriser des collections")
)

# Logique pour la sélection des fonctionnalités
if option == "Créer et catégoriser des collections":
    # Demander la clé API OpenAI via la barre latérale pour des raisons de sécurité
    api_key = st.sidebar.text_input("Entrez votre clé API OpenAI", type="password")

    # Champs de saisie utilisateur pour le thème et les produits
    store_thematic = st.text_input("Entrez la thématique de la boutique")
    products_input = st.text_area("Entrez les produits (séparés par des virgules)")

    if st.button("Lancer le processus"):
        if not api_key or not store_thematic or not products_input:
            st.error("Merci de fournir tous les champs requis, y compris la clé API !")
        else:
            # Configure la clé API OpenAI
            utils.set_api_key(api_key)

            # Préparer la liste des produits
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
                        "Collections": ", ".join(categories)
                    }
                    for product, categories in categorized_products.items()
                ]

                # Afficher le tableau de produits catégorisés
                st.subheader("Produits catégorisés")
                st.table(categorized_table)
else:
    st.write("Veuillez sélectionner une opération à partir du menu déroulant à gauche.")
