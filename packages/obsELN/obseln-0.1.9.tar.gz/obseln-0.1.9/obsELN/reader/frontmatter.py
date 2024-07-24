"""
 This file is part of the Obsidian ELN Import package. Obsidian ELN Import
 provides a set of tools to import data and metadata from various analytical
 instruments into Obsidian ELN, which is distributed as a separate project.

    Copyright (C) 2024  Frieder Scheiba

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

This file defines helper functions used to process YAML from markdown files.
"""
import os
import re
from typing import Dict
from ruamel.yaml import YAML


def get_yaml_frontmatter(template: str, body: bool = False) -> Dict:
    """
    Read YAML frontmatter from file.

    Parameters
    ----------
    template : str
        template as string or path to template file.
    body : bool (optional)
        If True, return body as well as frontmatter, by default False

    Returns
    -------
    dict
        YAML frontmatter as dict. If body is True, return dict with keys
        'meta' and 'body'. 'meta' contains the YAML frontmatter, 'body'
        contains the rest of the file.
    """
    # check if template is a string or a file
    if os.path.isfile(template):
        with open(template, 'r', encoding='utf8') as file:
            content = file.read()
        try:
            fm_dict = get_yaml_frontmatter_from_string(content, body)
            return fm_dict
        except:
            print(f'Error reading frontmatter from {template}')
            return None
    else:
        try:
            fm_dict = get_yaml_frontmatter_from_string(template, body)
            return fm_dict
        except:
            print(f'Error reading frontmatter from string')
            return None


def get_yaml_frontmatter_from_string(content: str, body: bool = False) -> Dict:
    """
    Get YAML frontmatter from string.

    Parameters
    ----------
    content : str
        String containing YAML frontmatter.
    body : bool (optional)
        If True, return body as well as frontmatter, by default False

    Returns
    -------
    dict
        If body is True, return dict with keys 'yaml' and 'body'.
        'yaml' contains the YAML frontmatter, 'body' contains the rest of
        the file.
        If body is False, return YAML frontmatter as dict.
    """
    match = re.match(r'---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if match:
        frontmatter = match.group(1)
        content = match.group(2)
        yaml = YAML(typ='safe')
        if body:
            file_dict = {}
            file_dict['yaml'] = yaml.load(frontmatter)
            file_dict['body'] = content
            return file_dict
        else:
            return yaml.load(frontmatter)
    else:
        return {}


def save_as_markdown(file_path: str, frontmatter: Dict, body: str) -> None:
    """
    Save frontmatter and body as markdown file.

    Parameters
    ----------
    file_path : str
        Path to file.
    frontmatter : dict
        Frontmatter as dict.
    body : str
        Body as string.
    """
    yaml = YAML()
    yaml.default_flow_style = False
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.width = 4096  # large nuber to prevent wrapping of lines

    with open(file_path, 'w', encoding='utf8') as file:
        file.write('---\n')
        yaml.dump(frontmatter, file)
        file.write('\n---\n')
        file.write(body)
