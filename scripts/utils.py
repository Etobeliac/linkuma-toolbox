# scripts/utils.py

import openai
import logging
from langdetect import detect

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_api_key(api_key: str):
    """Set the OpenAI API key."""
    openai.api_key = api_key

def create_collections_from_gpt(thematic, product_names):
    """Generate collections using OpenAI GPT based on thematic and product names."""
    try:
        logging.info("Using ChatGPT to create store collections.")

        prompt = (
            f"Create up to a maximum of 30 collections and sub-collections, "
            f"based on the store theme '{thematic}' and my product names "
            f"'{', '.join(product_names)}', for an e-commerce store. "
            f"I want at least 5 categories, but no more than 30, and only the result without additional comments."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )

        collections = response.choices[0].message.content.strip().split("\n")
        logging.info("Collections generated successfully by ChatGPT.")
        return [c.strip() for c in collections if c.strip()]
    except Exception as e:
        logging.error(f"Error calling OpenAI API for collection generation: {e}")
        return []

def categorize_products_with_collections(products, collections):
    categorized_products = {}
    logging.info("Starting product categorization...")

    for product in products:
        categories = []
        for collection in collections:
            if any(word.lower() in product.lower() for word in collection.split()):
                categories.append(collection)

        if not categories:
            categories.append("Miscellaneous / Unspecified")

        categorized_products[product] = categories

    logging.info("Product categorization completed.")
    return categorized_products
