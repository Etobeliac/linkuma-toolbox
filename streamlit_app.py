import streamlit as st
import scripts.utils as utils

# Menu principal pour choisir l'opération
def main():
    st.sidebar.title("Menu Principal")
    option = st.sidebar.selectbox(
        "Choisissez une option",
        ("Accueil", "Créer et catégoriser des collections")
    )
    
    if option == "Accueil":
        st.title("Bienvenue sur l'application de gestion de collections")
        st.write("Utilisez le menu à gauche pour commencer.")
    elif option == "Créer et catégoriser des collections":
        utils.run_create_and_categorize()

if __name__ == "__main__":
    main()
