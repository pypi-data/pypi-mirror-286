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

This file defines the BiologicMPT class which is used to read and process MPT files
from Bio-Logic.
It also provides a set of methods to generate plots of the data and to extract cycle
based information from the data.
"""
from datetime import datetime
import os
import re
import logging
import pkgutil

import numpy as np
import pandas as pd
import yaml
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib.ticker as mticker
import matplotlib.legend as mlegend

__main_package__ = 'obsELN'
logging.basicConfig(level=logging.INFO)


class BiologicMPT:
    """
    Class MptFile definies a MPT file reader object.

    The MptFile class is used to read and store the data from a MPT file.
    The MPT file format is used by the EC-Lab software from Bio-Logic.

    The MptFile class has the following properties:
    - file_path: str
        Path to the MPT file.
    - decimal_separator: str
        Decimal separator used in the MPT file.
    - date_format: str
        Date format used in the MPT file.
    - encoding: str
        Encoding used in the MPT file.
    - header: dict
        Header section of the MPT file stored as a dictionary.
    - blank_header_lines: int
        Number of blank lines in the header section of the MPT file.
    - parameter_table: pandas DataFrame
        Parameter table section of the MPT file stored as a pandas DataFrame.
    - parameter_table_start: int
        Line number where the parameter table section starts.
    - data: pandas DataFrame
        Data section of the MPT file stored as a pandas DataFrame.

    The MptFile class has the following methods:
    - read_header()
        Reads the header section of the MPT file and stores it as a dictionary.
    - read_parameter_table()
        Reads the parameter table section of the MPT file and stores it as a pandas DataFrame.
    - read_data()
        Reads the data section of the MPT file and stores it as a pandas DataFrame.
    - print_header()
        Prints the header section of the MPT file.
    - print_parameter_table()
        Prints the parameter table section of the MPT file.
    - print_data()
        Prints the data section of the MPT file.

    Parameters
    ----------
    file_path: str (required)
        Path to the MPT file.
    decimal_separator: str (optional)
        Decimal separator used in the MPT file. If not specified, the decimal separator
        is automatically detected.
    date_format: str (optional)
        Date format used in the MPT file. If not specified, the date format is set to
        '%m/%d/%Y %H:%M:%S.%f'.
    encoding: str (optional)
        Encoding used in the MPT file. If not specified, the encoding is set to
        'windows-1252'.

    Returns
    -------
    MptFile object
        MptFile object containing the data from the MPT file.

    """

    def __init__(self,
                 file_path,
                 decimal_separator=None,
                 date_format='%m/%d/%Y %H:%M:%S.%f',
                 encoding='windows-1252',
                 first_cycle_number: int = 1,
                 negative_charge_current: bool = None,
                 cycle_starts_with: str = None,
                 offset: int = None,
                 process: bool = False):
        self.file_path = file_path
        self.decimal_separator = decimal_separator
        self.date_format = date_format
        self.encoding = encoding
        self.header = {}
        self.blank_header_lines = 0
        self.parameter_table = None
        self.parameter_table_start = None
        self.lines_modified_on = None
        self.data = None
        self.cycles = None
        self.cycle_indices = None
        self.cycle_info = {
            'first cycle number': first_cycle_number,
            'negative charge current': negative_charge_current,
            'cycle starts with': cycle_starts_with,
            'offset': offset,
            'number of cycles': None,
        }
        self.method = None
        self.settings = None
        info_msg = f'Processing file: {self.file_path}'
        logging.info(info_msg)
        logging.info('   Reading header...')
        self.read_header()
        logging.info('   Reading parameter table...')
        self.read_parameter_table()
        logging.info('   Reading data...')
        self.read_data()
        self.load_settings()
        self.set_method()
        self.set_cycle_info(cycle_starts_with=cycle_starts_with,
                            negative_charge_current=negative_charge_current,
                            offset=offset)
        print(f'1. Cycle info: {self.cycle_info}')
        if process:
            self.process_data()

    def process_data(self):
        """
        Process the data section of the MPT file.
        """
        logging.info('   Processing data...')
        negative_charge_current = self.cycle_info['negative charge current']
        if negative_charge_current:
            logging.info('      Swapping charge and discharge column names...')
            self.swap_charge_discharge_column_names()
        logging.info('      Updating cycle number column...')
        self.update_column_cycle_number()
        print(f'2. Cycle info: {self.cycle_info}')
        logging.info('      Adding state column...')
        self.add_column_state()
        logging.info('      Adding specific capacity column...')
        self.add_column_specific_capacity()
        logging.info('      Adding intrinsic capacity column...')
        self.add_column_intrinsic_capacity()
        logging.info('      Adding dQ/dV column...')
        self.add_column_dq_dv(dv_step=5, update=True)
        print(f'3. Cycle info: {self.cycle_info}')
        logging.info('   Processing cycles...')
        try:
            self.process_cycles()
        except (ValueError, RuntimeError, TypeError, NameError):
            print('There was an error while attempting to process '
                  'cycle based inforamtion from the mpt-file.')
        print(f'4. Cycle info: {self.cycle_info}')

    def read_header(self):
        """
        Reads the header section of the MPT file and stores it as a dictionary.

        The keys of the dictionary are the header labels and the values are the
        corresponding values. The header section is defined as the lines before
        the parameter table section.

        Parameters
        ----------
        self: MptFile object
            read_header() is called as a method of the MptFile object without
            additional parameters.

        Returns
        -------
        self.header: dict
            Header section of the MPT file stored as a dictionary in the
            header property of the object.
        """

        supported_techniques = [
            'Galvanostatic Cycling with Potential Limitation',
            'Cyclic Voltammetry'
        ]

        param_table_technique_keys = {
            'Galvanostatic Cycling with Potential Limitation': 'Ns              ',
            'Cyclic Voltammetry': 'Ei (V)           '
        }
        reading_parameter_table = False

        with open(self.file_path, 'r', encoding=self.encoding) as file:
            first_line = file.readline()
            line_number = 1
            if first_line != "EC-Lab ASCII FILE\n":
                raise ValueError(
                    "Invalid MPT file. First line should be 'EC-Lab ASCII FILE'.")

            blank_header_lines = 0
            # Get header lines:
            line = file.readline()
            line_number += 1
            key, value = line.split(":", 1)
            if key.strip() == 'Nb header lines':
                header_lines = value.strip()
                self.header['Nb header lines'] = header_lines
            else:
                raise ValueError(
                    "Missing 'Nb header lines' key in line 2.")

            # Try to determine technique name
            line = file.readline().strip()
            line_number += 1
            if line == '':
                blank_header_lines += 1
                line = file.readline().strip()
                line_number += 1
                if not line == '':
                    technique = line
                    self.header['technique'] = technique
                    if technique not in supported_techniques:
                        raise ValueError(
                            f"Technique '{technique}' is not supported.")

                    param_table_starts_with = param_table_technique_keys[technique]

                else:
                    raise ValueError(
                        "Unable to determine technique name.")
            else:
                raise ValueError(
                    "Unable to determine technique name.")

            key = None
            value = None
            nested_level = 0  # Track the nested level using tabs

            for line in file:
                line_number += 1

                if line_number == header_lines:
                    break

                if line.strip() == '':
                    blank_header_lines += 1
                    if reading_parameter_table:
                        reading_parameter_table = False
                    continue

                if reading_parameter_table:
                    continue

                if nested_level > 0:  # Handle nested values

                    # Check for end of nested block
                    if line.startswith('\t' * nested_level):
                        if ':' in line:
                            subkey, subvalue = line.split(":", 1)
                            if subkey is not None and subvalue is not None:
                                self.header[key][subkey.strip()
                                                 ] = subvalue.strip()
                            # continue reading next line, do not reset nested_level
                            # since we may still be inside the nested block
                        elif '=' in line:
                            subkey, subvalue = line.split("=", 1)
                            if subkey is not None and subvalue is not None:
                                self.header[key][subkey.strip()
                                                 ] = subvalue.strip()
                        elif '>' in line:
                            subkey, subvalue = line.split("=", 1)
                            self.header[key][f'{subkey.strip()} larger'
                                             ] = subvalue.strip()
                        else:
                            subkey = line.strip()
                            self.header[key][subkey] = True
                        continue
                    elif key == 'Mass of active material' and line.startswith(' at x = '):
                        at_x_value = float(line.split('at x = ')
                                           [1].replace(',', '.'))
                        self.header[key]['at x'] = at_x_value
                        nested_level -= 1
                        continue
                    else:
                        # line does not belong to nested block
                        # resetting nested_level
                        nested_level -= 1
                        # continue executing rest of for loop

                if ':' in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    if key == 'Comments' and key in self.header:
                        # if 'Comments' already exists
                        self.header[key] += f'\n{value.strip()}'
                    elif key is not None and value is not None:
                        self.header[key] = value.strip()

                    if key == 'Saved on':
                        self.header[key] = {}
                        nested_level = 1  # Start parsing nested values in next loop
                    elif key == 'Safety Limits':
                        self.header[key] = {}
                        nested_level = 1  # Start parsing nested values in next loop
                    elif key == 'Mass of active material':
                        value_str, unit = self.header[key].split(' ', 1)
                        if self.decimal_separator is None:
                            decimal_separator = ',' if ',' in value_str else '.'
                            self.decimal_separator = decimal_separator
                        if decimal_separator != '.':
                            value_str = value_str.replace(
                                decimal_separator, '.')
                        self.header[key] = {
                            'value': float(value_str),
                            'unit': unit
                        }
                        nested_level = 1
                else:
                    if line.startswith(param_table_starts_with):
                        if self.parameter_table_start is None:
                            self.parameter_table_start = line_number
                            reading_parameter_table = True
                    elif line.startswith('Modify on'):
                        reading_parameter_table = False
                        if self.lines_modified_on is None:
                            self.lines_modified_on = [line_number]
                        else:
                            self.lines_modified_on.append(line_number)
                    elif line.startswith('for DX = 1,'):
                        value_str = line.split('for DX = 1, DQ =')[1]
                        self.header['DQ for DX = 1'] = value_str.strip()
                    elif line.startswith('EC-Lab for windows'):
                        self.match_version(
                            line, 'EC-Lab for windows', 'software')
                    elif line.startswith('Internet server'):
                        self.match_version(line, 'Internet server', 'firmware')
                    elif line.startswith('Command interpretor'):
                        self.match_version(
                            line, 'Command interpretor', 'firmware')
                    elif line.startswith('Record '):
                        key = line.split('Record ')[1].strip()
                        if 'Record' not in self.header and key is not None:
                            self.header['Record'] = {}
                        if key is not None:
                            self.header['Record'][key] = True

        self.blank_header_lines = blank_header_lines

        # ******** Post processing of header ********** #
        # Convert 'Acquisition started on' to timestamp
        if 'Acquisition started on' in self.header:
            date_str = self.header['Acquisition started on']
            timestamp = datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S.%f')
            self.header['Acquisition started on'] = timestamp

        # Extract and store numeric values with units for specific keys
        float_unit_keys = [
            'Molecular weight of active material (at x = 0)',
            'Atomic weight of intercalated ion',
            'DQ for DX = 1',
            'Battery capacity',
            'Electrode surface area',
            'Characteristic mass',
            'Volume (V)'
        ]
        for key in float_unit_keys:
            self.format_as_value_with_unit(key)

        int_keys = [
            'Nb header lines',
            'Number of e- transfered per intercalated ion'
        ]
        for key in int_keys:
            if key in self.header:
                self.header[key] = int(self.header[key])

        # Add key 'Mass of active material' to header if it does not exist
        if 'Mass of active material' not in self.header:
            self.header['Mass of active material'] = {
                'value': None,
                'unit': None,
                'at x': None
            }

    def load_settings(self):
        """
        Load settings from biologic_mpt.yaml.
        """
        # use pkgutil to load the settings file from the package
        settings_file = os.path.join('resources', 'biologic_mpt.yaml')
        settings_data = pkgutil.get_data(__main_package__, settings_file)
        if settings_data is not None:
            settings_data = settings_data.decode('utf-8')
            self.settings = yaml.safe_load(settings_data)
        else:
            raise FileNotFoundError(
                "Settings file 'biologic_mpt.yaml' not found.")

    def format_as_value_with_unit(self, key: str):
        """
        Function docstring
        """
        if key in self.header:
            value_str, unit = self.header[key].split(' ', 1)
            if self.decimal_separator is None:
                decimal_separator = ',' if ',' in value_str else '.'
                self.decimal_separator = decimal_separator
            else:
                decimal_separator = self.decimal_separator
            if decimal_separator != '.':
                value_str = value_str.replace(decimal_separator, '.')
            value = float(value_str)
            self.header[key] = {
                'value': value,
                'unit': unit
            }
        else:
            # if key does not exist in header, add it with value and unit set to None
            self.header[key] = {
                'value': None,
                'unit': None
            }

    def match_version(self, line: str, id_string: str, program_type: str):
        """
        Function docstring
        """
        pattern = rf'{id_string} v(.*?) \({program_type}\)'
        match = re.search(pattern, line)
        key = f'{id_string} version'
        if match:
            self.header[key] = match.group(1)
        else:
            self.header[key] = ''

    def read_parameter_table(self):
        """
        Function docstring
        """
        gcpl_data_types = {
            # GCPL
            'Ns': int,
            'Set I/C': str,
            'Is': float,
            'unit Is': str,
            'N': float,
            'I sign': str,
            't1 (h:m:s)': str,
            'I Range':  str,
            'Bandwidth': int,
            'dE1 (mV)': float,
            'dt1 (s)': float,
            'EM (V)': float,
            'tM(h: m: s)': str,
            'Im': float,
            'unit Im':  str,
            'dI/dt': float,
            'dunit dI/dt': str,
            'E range min (V)': float,
            'E range maxis_obj (V)': float,
            'dq': float,
            'unit dq': str,
            'dtq (s)': float,
            'dQM': float,
            'unit dQM': str,
            'dxM': float,
            'delta SoC (%)': str,
            'tR (h: m: s)': str,
            'dER/dt (mV/h)': float,
            'dER (mV)':  float,
            'dtR (s)': float,
            'EL (V)': str,
            "goto Ns'": int,
            'nc cycles': int
        }
        cv_data_types = {
            # CV
            'Ei(V)': float,
            'vs.': str,
            'dE/dt': float,
            'dE/dt unit': str,
            'E1(V)': float,
            # 'vs.'              -- duplicate
            'Step percent': int,
            'N': int,
            'E range min(V)': float,
            'E range maxis_obj(V)': float,
            'I Range': str,
            'I Range min': str,
            'I Range maxis_obj': str,
            'I Range init': str,
            'Bandwidth': int,
            'E2(V)': float,
            # 'vs.'              -- duplicate
            'nc cycles': int,
            'Reverse Scan': int,
            'Ef(V)': float,
            # 'vs.'              -- duplicate
        }
        technique = self.header['technique']

        if technique == 'Galvanostatic Cycling with Potential Limitation':
            data_types = gcpl_data_types
        elif technique == 'Cyclic Voltammetry':
            data_types = cv_data_types
        else:
            raise ValueError(
                f"Technique '{technique}' is not supported.")

        with open(self.file_path, 'r', encoding=self.encoding) as file:
            reading_table = False
            line_number = 0
            param_table_dict = {}

            for line in file:
                line_number += 1
                line = line.strip()
                if line_number == self.parameter_table_start:
                    # Start reading the parameter table
                    reading_table = True

                if reading_table and line:
                    # Read data rows and append to the DataFrame
                    index_value = line[:20].strip()
                    if technique == 'Cyclic Voltammetry' and index_value == 'vs.':
                        # get last key in the dictionary
                        index_value = f'{list(param_table_dict.keys())[-1]} vs.'
                    row_values = [line[i:i+20].strip()
                                  for i in range(20, len(line), 20)]
                    row_type = data_types.get(index_value, str)
                    if row_type == float:
                        row_values = [row_type(item.replace(
                            self.decimal_separator, '.')) for item in row_values]
                    else:
                        row_values = [row_type(item) for item in row_values]
                    param_table_dict[index_value] = row_values

                elif reading_table and not line:
                    # End of the parameter table section
                    break

            self.parameter_table = pd.DataFrame(param_table_dict)
            # self.parameter_table = self.parameter_table.set_index(
            #    self.parameter_table.columns[0])

    def read_data(self):
        """
        Reads the data section of the MPT file and stores it as a pandas DataFrame.

        Method of the MptFile class that reads the data section of the MPT file defined
        by the file_path property of the object and stores it as a pandas DataFrame
        in the data property of the object.

        Parameters
        ----------
        self: MptFile object
            read_data() is called as a method of the MptFile object without
            additional parameters.

        Returns
        -------
        self.data: pandas DataFrame
            Data section of the MPT file stored as pandas DataFrame in the
            data property of the object.
        """
        if not self.header:
            self.read_header()

        if 'Nb header lines' in self.header:
            n_header_lines = self.header['Nb header lines'] - \
                (1+self.blank_header_lines)
            debug_msg = f'Number of header lines: {n_header_lines}'
            logging.debug(debug_msg)
        else:
            raise ValueError(
                "Number of header lines could not be detected.\n"
                "Make sure the input file is a valid 'EC-Lab ASCII FILE'"
                "and has 'Nb header lines:' defined in line 2.")

        self.data = pd.read_csv(self.file_path,
                                header=n_header_lines,
                                delimiter='\t',
                                decimal=self.decimal_separator,
                                encoding=self.encoding)
        # The last colunm name in Biologic MPT files may end with a tab character,
        # which causes pd.read_csv to add an extra column with no name. So we need
        # to remove the last column if it starts with 'Unnamed'.
        if self.data.columns[-1].startswith('Unnamed:'):
            self.data.drop(self.data.columns[-1], axis=1, inplace=True)

    def swap_charge_discharge_column_names(self):
        """
        Swap the assignment of charge and discharge specific column names 
        of self.data
        """
        col_capacity_charge = self.settings['columns'][self.method]['charge capacity']
        col_capacity_discharge = self.settings['columns'][self.method]['discharge capacity']
        col_energy_charge = self.settings['columns'][self.method]['charge energy']
        col_energy_discharge = self.settings['columns'][self.method]['discharge energy']
        col_capacitance_charge = self.settings['columns'][self.method]['charge capacitance']
        col_capacitance_discharge = self.settings['columns'][self.method]['discharge capacitance']

        col_map = {
            'capacity charge': (col_capacity_charge, False),
            'capacity discharge': (col_capacity_discharge, False),
            'energy charge': (col_energy_charge, False),
            'energy discharge': (col_energy_discharge, False),
            'capacitance charge': (col_capacitance_charge, False),
            'capacitance discharge': (col_capacitance_discharge, False)
        }

        # check if columns exist in self.data
        for col_name, (col, _) in col_map.items():
            if col in self.data.columns:
                col_map[col_name] = (col, True)

        def rename_columns(data, col_map, parameter):
            # rename capacity columns
            is_renamed_charge = col_map[f'{parameter} charge'][1]
            is_renamed_discharge = col_map[f'{parameter} discharge'][1]

            if is_renamed_charge and is_renamed_discharge:
                data.rename(columns={
                    col_map[f'{parameter} charge'][0]: 'temp',
                    col_map[f'{parameter} discharge'][0]: col_map[f'{parameter} charge'][0]
                }, inplace=True)
                data.rename(columns={'temp': col_map[f'{parameter} discharge'][0]}, inplace=True)
            elif is_renamed_charge:
                data.rename(columns={
                    col_map[f'{parameter} charge'][0]: col_map[f'{parameter} discharge'][0]
                }, inplace=True)
            elif is_renamed_discharge:
                data.rename(columns={
                    col_map[f'{parameter} discharge'][0]: col_map[f'{parameter} charge'][0]
                }, inplace=True)

        rename_columns(self.data, col_map, 'capacity')
        rename_columns(self.data, col_map, 'energy')
        rename_columns(self.data, col_map, 'capacitance')

    def update_column_cycle_number(self,
                                   first_cycle_number: int = None,
                                   cycle_offset: int = None):
        """
        Update cycle number column in self.data. If the column does not exist,
        it is added to self.data.
        """
        if first_cycle_number is None and 'first cycle number' in self.cycle_info:
            first_cycle_number = self.cycle_info['first cycle number']
        elif first_cycle_number is None:
            first_cycle_number = 1
            self.cycle_info['first cycle number'] = first_cycle_number
        else:
            self.cycle_info['first cycle number'] = first_cycle_number

        if cycle_offset is None and 'cycle offset' in self.cycle_info:
            cycle_offset = self.cycle_info['cycle offset']
        elif cycle_offset is None:
            cycle_offset = self.get_cycle_offset()
        else:
            self.cycle_info['cycle offset'] = cycle_offset

        # if cycle_offset == 1:
        #     first_cycle_number -= 1

        col_cycle_number = self.settings['columns'][self.method]['cycle number']
        col_half_cycle = self.settings['columns'][self.method]['half cycle number']
        # renumber half cycle column if half cycle numbers are not consecutive
        # get unique values in half cycle column
        half_cycle_numbers = self.data[col_half_cycle].unique()
        if len(half_cycle_numbers)-1 < half_cycle_numbers.max():
            # apply consecutive numbering
            self.data[col_half_cycle] = self.data[col_half_cycle].apply(
                lambda x: half_cycle_numbers.tolist().index(x))

        # add or update column 'cycle number' to data
        self.data[col_cycle_number] = self.data[col_half_cycle].apply(
            lambda x: int((x+cycle_offset)/2) + first_cycle_number)
        
        # fix ox/red column 
        self.fix_ox_red()

        # change sequence of columns
        # make cycle number column the first, half cycle the second, ox/red the third
        # and mode the fourth column in the DataFrame
        cols = self.data.columns.tolist()
        cols.remove(col_cycle_number)
        cols.remove(col_half_cycle)
        cols = [col_cycle_number, col_half_cycle] + cols
        self.data = self.data.reindex(columns=cols)

        # update the index column in data with new cycle numbers
        # self.data.index = self.data.index.set_levels(
        #     self.data.index.get_level_values(col_half_cycle).unique().apply(
        #         lambda x: int((x+cycle_offset)/2) + first_cycle_number),
        #     level=col_cycle_number)

    def fix_ox_red(self, drop: bool = False):
        """
        Fix values of the ox/red coulumn in self.data.

        ECLab assignes the ox/red value based on the sign of the control current.
        However, sometimes the sign of the control current does not match the sign 
        of the real current. This seams to happen most frequently when the control current
        is changed during the experiment and leads to single data points at the end of a
        charge or discharge step with the wrong ox/red value.

        This function fixes the ox/red column by checking the sign of the real current.
        Alternatively the data points with the wrong ox/red value can be removed.
        """
        # col_half_cycle = self.settings['columns'][self.method]['half cycle number']
        col_ox_red = self.settings['columns'][self.method]['ox/red']
        # col_control = self.settings['columns'][self.method]['control current']
        col_current = self.settings['columns'][self.method]['current']
        # get index of the first data point in the first cycle excluding the first ocv step
        col_mode = self.settings['columns'][self.method]['mode']
        
        # get indices of datapoints where mode is 1 and the real current is negative
        #  and ox/red is 1 or where it is positive and ox/red is zero
        ix_false_ox_red = self.data[
            ((self.data[col_current] < 0) & (self.data[col_ox_red] == 1) |
             (self.data[col_current] > 0) & (self.data[col_ox_red] == 0)) &
            (self.data[col_mode] == 1)].index
        if drop:
            # drop data points with wrong ox/red value
            self.data.drop(ix_false_ox_red, inplace=True)
        else:
            # fix ox/red value
            self.data.loc[ix_false_ox_red, col_ox_red] = abs(
                1 - self.data.loc[ix_false_ox_red, col_ox_red])

        # if self.data[col_mode].iloc[0] == 3:
        #     # get index of first data point which is not an ocv step
        #     index_start = self.data[self.data[col_mode] != 3].head(1).index[0]
        # else:
        #     index_start = 0
        #
        # index_cycle_end = self.data.loc[index_start:].groupby(col_half_cycle).tail(1).index
        # for _, idx in enumerate(index_cycle_end):
        #     if idx > 0 and self.data.loc[idx, col_ox_red] != \
        #             self.data.loc[idx-1, col_ox_red]:
        #         if self.data.loc[idx, col_current] > 0 and \
        #                 self.data.loc[idx, col_ox_red] == 0:
        #             self.data.loc[idx, col_ox_red] = 1
        #         elif self.data.loc[idx, col_current] < 0 and \
        #                 self.data.loc[idx, col_ox_red] == 1:
        #             self.data.loc[idx, col_ox_red] = 0

    def set_mulit_index(self, data=None):
        """
        Return a copy of self.data with cycle number, half cycle number and state as multi index.
        """
        col_cycle_number = self.settings['columns'][self.method]['cycle number']
        col_half_cycle = self.settings['columns'][self.method]['half cycle number']
        col_state = self.settings['columns'][self.method]['state']
        # make cycle number column the first, half cycle the second and state the
        # third column in the DataFrame
        cols = self.data.columns.tolist()
        cols.remove(col_cycle_number)
        cols.remove(col_half_cycle)
        cols.remove(col_state)
        cols = [col_cycle_number, col_half_cycle, col_state] + cols
        if data is None:
            # make a copy of self.data
            data = self.data.copy()
        # reindex columns
        data = data.reindex(columns=cols)
        # set these columns as index
        data.set_index(
            [col_cycle_number, col_half_cycle, col_state], inplace=True)
        return data

    # def add_column_cycle_number(self):
    #     """
    #     Add column 'cycle number' to data section of MPT file.
    #     """
    #     # check if data has a column named 'cycle number'
    #     offset = 0
    #     if 'cycle number' in self.data.columns:
    #         return
    #     else:
    #         if 'half cycle' in self.data.columns:
    #             if 'Cycle Definition' in self.header:
    #                 # if 'Cycle Definition' exists in header
    #                 # get cycle definition from header
    #                 cycle_definition = self.header['Cycle Definition']
    #                 if cycle_definition == 'Charge/Discharge alternace':
    #                     # determine first half cycle number where current is positive
    #                     first_positive_half_cycle = self.data.loc[
    #                         self.data['ox/red'] == 1, 'half cycle'].min()
    #                     # determine offset of first full cycle
    #                     # if first positive half cycle is even number, offset is 0
    #                     # if first positive half cycle is odd number, offset is 1
    #                     offset = 0 if first_positive_half_cycle % 2 == 0 else 1

    #                 elif cycle_definition == 'Discharge/Charge alternace':
    #                     # determine first half cycle number where current is negative
    #                     first_negative_half_cycle = self.data.loc[
    #                         self.data['ox/red'] == 0, 'half cycle'].min()
    #                     # determine offset of first full cycle
    #                     # if first negative half cycle is even number, offset is 1
    #                     # if first negative half cycle is odd number, offset is 0
    #                     offset = 1 if first_negative_half_cycle % 2 == 0 else 0

    #                 else:
    #                     offset = 0

    #             self.data['cycle number'] = self.data['half cycle'].apply(
    #                 lambda x: int((x+offset)/2))
    #         else:
    #             raise ValueError(
    #                 "Unable to determine cycle number.")
    #         # add column 'cycle number' to data

    def add_column_dq_dv(self, dv_step: float = 0, update: bool = False):
        """
        Add column 'dQ/dV' to data section of MPT file.

        Parameters
        ----------
        dv_step: float (optional)
            Voltage step size for resampling data in mV. If not specified, dv_step is set to 0
            and no resampling is performed.
        """
        # column names for voltage and charge
        voltage_columns = ['Ewe/V', 'Ecell/V']
        charge_columns = ['(Q-Qo)/mA.h', 'Q charge/discharge/mA.h']
        # find first column name in data that contains voltage
        voltage_column = next(
            (column for column in voltage_columns if column in self.data.columns), None)
        # find first column name in data that contains charge
        charge_column = next(
            (column for column in charge_columns if column in self.data.columns), None)
        # techniques that support adding dQ/dV column
        supported_techniques = [
            'Galvanostatic Cycling with Potential Limitation',
            'Galvanostatic Cycling with Potential Limitation 2',
            'Galvanostatic Cycling with Potential Limitation 3',
            'Galvanostatic Cycling with Potential Limitation 4',
            'Galvanostatic Cycling with Potential Limitation 5',
            'Galvanostatic Cycling with Potential Limitation 6',
            'Galvanostatic Cycling with Potential Limitation 7',
            'Potentiodynaic Cycling with Galvanostatic Acceleration'
        ]

        # check if technique is supported
        if self.header['technique'] not in supported_techniques:
            return
        # check if data has a column named 'dQ/dV'
        elif 'dQ/dV' in self.data.columns and not update:
            return
        elif voltage_column is not None and charge_column is not None:
            self.data['dQ/dV'] = 0.0
            self.data['dQ/dV grad'] = 0.0
            cycles = self.data['cycle number'].unique()
            for cycle in tqdm(cycles, desc='Calculating dQ/dV'):
                # logging.debug(f'Calculating dQ/dV for cycle {cycle}...')
                # calculate dQ/dV for charge step
                if not self.cycle_info['negative charge current']:
                    indices = self.data[(self.data['cycle number'] == cycle) &
                                        (self.data['<I>/mA'] > 0)].index
                else:
                    indices = self.data[(self.data['cycle number'] == cycle) &
                                        (self.data['<I>/mA'] < 0)].index
                dq_dv, dq_dv_grad = self.calculate_dq_dv(
                    voltage_column=voltage_column,
                    charge_column=charge_column,
                    dv_step=dv_step,
                    indices=indices)

                self.data.loc[indices, 'dQ/dV grad'] = dq_dv_grad
                self.data.loc[indices, 'dQ/dV'] = dq_dv

                # calculate dQ/dV for discharge step
                if not self.cycle_info['negative charge current']:
                    indices = self.data[(self.data['cycle number'] == cycle) &
                                        (self.data['<I>/mA'] < 0)].index
                else:
                    indices = self.data[(self.data['cycle number'] == cycle) &
                                        (self.data['<I>/mA'] > 0)].index
                dq_dv, dq_dv_grad = self.calculate_dq_dv(
                    voltage_column=voltage_column,
                    charge_column=charge_column,
                    dv_step=dv_step,
                    indices=indices)

                self.data.loc[indices, 'dQ/dV grad'] = dq_dv_grad
                self.data.loc[indices, 'dQ/dV'] = dq_dv
        else:
            raise ValueError(
                "Unable to determine voltage and charge columns.")

    def calculate_dq_dv(
            self, voltage_column, charge_column,
            dv_step: float = 0, indices: list = None,
            cycle: int = 1, state: str = 'charge'):
        """
        Calculate dQ/dV for a specific cycle.

        Parameters
        ----------
        dv_step: float (optional)
            Voltage step size for resampling data in mV. If not specified, dv_step is set to 0
            and no resampling is performed.
        cycle: int (optional)
            Cycle number for which dQ/dV is calculated. If not specified, cycle is set to 1.
        state: str (optional)
            Allowed values are 'charge' and 'discharge'. If not specified, state is set to
            'charge'.
        """
        logging.debug(f'Calculating dQ/dV for cycle {cycle}\n' +
                      f'   with voltage_column "{voltage_column}" and ' +
                      f'charge_column "{charge_column}" and state "{state}"...')
        if indices is not None:
            voltage = self.data.loc[indices, voltage_column]
            capacity = self.data.loc[indices, charge_column]
        else:
            cycle_data = self.get_cycle_data(cycle_number=cycle)
            if state == 'charge':
                voltage = cycle_data.loc[cycle_data['<I>/mA']
                                         > 0, voltage_column]
                capacity = cycle_data.loc[cycle_data['<I>/mA']
                                          > 0, charge_column]
            elif state == 'discharge':
                voltage = cycle_data.loc[cycle_data['<I>/mA']
                                         < 0, voltage_column]
                capacity = cycle_data.loc[cycle_data['<I>/mA']
                                          < 0, charge_column]
            else:
                raise ValueError(
                    f"Invalid value for state: '{state}'. " +
                    "Allowed values are 'charge' and 'discharge'.")
        if voltage.empty or capacity.empty:
            # return empty arrays if voltage or capacity is empty
            return np.array([]), np.array([])
        # resample data
        if dv_step > 0:
            v_start = voltage.iloc[0]
            v_end = voltage.iloc[-1]
            if v_start > v_end:
                dv_step = -dv_step
            interpolated_v = np.arange(v_start, v_end, dv_step/1000)
            if dv_step < 0:
                interpolated_v = interpolated_v[::-1]
                voltage = voltage[::-1]
                capacity = capacity[::-1]
            interpolated_q = np.interp(interpolated_v, voltage, capacity)
            debug_msg = f'Length of interpolated_q: {len(interpolated_q)} and ' + \
                f'interpolated_v: {len(interpolated_v)}'
            logging.debug(debug_msg)
            if (len(interpolated_q) > 10):
                dq_dv_grad = 1/np.gradient(interpolated_v, interpolated_q)
                dq_dv_grad = np.interp(voltage, interpolated_v, dq_dv_grad)
                dq_dv = np.diff(interpolated_q)/dv_step
                dq_dv = np.interp(
                    voltage, interpolated_v[0:-1]+dv_step/2000, dq_dv)
            else:
                dq_dv_grad = np.zeros(len(voltage))
                dq_dv = np.zeros(len(voltage))
            if dv_step < 0:
                dq_dv = dq_dv[::-1]
                dq_dv_grad = dq_dv_grad[::-1]
        else:
            dq_dv_grad = 1/np.gradient(voltage, capacity)
            dq_dv = np.diff(capacity)/np.diff(voltage)
        return dq_dv, dq_dv_grad

    def add_column_state(self):
        """
        Add column 'select' to data section of MPT file.
        """
        # add column 'select' to data
        self.data['state'] = '-'
        col_current = self.settings['columns'][self.method]['current']
        # set select to 'relax' for all rows where 'current' is 0
        self.data.loc[self.data[col_current] == 0, 'state'] = 'relax'
        # set select to 'charge' for all rows where 'current' is positive
        if self.cycle_info['negative charge current']:
            self.data.loc[self.data[col_current] < 0, 'state'] = 'charge'
            self.data.loc[self.data[col_current] > 0, 'state'] = 'discharge'
        else:
            self.data.loc[self.data[col_current] > 0, 'state'] = 'charge'
            self.data.loc[self.data[col_current]
                          < 0, 'state'] = 'discharge'

    def add_column_specific_capacity(self):
        """
        Add column 'specific capacity' to data section of MPT file.
        """
        characteristic_mass = self.header['Characteristic mass']['value']
        if characteristic_mass is None or characteristic_mass == 0:
            characteristic_mass = 1
            print('WARNING: No value is given for the Characteristic mass.')
            print(
                'WARNING: Specific capacitiy will be calculated with a characteristic mass of 1 g')

        characteristic_mass_unit = self.header['Characteristic mass']['unit']
        if characteristic_mass_unit == 'mg':
            characteristic_mass /= 1000
        elif characteristic_mass_unit == 'g':
            pass
        elif characteristic_mass_unit == 'kg':
            characteristic_mass *= 1000
        else:
            print('WARNING: No or an invalid unit is given for the Characteristic mass.')
            print(
                'WARNING: Characteristic mass unit is assumed to be g for calculating specific capacity.')

        col_capacity = self.settings['columns'][self.method]['capacity']
        # add column 'specific capacity' to data
        self.data['specific capacity'] = self.data[col_capacity] / \
            characteristic_mass
        # set unit of 'specific capacity' column

    def add_column_intrinsic_capacity(self):
        """
        Add column 'intrinsic capacity' to data section of MPT file.
        """
        active_material_mass = self.header['Mass of active material']['value']
        if active_material_mass is None or active_material_mass == 0:
            active_material_mass = 1
            print('WARNING: No value is given for the Mass of active material.')
            print(
                'WARNING: Intrinsic capacitiy will be calculated with an active material mass of 1 g')
        active_material_mass_unit = self.header['Mass of active material']['unit']
        if active_material_mass_unit == 'mg':
            active_material_mass /= 1000
        elif active_material_mass_unit == 'g':
            pass
        elif active_material_mass_unit == 'kg':
            active_material_mass *= 1000
        else:
            print(
                'WARNING: No or an invalid unit is given for the Mass of active material.')
            print(
                'WARNING: Active material mass unit is assumed to be g for calculating intrinsic capacity.')

        col_capacity = self.settings['columns'][self.method]['capacity']
        # add column 'intrinsic capacity' to data
        self.data['intrinsic capacity'] = self.data[col_capacity] / \
            active_material_mass

    def get_technique(self):
        """
        Get technique.
        """
        return self.header['technique']

    def get_cycle_data(self, cycle_number: int = None):
        """
        Get data for a specific cycle number.
        """
        if cycle_number is None:
            return self.data
        else:
            if 'cycle number' not in self.data.columns:
                self.update_column_cycle_number()
            return self.data[self.data['cycle number'] == cycle_number]

    def set_cycle_info(self,
                       cycle_starts_with: str = None,
                       negative_charge_current: bool = None,
                       offset: int = None):
        """
        Set cycle info.
        """
        if cycle_starts_with is not None:
            self.cycle_info['cycle starts with'] = cycle_starts_with
        if negative_charge_current is not None:
            self.cycle_info['negative charge current'] = negative_charge_current
        if offset is not None:
            self.cycle_info['offset'] = offset

        if self.cycle_info['cycle starts with'] is None:
            self.cycle_info['cycle starts with'] = self.get_cycle_start_type()

        if (self.cycle_info['negative charge current'] is None
                and self.cycle_info['offset'] is None):
            self.cycle_info['offset'] = 0
            self.cycle_info['negative charge current'] = self.has_negative_charge_current(
            )
        elif self.cycle_info['negative charge current'] is None:
            self.cycle_info['negative charge current'] = self.has_negative_charge_current(
            )
        elif self.cycle_info['offset'] is None:
            self.cycle_info['offset'] = self.get_cycle_offset()

        self.cycle_info['first half cycle type'] = self.get_first_half_cycle_type()
        self.cycle_info['number of cycles'] = len(self.get_cycle_numbers())

    def get_cycle_info(self) -> dict:
        """
        Return dictionary with cycle info.
        """
        # check if cycle info is already set
        if not self.cycle_info:
            self.set_cycle_info()
        return self.cycle_info

    def get_cycles(self) -> pd.DataFrame:
        """
        Return DataFrame with cycle info.
        """
        # check if cycles are already processed
        if not self.cycles:
            self.process_cycles()
        return self.cycles

    def process_cycles(self,
                       first_cycle_number: int = None,
                       negative_charge_current: bool = False,
                       cycle_starts_with: str = None) -> None:
        """
        Process data to obtain cycle based information a

        Parameters
        ----------
        first_cycle_number: int (optional)
            Start value for the cycle number of the first cycle. If the first cycle
            in the mpt file contains only one half cycle, the first cycle number is
            applied to the first full cycle. If not specified, the first cycle number
            is set to 1.
        negative_charge_current: bool (optional)
            If True, a charge step is identified by a negative current and a discharge
            step is identified by a positive current. This differs from Bio-Logic's
            default behavior where a charge step is identified always by a positive current.
            If not specified, the default behavior is used.
        cycle_starts_with: str (optional)
            Allowed values are 'charge' and 'discharge'. If specified, the beginning of
            each cycle is identified by the first charge or discharge step, respectively.
            This will override the 'Cycle Definition' setting in the MPT file header and
            is used to reindex the cycle numbers.

        Returns
        -------
        self.cycles: pandas DataFrame
            Cycle based information such as capacity, coulomb efficiency and more stored
            as a pandas DataFrame in the cycles property of the object.
        """
        if first_cycle_number is None and 'first cycle number' in self.cycle_info:
            first_cycle_number = self.cycle_info['first cycle number']
        elif first_cycle_number is None:
            first_cycle_number = 1
            self.cycle_info['first cycle number'] = first_cycle_number
        else:
            self.cycle_info['first cycle number'] = first_cycle_number

        if cycle_starts_with:
            self.cycle_info['cycle starts with'] = cycle_starts_with
        else:
            self.get_cycle_start_type()
        # check if the first complete cycle is a offset by a half cycle
        self.get_cycle_offset()

        self.get_first_half_cycle_type()
        if negative_charge_current:
            self.cycle_info['negative charge current'] = negative_charge_current
        else:
            self.get_sign_of_charge_current()

        # create a DataFrame for cycle indices
        self.cycle_indices = pd.DataFrame()
        # create a DataFrame for cycle information
        self.cycles = pd.DataFrame()

        logging.info('    Adding cycle numbers...')
        self.cycles['cycle number'] = self.get_cycle_numbers()
        # set cycle number as index and keep it as normal column
        self.cycles.set_index('cycle number', inplace=True)
        self.cycles['cycle number'] = self.cycles.index

        self.cycle_indices['cycle number'] = self.cycles['cycle number']
        self.cycle_indices.set_index('cycle number', inplace=True)

        logging.info('    Adding indices...')
        logging.info('    - cycle')
        [self.cycle_indices['cycle (start)'],
         self.cycle_indices['cycle (end)']] = self.get_cycle_indices()

        logging.info('    - half cycle (charge)')
        [self.cycle_indices['half cycle (charge, start)'],
         self.cycle_indices['half cycle (charge, end)']] = self.get_indices(state='charge')

        logging.info('    - half cycle (discharge)')
        [self.cycle_indices['half cycle (discharge, start)'],
         self.cycle_indices['half cycle (discharge, end)']] = self.get_indices(state='discharge')

        logging.info('    - galvanostatic (charge)')
        [self.cycle_indices['cc (charge, start)'],
         self.cycle_indices['cc (charge, end)']] = self.get_indices(
             state='charge', mode='galvanostatic')

        logging.info('    - galvanostatic (discharge)')
        [self.cycle_indices['cc (discharge, start)'],
         self.cycle_indices['cc (discharge, end)']] = self.get_indices(
             state='discharge', mode='galvanostatic')
        
        logging.info('    - potentiostatic (charge)')
        [self.cycle_indices['cv (charge, start)'],
         self.cycle_indices['cv (charge, end)']] = self.get_indices(
             state='charge', mode='potentiostatic')

        logging.info('    - potentiostatic (discharge)')
        [self.cycle_indices['cv (discharge, start)'],
         self.cycle_indices['cv (discharge, end)']] = self.get_indices(
             state='discharge', mode='potentiostatic')

        logging.info('    - ocv (charge)')
        [self.cycle_indices['ocv (charge, start)'],
         self.cycle_indices['ocv (charge, end)']] = self.get_indices(
             state='charge', mode='ocv')
        logging.info('    - ocv (discharge)')
        [self.cycle_indices['ocv (discharge, start)'],
         self.cycle_indices['ocv (discharge, end)']] = self.get_indices(
             state='discharge', mode='ocv')

        logging.info('    Adding duration (charge)...')
        self.cycles['duration cc (charge)'] = self.get_duration(
            state='charge', mode='galvanostatic')

        logging.info('    Adding duration (discharge)...')
        self.cycles['duration cc (discharge)'] = self.get_duration(
            state='discharge', mode='galvanostatic')

        logging.info('    Adding current (charge)...')
        self.cycles['current cc (charge)'] = self.get_current(
            method='mean', state='charge', mode='galvanostatic')

        logging.info('    Adding current (discharge)...')
        self.cycles['current cc (discharge)'] = self.get_current(
            method='mean', state='discharge', mode='galvanostatic')
        if self.header['Battery capacity']['value']:
            logging.info('    Adding C-rate (charge)...')
            self.cycles['C-rate (charge)'] = self.get_c_rate(state='charge')
            logging.info('    Adding C-rate (discharge)...')
            self.cycles['C-rate (discharge)'] = self.get_c_rate(state='discharge')
        else:
            # add column with specific current
            logging.info('    Adding specific current (charge)...')
            self.cycles['specific current (charge)'] = \
                self.get_specific_current(state='charge')
            logging.info('    Adding specific current (discharge)...')
            self.cycles['specific current (discharge)'] = \
                self.get_specific_current(state='discharge')

        logging.info('    Adding capacity (charge)...')
        self.cycles['capacity (charge)'] = self.get_capacity(state='charge')

        logging.info('    Adding capacity (discharge)...')
        self.cycles['capacity (discharge)'] = self.get_capacity(state='discharge')

        logging.info('    Adding specific capacity (charge)...')
        if self.header['Characteristic mass']['value']:
            unit = self.header['Characteristic mass']['unit']
            mass = self.header['Characteristic mass']['value']
            match unit:
                case 'mg':
                    mass /= 1000
                case 'kg':
                    mass *= 1000
            self.cycles['specific capacity (charge)'] = \
                self.cycles['capacity (charge)'] / mass
            logging.info('    Adding specific capacity (discharge)...')
            self.cycles['specific capacity (discharge)'] = \
                self.cycles['capacity (discharge)'] / mass
        if self.header['Mass of active material']['value']:
            logging.info('    Adding intrinsic capacity (charge)...')
            unit = self.header['Mass of active material']['unit']
            mass = self.header['Mass of active material']['value']
            match unit:
                case 'mg':
                    mass /= 1000
                case 'kg':
                    mass *= 1000
            self.cycles['intrinsic capacity (charge)'] = \
                self.cycles['capacity (charge)'] / mass
            logging.info('    Adding intrinsic capacity (discharge)...')
            self.cycles['intrinsic capacity (discharge)'] = \
                self.cycles['capacity (discharge)'] / mass
        voltage_type = self.get_voltage_type()
        voltage_charge_min = self.get_voltage(
            voltage_type=voltage_type, method='min', state='charge',
            mode='galvanostatic')
        if voltage_charge_min is not None:
            logging.info(f'    Adding {voltage_type} voltage (charge, min)...')
            self.cycles[
                f'{voltage_type} voltage (charge, min)'] = voltage_charge_min
        voltage_charge_max = self.get_voltage(
            voltage_type=voltage_type, method='max', state='charge',
            mode='galvanostatic')
        if voltage_charge_max is not None:
            logging.info(f'    Adding {voltage_type} voltage (charge, max)...')
            self.cycles[
                f'{voltage_type} voltage (charge, max)'] = voltage_charge_max
        voltage_discarge_min = self.get_voltage(
            voltage_type=voltage_type, method='min', state='discharge',
            mode='galvanostatic')
        if voltage_discarge_min is not None:
            logging.info(f'    Adding {voltage_type} voltage (discharge, min)...')
            self.cycles[
                f'{voltage_type} voltage (discharge, min)'] = voltage_discarge_min
        voltage_discharge_max = self.get_voltage(
            voltage_type=voltage_type, method='max', state='discharge',
            mode='galvanostatic')
        if voltage_discharge_max is not None:
            logging.info(
                f'    Adding {voltage_type} voltage (discharge, max)...')
            self.cycles[
                f'{voltage_type} voltage (discharge, max)'] = voltage_discharge_max
        voltage_drop_charge = self.get_voltage_drop('charge', voltage_type)
        if voltage_drop_charge is not None:
            logging.info(f'    Adding {voltage_type} voltage drop (charge)...')
            self.cycles[
                f'{voltage_type} voltage drop (charge)'] = voltage_drop_charge
        voltage_drop_discharge = self.get_voltage_drop('discharge', voltage_type)
        if voltage_drop_discharge is not None:
            logging.info(
                f'    Adding {voltage_type} voltage drop (discharge)...')
            self.cycles[
                f'{voltage_type} voltage drop (discharge)'] = voltage_drop_discharge
        voltage_rise_charge = self.get_voltage_drop('charge', voltage_type, rise=True)
        if voltage_rise_charge is not None:
            logging.info(f'    Adding {voltage_type} voltage rise (charge)...')
            self.cycles[
                f'{voltage_type} voltage rise (charge)'] = voltage_rise_charge
        voltage_rise_discharge = self.get_voltage_drop('discharge', voltage_type, rise=True)
        if voltage_rise_discharge is not None:
            logging.info(
                f'    Adding {voltage_type} voltage rise (discharge)...')
            self.cycles[
                f'{voltage_type} voltage rise (discharge)'] = voltage_rise_discharge
        ir_drop_charge = self.get_ir_drop('charge', voltage_type)
        if ir_drop_charge is not None:
            logging.info(f'    Adding IR drop ({voltage_type}, charge)...')
            self.cycles[
                f'IR drop ({voltage_type}, charge)'] = ir_drop_charge
        ir_drop_discharge = self.get_ir_drop('discharge', voltage_type)
        if ir_drop_discharge is not None:
            logging.info(f'    Adding IR drop ({voltage_type}, discharge)...')
            self.cycles[
                f'IR drop ({voltage_type}, discharge)'] = ir_drop_discharge
        ir_rise_charge = self.get_ir_rise('charge', voltage_type)
        if ir_rise_charge is not None:
            logging.info(f'    Adding IR rise ({voltage_type}, charge)...')
            self.cycles[
                f'IR rise ({voltage_type}, charge)'] = ir_rise_charge
        ir_rise_discharge = self.get_ir_rise('discharge', voltage_type)
        if ir_rise_discharge is not None:
            logging.info(f'    Adding IR rise ({voltage_type}, discharge)...')
            self.cycles[
                f'IR rise ({voltage_type}, discharge)'] = ir_rise_discharge

        self.cycles['P (max, charge)'] = self.get_power(
            state='charge', mode='galvanostatic', method='max')
        logging.info('    Adding P (charge, min)...')
        self.cycles['P (min, charge)'] = self.get_power(
            state='charge', mode='galvanostatic', method='min')
        logging.info('    Adding P (discharge, max)...')
        self.cycles['P (max, discharge)'] = self.get_power(
            state='discharge', mode='galvanostatic', method='max')
        logging.info('    Adding P (discharge, min)...')
        self.cycles['P (min, discharge)'] = self.get_power(
            state='discharge', mode='galvanostatic', method='min')
        logging.info('    Adding energy (charge)...')
        self.cycles['energy (charge)'] = self.get_energy(state='charge')
        logging.info('    Adding energy (discharge)...')
        self.cycles['energy (discharge)'] = self.get_energy(state='discharge')
        logging.info('    Adding coulobm efficiency...')
        self.cycles['coulomb efficiency'] = self.get_coulomb_efficiency()
        logging.info('    Adding energy efficiency...')
        self.cycles['energy efficiency'] = self.get_energy_efficiency()
        logging.info('    Adding energy loss...')
        self.cycles['energy loss'] = self.get_energy_loss()
        logging.info('    Adding capacity loss...')
        self.cycles['capacity loss'] = self.get_capacity_loss()
        # set cycle number as index
        # self.cycles.set_index('cycle number', inplace=True)

    def get_number_of_cycles(self, cycle_numbers: list = None):
        """
        Get number of cycles.
        """
        if 'number of cycles' not in self.cycle_info:
            if cycle_numbers is None:
                cycle_numbers = self.get_cycle_numbers()
            self.cycle_info['number of cycles'] = len(cycle_numbers)

        return self.cycle_info['number of cycles']

    def get_cycle_numbers(self):
        """
        Get cycle numbers.
        """
        if 'cycle number' not in self.data.columns:
            self.update_column_cycle_number()
        cycle_numbers = self.data['cycle number'].unique()
        self.cycle_info['number of cycles'] = len(cycle_numbers)
        # logging.debug(f'Cycle numbers length: {len(cycle_numbers)}')
        return cycle_numbers

    def set_cycle_start_type(self, cycle_start_type: str = None):
        """
        Determine weather a cycle starts with a charge or discharge step.
        """
        if cycle_start_type:
            pass
        else:
            if self.header['Cycle Definition'] == 'Charge/Discharge alternance':
                cycle_start_type = 'charge'
            elif self.header['Cycle Definition'] == 'Discharge/Charge alternance':
                cycle_start_type = 'discharge'
            else:
                print('No valid cycle definition found.',
                      'Assuming that each new cycle starts with a charge step.')
                cycle_start_type = 'charge'
            logging.debug('Cycle Definition is: ' + self.header["Cycle Definition"] + '\n' +
                          'Cycle start type set to: ' + cycle_start_type)

        self.cycle_info['cycle starts with'] = cycle_start_type

    def get_cycle_start_type(self):
        """
        Return cycle start type. If cycle start type is not set, determine
        weather a cycle starts with a charge or discharge step.
        """
        if self.cycle_info['cycle starts with'] is None:
            self.set_cycle_start_type()
        return self.cycle_info['cycle starts with']

    def has_negative_charge_current(self):
        """
        Determine weather the charge current is negative.
        """
        if self.cycle_info['negative charge current'] is None:
            sign = self.get_sign_of_charge_current()
            self.cycle_info['negative charge current'] = True if sign == 'negativ' else False
        return self.cycle_info['negative charge current']

    def set_cycle_offset(self, cycle_offset: int = None):
        """
        Determine the cycle offset.
        """
        if cycle_offset:
            pass
        else:
            cycle_starts_with = self.get_cycle_start_type()
            negative_charge_current = self.has_negative_charge_current()

            if cycle_starts_with == 'charge' and negative_charge_current:
                negative_current = True
            elif cycle_starts_with == 'discharge' and not negative_charge_current:
                negative_current = True
            else:
                negative_current = False

            col_half_cycle = self.settings['columns'][self.method]['half cycle number']
            col_current = self.settings['columns'][self.method]['current']
            # determine sign of current in first half cycle
            # average_current_first_half_cycle = self.data.loc[(slice(None), 0), col_current].mean()
            average_current_first_half_cycle = self.data.query(
                f'`{col_half_cycle}` == 0')[col_current].mean()

            if negative_current and average_current_first_half_cycle < 0:
                cycle_offset = 0
            elif not negative_current and average_current_first_half_cycle > 0:
                cycle_offset = 0
            else:
                cycle_offset = 1

        self.cycle_info['offset'] = cycle_offset

    def get_cycle_offset(self):
        """
        Determine the cycle offset.
        """
        if not self.cycle_info['offset']:
            self.set_cycle_offset()
        return self.cycle_info['offset']

    def get_first_half_cycle_type(self):
        """
        Determine the type of the first half cycle.
        !!!!!!!!!!! NEEDS TO BE REWRITTEN !!!!!!!!!!!!!
        """
        # get column names form mpt settings
        col_cycle_number = self.settings['columns'][self.method]['cycle number']
        col_half_cycle_number = self.settings['columns'][self.method]['half cycle number']
        # determine weather the first cycle has only one half cycle
        cycle_1 = self.data[self.data[col_cycle_number] == 0]
        # get number of half cycles in first cycle
        half_cycles_in_cycle_1 = cycle_1[col_half_cycle_number].nunique()
        # if first cycle has only one half cycle, set offset to 1
        if half_cycles_in_cycle_1 == 1:
            self.cycle_info['first half cycle type'] = (
                'charge' if self.cycle_info['cycle starts with'] == 'discharge'
                else 'discharge')
        else:
            self.cycle_info['first half cycle type'] = self.cycle_info['cycle starts with']

        return self.cycle_info['first half cycle type']

    def get_sign_of_charge_current(self):
        """
        Determine the sign of the charge current. If the charge current is negative,
        cycle_info['negative charge current'] is set to True, otherwise it is set to False.
        """
        col_current = self.settings['columns'][self.method]['current']
        col_half_cycle_number = self.settings['columns'][self.method]['half cycle number']
        cycle_offset = self.cycle_info['offset']
        cycle_starts_with = self.cycle_info['cycle starts with']
        # determine sign of current in first half cycle
        average_current_first_half_cycle = self.data.loc[
            self.data[col_half_cycle_number] == 0, col_current].mean()
        if cycle_offset == 0:
            if cycle_starts_with == 'charge' and average_current_first_half_cycle < 0:
                negative_charge_current = True
            elif cycle_starts_with == 'discharge' and average_current_first_half_cycle > 0:
                negative_charge_current = True
            else:
                negative_charge_current = False
        elif cycle_offset == 1:
            # if cycle_offset is 1, the first charge or discharge step is missing
            # i.e. if a cycle normally starts with a charge step the first half cycle is
            # actually a discharge step and vice versa
            if cycle_starts_with == 'charge' and average_current_first_half_cycle > 0:
                # first half cycle is a discharge step, if its average current is positive
                # the current of the charge step must be negative
                negative_charge_current = True
            elif cycle_starts_with == 'discharge' and average_current_first_half_cycle < 0:
                # first half cycle is a charge step, so the current of the charge step
                # is negative
                negative_charge_current = True
            else:
                negative_charge_current = False
        sign_of_charge_current = 'negativ' if negative_charge_current else 'positiv'
        return sign_of_charge_current

    def get_cycle_indices(self, update: bool = False):
        """
        Get the first and last indices of each full cycle by finding the index
        of the first occurrence of each cycle number in the 'cycle number' column
        """
        if ('cycle index (start)' in self.cycles.columns and
                'cycle index (end)' in self.cycles.columns and not update):
            index_start = self.cycles['cycle index (start)']
            index_end = self.cycles['cycle index (end)']
        else:
            # get column names form mpt settings
            col_cycle_number = self.settings['columns'][self.method]['cycle number']
            index_start = self.data[col_cycle_number].drop_duplicates(
                keep='first').index
            index_end = self.data[col_cycle_number].drop_duplicates(
                keep='last').index
        debug_msg = f'Cycle indices length (start, end): {len(index_start)}, ' + \
            f'{len(index_end)}'
        logging.debug(debug_msg)
        return index_start, index_end

    def get_indices(self,
                    state: str = None,
                    mode: str = None,
                    position: str = None,
                    update: bool = False):
        """
        Get the first and last indices of each charge relaxation period by finding the index
        of the first occurrence of each charge relaxation period in the 'current' column
        """
        indices_start = None
        indices_end = None

        mode_map = {
            'galvanostatic': (1, 'cc'),
            'potentiostatic': (2, 'cv'),
            'ocv': (3, 'ocv'),
            None: (None, 'half cycle')
        }

        if mode not in mode_map:
            raise ValueError(f'Invalid mode {mode}')
        mode_val, mode_str = mode_map[mode]

        if state not in ['charge', 'discharge', None]:
            raise ValueError(f'Invalid state {state}')

        if position not in ['start', 'end', None]:
            raise ValueError(f'Invalid position {position}')

        def get_existing_indices(cycle_indices, col_name):
            if col_name in cycle_indices.columns:
                return cycle_indices[col_name]
            else:
                return None

        def get_first_cycle_start(data, settings):
            col_mode = settings['columns'][self.method]['mode']
            if data[col_mode].iloc[0] == 3:
                # get index of first data point which is not an ocv step
                index = data[data[col_mode] != 3].head(
                    1).index[0]
            else:
                index = 0
            return index

        def get_indices_by_position(data, state, mode_val, position, update=False):
            # check if indices already exist in cycle_indices
            if not update:
                indices = get_existing_indices(
                    self.cycle_indices, f'{mode_val} ({state}, {position})')
                if indices is not None:
                    return indices

            negative_charge_current = self.cycle_info['negative charge current']
            first_cycle_number = self.cycle_info['first cycle number']
            number_of_cycles = self.get_number_of_cycles()
            col_cycle_number = self.settings['columns'][self.method]['cycle number']
            col_ox_red = self.settings['columns'][self.method]['ox/red']
            col_mode = self.settings['columns'][self.method]['mode']

            if state == 'charge':
                ox_red = 1
            elif state == 'discharge':
                ox_red = 0

            # invert ox_red if negative charge current
            if negative_charge_current:
                ox_red = abs(ox_red - 1)

            if position == 'start':
                method = 'head'
            elif position == 'end':
                method = 'tail'
            else:
                raise ValueError('Invalid position')

            index_start = get_first_cycle_start(self.data, self.settings)
            if state is None:
                # get indices of whole cycles
                indices = data.loc[index_start:].groupby(
                    col_cycle_number).agg(method, 1).index
            elif mode_val is None:
                # get indices of charge or discharge half cycles
                indices = data.loc[index_start:].loc[
                    data[col_ox_red] == ox_red].groupby(
                        col_cycle_number).agg(method, 1).index
            else:
                # get indices of ocv, cv or cc steps
                indices = data.loc[index_start:].loc[
                    (data[col_ox_red] == ox_red)
                    & (data[col_mode] == mode_val)].groupby(
                        col_cycle_number).agg(method, 1).index

            cycle_numbers = data.loc[indices, col_cycle_number].values
            # convert into pd.Series and reindex with cycle numbers
            indices = pd.Series(indices, index=cycle_numbers)
            indices_new = pd.Series(
                index=range(first_cycle_number, first_cycle_number + number_of_cycles))
            indices_new.update(indices)
            return indices_new

        match position:
            case 'start' | 'end':
                indices = get_indices_by_position(
                    self.data, state, mode_val, position, update=update)
                return indices
            case _:
                indices_start = get_indices_by_position(
                    self.data, state, mode_val, 'start')
                indices_end = get_indices_by_position(
                    self.data, state, mode_val, 'end')
                return indices_start, indices_end
        
    def get_cycle_sequence(self):
        """
        Get the sequence number of charge and discharge steps for each cycle.
        """
        if 'cycle sequence' not in self.cycles.columns:
            col_cycle_number = self.settings['columns'][self.method]['cycle number']
            col_half_cycle_number = self.settings['columns'][self.method]['half cycle number']
            col_sequence_number = self.settings['columns'][self.method]['sequence number']
            self.cycles['cycle sequence'] = self.data.groupby(
                [col_cycle_number, col_half_cycle_number])[col_sequence_number].mean().reset_index(drop=True)
        return self.cycles['cycle sequence']

    def get_duration(self,
                     state: str,
                     mode: str = None,
                     update: bool = False):
        """
        Get the duration of each step.
        """
        mode_dict = {
            'galvanostatic': 'cc',
            'potentiostatic': 'cv',
            'ocv': 'ocv'
        }
        if mode in mode_dict:
            mode_str = mode_dict[mode] + ' '
        else:
            mode_str = ''

        if f'duration {mode_str}({state})' in self.cycles.columns and not update:
            duration = self.cycles[f'duration {mode_str}({state})']
        else:
            index_start, index_end = self.get_indices(state=state, mode=mode, update=update)
            col_time = self.settings['columns'][self.method]['time']
            # get indices where index_start and index_end are both not NaN
            not_nan = index_start.notna() & index_end.notna()
            tmp_duration = self.data.loc[index_end[not_nan], col_time].values - \
                self.data.loc[index_start[not_nan], col_time].values
            # set of not_nan==True as index for tmp_duration
            tmp_duration = pd.Series(tmp_duration, index=index_start[not_nan].index)
            # create new series with full range of cycle numbers as index
            duration = pd.Series(index=self.cycle_indices.index)
            # update values of duration with values from tmp_duration
            duration.update(tmp_duration)
        debug_msg = f'Duration {state} length: {len(duration)}'
        logging.debug(debug_msg)
        return duration

    def get_current(self,
                    method: str = None,
                    state: str = None,
                    mode: str = None,
                    update: bool = False):
        """
        Get the current of each step.
        """
        mode_dict = {
            'galvanostatic': 'cc',
            'potentiostatic': 'cv',
            'ocv': 'ocv'
        }
        if mode in mode_dict:
            mode_str = mode_dict[mode] + ' '
        else:
            mode_str = ''

        if f'current {mode_str}({state})' in self.cycles.columns and not update:
            current = self.cycles[f'current {mode_str}({state})']
        else:
            index_start, index_end = self.get_indices(state=state, mode=mode, update=update)
            col_current = self.settings['columns'][self.method]['current']
            # get indices where index_start and index_end are both not NaN
            not_nan = index_start.notna() & index_end.notna()
            intervals = pd.IntervalIndex.from_arrays(
                index_start[not_nan], index_end[not_nan])
            tmp_current = self.data.groupby(
                pd.cut(self.data.index, intervals), observed=False
            )[col_current].agg(method)
            # set index of not_nan as index for tmp_current
            tmp_current = tmp_current.reset_index(drop=True).reindex(
                index=not_nan.index)
            # create new series with full range of cycle numbers as index
            current = pd.Series(index=self.cycle_indices.index)
            # update values of current with values from tmp_current
            current.update(tmp_current)
        debug_msg = f'Current {mode_str}{state} length: {len(current)}'
        logging.debug(debug_msg)
        return current

    def get_c_rate(self,
                   state: str,
                   update: bool = False):
        """
        Get the c-rate of each charge step.
        """
        if f'C-rate ({state})' in self.cycles.columns and not update:
            c_rate = self.cycles[f'C-rate ({state})']
        else:
            current = self.get_current(method='mean', state=state, mode='galvanostatic')
            capacity = self.header['Battery capacity']['value']
            if capacity:
                c_rate = current.apply(
                    calc_c_rate, capacity=capacity)
            else:
                characteristic_mass = self.header['Characteristic mass']['value']
                characteristic_mass_unit = self.header['Characteristic mass']['unit']
                # convert characteristic mass to g
                if characteristic_mass_unit == 'mg':
                    characteristic_mass = characteristic_mass / 1000
                elif characteristic_mass_unit == 'kg':
                    characteristic_mass = characteristic_mass * 1000
                else:
                    pass

                c_rate = current.apply(
                    calc_mass_specific_current, mass=characteristic_mass)
        debug_msg = f'C-rate charge length: {len(c_rate)}'
        logging.debug(debug_msg)
        return c_rate

    def get_specific_current(self, state: str = None, update: bool = False):
        """
        Get the specific current of each charge step.
        """
        if f'specific current ({state})' in self.cycles.columns and not update:
            specific_current = self.cycles[f'specific current ({state})']
        else:
            match state:
                case 'charge':
                    current = self.get_current(method='mean', state='charge', mode='galvanostatic')
                case 'discharge':
                    current = self.get_current(method='mean', state='discharge', mode='galvanostatic')
                case _:
                    raise ValueError(
                        'Invalid state. Must be either "charge" or "discharge"')

            characteristic_mass = self.header['Characteristic mass']['value']
            characteristic_mass_unit = self.header['Characteristic mass']['unit']
            # convert characteristic mass to g
            if characteristic_mass_unit == 'mg':
                characteristic_mass = characteristic_mass / 1000
            elif characteristic_mass_unit == 'kg':
                characteristic_mass = characteristic_mass * 1000
            else:
                pass

            specific_current = current.apply(
                calc_mass_specific_current, mass=characteristic_mass)
        debug_msg = f'Specific current {state} length: {len(specific_current)}'
        logging.debug(debug_msg)
        return specific_current

    def get_capacity(self, state: str, update: bool = False):
        """
        Get the capacity of each step.
        """
        if f'capacity ({state})' in self.cycles.columns and not update:
            capacity = self.cycles[f'capacity ({state})']
        else:
            index_start, index_end = self.get_indices(state=state)
            not_nan = index_start.notna() & index_end.notna()
            col_charge = self.settings['columns'][self.method]['charge']
            tmp_capacity = self.data.loc[index_end[not_nan], col_charge].values - \
                self.data.loc[index_start[not_nan], col_charge].values
            # set of not_nan==True as index for tmp_capacity
            tmp_capacity = pd.Series(tmp_capacity, index=index_start[not_nan].index)
            # create new series with full range of cycle numbers as index
            capacity = pd.Series(index=self.cycle_indices.index)
            # update values of capacity with values from tmp_capacity
            capacity.update(tmp_capacity)

        debug_msg = f'Capacity {state} length: {len(capacity)}'
        logging.debug(debug_msg)
        return abs(capacity)
    
    def get_specific_capacity(self, state: str, update: bool = False):
        """
        Get the specific capacity of each step.
        """
        if f'specific capacity ({state})' in self.cycles.columns and not update:
            specific_capacity = self.cycles[f'specific capacity ({state})']
        else:
            capacity = self.get_capacity(state)
            characteristic_mass = self.header['Characteristic mass']['value']
            characteristic_mass_unit = self.header['Characteristic mass']['unit']
            # convert characteristic mass to g
            if characteristic_mass_unit == 'mg':
                characteristic_mass = characteristic_mass / 1000
            elif characteristic_mass_unit == 'kg':
                characteristic_mass = characteristic_mass * 1000
            else:
                pass

            specific_capacity = capacity / characteristic_mass
        debug_msg = f'Specific capacity {state} length: {len(specific_capacity)}'
        logging.debug(debug_msg)
        return specific_capacity

    def get_voltage(self,
                    voltage_type: str = None,
                    method: str = None,
                    state: str = None,
                    mode: str = None,
                    update: bool = False):
        """
        Get the voltage of each step.
        """
        voltage_type = voltage_type.lower()
        vt_map = {
            'cell': ('Cell', 'cell voltage'),
            'we': ('WE', 'working electrode voltage'),
            'ce': ('CE', 'counter electrode voltage')
        }
        voltage_type = voltage_type.lower()
        if voltage_type not in vt_map:
            raise ValueError('Invalid voltage type')
        v_str, v_key = vt_map[voltage_type]

        if method not in ['min', 'max', 'mean', 'sum', 'std', 'median', 'first', 'last']:
            raise ValueError('Invalid method')

        if f'{v_str} voltage ({state}, {method})' in self.cycles.columns and not update:
            voltage = self.cycles[f'{v_str} voltage ({state}, {method})']
        else:
            index_start, index_end = self.get_indices(state=state, mode=mode)
            col_voltage = self.settings['columns'][self.method][f'{v_key}']
            if col_voltage not in self.data.columns.tolist():
                warning_msg = f'Voltage column for {voltage_type} not found!'
                logging.warning(warning_msg)
                return None

            not_nan = index_start.notna() & index_end.notna()
            intervals = pd.IntervalIndex.from_arrays(
                index_start[not_nan], index_end[not_nan])
            tmp_voltage = self.data.groupby(
                pd.cut(self.data.index, intervals), observed=False)[
                    col_voltage].agg(method)
            # set index of not_nan as index for tmp_voltage
            tmp_voltage = tmp_voltage.reset_index(drop=True).reindex(
                index=not_nan.index)
            # create new series with full range of cycle numbers as index
            voltage = pd.Series(index=self.cycle_indices.index)
            # update values of voltage with values from tmp_voltage
            voltage.update(tmp_voltage)

        debug_msg = f'{v_str} Voltage {state} length: {len(voltage)}'
        logging.debug(debug_msg)
        return voltage
    
    def get_voltage_type(self):
        """
        Get voltage column and voltage type of the data file.
        """
        if 'Ewe/V' in self.data.columns:
            voltage_type = 'WE'
        elif 'Ecell/V' in self.data.columns:
            voltage_type = 'cell'
        else:
            voltage_type = None
        return voltage_type

    def get_voltage_drop(self,
                         state: str = None,
                         voltage_type: str = None,
                         rise: bool = False,
                         update: bool = False):
        """
        Get the voltage drop of each charge or discharge step.
        """
        match state:
            case 'charge':
                rise_state = 'discharge'
            case 'discharge':
                rise_state = 'charge'
            case _:
                raise ValueError(
                    'Invalid state. Must be either "charge" or "discharge"')
        
        device = self.header['Device']
        # check if device starts with 'VMP3'
        if voltage_type is None:
            if device.startswith('VMP3'):
                col_voltage = 'Ewe/V'
                voltage_type = 'WE'
            elif device.startswith('BCS'):
                if 'Ewe/V' in self.data.columns:
                    col_voltage = 'Ewe/V'
                    voltage_type = 'WE'
                elif 'Ecell/V' in self.data.columns:
                    col_voltage = 'Ecell/V'
                    voltage_type = 'cell'
                else:
                    warning_msg = 'No voltage column found! Voltage drop will not be calculated.'
                    logging.warning(warning_msg)
                    return None
            else:
                warning_msg = 'Device not supported for voltage drop calculation!'
                logging.warning(warning_msg)
                return None
        else:
            if voltage_type == 'WE':
                col_voltage = 'Ewe/V'
            elif voltage_type == 'cell':
                col_voltage = 'Ecell/V'
            else:
                warning_msg = f'Voltage type "{voltage_type}" not available for device "{device}"!'
                logging.warning(warning_msg)
                return None

        if rise:
            drop_state = 'rise'
        else:
            drop_state = 'drop'

        if f'{voltage_type} voltage {drop_state} ({state})' in self.cycles.columns and not update:
            voltage_drop = self.cycles[f'{voltage_type} voltage {drop_state} ({state})']
        else:
            # get indices of ocv, galvanostatic and potentiostatic steps
            if rise:
                indices_ocv = self.get_indices(mode='ocv', state=state, position='end')
                indices_galv = self.get_indices(mode='galvanostatic', state=rise_state, position='start')
                indices_pot = self.get_indices(mode='potentiostatic', state=rise_state, position='start')
                # get cycle definition from self.cycle_info
                cycle_starts_with = self.cycle_info['cycle starts with']
                if ((cycle_starts_with == 'charge' and state == 'discharge') or
                        (cycle_starts_with == 'discharge' and state == 'charge')):
                    indices_galv = indices_galv.shift(1)
                    indices_pot = indices_pot.shift(1)
            else:
                indices_ocv = self.get_indices(mode='ocv', state=state, position='start')
                indices_galv = self.get_indices(mode='galvanostatic', state=state, position='end')
                indices_pot = self.get_indices(mode='potentiostatic', state=state, position='end')
            # get indices of indices_pot wich are not NaN
            indices_not_nan_pot = indices_pot[~indices_pot.isnull()].index
            if len(indices_not_nan_pot) > 0:
                non_nan_pot_cycles = self.cycles.loc[indices_not_nan_pot, 'cycle number']
                warning_msg = ' ' + \
                    'Voltage drop calculation currently not supported for CCCV cycles!\n' + \
                    '    The following cycles will be excluded from the calculation:\n' + \
                    f'    {non_nan_pot_cycles.to_list()}'
                logging.warning(warning_msg)
            # create empty series for voltage drop for all indices
            voltage_drop = pd.Series(index=indices_galv.index)
            # remove indices_not_nan_pot from indices_ocv and indices_galv
            indices_ocv = indices_ocv.drop(indices_not_nan_pot)
            indices_galv = indices_galv.drop(indices_not_nan_pot)
            # get indices of all NaN values in indices_ocv and indices_galv
            indices_nan_ocv = indices_ocv[indices_ocv.isnull()].index
            indices_nan_galv = indices_galv[indices_galv.isnull()].index
            # get indices of all NaN values in indices_ocv and indices_galv
            indices_nan = indices_nan_ocv.union(indices_nan_galv)
            # get indices not in indices_nan
            indices_not_nan = indices_galv.index.difference(indices_nan)
            # calculate voltage drop for indices in indices_not_nan and 
            # convert to mV
            voltage_drop.loc[indices_not_nan] = (
                self.data.loc[indices_galv.loc[indices_not_nan], col_voltage].values -
                self.data.loc[indices_ocv.loc[indices_not_nan], col_voltage].values
            ) * 1000
            # drop index von voltage_drop
            voltage_drop = voltage_drop.reset_index(drop=True)

        return abs(voltage_drop)

    def get_ir_drop(self, state: str = None, vtype: str = None, update: bool = False):
        """
        Get the IR drop of each charge or discharge step.
        """
        degug_msg = f'Entering get_ir_drop ({vtype}, {state})'
        logging.info(degug_msg)
        match vtype:
            case 'WE' | 'cell':
                pass
            case None:
                vtype = 'WE'
            case _:
                raise ValueError('Invalid type. Must be either "WE" or "cell"')

        if f'IR drop ({vtype}, {state})' in self.cycles.columns and not update:
            ir_drop = self.cycles[f'IR drop ({vtype} ,{state})']
        else:
            if state == 'charge':
                voltage_drop = self.get_voltage_drop(state='charge', voltage_type=vtype)
                current = self.get_current(method='mean', state='charge', mode='galvanostatic')
            elif state == 'discharge':
                voltage_drop = self.get_voltage_drop(state='discharge', voltage_type=vtype)
                current = self.get_current(method='mean', state='discharge', mode='galvanostatic')
            else:
                raise ValueError(
                    'Invalid state. Must be either "charge" or "discharge"')

            if voltage_drop is not None and current is not None:
                # voltage drop is in mV, current in mA, ir_drop in Ohm
                ir_drop = abs(voltage_drop / current)
            else:
                ir_drop = None

        return ir_drop

    def get_ir_rise(self, state: str = None, vtype: str = None, update: bool = False):
        """
        Get the IR rise of each charge or discharge step.
        """
        match vtype:
            case 'WE' | 'cell':
                pass
            case None:
                vtype = 'WE'
            case _:
                raise ValueError('Invalid type. Must be either "WE" or "cell"')

        if f'IR rise ({vtype}, {state})' in self.cycles.columns and not update:
            ir_rise = self.cycles[f'IR rise ({vtype}, {state})']
        else:
            if state == 'charge':
                voltage_rise = self.get_voltage_drop(
                    state='charge', voltage_type=vtype, rise=True)
                current = self.get_current(method='mean', state='charge', mode='galvanostatic')
            elif state == 'discharge':
                voltage_rise = self.get_voltage_drop(
                    state='discharge', voltage_type=vtype, rise=True)
                current = self.get_current(method='mean', state='discharge', mode='galvanostatic')
            else:
                raise ValueError(
                    'Invalid state. Must be either "charge" or "discharge"')

            if voltage_rise is not None and current is not None:
                # voltage rise is in mV, current in mA, ir_rise in Ohm
                ir_rise = abs(voltage_rise / current)
            else:
                ir_rise = None

        return ir_rise

    def get_power(self,
                  state: str = None,
                  mode: str = None,
                  method: str = None,
                  update: bool = False):
        """
        Get the power of each step.
        """
        if f'P ({state}, {method})' in self.cycles.columns and not update:
            power = self.cycles[f'P ({state}, {method})']
        else:
            col_power = self.settings['columns'][self.method]['power']
            index_start, index_end = self.get_indices(state=state, mode=mode)
            not_nan = index_start.notna() & index_end.notna()
            intervals = pd.IntervalIndex.from_arrays(
                index_start[not_nan], index_end[not_nan])
            tmp_power = self.data.groupby(
                pd.cut(self.data.index, intervals), observed=False)[
                    col_power].agg(method)
            # set index of not_nan as index for tmp_power
            tmp_power = tmp_power.reset_index(drop=True).reindex(
                index=not_nan.index)
            # create new series with full range of cycle numbers as index
            power = pd.Series(index=self.cycle_indices.index)
            # update values of power with values from tmp_power
            power.update(tmp_power)

        debug_msg = f'Power {state} length: {len(power)}'
        logging.debug(debug_msg)
        return power
    
    def get_energy(self,
                   state: str = None,
                   mode: str = None,
                   update: bool = False):
        """
        Get the energy of each step.
        """
        if f'energy ({state})' in self.cycles.columns and not update:
            energy = self.cycles[f'energy ({state})']
        else:
            col_energy = self.settings['columns'][self.method][f'{state} energy']
            index_start, index_end = self.get_indices(state=state, mode=mode)
            not_nan = index_start.notna() & index_end.notna()
            tmp_energy = self.data.loc[index_end[not_nan], col_energy].values - \
                self.data.loc[index_start[not_nan], col_energy].values
            
            # convert energy from Wh to Wh / kg
            characteristic_mass = self.header['Characteristic mass']['value']
            characteristic_mass_unit = self.header['Characteristic mass']['unit']
            # convert characteristic mass to g
            conversion_dict = {
                'mg': 0.000001,
                'g': 0.001,
                'kg': 1,
            }
            if characteristic_mass is not None:
                if characteristic_mass_unit in conversion_dict:
                    characteristic_mass = (
                        characteristic_mass * conversion_dict[characteristic_mass_unit]
                    )
                elif characteristic_mass_unit in ['', None]:
                    warning_msg = 'Characteristic mass unit is not specified.\n' + \
                        '    Characteristic mass unit is assumed to be "mg".'
                    logging.warning(warning_msg)
                    characteristic_mass = (
                        characteristic_mass * conversion_dict['mg']
                    )
                else:
                    warning_msg = (
                        f'Characteristic mass unit is specified as "{characteristic_mass_unit}" which is not supported.\n' +
                        '    Characteristic mass unit is assumed to be "mg".'
                    )
                    logging.warning(warning_msg)
                    characteristic_mass = (
                        characteristic_mass * conversion_dict['mg']
                    )

                tmp_energy = tmp_energy / characteristic_mass
            else:
                warning_msg = 'Characteristic mass is not specified.\n' + \
                    '    Energy is not converted to Wh / kg.'
                logging.warning(warning_msg)
            # set of not_nan==True as index for tmp_energy
            tmp_energy = pd.Series(tmp_energy, index=index_start[not_nan].index)
            # create new series with full range of cycle numbers as index
            energy = pd.Series(index=self.cycle_indices.index)
            # update values of energy with values from tmp_energy
            energy.update(tmp_energy)

        debug_msg = f'Energy {state} length: {len(energy)}'
        logging.debug(debug_msg)
        return energy

    def get_coulomb_efficiency(self, update: bool = False):
        """
        Get the coulomb efficiency of each cycle
        """
        if 'coulomb efficiency' in self.cycles.columns and not update:
            coulomb_efficiency = self.cycles['coulomb efficiency']
        else:
            capacity_charge = self.get_capacity(state='charge', update=update)
            capacity_discharge = self.get_capacity(state='discharge', update=update)
            coulomb_efficiency = abs(capacity_discharge / capacity_charge)*100
        return coulomb_efficiency

    def get_capacity_loss(self, update: bool = False):
        """
        Get the capacity loss of each cycle.
        """
        if 'capacity loss' in self.cycles.columns and not update:
            capacity_loss = self.cycles['capacity loss']
        else:
            capacity_charge = self.get_specific_capacity(state='charge', update=update)
            capacity_discharge = self.get_specific_capacity(state='discharge', update=update)
            capacity_loss = capacity_charge - capacity_discharge
        return capacity_loss

    def get_energy_efficiency(self, update: bool = False):
        """
        Get the energy efficiency of each cycle.
        """
        if 'energy efficiency' in self.cycles.columns and not update:
            energy_efficiency = self.cycles['energy efficiency']
        else:
            energy_charge = self.get_energy(state='charge', update=update)
            energy_discharge = self.get_energy(state='discharge', update=update)
            energy_efficiency = abs(energy_discharge / energy_charge)*100
        return energy_efficiency

    def get_energy_loss(self, update: bool = False):
        """
        Get the energy loss of each cycle.
        """
        if 'energy loss' in self.cycles.columns and not update:
            energy_loss = self.cycles['energy loss']
        else:
            energy_charge = self.get_energy(state='charge', update=update)
            energy_discharge = self.get_energy(state='discharge', update=update)
            energy_loss = energy_charge - energy_discharge
            if self.cycle_info['negative charge current']:
                energy_loss = -energy_loss
        return energy_loss

    def pad_cycle_indices(self, series: pd.Series, type: str = 'charge'):
        """
        Pad cycle series indices with zero or len(self.cycles) to match length of self.cycles.
        """
        offset = self.cycle_info['offset']
        cycle_starts_with = self.cycle_info['cycle starts with']
        if cycle_starts_with != type and offset == 1:
            series = pd.Index([0], dtype='int64').append(series)

        if len(series) < len(self.cycles):
            series = series.append(
                pd.Index([len(self.data)-1]*(len(self.cycles)-len(series))))

        return series

    def save_data(self, file_path: str = None):
        """
        Save data to CSV file.
        """
        if file_path is None:
            file_path = os.path.splitext(self.file_path)[0] + '_data.csv'
        else:
            pass

        self.data.to_csv(file_path, index=False)

    def save_reduced_data(self, file_path: str = None):
        """
        Save reduced data to CSV file.
        """
        # Define cycles for export
        cycles = [1, 2, 3, 4, 5, 10, 15, 15, 50, 100,
                  250, 750, 1000, 1250, 1500, 1750, 2000]
        # Define columns for export
        col_cycle_number = self.settings['columns'][self.method]['cycle number']
        col_state = 'state'
        col_half_cycle_number = self.settings['columns'][self.method]['half cycle number']
        col_time = self.settings['columns'][self.method]['time']
        col_we_voltage = self.settings['columns'][self.method]['working electrode voltage']
        col_cell_voltage = self.settings['columns'][self.method]['cell voltage']
        col_current = self.settings['columns'][self.method]['current']
        col_capacity = self.settings['columns'][self.method]['capacity']
        col_dq_dv = self.settings['columns'][self.method]['qQ_dV']
        columns = [col_cycle_number, col_state,
                   col_half_cycle_number, col_time]
        if col_we_voltage in self.data.columns:
            columns.append(col_we_voltage)
        for item in col_cell_voltage:
            if item in self.data.columns:
                columns.append(item)
        columns.extend(
            [col_current, col_capacity, col_dq_dv])

        # create reduced data set with only the columns defined in columns and cycles defined in cycles
        reduced_data = pd.DataFrame(columns=columns)
        for cycle in cycles:
            if cycle <= len(self.cycles):
                cycle_data = self.get_cycle_data(cycle)
                reduced_data = pd.concat(
                    [reduced_data, cycle_data[columns]], ignore_index=True)

        # set file_path for saving reduced data
        if file_path is None:
            file_path = os.path.splitext(self.file_path)[
                0] + '_reduced_data.csv'
        else:
            pass

        # save reduced data
        reduced_data.to_csv(file_path, index=False)

    def save_parameter_table(self, file_path: str = None):
        """
        Save parameter table to CSV file.
        """
        if file_path is None:
            file_path = os.path.splitext(
                self.file_path)[0] + '_parameter_table.csv'
        else:
            pass

        self.parameter_table.T.to_csv(file_path, index=True, header=False)

    def save_cycles(self, file_path: str = None):
        """
        Save cycle info to CSV file.
        """
        if self.cycles is None:
            self.get_cycles()

        if file_path is None:
            file_path = os.path.splitext(self.file_path)[0] + '_cycle_info.csv'
        else:
            pass

        self.cycles.to_csv(file_path, index=False)

    def create_plots(self,
                     plot_options: dir = None,
                     canvases: list = None,
                     save_plots: bool = False,
                     file_path_base: str = None):
        """
        Create plots.
        """
        if plot_options is not None:
            exclude_cycles = plot_options['exclude cycles']
            cycles_to_plot_vvsq = plot_options['cycles to plot v vs q']
            cycles_to_plot_dqdv = plot_options['cycles to plot dqdv']
        else:
            exclude_cycles = []
            first_cycle_number = self.cycle_info['first cycle number']
            cycles_to_plot_vvsq = [1, 2, 3, 4, 5, 10, 25, 50, 100, 250, 500, 750, 1000,
                                   1250, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000,
                                   5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000]
            # add first cycle number to cycles_to_plot_vvsq
            cycles_to_plot_vvsq = [cycle + first_cycle_number - 1
                                   for cycle in cycles_to_plot_vvsq]
            cycles_to_plot_dqdv = [1, 3]
            # add first cycle number to cycles_to_plot_dqdv
            cycles_to_plot_dqdv = [cycle + first_cycle_number - 1
                                   for cycle in cycles_to_plot_dqdv]

        debug_info = f'Creating plots was called with plot_options: {plot_options}'
        logging.debug(debug_info)
        # load plot colors from yaml file
        color_settings_path = os.path.join('resources', 'plot_colors.yaml')
        color_settings_data = pkgutil.get_data(
            __main_package__, color_settings_path)
        if color_settings_data is not None:
            color_settings_data = color_settings_data.decode('utf-8')
            plot_colors = yaml.safe_load(color_settings_data)
        else:
            plot_colors = None

        if plot_colors:
            line_colors = plot_colors['line']['colors']
            line_gradients = plot_colors['line']['gradients']
        else:
            line_colors = [
                [11, 122, 153],   # saphire
                [173, 26, 114],   # pink
                [15, 123, 123],   # teal
                [23, 146, 153],   # maroon
                [102, 64, 165],   # mauve
                [186, 82, 117],   # flamingo
                [228, 122, 112],  # rosewater
                [224, 62, 62],    # red
                [217, 115, 13],   # peach
                [223, 171, 1],    # yellow
                [15, 123, 108],   # green
                [11, 136, 153],   # sky
                [11, 110, 153],   # blue
                [107, 84, 141],   # lavender
            ]
            line_gradients = [
                [[11, 122, 153], [15, 123, 123]],
                [[173, 26, 114], [107, 84, 141]],
            ]

        if file_path_base is None:
            file_path_base = os.path.splitext(self.file_path)[0]

        if 'first cycle number' in self.cycle_info:
            first_cycle_number = self.cycle_info['first cycle number']
        else:
            first_cycle_number = 1

        info_msg = f'Plotting cycles: {cycles_to_plot_vvsq} and {cycles_to_plot_dqdv}'
        logging.info(info_msg)

        figure_objects = []
        if canvases is None:
            figure_objects.append(self.plot_capacity_vs_cycle(
                exclude_cycles=exclude_cycles,
                save_plots=save_plots,
                file_path_base=file_path_base))
            figure_objects.append(self.plot_energy_vs_cycle(
                exclude_cycles=exclude_cycles,
                save_plots=save_plots,
                file_path_base=file_path_base))
            figure_objects.append(self.plot_efficiency_vs_cycle(
                exclude_cycles=exclude_cycles,
                save_plots=save_plots,
                file_path_base=file_path_base))
            figure_objects.append(self.plot_ir_drop_vs_cycle(
                exclude_cycles=exclude_cycles,
                save_plots=save_plots,
                file_path_base=file_path_base))
            figure_objects.append(self.plot_ir_rise_vs_cycle(
                exclude_cycles=exclude_cycles,
                save_plots=save_plots,
                file_path_base=file_path_base))

            figure_objects.append(self.plot_voltage_vs_capacity(
                cycles=cycles_to_plot_vvsq,
                line_gradients=line_gradients,
                save_plots=save_plots,
                file_path_base=file_path_base))
            figure_objects.append(self.plot_dq_dv_vs_voltage(
                cycles=cycles_to_plot_dqdv,
                line_gradients=line_gradients,
                save_plots=save_plots,
                file_path_base=file_path_base))
            return figure_objects
        elif len(canvases) >= 6:
            self.plot_capacity_vs_cycle(
                exclude_cycles=exclude_cycles,
                canvas=canvases[0],
                save_plots=save_plots,
                file_path_base=file_path_base)
            self.plot_energy_vs_cycle(
                exclude_cycles=exclude_cycles,
                canvas=canvases[1],
                save_plots=save_plots,
                file_path_base=file_path_base)
            self.plot_efficiency_vs_cycle(
                exclude_cycles=exclude_cycles,
                canvas=canvases[2],
                save_plots=save_plots,
                file_path_base=file_path_base)
            self.plot_ir_drop_vs_cycle(
                exclude_cycles=exclude_cycles,
                canvas=canvases[3],
                save_plots=save_plots,
                file_path_base=file_path_base)
            self.plot_ir_rise_vs_cycle(
                exclude_cycles=exclude_cycles,
                canvas=canvases[4],
                save_plots=save_plots,
                file_path_base=file_path_base)
            self.plot_voltage_vs_capacity(
                cycles=cycles_to_plot_vvsq,
                line_gradients=line_gradients,
                canvas=canvases[5],
                save_plots=save_plots,
                file_path_base=file_path_base)
            self.plot_dq_dv_vs_voltage(
                cycles=cycles_to_plot_dqdv,
                line_gradients=line_gradients,
                canvas=canvases[6],
                save_plots=save_plots,
                file_path_base=file_path_base)
        else:
            raise ValueError(
                'figure_objects must contain at least 4 figure objects')

    def plot_capacity_vs_cycle(self, exclude_cycles: list = None,
                               canvas=None, save_plots: bool = False,
                               file_path_base: str = None):
        """
        Plot voltage vs capacity.
        """
        if exclude_cycles is not None:
            exclude_cycles = [cycle for cycle in exclude_cycles
                              if cycle in self.cycles['cycle number']]
            data = self.cycles.drop(exclude_cycles)
        else:
            data = self.cycles
        data1 = data[['cycle number', 'specific capacity (charge)']]
        data2 = data[['cycle number', 'specific capacity (discharge)']]

        figure_obj = self.single_axis_plot(
            [data1, data2], title='capacity vs cycle number',
            xlabel='cycle number',
            ylabel=r'specific capacity / $\mathregular{mAh \cdot g^{-1}}$',
            data_label=['charge', 'discharge'],
            canvas=canvas)

        if save_plots:
            self.save_plot(figure_obj, name='cap_vs_cyc',
                           file_path_base=file_path_base)
        else:
            plt.show()
        return figure_obj

    def plot_energy_vs_cycle(self, exclude_cycles: list = None,
                             canvas=None, save_plots: bool = False,
                             file_path_base: str = None):
        """
        Plot energy vs cycle.
        """
        if exclude_cycles is not None:
            exclude_cycles = [cycle for cycle in exclude_cycles
                              if cycle in self.cycles['cycle number']]
            data = self.cycles.drop(exclude_cycles)
        else:
            data = self.cycles
        data1 = data[['cycle number', 'energy (charge)']]
        data2 = data[['cycle number', 'energy (discharge)']]

        figure_obj = self.single_axis_plot(
            [data1, data2], title='energy vs cycle number',
            xlabel='cycle number',
            ylabel=r'specifc energy / $\mathregular{Wh \cdot kg^{-1}}$',
            data_label=['charge', 'discharge'],
            canvas=canvas)

        if save_plots:
            self.save_plot(figure_obj, name='energy_vs_cycle',
                           file_path_base=file_path_base)
        else:
            plt.show()
        return figure_obj

    def plot_efficiency_vs_cycle(self, exclude_cycles: list = None,
                                 canvas=None, save_plots: bool = False,
                                 file_path_base: str = None):
        """
        Plot Coulomb and energy efficiency vs. cycle number
        """
        if exclude_cycles is not None:
            exclude_cycles = [cycle for cycle in exclude_cycles
                              if cycle in self.cycles['cycle number']]
            data = self.cycles.drop(exclude_cycles)
        else:
            data = self.cycles

        # print('Cycle data has columns: ', data.columns)
        data1 = data[['cycle number', 'coulomb efficiency']]
        # data2 = data[['cycle number', 'energy loss']]
        data2 = data[['cycle number', 'capacity loss']]
        # convert capacity loss in culmulative capacity loss
        data2['capacity loss'] = data2['capacity loss'].cumsum()

        figure_obj = self.dual_axis_plot(
            data1, data2, title='efficiency',
            xlabel='cycle number',
            ylabel1='coulomb efficiency / %',
            # ylabel2=r'specific energy loss / $\mathregular{Wh \cdot kg^{-1}}$',
            ylabel2=r'cumulative capacity loss / $\mathregular{mAh \cdot g^{-1}}$',
            data_label1='coulomb efficiency',
            data_label2='capacity loss',
            canvas=canvas)

        if save_plots:
            self.save_plot(figure_obj, name='efficiency',
                           file_path_base=file_path_base)
        else:
            plt.show()
        return figure_obj

    def plot_voltage_drop_vs_cycle(
            self, exclude_cycles: list = None,
            canvas=None, save_plots: bool = False,
            file_path_base: str = None):
        """
        Plot voltage drop vs cycle.
        """
        if exclude_cycles is not None:
            exclude_cycles = [cycle for cycle in exclude_cycles
                              if cycle in self.cycles['cycle number']]
            data = self.cycles.drop(exclude_cycles)
        else:
            data = self.cycles

        data1 = data[['cycle number', 'WE voltage drop (charge)']]
        data2 = data[['cycle number', 'WE voltage drop (discharge)']]

        figure_obj = self.dual_axis_plot(
            data1, data2, title='voltage drop',
            xlabel='cycle number',
            ylabel1='WE voltage drop (charge) / mV',
            ylabel2='WE voltage drop (discharge) / mV',
            data_label1='WE voltage drop (charge)',
            data_label2='WE voltage drop (discharge)',
            canvas=canvas)
        if save_plots:
            self.save_plot(figure_obj, name='voltage_drop',
                           file_path_base=file_path_base)
        else:
            plt.show()
        return figure_obj

    def plot_ir_drop_vs_cycle(
            self, exclude_cycles: list = None,
            canvas=None, dualaxis: bool = False,
            save_plots: bool = False,
            file_path_base: str = None):
        """
        Plot IR drop vs cycle.
        """
        if exclude_cycles is not None:
            exclude_cycles = [cycle for cycle in exclude_cycles
                              if cycle in self.cycles['cycle number']]
            data = self.cycles.drop(exclude_cycles)
        else:
            data = self.cycles

        data1 = data[['cycle number', 'IR drop (WE, charge)']]
        data2 = data[['cycle number', 'IR drop (WE, discharge)']]

        if dualaxis:
            figure_obj = self.dual_axis_plot(
                data1, data2, title='IR drop',
                xlabel='cycle number',
                ylabel1=r'IR drop (charge) / $\mathregular{Ohm}$',
                ylabel2=r'IR drop (discharge) / $\mathregular{Ohm}$',
                data_label1='IR drop (charge)',
                data_label2='IR drop (discharge)',
                canvas=canvas)
        else:
            figure_obj = self.single_axis_plot(
                [data1, data2], title='IR drop',
                xlabel='cycle number',
                ylabel=r'IR drop / $\mathregular{Ohm}$',
                data_label=['IR drop (charge)', 'IR drop (discharge)'],
                canvas=canvas)

        if save_plots:
            self.save_plot(figure_obj, name='ir_drop',
                           file_path_base=file_path_base)
        else:
            plt.show()
        return figure_obj

    def plot_ir_rise_vs_cycle(
            self, exclude_cycles: list = None,
            canvas=None, dualaxis: bool = False,
            save_plots: bool = False,
            file_path_base: str = None):
        """
        Plot IR rise vs cycle.
        """
        if exclude_cycles is not None:
            exclude_cycles = [cycle for cycle in exclude_cycles
                              if cycle in self.cycles['cycle number']]
            data = self.cycles.drop(exclude_cycles)
        else:
            data = self.cycles

        data1 = data[['cycle number', 'IR rise (WE, charge)']]
        data2 = data[['cycle number', 'IR rise (WE, discharge)']]

        if dualaxis:
            figure_obj = self.dual_axis_plot(
                data1, data2, title='IR rise',
                xlabel='cycle number',
                ylabel1=r'IR rise (charge) / $\mathregular{Ohm}$',
                ylabel2=r'IR rise (discharge) / $\mathregular{Ohm}$',
                data_label1='IR rise (charge)',
                data_label2='IR rise (discharge)',
                canvas=canvas)
        else:
            figure_obj = self.single_axis_plot(
                [data1, data2], title='IR rise',
                xlabel='cycle number',
                ylabel=r'IR rise / $\mathregular{Ohm}$',
                data_label=['IR rise (charge)', 'IR rise (discharge)'],
                canvas=canvas)

        if save_plots:
            self.save_plot(figure_obj, name='ir_rise',
                           file_path_base=file_path_base)
        else:
            plt.show()
        return figure_obj

    def plot_voltage_rise_vs_cycle(
            self, exclude_cycles: list = None,
            canvas=None, save_plots: bool = False,
            file_path_base: str = None):
        """
        Plot voltage rise vs cycle.
        """
        if exclude_cycles is not None:
            exclude_cycles = [cycle for cycle in exclude_cycles
                              if cycle in self.cycles['cycle number']]
            data = self.cycles.drop(exclude_cycles)
        else:
            data = self.cycles

        data1 = data[['cycle number', 'WE voltage rise (charge)']]
        data2 = data[['cycle number', 'WE voltage rise (discharge)']]

        figure_obj = self.dual_axis_plot(
            data1, data2, title='voltage rise',
            xlabel='cycle number',
            ylabel1='WE voltage rise (charge) / mV',
            ylabel2='WE voltage rise (discharge) / mV',
            data_label1='WE voltage rise (charge)',
            data_label2='WE voltage rise (discharge)',
            canvas=canvas)
        if save_plots:
            self.save_plot(figure_obj, name='voltage_rise',
                           file_path_base=file_path_base)
        else:
            plt.show()
        return figure_obj

    def save_plot(self, figure_obj, name: str = None, file_path_base: str = None):
        """
        Save plot.
        """
        resolution = 300
        if file_path_base is None:
            file_path_base = os.path.splitext(self.file_path)[0]
        if name is None:
            name = 'plot'
        file_path = file_path_base + '_' + name
        figure_obj.savefig(file_path + '.png', dpi=resolution)
        figure_obj.savefig(file_path + '.svg')
        plt.close(figure_obj)

    def single_axis_plot(self, data, exclude: list = None,
                         color=None, marker=None, linestyle=None,
                         title: str = None, xlabel: str = None,
                         ylabel: str = None, data_label: str = None,
                         canvas=None):
        """
        Create a plot with a single y-axis.

        Parameters
        ----------
        data : pandas dataframe, list or numpy array
            Data to plot.
        exclude : list, optional
            List of indices to exclude from plot. The default is None.
        color : RGB color tuple or array of color tuples, optional
            If not specified default colors will be used.
            RGB color vaulues range from 0 to 255, e.g. (255, 0, 0) for red.
        title : str, optional
            Title of the plot. The default is None.
        xlabel : str, optional
            Label of the x-axis. The default is None.
        ylabel : str, optional
            Label of the y-axis. The default is None.
        data_label : str, optional
            Label of the data. The default is None.
        """

        if exclude is not None:
            exclude_indices = [cycle for cycle in exclude
                               if cycle in self.cycles.index.to_list()]
        length = None
        # check if data is a list
        if isinstance(data, list):
            # get length of list
            length = len(data)
            # get type of first item in list
            if length > 0:
                if exclude is not None:
                    print('Cannot exclude indices from a list of datasets.')
                type1 = type(data[0])
                if type1 == pd.Series:
                    data_type = 'list of series'
                elif type1 == pd.DataFrame:
                    data_type = 'list of dataframes'
                elif type1 == np.ndarray:
                    data_type = 'list of numpy arrays'
                elif type1 == tuple:
                    if len(data[0]) > 0:
                        type2 = type(data[0][0])
                        if type2 == pd.Series:
                            data_type = 'list of series tuples'
                        elif type2 == np.ndarray:
                            data_type = 'list of numpy array tuples'
                        elif type2 == list:
                            data_type = 'list of lists tuples'
                        else:
                            raise ValueError('unsupported data type')
                else:
                    raise ValueError('unsupported data type')
            else:
                raise ValueError('data is empty')
        else:
            if isinstance(data, pd.Series):
                data_type = 'series'
            elif isinstance(data, pd.DataFrame):
                data_type = 'dataframe'
            elif isinstance(data, np.ndarray):
                data_type = 'numpy array'
            else:
                raise ValueError('unsupported data type')

        match data_type:
            case 'series':
                x_data = data.index
                y_data = data
                if exclude is not None:
                    x_data = x_data.drop(exclude_indices)
                    y_data = y_data.drop(exclude_indices)
            case 'dataframe':
                x_data = data.iloc[:, 0]
                y_data = data.iloc[:, 1]
                if exclude is not None:
                    x_data = x_data.drop(exclude_indices)
                    y_data = y_data.drop(exclude_indices)
            case 'numpy array':
                x_data = data[0]
                y_data = data[1]
                if exclude is not None:
                    x_data = np.delete(x_data, exclude_indices)
                    y_data = np.delete(y_data, exclude_indices)
            case 'list of series':
                x_data = [data[i].index for i in range(length)]
                y_data = data
            case 'list of dataframes':
                x_data = [data[i].iloc[:, 0] for i in range(length)]
                y_data = [data[i].iloc[:, 1] for i in range(length)]
            case 'list of numpy arrays':
                x_data = [data[i][0] for i in range(length)]
                y_data = [data[i][1] for i in range(length)]
            case 'list of series tuples':
                x_data = [data[i][0] for i in range(length)]
                y_data = [data[i][1] for i in range(length)]
            case 'list of numpy array tuples':
                x_data = [data[i][0] for i in range(length)]
                y_data = [data[i][1] for i in range(length)]
            case 'list of lists tuples':
                x_data = [data[i][0] for i in range(length)]
                y_data = [data[i][1] for i in range(length)]
            case _:
                raise ValueError('unsupported data type')

        default_colors = [
            (11, 122, 153),   # saphire
            (173, 26, 114),   # pink
            (15, 123, 123),   # teal
            (23, 146, 153),   # maroon
            (102, 64, 165),   # mauve
            (186, 82, 117),   # flamingo
            (228, 122, 112),  # rosewater
            (224, 62, 62),    # red
            (217, 115, 13),   # peach
            (223, 171, 1),    # yellow
            (15, 123, 108),   # green
            (11, 136, 153),   # sky
            (11, 110, 153),   # blue
            (107, 84, 141),   # lavender
        ]

        if color is None:
            if length is None:
                color = (11, 122, 153)
            elif length > len(default_colors):
                # repeat default colors to match length of data
                color = default_colors * (length // len(default_colors)) + \
                    default_colors[:(length % len(default_colors))]
            else:
                color = default_colors
        else:
            if length is None:
                pass
            elif length > len(color):
                # repeat color to match length of data
                color = color * (length // len(color)) + \
                    color[:(length % len(color))]

        default_markers = [
            'o', 'D', 'v', '^', '<', '>', 's', 'p', 'P', '*', 'h', 'H', 'X', 'd'
        ]

        if marker is None:
            if length is None:
                marker = 'o'
            elif length > len(default_markers):
                # repeat default markers to match length of data
                marker = default_markers * (length // len(default_markers)) + \
                    default_markers[:(length % len(default_markers))]
            else:
                marker = default_markers
        else:
            if length is None:
                pass
            elif length > len(marker):
                # repeat marker to match length of data
                marker = marker * (length // len(marker)) + \
                    marker[:(length % len(marker))]

        default_linestyles = [
            'solid', 'dashed', 'dashdot', 'dotted'
        ]

        if linestyle is None:
            if length is None:
                linestyle = 'solid'
            elif length > len(default_linestyles):
                # repeat default linestyles to match length of data
                linestyle = default_linestyles * (length // len(default_linestyles)) + \
                    default_linestyles[:(length % len(default_linestyles))]
            else:
                linestyle = default_linestyles
        else:
            if length is None:
                pass
            elif length > len(linestyle):
                # repeat linestyle to match length of data
                linestyle = linestyle * (length // len(linestyle)) + \
                    linestyle[:(length % len(linestyle))]

        if canvas is None:
            figure_obj, axis_obj = plt.subplots()
        else:
            figure_obj = canvas.figure
            axis_obj = canvas.axis

        if length is None:
            color = self.rgb_color_tuple_from_array(color)
            axis_obj.plot(x_data, y_data, linestyle='None', color=color,
                          marker='o', markersize=4,  markeredgecolor=color,
                          markeredgewidth=0.5, fillstyle='full',
                          markerfacecolor=color + (0.2,),
                          label=data_label)
        elif length > 0:
            for i in range(length):
                line_color = self.rgb_color_tuple_from_array(color[i])
                marker_style = marker[i]
                axis_obj.plot(x_data[i], y_data[i], linestyle='None', color=line_color,
                              marker=marker_style, markersize=4,  markeredgecolor=line_color,
                              markeredgewidth=0.5, fillstyle='full',
                              markerfacecolor=line_color + (0.2,),
                              label=data_label[i])

        axis_obj.set_title(title)
        axis_obj.set_xlabel(xlabel)
        axis_obj.set_ylabel(ylabel)
        axis_obj.legend(loc='upper right')
        self.format_plot(figure_obj, [axis_obj])

        return figure_obj

    def remove_plot_data_points(self, figure_obj,
                                exclude_x_values: list = None,
                                exclude_points: list = None,
                                exclude_indices: list = None):
        """
        Remove list of data points from existing plot.

        Parameters
        ----------
        figure_obj : matplotlib figure object
            Figure object to remove data points from.
        exclude_x_values : list, optional
            List of x values to exclude from plot. The default is None.
        exclude_points : list, optional
            List of (x, y) data points to exclude from plot, defined as list of lists or tuples.
            The default is None.
        exclude_index : list, optional
            List of indices to exclude from plot. The default is None.
        """

        for axis_obj in figure_obj.get_axes():
            axis_obj.set_autoscale_on(True)
            for line in axis_obj.get_lines():
                x_data = line.get_xdata()
                y_data = line.get_ydata()
                n_points = len(x_data)
                if exclude_x_values is not None:
                    exclude_indices = [i for i, x in enumerate(
                        x_data) if x in exclude_x_values]
                if exclude_points is not None:
                    # check if exclude_points is a list of lists or tuples
                    if isinstance(exclude_points[0], list):
                        exclude_indices = [i for i, (x, y) in enumerate(
                            zip(x_data, y_data)) if [x, y] in exclude_points]
                    elif isinstance(exclude_points[0], tuple):
                        exclude_indices = [i for i, (x, y) in enumerate(
                            zip(x_data, y_data)) if (x, y) in exclude_points]
                    else:
                        raise ValueError(
                            'exclude_points must be a list of lists or tuples')
                if exclude_indices is not None:
                    # remove indices that are out of range
                    exclude_indices = [
                        index for index in exclude_indices if index < n_points]
                else:
                    exclude_indices = []
                x_data = np.delete(x_data, exclude_indices)
                y_data = np.delete(y_data, exclude_indices)
                line.set_xdata(x_data)
                line.set_ydata(y_data)
            # recompute axis data limits
            axis_obj.relim()
            # update view limits
            axis_obj.autoscale_view()
            # reset tick positions
            axis_obj.xaxis.set_major_locator(mticker.AutoLocator())
            axis_obj.yaxis.set_major_locator(mticker.AutoLocator())
            # update tick labels
            axis_obj.xaxis.set_major_formatter(mticker.ScalarFormatter())
            axis_obj.yaxis.set_major_formatter(mticker.ScalarFormatter())

        figure_obj.canvas.draw_idle()
        return figure_obj

    def dual_axis_plot(self, data1, data2, color1: tuple = (11, 122, 153),
                       color2: tuple = (173, 26, 114),
                       title: str = None, xlabel: str = None,
                       ylabel1: str = None, ylabel2: str = None,
                       data_label1: str = None, data_label2: str = None,
                       canvas=None):
        """
        Create a plot with two y-axes.

        Parameters
        ----------
        data1 : pandas series, dataframe, list or numpy array
            Data for the first y-axis.
        data2 : pandas series, dataframe, list or numpy array
            Data for the second y-axis.
        color1 : tuple, optional
            Color for data1. The default is (11, 122, 153).
        color2 : tuple, optional
            Color for data2. The default is (173, 26, 114).
        title : str, optional
            Title of the plot. The default is None.
        xlabel : str, optional
            Label of the x-axis. The default is None.
        ylabel1 : str, optional
            Label of the first y-axis. The default is None.
        ylabel2 : str, optional
            Label of the second y-axis. The default is None.
        data_label1 : str, optional
            Label of data1. The default is None.
        data_label2 : str, optional
            Label of data2. The default is None.
        """
        color1 = self.rgb_color_tuple_from_array(color1)
        color2 = self.rgb_color_tuple_from_array(color2)

        figure_obj, axis_obj1, axis_obj2 = self.create_doulbe_yaxis_plot(
            canvas)

        # check if data1 is a pandas series
        if isinstance(data1, pd.Series):
            data1_x = data1.index
            data1_y = data1
        elif isinstance(data1, pd.DataFrame):
            data1_x = data1.iloc[:, 0]
            data1_y = data1.iloc[:, 1]
        elif isinstance(data1, list):
            data1_x = data1[0]
            data1_y = data1[1]
        elif isinstance(data1, np.ndarray):
            data1_x = data1[0]
            data1_y = data1[1]
        else:
            print('data1 is neither a pandas series, dataframe, list nor a numpy array')
            return None

        # check if data2 is a pandas series
        if isinstance(data2, pd.Series):
            data2_x = data2.index
            data2_y = data2
        elif isinstance(data2, pd.DataFrame):
            data2_x = data2.iloc[:, 0]
            data2_y = data2.iloc[:, 1]
        elif isinstance(data2, list):
            data2_x = data2[0]
            data2_y = data2[1]
        elif isinstance(data2, np.ndarray):
            data2_x = data2[0]
            data2_y = data2[1]
        else:
            print('data2 is neither a pandas series, dataframe, list nor a numpy array')
            return None

        lh_ax1 = axis_obj1.plot(
            data1_x, data1_y,
            linestyle='None', color=color1,
            marker='o', markersize=4,  markeredgecolor=color1,
            markeredgewidth=0.5, fillstyle='full',
            markerfacecolor=color1 + (0.2,),
            label=data_label1
        )
        lh_ax2 = axis_obj2.plot(
            data2_x, data2_y,
            linestyle='None', color=color2,
            marker='D', markersize=3, markeredgecolor=color2,
            markeredgewidth=0.5, fillstyle='full',
            markerfacecolor=color2 + (0.2,),
            label=data_label2
        )

        axis_obj1.set_title(title)
        axis_obj1.set_xlabel(xlabel)
        axis_obj1.set_ylabel(ylabel1)
        axis_obj2.set_ylabel(ylabel2)
        axis_obj1.legend(loc='upper right', handles=[lh_ax1[0], lh_ax2[0]])
        self.format_plot(figure_obj, [axis_obj1, axis_obj2])

        return figure_obj

    def plot_voltage_vs_capacity(self, cycles: list = None,
                                 line_gradients: list = None,
                                 canvas=None,
                                 save_plots: bool = False,
                                 file_path_base: str = None):
        """
        Plot voltage vs capacity.
        """
        if cycles is None:
            cycles = self.get_cycle_numbers()
        else:
            number_of_cycles = self.cycle_info['number of cycles']
            cycles = [cycle for cycle in cycles if cycle <= number_of_cycles]

        col_voltage = self.settings['columns'][self.method]['working electrode voltage']
        col_capacity = self.settings['columns'][self.method]['specific capacity']

        figure_obj = self.multi_line_plot(
            data=self.data,
            dataset_selector='state',
            dataset_selector_values=['charge', 'discharge'],
            line_selector='cycle number',
            line_selector_values=cycles,
            x_data_column=col_capacity,
            y_data_column=col_voltage,
            title='voltage vs. capacity',
            xlabel=r'specific capacity / $\mathregular{mAh \cdot g^{-1}}$',
            ylabel='working electrode voltage / V',
            dataset_labels=['charge', 'discharge'],
            line_gradients=line_gradients,
            canvas=canvas)

        if save_plots:
            self.save_plot(figure_obj, name='v_vs_cap',
                           file_path_base=file_path_base)
        else:
            plt.show()

    def plot_dq_dv_vs_voltage(self, cycles: list = None,
                              line_gradients: list = None,
                              canvas=None,
                              save_plots: bool = False,
                              file_path_base: str = None):
        """
        Plot dQ/dV vs voltage.
        """
        if cycles is None:
            cycles = self.get_cycle_numbers()
        else:
            number_of_cycles = self.cycle_info['number of cycles']
            cycles = [cycle for cycle in cycles if cycle <= number_of_cycles]

        col_dq_dv = self.settings['columns'][self.method]['qQ_dV']
        col_voltage = self.settings['columns'][self.method]['working electrode voltage']

        figure_obj = self.multi_line_plot(
            data=self.data,
            dataset_selector='state',
            dataset_selector_values=['charge', 'discharge'],
            line_selector='cycle number',
            line_selector_values=cycles,
            x_data_column=col_voltage,
            y_data_column=col_dq_dv,
            title='dQ/dV vs. voltage',
            xlabel='working electrode voltage / V',
            ylabel=r'dQ/dV / $\mathregular{mAh \cdot g^{-1} \cdot V^{-1}}$',
            dataset_labels=['charge', 'discharge'],
            line_gradients=line_gradients,
            canvas=canvas)

        if save_plots:
            self.save_plot(figure_obj, name='dq_dv_vs_v',
                           file_path_base=file_path_base)
        else:
            plt.show()

    def multi_line_plot(self,
                        data: pd.DataFrame = None,
                        dataset_selector: str = None,
                        dataset_selector_values: list = None,
                        line_selector: str = None,
                        line_selector_values: list = None,
                        x_data_column: str = None,
                        y_data_column: str = None,
                        title: str = None,
                        xlabel: str = None, ylabel: str = None,
                        dataset_labels: list = None,
                        line_gradients: list = None,
                        canvas=None):
        """
        make multi line plot from data set based on a selector

        Parameters
        ----------
        data : pandas dataframe
            data to plot
        dataset_selector : str
            column name of the dataset selector
        dataset_selector_values : list
            values of the dataset selector
        line_selector : str
            column name of the line selector
        line_selector_values : list
            values of the line selector
        x_data_column : str
            column name of the x data
        y_data_column : str
            column name of the y data
        title : str
            title of the plot
        xlabel : str
            label of the x axis
        ylabel : str
            label of the y axis
        dataset_labels : list
            labels of the datasets
        line_gradients : list
            list of line gradients
        canvas : matplotlib canvas object
            canvas to plot on
        """
        default_line_gradients = [
            [[11, 122, 153], [15, 123, 123]],
            [[173, 26, 114], [107, 84, 141]],
            [[15, 123, 108], [11, 136, 153]],
            [[11, 110, 153], [107, 84, 141]],
            [[11, 122, 153], [15, 123, 123]],
            [[173, 26, 114], [107, 84, 141]],
            [[15, 123, 108], [11, 136, 153]],
            [[11, 110, 153], [107, 84, 141]],
        ]

        # validate input parameters
        if data is None:
            raise ValueError('data must be specified')
        # convert index of dataframe to multi index
        if dataset_selector is not None:
            # check if dataset_selector is a valid column name in data
            if dataset_selector not in data.columns:
                warning_msg = f'Column {dataset_selector} not found in data.' \
                    'Empty figure will be returned.'
                logging.warning(warning_msg)
                # return empty figure
                return None
            else:
                if dataset_selector_values is None:
                    # get unique values from dataset_selector column
                    dataset_selector_values = data[dataset_selector].unique()
                else:
                    # check if dataset_selector_values are in data
                    dataset_selector_values = [value for value in dataset_selector_values
                                               if value in data[dataset_selector].unique()]
                    if len(dataset_selector_values) == 0:
                        warning_msg = 'No valid dataset_selector_values found in dataset. ' \
                            'Empty figure will be returned.'
                        logging.warning(warning_msg)
                        # return empty figure
                        return None
        if line_selector is not None:
            # check if line_selector is a valid column name in data
            if line_selector not in data.columns:
                warning_msg = f'Column {line_selector} not found in data.' \
                    'Empty figure will be returned.'
                logging.warning(warning_msg)
                # return empty figure
                return None
            else:
                if line_selector_values is None:
                    line_selector_values = data[line_selector].unique()
                else:
                    # check if line_selector_values are in data
                    line_selector_values = [value for value in line_selector_values
                                            if value in data[line_selector].unique()]
                    if len(line_selector_values) == 0:
                        warning_msg = 'No valid line_selector_values found in dataset. ' \
                            'Empty figure will be returned.'
                        logging.warning(warning_msg)
                        # return empty figure
                        return None

        if x_data_column is None:
            warning_msg = 'x_data_column must be specified. ' \
                'Empty figure will be returned.'
            logging.warning(warning_msg)
            # return empty figure
            return None
        if y_data_column is None:
            warning_msg = 'y_data_column must be specified. ' \
                'Empty figure will be returned.'
            logging.warning(warning_msg)
            # return empty figure
            return None
        if line_gradients is None:
            line_gradients = default_line_gradients
        if title is None:
            title = ''
        if xlabel is None:
            xlabel = 'x'
        if ylabel is None:
            ylabel = 'y'
        if dataset_labels is None:
            dataset_labels = dataset_selector_values

        # create copy of data cointaining only columns defined by dataset_selector,
        # line_selector, x_data_column and y_data_column.
        plot_data = data[[dataset_selector,
                          line_selector, x_data_column, y_data_column]]
        # Use dataset_selector_values and line_selector_values as multi index
        plot_data = plot_data.set_index([dataset_selector, line_selector])

        # create figure and axis objects
        if canvas is None:
            figure_obj, axis_obj = plt.subplots()
        else:
            figure_obj = canvas.figure
            axis_obj = canvas.axis

        n_lines = len(line_selector_values)
        # create list for line objects for dataset 1
        line_handles = [[None for _ in range(n_lines)]
                        for _ in range(len(dataset_selector_values))]
        for d_index, dataset in enumerate(dataset_selector_values):
            line_gradient = self.color_gradient(
                rgb1=line_gradients[d_index][0], rgb2=line_gradients[d_index][1], steps=n_lines)
            for index, line in enumerate(line_selector_values):
                mindex = (dataset, line)
                # check if data_index is in data
                if mindex in plot_data.index:
                    info_msg = f'Creating plot for dataset {dataset} and line {line}'
                    logging.info(info_msg)
                    x_data = plot_data.loc[mindex, x_data_column]
                    y_data = plot_data.loc[mindex, y_data_column]
                    line_handles[d_index][index] = axis_obj.plot(
                        x_data, y_data, color=line_gradient[index])
                else:
                    warning_msg = f'No data found for dataset {dataset} and line {line}'
                    logging.warning(warning_msg)

        axis_obj.set_xlabel(xlabel)
        axis_obj.set_ylabel(ylabel)
        axis_obj.set_title(title)

        # expand x axis to the right by 20% to make room for legend
        axis_obj.set_xlim(left=0.95 * axis_obj.get_xlim()[0], right=1.2 * axis_obj.get_xlim()[1])

        # make concatenate lists in line_handles
        line_handles_flat = [
            item for sublist in line_handles for item in sublist]
        # line_handels_flat is now a nested list where each handle is stored in its own list
        # make line_handles_flat a flat list
        line_handles_flat = [item for sublist in line_handles_flat for item in sublist]
        line_labels = line_selector_values * len(dataset_selector_values)
        # make list of line handles selecting the first line of each dataset
        line_handles_dataset = [line_handles[i][0][0]
                                for i in range(len(dataset_selector_values))]
        print(f'line_handles_dataset: {line_handles_dataset}')
        legend_lines = axis_obj.legend(
            title=line_selector,
            alignment='left',
            title_fontproperties={
                'size': 7, 'weight': 'bold'},
            loc='lower right',
            handles=line_handles_flat,
            labels=line_labels,
            ncols=len(dataset_selector_values),
            # bbox_to_anchor=(1.02, 1.0), borderaxespad=0.5,
            fontsize=7,
            handlelength=0.5,
            handletextpad=0.5,
            labelspacing=0.5,
            columnspacing=0.8)
        legend_datasets = axis_obj.legend(
            loc='upper right',
            handles=line_handles_dataset,
            labels=dataset_labels)

        axis_obj.add_artist(legend_lines)
        axis_obj.add_artist(legend_datasets)
        self.format_plot(figure_obj, axis_obj)
        return figure_obj

    def color_gradient(self, rgb1: tuple = (255, 0, 0),
                       rgb2: tuple = (0, 0, 255), steps: int = 10):
        """
        Create color gradient between rgb1 and rgb2.
        """
        # create color gradient
        gradient = []
        gradient = [tuple(rgb1[j]/255 + (rgb2[j] - rgb1[j])/255 * i / steps for j in range(3))
                    for i in range(steps)]
        return gradient

    def rgb_color_tuple_from_array(self, color):
        """
        Return normalized RGB color tuple from an array of RGB colors.
        """
        # convert color to normalized RGB color tuple
        return tuple([x/255 for x in color])

    def create_doulbe_yaxis_plot(self, canvas=None):
        """
        Create double y-axis plot.
        """
        if canvas is None:
            figure_obj, axis_obj = plt.subplots()
            axis_obj2 = axis_obj.twinx()
        else:
            figure_obj = canvas.figure
            axis_obj = canvas.axis
            axis_obj2 = axis_obj.twinx()

        return figure_obj, axis_obj, axis_obj2

    def format_plot(self, figure_obj, axis_objects):
        """
        Format plot.
        """
        def get_twin(ax, axis):
            if axis == "x":
                siblings = ax.get_shared_x_axes().get_siblings(ax)
            elif axis == "y":
                siblings = ax.get_shared_y_axes().get_siblings(ax)
            else:
                return None
            for sibling in siblings:
                if sibling.bbox.bounds == ax.bbox.bounds and sibling is not ax:
                    return sibling
            return None

        # load plot colors from yaml file
        color_settings_path = os.path.join('resources', 'plot_colors.yaml')
        color_settings_data = pkgutil.get_data(
            __main_package__, color_settings_path)
        if color_settings_data is not None:
            color_settings_data = color_settings_data.decode('utf-8')
            plot_colors = yaml.safe_load(color_settings_data)
        else:
            plot_colors = None

        if plot_colors:
            title_color = self.rgb_color_tuple_from_array(
                plot_colors['text']['colors'][0])
            axes_color = self.rgb_color_tuple_from_array(
                plot_colors['axes']['colors'][0])
            axes_label_color = self.rgb_color_tuple_from_array(
                plot_colors['text']['colors'][0])
            grid_color = self.rgb_color_tuple_from_array(
                plot_colors['grid']['colors'][0])
            tick_color = axes_color
        else:
            axes_color = self.rgb_color_tuple_from_array([55, 53, 47])
            axes_label_color = self.rgb_color_tuple_from_array([55, 53, 47])
            grid_color = self.rgb_color_tuple_from_array([99, 95, 84])
            tick_color = self.rgb_color_tuple_from_array([55, 53, 47])

        x_axis_color = axes_color
        y1_axis_color = axes_color
        y2_axis_color = axes_color

        x_display_state = True
        y1_display_state = True
        y2_display_state = True

        # test if axis_objects is a list
        if not isinstance(axis_objects, list):
            axis_objects = [axis_objects]

        for index, axis_obj in enumerate(axis_objects):

            # set line width of axis
            axis_obj.spines['top'].set_linewidth(1.0)
            axis_obj.spines['right'].set_linewidth(1.0)
            axis_obj.spines['bottom'].set_linewidth(1.0)
            axis_obj.spines['left'].set_linewidth(1.0)

            if get_twin(axis_obj, "x") is not None:
                # get line objects of axis
                lines = axis_obj.get_lines()
                # get color from first line object
                yaxis_color = lines[0].get_color()
                # logging.debug(f'yaxis_color of axis {index} is {yaxis_color}')
                yaxis_label_color = yaxis_color
                if index == 0:
                    x_axis_color = axes_color
                    y1_axis_color = yaxis_color
                    y2_axis_color = axes_color
                    y1_display_state = True
                    y2_display_state = False
                elif index == 1:
                    x_axis_color = axes_color
                    y1_axis_color = axes_color
                    y2_axis_color = yaxis_color
                    y1_display_state = False
                    y2_display_state = True
                else:
                    x_axis_color = axes_color
                    y1_axis_color = axes_color
                    y2_axis_color = axes_color
            else:
                yaxis_color = axes_color
                yaxis_label_color = axes_label_color

            # set axis spine display state
            axis_obj.spines['top'].set_visible(x_display_state)
            axis_obj.spines['bottom'].set_visible(x_display_state)
            axis_obj.spines['right'].set_visible(y2_display_state)
            axis_obj.spines['left'].set_visible(y1_display_state)

            # set axis colors
            axis_obj.spines['top'].set_color(x_axis_color)
            axis_obj.spines['bottom'].set_color(x_axis_color)
            axis_obj.spines['left'].set_color(y1_axis_color)
            axis_obj.spines['right'].set_color(y2_axis_color)

            # set axis tick colors
            axis_obj.tick_params(axis='x', colors=tick_color)
            axis_obj.tick_params(axis='y', colors=tick_color)

            # set axis label and title font size, weight and family
            axis_obj.xaxis.label.set_fontsize(10)
            axis_obj.yaxis.label.set_fontsize(10)
            axis_obj.title.set_fontsize(12)

            # set font
            font_list = ['Metropolis', 'Roboto',
                         'Helvetica Neue', 'Helvetica', 'Aptos', 'Arial']
            # check if any of the fonts in font_list is available:
            font_list = [
                font for font in font_list if font in font_manager.get_font_names()]
            if len(font_list) > 0:
                font_name = font_list[0]
            else:
                font_name = 'sans-serif'
            # apply font to axis labels, title, legend and ticks
            axis_obj.xaxis.label.set_fontname(font_name)
            axis_obj.yaxis.label.set_fontname(font_name)
            axis_obj.title.set_fontname(font_name)
            xticks_loc = axis_obj.get_xticks()
            xlabels = axis_obj.get_xticklabels()
            axis_obj.xaxis.set_major_locator(mticker.FixedLocator(xticks_loc))
            axis_obj.set_xticklabels(xlabels,
                                     fontname=font_name, fontsize=8, fontweight='medium',
                                     color=axes_label_color)
            yticks_loc = axis_obj.get_yticks()
            ylabels = axis_obj.get_yticklabels()
            axis_obj.yaxis.set_major_locator(mticker.FixedLocator(yticks_loc))
            axis_obj.set_yticklabels(ylabels,
                                     fontname=font_name, fontsize=8, fontweight='medium',
                                     color=yaxis_label_color)
            axis_obj.tick_params(axis='y', colors=yaxis_label_color)

            # set axis label and title font weight
            axis_obj.xaxis.label.set_weight('bold')
            axis_obj.yaxis.label.set_weight('bold')
            axis_obj.title.set_weight('bold')

            # set font colors
            axis_obj.xaxis.label.set_color(axes_label_color)
            axis_obj.yaxis.label.set_color(yaxis_color)
            axis_obj.title.set_color(title_color)
            # axis_obj.tick_params(axis='x', colors=tick_color)
            # axis_obj.tick_params(axis='y', colors=tick_color)

            # show horizontal and vertical grid
            axis_obj.grid(axis='y', linestyle='-',
                          color=yaxis_color, linewidth=0.4, alpha=0.3)
            axis_obj.grid(axis='x', linestyle='-',
                          color=grid_color, linewidth=0.4, alpha=0.3)

            axis_obj.set_facecolor((1, 1, 1, 0))

            # format axis legend
            legends = [item for item in axis_obj.get_children(
            ) if isinstance(item, mlegend.Legend)]
            for legend in legends:
                # set legend frame color
                legend_frame_color = self.rgb_color_tuple_from_array(
                    plot_colors['legend']['colors'][0])
                legend.get_frame().set_facecolor(legend_frame_color)
                # hide frame border
                legend.get_frame().set_linewidth(0.0)
                legend.get_frame().set_edgecolor(legend_frame_color)
                # set legend frame transparency
                legend.get_frame().set_alpha(0.3)
                # format legend text
                for text in legend.get_texts():
                    text.set_color(axes_label_color)
                    # text.set_fontsize(10)
                    text.set_fontname(font_name)
                    text.set_weight('medium')

        # set figure and axis background color to transparent white
        figure_obj.set_facecolor((1, 1, 1, 0))

        # set figure size and aspect ratio
        ratio = 4/3
        width = 16
        # convert width to inches
        width = width/2.54
        figure_obj.set_figwidth(width)
        figure_obj.set_figheight(width/ratio)
        # figure_obj.tight_layout()

    def export_parameters(self) -> dict:
        """
        Prepare dictionary with parameters for export.
        """
        # Look up parameters for export in biologic_mpt.yaml.
        # Use keys of yaml dictionary in biologic_mpt.yaml to rename parameters
        # for export.

        technique = None

        mpt_export = self.settings

        techniques = mpt_export['method identifier']
        # inverse technique dictionary
        techniques_inv = {value: key for key, value in techniques.items()}
        if self.header['technique'] not in techniques_inv.keys():
            raise ValueError(
                f"Technique '{self.header['technique']}' is not defined in ",
                f"{export_settings_file}.\n",
                f"Supported techniques are:\n{list(techniques_inv.keys())}\n",
                f"Update {export_settings_file} to add another technique."
            )
        else:
            technique = techniques_inv[self.header['technique']]
            export_parameters = mpt_export['export parameters'][technique]['parameters']
            export_settings = mpt_export['export parameters'][technique]['settings']

        # Create dictionary with parameters for export
        export_dict = {}
        for key, value in export_parameters.items():
            if value in self.header:
                export_dict[key] = self.header[value]

        for key, value in export_settings.items():
            if value in self.parameter_table.columns:
                export_dict['settings'][key] = self.parameter_table[value].tolist()

        return export_dict

    def set_method(self):
        """
        Set method.
        """
        techniques = self.settings['method identifier']
        # inverse technique dictionary
        techniques_inv = {value: key for key, value in techniques.items()}
        if self.header['technique'] not in techniques_inv.keys():
            technique = self.header['technique']
        else:
            technique = techniques_inv[self.header['technique']]
        self.method = technique

    def get_settings_table_template(self):
        """
        Get settings table view for the analysis file from
        experimental_settings.md file.
        """
        # read experimental_settings.md template file
        settings_table_template_file = os.path.join(
            'resources', 'experimental_settings.md')
        settings_table_template_data = pkgutil.get_data(
            __main_package__, settings_table_template_file)

        if settings_table_template_data is not None:
            settings_table_template = settings_table_template_data.decode(
                'utf-8')
        else:
            settings_table_template = None

        return settings_table_template


def calc_c_rate(current: float, capacity: float) -> str:
    """
    Get C-rate.

    Parameters
    ----------
    current: float
        Current in mA.
    rated_capacity: float
        Capacity in mA.h.

    Returns
    -------
    c_rate: str
        C-rate.
    """
    # determin data type of current
    if capacity:
        c_rate = abs(current / capacity)
        if c_rate < 1:
            c_over_n = round(1 / c_rate)
            if c_over_n == 1:
                c_rate = '1C'
            else:
                c_rate = f'C/{c_over_n}'
        elif c_rate >= 1:
            c_rate = f'{round(c_rate)}C'
        else:
            c_rate = None
    else:
        c_rate = None
    return c_rate


def calc_mass_specific_current(current: float, mass: float) -> float:
    """
    Get mass specific current.

    Parameters
    ----------
    current: float
        Current in mA.
    mass: float
        Mass in g.

    Returns
    -------
    mass_specific_current: float
        Mass specific current in mA/g.
    """
    mass_specific_current = current / mass
    return mass_specific_current
