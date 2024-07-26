#coding: utf-8

# import pkg_resources
from os import path

def read_text_file(file_path: str) -> str|None:
    if not path.exists(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} est manquant")
    
    with open(file_path, 'r') as in_file:
        return in_file.read()