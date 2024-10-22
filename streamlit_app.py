import streamlit as st
import importlib.util
import os

# Titre de l'application
st.title('ToolBox')

# Barre latérale pour la navigation
st.sidebar.header('Menu')

# Menu déroulant - Ajouter l'option "Create Collections"
option1 = st.sidebar.selectbox(
    'G-News', 
    ['Tutoriel', 'Create Collections']
)

def load_module(module_name, file_path):
    if not os.path.isfile(file_path):
        st.error(f"Le fichier {file_path} est introuvable. Veuillez vérifier le chemin.")
        st.write(f"Tentative de chargement depuis : {file_path}")  # Information de débogage
        return None
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

if option1 == 'Tutoriel':
    # Afficher un tutoriel ou des explications
    st.header("Tutoriel - Guide d'Utilisation")
    st.write("""
    **Bienvenue dans l'application !**
    
    Cette application vous permet de réaliser différentes tâches via des scripts automatisés :
    
    - **Create Collections** : Crée des collections et catégories pour vos produits en utilisant ChatGPT.
    
    ### Comment Utiliser :
    
    - Sélectionnez "Create Collections" dans le menu latéral pour accéder à cette fonctionnalité.
    - Remplissez les informations nécessaires et lancez le processus pour générer des collections.
    
    *Pour toute question supplémentaire, n'hésitez pas à contacter notre équipe de support.*
    """)

elif option1 == 'Create Collections':
    # Remplacez avec le nouveau chemin du fichier
    file_path = os.path.join('scripts', 'new-creation-collections.py')  # Modifiez le nom du fichier ici
    
    # Afficher le chemin pour le débogage
    st.write(f"Tentative de chargement du module depuis : {file_path}")
    
    # Charger et exécuter le module
    module = load_module('new_creation_collections', file_path)
    
    # Appeler la fonction principale du module si elle est chargée avec succès
    if module:
        module.main()
