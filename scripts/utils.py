# scripts/utils.py

import streamlit as st
import openai
import logging
import pandas as pd
import unicodedata

# Configurer le logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def set_api_key(api_key: str):
    """Configurer la clé API OpenAI."""
    openai.api_key = api_key

def remove_accents(input_str):
    """Supprime les accents d'une chaîne de caractères."""
    return ''.join(
        (c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn')
    )

def create_collections_from_gpt(thematic, product_names):
    """Générer des collections basées sur le thème et les noms des produits."""
    try:
        logging.info("Début de la génération des collections avec GPT...")
        logging.info(f"Thématique: {thematic}")
        logging.info(f"Noms de produits: {product_names}")

        prompt = (
            f"Créer jusqu'à un maximum de 30 collections et sous-collections, "
            f"en fonction de la thématique de la boutique '{thematic}' et des noms de mes produits "
            f"'{', '.join(product_names)}', pour une boutique e-commerce. "
            f"Je veux au moins 5 catégories, mais pas plus de 30, et uniquement le résultat sans commentaires supplémentaires."
        )

        logging.info(f"Prompt envoyé à OpenAI: {prompt}")

        # Appel à l'API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )

        # Vérifier et enregistrer la réponse brute de l'API
        logging.info(f"Réponse brute de l'API: {response}")

        if response and response.choices:
            collections = response.choices[0].message.content.strip().split("\n")
            logging.info("Collections générées avec succès par GPT.")
            logging.info(f"Collections: {collections}")

            # Enlever les accents des noms de collections
            return [remove_accents(c.strip()) for c in collections if c.strip()]
        else:
            logging.warning("Aucune réponse valide reçue de GPT.")
            return []
    except Exception as e:
        logging.error(f"Erreur lors de l'appel à l'API OpenAI : {e}")
        return []

def categorize_products_with_collections(products, collections):
    """Catégoriser les produits selon les collections générées."""
    categorized_products = {}
    logging.info("Début de la catégorisation des produits...")

    for product in products:
        categories = []
        for collection in collections:
            if any(word.lower() in product.lower() for word in collection.split()):
                categories.append(collection)

        if not categories:
            categories.append("Divers / Non Spécifié")

        categorized_products[product] = categories

    logging.info("Catégorisation terminée.")
    return categorized_products

def run_create_and_categorize():
    """Exécuter la fonctionnalité de création et catégorisation."""
    st.sidebar.title("Navigation")
    option = st.sidebar.selectbox(
        "Choisissez une opération:",
        ("Sélectionnez", "Créer et catégoriser des collections")
    )

    if option == "Créer et catégoriser des collections":
        st.title("Créer et catégoriser des collections")

        # Champs de saisie utilisateur
        api_key = st.text_input("Entrez votre clé API OpenAI", type="password")
        store_thematic = st.text_input("Entrez la thématique de la boutique")
        products_input = st.text_area("Entrez les produits (séparés par des virgules)")

        # Bouton pour lancer le processus
        if st.button("Lancer le processus"):
            if not api_key or not store_thematic or not products_input:
                st.error("Merci de fournir tous les champs requis, y compris la clé API !")
            else:
                # Configure la clé API OpenAI
                set_api_key(api_key)

                # Préparer la liste des produits
                product_list = [p.strip() for p in products_input.split(",")]

                # Générer les collections avec GPT
                collections = create_collections_from_gpt(store_thematic, product_list)

                # Vérifier si des collections ont été générées
                if not collections:
                    st.warning("Aucune collection générée. Merci de réessayer.")
                else:
                    # Afficher le tableau des collections générées avec pandas
                    st.subheader("Collections générées")
                    collections_df = pd.DataFrame({"Collection": collections})
                    st.table(collections_df)

                    # Catégoriser les produits dans les collections générées
                    categorized_products = categorize_products_with_collections(product_list, collections)

                    # Préparer les données pour l'affichage des résultats de la catégorisation avec pandas
                    categorized_table = [
                        {
                            "Produit": product,
                            "Collections": ", ".join(categories)
                        }
                        for product, categories in categorized_products.items()
                    ]
                    
                    categorized_df = pd.DataFrame(categorized_table)

                    # Afficher le tableau de produits catégorisés
                    st.subheader("Produits catégorisés")
                    st.table(categorized_df)
