from __future__ import annotations  # for python 3.8

import fnmatch
import os
import re
from typing import List
from pathlib import Path

from agstoolbox.core.ags.datafile_writer import get_multifile_lib, make_data_file_from_multifile_lib
from agstoolbox.core.ags.game_project import GameProject
from agstoolbox.core.ags.multifilelib import MultiFileLib
from agstoolbox.core.utils.file import join_paths_as_posix


def case_insensitive_glob(directory: str, file_mask: str) -> list[Path]:
    reg_expr = re.compile(fnmatch.translate(file_mask), re.IGNORECASE)
    list_path = [i for i in os.listdir(directory) if os.path.isfile(os.path.join(directory, i))]
    result = [os.path.join(directory, j) for j in list_path if re.match(reg_expr, j)]
    result = [Path(j) for j in result]
    if result is None:
        return []
    return result


def get_dir_file_list(directory: str, file_mask: str):
    try:
        path = Path(directory).as_posix()
        return case_insensitive_glob(path, file_mask)
    except IOError:
        return []


def add_matching_files(file_list: List[str], file_mask: str, parent_dir: str,
                       full_paths: bool = False):
    files = get_dir_file_list(parent_dir, file_mask)
    if full_paths:
        file_list.extend([str(file) for file in files])
    else:
        file_list.extend([str(file.relative_to(parent_dir)) for file in files])


def construct_template_filelist(parent_dir: str) -> List[str]:
    files_to_include: List[str] = list()
    add_matching_files(files_to_include, "*.ico", parent_dir)
    add_matching_files(files_to_include, "Game.agf", parent_dir)
    add_matching_files(files_to_include, "acsprset.spr", parent_dir)
    add_matching_files(files_to_include, "preload.pcx", parent_dir)
    add_matching_files(files_to_include, "AudioCache/*.*", parent_dir)
    add_matching_files(files_to_include, "Speech/*.*", parent_dir)
    add_matching_files(files_to_include, "flic*.fl?", parent_dir)
    add_matching_files(files_to_include, "agsfnt*.ttf", parent_dir)
    add_matching_files(files_to_include, "agsfnt*.wfn", parent_dir)
    add_matching_files(files_to_include, "*.crm", parent_dir)
    add_matching_files(files_to_include, "*.asc", parent_dir)
    add_matching_files(files_to_include, "*.ash", parent_dir)
    add_matching_files(files_to_include, "*.txt", parent_dir)
    add_matching_files(files_to_include, "*.trs", parent_dir)
    add_matching_files(files_to_include, "*.pdf", parent_dir)
    add_matching_files(files_to_include, "*.ogv", parent_dir)
    return files_to_include


def create_template_from_game_dir(project_dir: str, template_filepath: str):
    if Path(template_filepath).exists():
        Path(template_filepath).unlink()

    template_filename: str = Path(template_filepath).name
    template_dir: str = str(Path(template_filepath).parent.as_posix())

    template_filelist: List[str] = construct_template_filelist(project_dir)
    filelist: List[str] = list()
    for file in template_filelist:
        filelist.append(join_paths_as_posix(project_dir, file))

    mlib: MultiFileLib = get_multifile_lib(filelist, project_dir, template_filename, False)
    make_data_file_from_multifile_lib(mlib, template_dir)


def create_template_from_project(game_project: GameProject, template_name: str, out: str | None):
    if out is None:
        out = game_project.directory

    template_name = Path(template_name).name
    template_filepath: str = join_paths_as_posix(out, template_name)
    create_template_from_game_dir(game_project.directory, template_filepath)
