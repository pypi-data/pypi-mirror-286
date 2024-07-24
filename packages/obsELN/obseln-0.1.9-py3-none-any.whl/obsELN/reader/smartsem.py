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

This file defines the SmartSEMImage class used to read metadata and image data
from ZEISS SmartSEM TIFF files.
"""

import os
import pkgutil
from datetime import datetime
import numpy as np

from PIL import Image
import yaml


__main_package__ = 'obsELN'
__sub_package__ = 'reader'

class SmartSEMImage:
    """
    Class SmartSemFile definies a MPT file reader object.

    The SmartSemFile class is used to read and store the data from a ZEISS SmartSEM TIFF file.

    The SmartSemFile class has the following properties:
    - file_path: str
        Path to the SmartSEM TIFF file.
    """

    def __init__(self, file_path: str):
        """
        Initialize a SmartSemFile object.

        Parameters
        ----------
        file_path : str
            Path to the SmartSEM TIFF file.
        """
        self.file_path = file_path
        self.header = None
        self.image = None
        self.method = None

        self.read_header()
        self.read_image()

    def read_header(self):
        """
        Reads metadata from the header section of the SmartSEM TIFF file.
        """
        out_dic = {}
        with open(self.file_path, 'rb') as file:
            # file.readline()    # this seems to be unnecessary
            file.seek(0)         # this can probably be removed too
            # skip lines until we find a line that starts with '0'
            # print('First skipped header part:')
            while True:
                line = (file.readline()).decode('latin_1').strip()
                # print('   ', line)
                if line == '0':
                    break
            # skip 32 lines
            # print('Second skipped header part:')
            for _ in range(32):
                # print('   ', file.readline())
                file.readline()

            line = file.readline()
            head_count = int(line)
            # print('head_count: ', head_count)
            for _ in range(head_count):
                file.readline()
                # print map(str.strip, file.readline().split('='))
                # Read the next line, decode it, and split it into two parts
                ext = list(
                    map(str.strip,
                        file.readline().decode('latin_1').split('=')))
                # If we have exactly two parts, add them to the dictionary.
                if len(ext) == 2:
                    key, val = ext
                    out_dic[key] = val
                elif len(ext) == 1:
                    # print ext
                    res = ext[0].split(":")
                    if res[0] == "Time ":
                        out_dic['File Time'] = datetime.strptime(
                            ext[0], "Time :%H:%M:%S")
                    if res[0] == "Time":
                        out_dic['File Time'] = datetime.strptime(
                            ext[0], "Time: %H:%M:%S")
                        # note that date is not considered, thus only measurement
                        # in 1 day is allowed to compare.
                        # definitely bugs in future. need to resolve date.
                        # skip at this point.
        self.header = out_dic
        self.set_method()

    def read_image(self):
        """
        Reads the image data from the SmartSEM TIFF file.
        """
        self.image = Image.open(self.file_path)

    def save_image(self,
                   file_name: str = None,
                   image_format: str = None):
        """
        Saves the image data from the SmartSEM TIFF file.

        Parameters
        ----------
        out_folder : str
            Folder to save the image in.
        image_format : str
            Image format to save the image in.
        """
        if file_name is not None:
            # try to get image format from file name
            if image_format is None:
                # try to determin image from file extension
                extension = file_name.split('.')[-1]
                image_format = extension
            else:
                pass  # image_format is already defined
        else:
            if image_format is None:
                # use jpg as default image format
                extension = 'jpg'
                image_format = 'jpeg'

            # use file name and path from SmartSEM TIFF file and replace extension
            # to match output image format
            file_name_base = os.path.basename(self.file_path).split('.')[0]
            file_name = f"{file_name_base}.{extension}"

        # change image format identifier to match PIL.Image.save() requirements
        image_format = image_format.lower()
        if image_format == 'jpg':
            image_format = 'jpeg'
        if image_format == 'tif':
            image_format = 'tiff'

        # convert image to RGB to save as JPEG
        if image_format == 'jpeg':
            output_image = self.image.convert('RGB')
        else:
            output_image = self.image

        # get folder path from file path
        folder_path = os.path.dirname(file_name)
        # create folder if it does not exist
        if folder_path != '':
            if not os.path.exists(folder_path):
                try:
                    os.makedirs(folder_path)
                except OSError:
                    print('Error creating folder: ', folder_path)
                    return

        output_image.save(file_name, format=image_format)

    def get_image_data(self):
        """
        Returns the image data from the SmartSEM TIFF file as a numpy array.

        Returns
        -------
        array
            numpy array containing the image data.
        """
        return np.array(self.image)

    def set_method(self, method: str = None):
        """
        Sets the method used to acquire the image data.

        The method is determined from the metadata in the header section of the SmartSEM TIFF file.
        """
        if method is not None:
            self.method = method
        elif 'Detector' in self.header:
            detector = self.header['Detector']
            smartsem_settings_file = os.path.join('resources', 'smartsem_tiff.yaml')
            smartsem_settings_data = pkgutil.get_data(__main_package__, smartsem_settings_file)
            if smartsem_settings_data is not None:
                smartsem_settings_data = smartsem_settings_data.decode('utf-8')
                smartsem_settings = yaml.safe_load(smartsem_settings_data)
            else:
                # set default values
                smartsem_settings = {
                    'method identifier': {
                        'SE inlens': 'SE1',
                        'SE thorny': 'SE2',
                        'EsB': 'ESB',
                    },
                    'export parameters': {
                        'SE inlens': {
                            'magnification': 'Mag',
                            'working distance': 'WD',
                            'landing energy': 'Landing energy',
                            'probe current': 'I Probe',
                            'brightness': 'Brightness',
                            'contrast': 'Contrast',
                            'pixel size': 'Pixel Size',
                            'image width': 'Width',
                            'image height': 'Height',
                            'image resolution': 'Store resolution',
                            'scan speed': 'Scan Speed',
                            'tilt angle': 'Tilt Angle',
                            'stage position x': 'Stage at X',
                            'stage position y': 'Stage at Y',
                            'stage position z': 'Stage at Z',
                            'stage rotation': 'Stage at R',
                            'file number': 'File No',
                            'software version': 'Version'
                        },
                        'SE thorny': {
                            'magnification': 'Mag',
                            'working distance': 'WD',
                            'landing energy': 'Landing energy',
                            'probe current': 'I Probe',
                            'brightness': 'Brightness',
                            'contrast': 'Contrast',
                            'pixel size': 'Pixel Size',
                            'image width': 'Width',
                            'image height': 'Height',
                            'image resolution': 'Store resolution',
                            'scan speed': 'Scan Speed',
                            'tilt angle': 'Tilt Angle',
                            'stage position x': 'Stage at X',
                            'stage position y': 'Stage at Y',
                            'stage position z': 'Stage at Z',
                            'stage rotation': 'Stage at R',
                            'file number': 'File No',
                            'software version': 'Version'
                        },
                        'EsB': {
                            'magnification': 'Mag',
                            'working distance': 'WD',
                            'landing energy': 'Landing energy',
                            'probe current': 'I Probe',
                            'grid voltage': 'ESB Grid',
                            'brightness': 'Brightness',
                            'contrast': 'Contrast',
                            'pixel size': 'Pixel Size',
                            'image width': 'Width',
                            'image height': 'Height',
                            'image resolution': 'Store resolution',
                            'scan speed': 'Scan Speed',
                            'tilt angle': 'Tilt Angle',
                            'stage position x': 'Stage at X',
                            'stage position y': 'Stage at Y',
                            'stage position z': 'Stage at Z',
                            'stage rotation': 'Stage at R',
                            'file number': 'File No',
                            'software version': 'Version'
                        }
                    }
                }

            methods = smartsem_settings['method identifier']
            # inverse technique dictionary
            methods_inv = {value: key for key, value in methods.items()}
            if detector not in methods_inv:
                method = detector
            else:
                method = methods_inv[detector]
            self.method = method
        else:
            self.method = None
