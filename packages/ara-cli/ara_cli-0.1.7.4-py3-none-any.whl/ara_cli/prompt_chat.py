import os
import shutil
from ara_cli.chat import Chat
from ara_cli.classifier import Classifier
from ara_cli.update_config_prompt import update_artefact_config_prompt_files

def initialize_prompt_chat_mode(classifier, param, chat_name, reset=None, output_mode=False, append_strings=[]):
    sub_directory = Classifier.get_sub_directory(classifier)
    artefact_data_path = os.path.join("ara", sub_directory, f"{param}.data") # f"ara/{sub_directory}/{parameter}.data"

    if chat_name is None:
        chat_name = classifier

    update_artefact_config_prompt_files(classifier, param, automatic_update=True)

    classifier_chat_file = os.path.join(artefact_data_path, f"{chat_name}")
    start_chat_session(classifier_chat_file, reset, output_mode, append_strings)

def start_chat_session(chat_file, reset, output_mode, append_strings):
    chat = Chat(chat_file, reset=reset)
    if append_strings:
        chat.append_strings(append_strings)
    if output_mode:
        chat.start_non_interactive()
        return
    chat.start()

