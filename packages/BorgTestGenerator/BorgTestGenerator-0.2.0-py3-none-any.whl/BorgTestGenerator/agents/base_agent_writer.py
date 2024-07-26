#coding: utf-8

from .base_agent import Agent
import os

# from hashlib import sha1

class FilesListToUpload(list):
    def __init__(self, files: list[str] = [],
                 vector_store_name: str|None = None):
        super().__init__(files)
        self.vector_store_name = vector_store_name
    
    def is_empty(self) -> bool:
        return len(self) == 0
    
    def is_unnamed(self) -> bool:
        return (type(self.vector_store_name) == None) or (len(f"{self.vector_store_name}") == 0)

    def add_file(self, filepath: str) -> None:
        self.append(filepath)

    def add_files(self, files: list[str]) -> None:
        for file in files:
            self.add_file(file)

    def remove_file(self, filepath: str) -> None:
        self.remove(filepath)

    def list_files(self) -> list[str]:
        return self
    
    def set_vector_store_name(self, vector_store_name: str) -> None:
        self.vector_store_name = vector_store_name
        
    def get_vector_store_name(self) -> str:
        return self.vector_store_name
    


class BaseAgentWriter(Agent):
    def __init__(self, assistant_id: str|None = None):
        super().__init__(assistant_id)

    def check_and_retreive(self) -> Agent:
        if (type(self.assistant) == None) or (self.assistant.assistant_id == None):
            self.search_and_retreive_assistant()
        return self

    def run_generation(self, 
                       message_from_user: str,
                       vector_store_name: str|None = None, 
                       files_to_upload: list[str]|None = None) -> Agent:
        try:
            print("Début de la génération...")
            if (type(vector_store_name)!=None):
                self.upload_files(vector_store_name, files_to_upload)
            self.create_new_thread()
            self.create_new_user_message(f"{message_from_user}")
            self.run()
            self.print_assistant_result()
            print("Génération terminée avec succès.")
        except FileNotFoundError as fnf_error:
            print(f"Erreur : {fnf_error}")
        except Exception as e:
            print(f"Erreur inattendue : {e}")
        return self

        
    def save_generation(self, 
                        output_filepath: str,
                        language: str|bytes|list|None = ["python"],
                        force_overwrite: bool = False,
                        backup_if_exists: bool = True) -> Agent:
        
        if os.path.exists(output_filepath):
            if force_overwrite:
                os.remove(output_filepath)
            else:
                print(f"Le fichier {output_filepath} existe déjà !")
                return self
            
        print("Sauvegarde de la réponse de l'assistant...")
        success_, saved_filepath = self.save_assistant_response_to_file(output_filepath, 
                                             remove_block_delimiters=True, 
                                             language=language, 
                                             force_overwrite=force_overwrite, 
                                             backup_if_exists=backup_if_exists)
        if success_:
            print(f"Réponse de l'assistant sauvegardée dans le fichier : {saved_filepath}")
        else:
            print("Erreur lors de la sauvegarde de la réponse de l'assistant dans le fichier : {saved_filepath}")
        return self


