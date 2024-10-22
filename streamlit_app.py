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
    Loading
    """)

elif option == 'Create Collections':
    # Path to the script for creating collections
    file_path = os.path.join('scripts', 'creation-collections.py')
    
    # Load and execute the module
    module = load_module('creation_collections', file_path)
    
    # Call the main function of the module if successfully loaded
    if module:
        module.main()

