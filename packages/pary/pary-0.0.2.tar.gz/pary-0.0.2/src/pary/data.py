"""
pary.data
=====

Specific data functions.
"""


# Importing the required libraries
import os
import pandas as pd


# -------------------------------------------------------
# Import data
# -------------------------------------------------------


def import_data(path=None, sep=''):

    path_tree = get_path_tree(path)

    data = load_path_tree(path_tree)

    return data


def get_path_tree(repertoire):
    """
    Create a dictionary of the directory structure of a folder.
    This function load only .csv file
    """
    # Fonction pour ajouter récursivement des chemins au dictionnaire
    def add_path(chemin, path_tree):

        for name in os.listdir(chemin):

            # Complete path
            complete_path = os.path.join(chemin, name)

            # Check if folder
            if os.path.isdir(complete_path):

                # Créer un sous-dictionnaire pour un dossier
                path_tree[name] = {}

                # Appel récursif pour remplir le sous-dictionnaire
                add_path(complete_path, path_tree[name])

            elif name.endswith('.csv'):
                path_tree[name] = complete_path  # Ajouter le chemin complet pour un fichier

    path_tree = {}

    add_path(repertoire, path_tree)

    return path_tree


def load_path_tree(path_tree):
    """
    Load a file from the path_tree dictionary.
    """
    for key, value in path_tree.items():

        if isinstance(value, dict):
            path_tree[key] = load_path_tree(value)

        elif isinstance(value, str):
            path_tree[key] = pd.read_csv(path_tree[key], dtype=str)

    return path_tree


# -------------------------------------------------------
# Main
# -------------------------------------------------------


if __name__ == "__main__":
    path = r"C:\Users\MClavier\Documents\WORK\MAP_FIN_LH17"
    data = import_data(path)
