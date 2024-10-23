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
            "Je veux au moins 5 catégories, mais pas plus de 30, et uniquement le résultat sans commentaires supplémentaires."
        )

        logging.info(f"Prompt envoyé à OpenAI: {prompt}")

        # Appel à l'API OpenAI avec la nouvelle méthode basée sur `openai.ChatCompletion`
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Spécifie le modèle que tu souhaites utiliser
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )

        # Vérifier et enregistrer la réponse brute de l'API
        logging.info(f"Réponse brute de l'API: {response}")

        if response and response.choices:
            collections = response.choices[0].message['content'].strip().split("\n")
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
