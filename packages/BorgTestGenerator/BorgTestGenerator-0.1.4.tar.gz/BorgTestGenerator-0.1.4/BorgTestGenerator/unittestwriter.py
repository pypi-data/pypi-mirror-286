#coding: utf-8
from .agents.py3_unit_tests_writer import py3UnitTestFileWriter
import os

class unittestwriter(py3UnitTestFileWriter):
    def __init__(self, assistant_id: str|None = None):
        super().__init__(assistant_id)
        #self.check_and_retreive()

    def check_and_retreive(self) -> py3UnitTestFileWriter:
        if (type(self.assistant) == None) or (self.assistant.assistant_id == None):
            self.search_and_retreive_assistant()
        return self
    
    def run_generation(self, 
                       vector_store_name: str, 
                       files_to_upload: list[str]) -> py3UnitTestFileWriter:
        try:
            print("Début de la génération...")
            self.upload_files(vector_store_name, files_to_upload)
            self.create_new_thread()
            self.create_new_user_message()
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
                        backup_if_exists: bool = True) -> py3UnitTestFileWriter:
        
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



"""
from unittestwriter import unittestwriter
utw = unittestwriter()
utw.run_generation("vector_store_name", ["unittestwriter.py"])
utw.save_generation("test_unittestwriter.py")
"""