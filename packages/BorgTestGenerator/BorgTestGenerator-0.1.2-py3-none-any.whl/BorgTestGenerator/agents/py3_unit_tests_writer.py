#coding: utf-8
from ..assistant import Assistant
from ..parsers.code_blocks_parsing import codeBlocksParser
import os
import pkg_resources

def read_text_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} est manquant")
    
    with open(file_path, 'r') as in_file:
        return in_file.read()

class py3UnitTestFileWriter(object):
    def __init__(self, assistant_id=None):
        self.agent_model = "gpt-4o"
        self.agent_name = "py3UnitTestFileWriter"
        self.agent_act_as = read_text_file(pkg_resources.resource_filename(__name__, "prompts/roles/linus_torvald.txt"))
        self.agent_instructions = read_text_file(pkg_resources.resource_filename(__name__, "prompts/instructions/py3_unit_tests_writer.txt"))
        # 0. Définir l'assistant
        
        self.define_assistant(assistant_id)


    def define_assistant(self, assistant_id):
        if assistant_id == None:
            self.assistant = Assistant(assistant_id)
            self.assistant.create_assistant(self.agent_name, self.agent_instructions, self.agent_model, tool_code_interpreter=True, tool_file_search=True)
            self.assistant.load_assistant(self.assistant.get_assistant_id())
        else:
            self.assistant = Assistant(assistant_id)
            self.assistant.load_assistant()
        return self
    
    def search_and_retreive_assistant(self):
        self.assistant = Assistant(assistant_id=None)
        assistant = self.assistant.exact_search_assistant(
                                                            self.agent_name,
                                                            self.agent_model,
                                                            self.agent_instructions
                                                         )
        if assistant:
            self.define_assistant(assistant.id)
        else:
            self.define_assistant(None)
            self.define_assistant(self.assistant.create_assistant(self.agent_name, self.agent_instructions, self.agent_model, tool_code_interpreter=True).get_assistant_id())
        return self

    def upload_files(self, vector_store_name, files_to_upload):
        missing_files = [f for f in files_to_upload if not os.path.exists(f)]
        if missing_files:
            raise FileNotFoundError(f"Les fichiers suivants sont manquants : {missing_files}")
        
        print(f"Téléchargement des fichiers : {files_to_upload} vers {vector_store_name}")
        try:
            self.assistant.upload_files(files_to_upload, f"{vector_store_name}")
            print("Fichiers téléchargés avec succès.")
        except Exception as e:
            print(f"Erreur lors du téléchargement des fichiers : {e}")

        # 4. Mettre à jour l'assistant avec le vector store
        try:
            self.assistant.update_assistant_with_vector_store()
            print("Assistant mis à jour avec le vector store.")
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'assistant avec le vector store : {e}")
        return self


    def create_new_thread(self):
        print("Création d'un nouveau thread")
        self.assistant.create_thread()
        return self

    def create_new_user_message(self):
        print("Création d'un message utilisateur")
        self.assistant.create_message("user", "Écrit le code du fichier test correspondant a ce script python")
        return self

    def run(self):
        print("Exécution du run")
        self.assistant.create_run()
        return self

    def print_assistant_result(self):
        # 8. Récupérer les messages de l'assistant
        print(self.assistant.get_assistant_messages())
        return self
    
    def get_assistant_result(self):
        return self.assistant.get_assistant_messages()

    def save_assistant_response_to_file(self, 
                                        file_path, 
                                        remove_block_delimiters=True,
                                        language=None,
                                        force_overwrite=False,
                                        backup_if_exists=True):
        def backup_file(file_path, 
                        remove_existing_file=False):
            import shutil
            """
            # backup_file_path = f"{file_path}.bak"
            cela est trop basique,
            si f"{file_path}.bak" existe deja cela resterai leger comme probleme
            , mais si f"{file_path}.bak" et f"{file_path}.bak.bak" existent deja et qui sait encore...
            cela deviendra un probleme serieux, autant dire cela serait une catastrophe !
            rendez vous compte que cela ferait que cette protection serait inutile !
            Donc,
            Ce que je propose en tant qu'humain, c'est de faire une boucle qui verifie si le fichier existe deja,
            et si oui, on ajoute un numero a la fin du fichier de sauvegarde, et on verifie a nouveau si le fichier existe deja,
            et on continue jusqu'a ce qu'on trouve un nom de fichier qui n'existe pas encore.
            """
            def find_available_backup_filename(file_path):
                backup_file_path = f"{file_path}.bak"
                if os.path.exists(backup_file_path):
                    i = 1
                    while True:
                        backup_file_path = f"{file_path}.bak.{i}"
                        if not os.path.exists(backup_file_path):
                            break
                        i += 1
                return backup_file_path
            
            backup_file_path = find_available_backup_filename(file_path)
            
            if os.path.exists(file_path):
                if remove_existing_file:
                    # rename (move) the file to the backup file
                    os.rename(file_path, backup_file_path)
                else:
                    # copy the file to the backup file
                    shutil.copy(file_path, backup_file_path)
            return self

        
        def write_file(file_path: str, 
                       data: str|bytes, 
                       force_overwrite: bool = False) -> None:
            
            file_exists = os.path.exists(file_path)

            if ( ( file_exists == True ) and ( force_overwrite == True ) ) or ( file_exists == False ):
                if type(data) == bytes:
                    with open(file_path, 'wb') as output_file:
                        output_file.write(data)

                elif type(data) == str:
                    with open(file_path, 'w') as output_file:
                        output_file.write(data)
            else:
                raise FileExistsError

        data = self.assistant.get_assistant_messages()
        if remove_block_delimiters:
            parsed_data = codeBlocksParser(data, language=language)
            final_blocks = [ block["code"] for block in parsed_data['code_blocks'] ]
            final_data = '\n'.join(final_blocks)
        else:
            final_data = data

        if backup_if_exists:
            backup_file(file_path, remove_existing_file=force_overwrite)
        
        file_saved_with_success = None
        try:
            write_file(file_path, final_data, force_overwrite)
            file_saved_with_success = True
        except FileExistsError:
            file_saved_with_success = False
        finally:
            return file_saved_with_success, file_path

