from os import listdir, path
from typing import Tuple, List


def get_txt_files(chats_path: str) -> Tuple[List[str], List[str]]:
    files_name = listdir(path=chats_path)
    txt_files_name = [file for file in files_name if file.endswith(".txt")]
    txt_files_paths = [path.join(chats_path, file) for file in txt_files_name]
    return txt_files_name, txt_files_paths
