import openai
import logging
import streamlit as st

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_api_key():
    """Retrieve the API key from Streamlit input."""
    return st.text_input("Entrez votre clé API OpenAI :", type="password")

def get_store_thematic():
    """Get store thematic from Streamlit input."""
    return st.text_input("Entrez la thématique de la boutique :")

def get_product_list():
    """Get a list of products from Streamlit input."""
    products_input = st.text_area("Entrez les produits de la boutique (séparés par des virgules) :")
    return [p.strip() for p in products_input.split(",") if p.strip()]

def create_collections_from_gpt(thematic, product_names):
    """Generate collections using OpenAI's GPT."""
    try:
        logging.info("Utilisation de ChatGPT pour créer les collections de la boutique.")
        prompt = (
            f"Créer jusqu'à un maximum de 30 collections et sous-collections, "
            f"en fonction de la thématique de la boutique '{thematic}' et des noms de mes produits "
            f"'{', '.join(product_names)}', pour une boutique e-commerce. "
            f"Je veux au moins 5 catégories, mais pas plus de 30, et uniquement le résultat sans commentaires supplémentaires."
        )
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500  # Adjust if needed
        )
        collections = response.choices[0].message.content.strip().split("\n")
        return [c.strip() for c in collections if c.strip()]
    except Exception as e:
        logging.error(f"Erreur lors de l'appel à l'API OpenAI pour la génération de collections : {e}")
        return []

def main():
    # Set up the Streamlit UI and logic
    openai.api_key = get_api_key()
    store_thematic = get_store_thematic()
    product_list = get_product_list()
    
    if st.button("Générer les collections"):
        if not openai.api_key or not store_thematic or not product_list:
            st.warning("Veuillez remplir tous les champs requis.")
        else:
            collections = create_collections_from_gpt(store_thematic, product_list)
            if collections:
                st.subheader("Collections générées par ChatGPT :")
                for collection in collections:
                    st.write(f"- {collection}")
            else:
                st.warning("Aucune collection générée par ChatGPT.")

if __name__ == "__main__":
    main()

