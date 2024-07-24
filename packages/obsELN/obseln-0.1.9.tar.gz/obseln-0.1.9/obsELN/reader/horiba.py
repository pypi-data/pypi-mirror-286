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

This file defines the HoribaTXT class which is used to read and process TXT data files
from Horiba LabSpec Software.
It also provides a set of methods to generate plots of the data.
"""

import os
from datetime import datetime
import pandas as pd

from obsELN.plot import sciplots as sp


class HoribaTXT:
    """
    Class to read and process TXT data files from Horiba LabSpec Software.
    """

    def __init__(self,
                 file_path,
                 date_format='%d.%m.%Y %H:%M',
                 encoding='windows-1252',
                 delimiter='\t'):
        """
        Constructor for HoribaTXT class.
        :param filename: str, path to the TXT file
        """
        self.file_path = file_path
        self.filename = file_path.split('/')[-1]
        self.filename_base = self.filename.split('.')[0]
        self.date_format = date_format
        self.encoding = encoding
        self.delimiter = delimiter
        self.data = None
        self.header = None
        self.header_rows = None
        self.method = 'Raman Spectroscopy'
        self.read_header()
        self.read_data()

    def read_header(self):
        """
        Read the header of the Horiba TXT file.

        Each line of the header section starts with a # character, followed by
        a key-value pair separated by a '=\t'.
        """
        with open(self.file_path, 'r', encoding=self.encoding) as file:
            self.header = {}
            for line in file:
                if line.startswith('#'):
                    key, value = line[1:].strip().split('=')
                    self.header[key] = value.strip()
                else:
                    break
        # Convert date string to datetime object
        if 'Date' in self.header:
            self.header['Date'] = datetime.strptime(self.header['Date'],
                                                    self.date_format)
        self.header_rows = len(self.header)
        # The metadata contains several keys which start with AxisType followed by
        # a number in brackets (i.e. AxisType[0], AxisType[1], ...). Merge these
        # keys into a single key with a list of values and remove the original keys.
        # Do the same for AxisUnit keys.
        axis_types = {}
        axis_units = {}
        for key in list(self.header.keys()):  # Create a copy of the keys
            value = self.header[key]
            if key.startswith('AxisType'):
                axis_types[int(key[9:-1])] = value
                # Remove original key
                del self.header[key]
            elif key.startswith('AxisUnit'):
                axis_units[int(key[9:-1])] = value
                # Remove original key
                del self.header[key]
        # Sort axis types and units by key in descending order
        self.header['AxisType'] = [axis_types[i] for i in reversed(range(len(axis_types)))]

        self.header['AxisUnit'] = [axis_units[i] for i in reversed(range(len(axis_units)))]
        # Replace abbreviated axis type and unit names with full names
        axis_type_dict = {
            'Intens': 'Intensity',
            'Spectr': 'Wavenumber',
        }
        axis_units_dict = {
            'Cnt': 'Counts',
            '1/cm': '1/cm'
        }
        self.header['AxisType'] = [axis_type_dict.get(axis_type, axis_type)
                                      for axis_type in self.header['AxisType']]
        self.header['AxisUnit'] = [axis_units_dict.get(axis_unit, axis_unit)
                                        for axis_unit in self.header['AxisUnit']]

    def read_data(self):
        """
        Read the data section of the Horiba TXT file.

        The data section starts after the header section and is tab-separated.
        The number and name of columns is determined by the number of AxisType
        keys in the header section.
        """
        self.data = pd.read_csv(self.file_path,
                                header=None,
                                sep=self.delimiter,
                                skiprows=self.header_rows,
                                encoding=self.encoding)
        # Rename columns to AxisType values
        self.data.columns = self.header['AxisType']

    def plot_spectrum(
            self,
            title: str = None,
            data_label: str = None,
            canvas=None,
            save_plots: bool = False,
            file_path_base: str = None):
        """
        Generate a plot of the data.
        """
        if ('Intensity' in self.data.columns and
            'Wavenumber' in self.data.columns):
            # Select the columns 'Wavenumber' and 'Intensity'
            data = self.data[['Wavenumber', 'Intensity']]
            if title is None:
                title = 'Raman Spectrum'
            if data_label is None:
                data_label = self.filename_base
            # Single axis plot
            figure_obj = sp.single_axis_plot(
                data,
                marker='none',
                linestyle='solid',
                title=title,
                xlabel=r'wave number / $\mathregular{cm^{-1}}$',
                ylabel='intensity / counts',
                data_label=data_label,
                canvas=canvas)
            if save_plots:
                resolution = 300
                if file_path_base is None:
                    file_path_base = self.file_path.split('.')[0]
                figure_obj.savefig(
                    file_path_base + '_spectrum.png',
                    dpi=resolution)
                figure_obj.savefig(
                    file_path_base + '_spectrum.svg')
            else:
                figure_obj.show()

        return figure_obj
    
    def save_data(self, file_path: str = None):
        """
        Save the data to a CSV file.
        """
        if file_path is None:
            file_path = os.path.splitext(self.file_path)[0] + '_data.csv'
        else:
            pass

        self.data.to_csv(file_path, index=False)
