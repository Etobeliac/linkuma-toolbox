import streamlit as st
import importlib.util
import os

# Title of the application
st.title('ToolBox')

# Sidebar for navigation
st.sidebar.header('Menu')

# Dropdown - Adding "Create Collections" Option
option = st.sidebar.selectbox(
    'G-News',
    ['Tutoriel', 'Create Collections']
)

def load_module(module_name, file_path):
    if not os.path.isfile(file_path):
        st.error(f"Le fichier {file_path} est introuvable. Veuillez vérifier le chemin.")
        return None
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

if option == 'Tutoriel':
    # Show tutorial information
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

elif option == 'Create Collections':
    # Path to the script for creating collections
    file_path = os.path.join('scripts', 'creation-collections.py')
    
    # Load and execute the module
    module = load_module('creation_collections', file_path)
    
    # Call the main function of the module if successfully loaded
    if module:
        module.main()

