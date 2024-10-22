# scripts/utils.py

import openai
import logging
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
        logging.info("Utilisation de ChatGPT pour créer des collections.")

        prompt = (
            f"Créer jusqu'à un maximum de 30 collections et sous-collections, "
            f"en fonction de la thématique de la boutique '{thematic}' et des noms de mes produits "
            f"'{', '.join(product_names)}', pour une boutique e-commerce. "
            f"Je veux au moins 5 catégories, mais pas plus de 30, et uniquement le résultat sans commentaires supplémentaires."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )

        collections = response.choices[0].message.content.strip().split("\n")
        logging.info("Collections générées avec succès par ChatGPT.")
        
        # Enlever les accents des noms de collections
        return [remove_accents(c.strip()) for c in collections if c.strip()]
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
