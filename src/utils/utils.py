import json
from os import listdir, path
from typing import Tuple, List
from argparse import Namespace


def params_printer(params: Namespace):
    print(f"Inputs provided: {json.dumps(vars(params), indent=4)}")


def get_dir_files(dir_path: str, extension_filter: str = None) -> Tuple[List[str], List[str]]:
    files_name = listdir(path=dir_path)
    if extension_filter:
        files_name = [file for file in files_name if file.endswith(extension_filter)]
    txt_files_paths = [path.join(dir_path, file) for file in files_name]
    return files_name, txt_files_paths


def extract_dict_structure(dictionary: dict) -> dict:
    """
    Return a dictionary with the same structure of input dict, but without data.
    When a key name is surrounded by square brackets, it means that the key contain a list of dict.

    TODO bug: list is copied two times
    """
    structure = {}
    for key in dictionary.keys():
        structure[key] = 'leaf'
        if type(dictionary[key]) == dict:
            sub_structure = extract_dict_structure(dictionary[key])
            structure[key] = sub_structure
        elif type(dictionary[key]) == list and dictionary[key]:
            first_el = dictionary[key][0]
            if type(first_el) == dict:  # assume that the list contain same dictionaries
                sub_structure = extract_dict_structure(first_el)
                structure[f"[{key}]"] = sub_structure
    return structure


def split_in_sessions(t_current, t_last, chat_text, delta_h_threshold, session_token):
    if session_token:
        if t_last and t_current:
            delta_h = divmod((t_current - t_last).total_seconds(), 3600)[0]
            if delta_h >= delta_h_threshold:
                chat_text.append(session_token)
