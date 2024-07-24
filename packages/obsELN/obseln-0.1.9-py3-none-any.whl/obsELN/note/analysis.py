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

This file defines the AnalysisNote class which is an interface to the different
data file readers and prepares the data for export to Obsidian ELN. The class
also provides methods to create a markdown report of the analysis file and to
export the analysis data to local files.
"""

import os
import sys
import datetime as dt
import logging
import pkgutil

import yaml
from ..reader import frontmatter as fm
from ..reader.smartsem import SmartSEMImage
from ..reader.biologic import BiologicMPT
from ..reader.horiba import HoribaTXT


__main_package__ = 'obsELN'

class AnalysisNote:
    """
    AnalysisNote class to read and write analysis files to Obsidian ELN vault.
    """
    def __init__(self,
                 file_path: str,
                 analysis_info: dict = None,
                 template_file: str = None,
                 obsidian_base_folder: str = None,
                 options: dict = None):
        """
        Initialize analysis file.

        Parameters
        ----------
        file_path : str
            Path to analysis file.
        """
        self.file_path = file_path
        self.info = None
        self.template = template_file
        self.analysis = None
        self.analysis_name = None
        self.analysis_base_name = None
        self.analysis_folder = None
        self.analysis_base_folder = None
        self.data_type = None
        self.method = None
        self.obsidian_base_folder = obsidian_base_folder
        self.options = options
        self.eln_settings = None

        if obsidian_base_folder is not None:
            self.eln_settings = self.get_eln_settings()

        self.get_data_type()
        self.load_analysis_file()
        self.initialize_analysis_info()
        if analysis_info is not None:
            self.update_analysis_info(analysis_info)

        self.project_name = self.info['project name']
        self.sample_name = self.info['sample name']
        self.set_analysis_base_folder()
        self.set_analysis_name()
        self.set_analysis_folder()
        self.load_analysis_template()

    def initialize_analysis_info(self):
        """
        Initialize analysis info dict with default values.
        """
        mdate_time = self.get_mdate('%Y-%m-%d %H:%M')
        mdate = mdate_time.split(' ')[0]
        mtime = mdate_time.split(' ')[1]

        self.info = {
            'author': None,
            'date created': self.get_current_date(),
            'project name': None,
            'sample name': None,
            'sample type': None,
            'sample description': None,
            'instrument': None,
            'instrument type': None,
            'operator': None,
            'status': 'completed',
            'analysis date': mdate,
            'analysis time': mtime,
        }

    def update_analysis_info(self, analysis_info: dict):
        """
        Update analysis info dict with new values.
        """
        self.info.update(analysis_info)

    def get_current_date(self):
        """
        Get current date.
        """
        return dt.datetime.now().strftime('%Y-%m-%d')

    def get_mdate(self, formatstr='%Y-%m-%d'):
        """
        Get modification date of analysis file.
        """
        # check that the file exists
        assert os.path.exists(
            self.file_path), f'No such file: {self.file_path}'
        mdate = (
            dt.datetime.fromtimestamp(os.stat(self.file_path).st_mtime)
                       .strftime(formatstr)
        )

        return mdate

    def load_analysis_template(self, template_file: str = None):
        """
        Load markdown analysis template file.
        """
        if template_file is not None:
            self.template_file = template_file
            template = fm.get_yaml_frontmatter(self.template_file, body=True)
        else:
            # load default template file from resources folder
            template_file = os.path.join(
                'resources', 'analysis_template.md')
            template_data = pkgutil.get_data(__main_package__, template_file)
            if template_data is not None:
                template_data = template_data.decode('utf-8')
                template = fm.get_yaml_frontmatter_from_string(
                    template_data, body=True)
            else:
                template = None
                d = os.path.dirname(sys.modules[__main_package__].__file__)
                info_msg = f'No analysis template file found in {d}/resources.'
                logging.info(info_msg)

        self.template = template

    def load_analysis_file(self):
        """
        Load analysis file from Obsidian ELN vault.
        """
        if os.path.isfile(self.file_path):
            self.get_data_type()
            if self.data_type == 'Biologic MPT':
                if self.options is not None:
                    self.analysis = BiologicMPT(self.file_path, **self.options)
                else:
                    self.analysis = BiologicMPT(self.file_path)
                self.method = self.analysis.method
            elif self.data_type == 'SmartSEM TIFF':
                self.analysis = SmartSEMImage(self.file_path)
                self.method = self.analysis.method
            elif self.data_type == 'Horiba TXT':
                self.analysis = HoribaTXT(self.file_path)
                self.method = self.analysis.method
            else:
                print('Unsuported file type.')
        else:
            print('File does not exist.')

    def get_data_type(self) -> str:
        """
        Detect data type from file extension for import into Obsidian ELN.

        Parameters
        ----------
        file_path : str
            Path to file.

        """
        file_extension = os.path.splitext(self.file_path)[1]
        if file_extension in ['.tiff', '.tif']:
            self.data_type = 'SmartSEM TIFF'
        elif file_extension in ['.mpt']:
            self.data_type = 'Biologic MPT'
        elif file_extension in ['.txt']:
            # get first line of file
            encoding = 'windows-1252'
            with open(self.file_path, 'r', encoding=encoding) as file:
                first_line = file.readline()
            if first_line.startswith('#'):
                self.data_type = 'Horiba TXT'
            elif first_line.startswith('EC-Lab ASCII FILE'):
                self.data_type = 'Biologic MPT'
        else:
            raise ValueError('File type not supported.')

    def update_yaml(self):
        """
        Update YAML frontmatter of analysis file.
        """
        if self.template is None:
            self.load_analysis_template()

        analysis_fm = self.template['yaml']
        analysis_fm['author'] = self.info['author']
        analysis_fm['date created'] = self.get_current_date()
        analysis_fm['project']['name'] = self.info['project name']
        analysis_fm['project']['link'] = f'[[{self.info["project name"]}]]'
        analysis_fm['sample']['name'] = self.info['sample name']
        analysis_fm['sample']['link'] = f'[[{self.info["sample name"]}]]'
        analysis_fm['sample']['type'] = self.info['sample type']
        analysis_fm['sample']['description'] = self.info['sample description']
        analysis_fm['instrument']['name'] = self.info['instrument']
        analysis_fm['instrument']['link'] = f'[[{self.info["instrument"]}]]'
        analysis_fm['instrument']['type'] = self.info['instrument type']
        analysis_fm['analysis']['method'] = self.analysis.method
        analysis_fm['analysis']['date'] = self.info['analysis date']
        analysis_fm['analysis']['time'] = self.info['analysis time']
        analysis_fm['analysis']['operator'] = self.info['operator']
        analysis_fm['analysis']['status'] = self.info['status']
        analysis_fm['analysis']['data']['local']['file'] = os.path.basename(
            self.file_path)
        analysis_fm['analysis']['data']['local']['folder'] = os.path.dirname(
            self.file_path)

        # define inner function to format external file link for Obsidian
        def format_external_file_url(link: str) -> str:
            """
            Format external file link for Obsidian.
            """
            # replace whitespace with '%20' and add 'file://' prefix
            link = link.replace(" ", "%20")
            # replace backslashes with forward slashes
            link = link.replace("\\", "/")
            # replace Ä, Ö, Ü, ä, ö, ü, ß with %C3%84, %C3%96, %C3%9C, %C3%A4, %C3%B6, %C3%BC, %C3%9F
            link = link.replace("Ä", "%C3%84")
            link = link.replace("Ö", "%C3%96")
            link = link.replace("Ü", "%C3%9C")
            link = link.replace("ä", "%C3%A4")
            link = link.replace("ö", "%C3%B6")
            link = link.replace("ü", "%C3%BC")
            link = link.replace("ß", "%C3%9F")
            # add 'file://' prefix
            link = f'file://{link}'
            return link

        file_link = format_external_file_url(self.file_path)
        folder_link = format_external_file_url(
            os.path.dirname(self.file_path))
        analysis_fm['analysis']['data']['local'][
            'link'] = f'[local data file]({file_link})'
        analysis_fm['analysis']['data']['local'][
            'folder_link'] = f'[local data folder]({folder_link})'
        if self.data_type == 'Biologic MPT':
            remote_data_file = self.analysis.header['Saved on']['File']
            remote_data_folder = self.analysis.header['Saved on']['Directory']
            # get drive letter from remote_data_folder, first folder and year (second folder)
            remote_data_folder_splited = remote_data_folder.split('\\')
            drive_letter = remote_data_folder_splited[0]
            first_folder = remote_data_folder_splited[1]
            year = remote_data_folder_splited[2]
            # remove drive_letter, first_folder and year in remote_data_folder
            remote_data_folder = remote_data_folder.replace(
                f'{drive_letter}\\{first_folder}\\{year}\\', '')
            # strip the year from remote_data_folder
            remote_root_folder = self.eln_settings['folder']['remote data']
            # check if the analysis was performed with a VMP potentiostat
            # check if self.analysis.anlysis.header['Device'] starts with 'VMP3'
            if self.analysis.header['Device'].startswith('VMP3'):
                potentiostat_folder = 'Potentiostaten_VMP'
            elif self.analysis.header['Device'].startswith('BCS'):
                potentiostat_folder = 'Potentiostaten_BCS'
            # join remote_root_folder and remote_data_folder
            remote_data_folder = os.path.join(
                remote_root_folder, year, potentiostat_folder,
                remote_data_folder)
            remote_file_link = os.path.join(remote_data_folder, remote_data_file)
            # format as external file link for Obsidian
            remote_file_link = format_external_file_url(remote_file_link)
            remote_data_folder = format_external_file_url(remote_data_folder)
            analysis_fm['analysis']['data']['remote'][
                'file_link'] = f'[remote data file]({remote_file_link})'
            analysis_fm['analysis']['data']['remote'][
                'folder_link'] = f'[remote data folder]({remote_data_folder})'
        
        analysis_fm['analysis']['parameters'] = self.get_export_parameters()

        self.template['yaml'] = analysis_fm

    def update_body(self):
        """
        Update body of analysis file.
        """
        if self.template is None:
            self.load_analysis_template()

        self.insert_data_preview()
        self.insert_settings_view()

    def export_analysis_data(self, plot_options: dict = None):
        """
        Export analysis data to local file.
        """

        if self.analysis_folder is None:
            self.set_analysis_folder()
        if self.analysis_name is None:
            self.set_analysis_name()

        file_path_base = os.path.join(self.analysis_folder, self.analysis_name)
        # check if analysis folder exists
        if not os.path.isdir(self.analysis_folder):
            try:
                os.makedirs(self.analysis_folder)
            except OSError as error:
                print(error)

        if self.data_type == 'Biologic MPT':
            data_folder = os.path.join(self.analysis_folder, 'data')
            if not os.path.isdir(data_folder):
                try:
                    os.makedirs(data_folder)
                except OSError as error:
                    print(error)
            data_path_base = os.path.join(data_folder, self.analysis_name)
            self.analysis.save_data(data_path_base + '_data.csv')
            self.analysis.save_reduced_data(data_path_base + '_reduced_data.csv')
            self.analysis.save_parameter_table(data_path_base + '_param.csv')
            self.analysis.save_cycles(data_path_base + '_cycles.csv')
            # create subfolder for plots
            plots_folder = os.path.join(self.analysis_folder, 'plots')
            if not os.path.isdir(plots_folder):
                try:
                    os.makedirs(plots_folder)
                except OSError as error:
                    print(error)
            plot_path_base = os.path.join(plots_folder, self.analysis_name)
            self.analysis.create_plots(plot_options=plot_options,
                                       save_plots=True,
                                       file_path_base=plot_path_base)
        elif self.data_type == 'SmartSEM TIFF':
            msg = 'Saving image: ', file_path_base + '.jpg'
            logging.info(msg)
            self.analysis.save_image(file_path_base + '.jpg')
        elif self.data_type == 'Horiba TXT':
            data_folder = os.path.join(self.analysis_folder, 'data')
            if not os.path.isdir(data_folder):
                try:
                    os.makedirs(data_folder)
                except OSError as error:
                    print(error)
            data_path_base = os.path.join(data_folder, self.analysis_name)
            self.analysis.save_data(data_path_base + '_data.csv')
            # create subfolder for plots
            plots_folder = os.path.join(self.analysis_folder, 'plots')
            if not os.path.isdir(plots_folder):
                try:
                    os.makedirs(plots_folder)
                except OSError as error:
                    print(error)
            plot_path_base = os.path.join(plots_folder, self.analysis_name)
            self.analysis.plot_spectrum(save_plots=True,
                                        file_path_base=plot_path_base)

    def insert_data_preview(self):
        """
        Insert data preview into body of analysis file.
        """
        if self.data_type == 'Biologic MPT':
            template_text = self.get_data_preview_template()
            # replace all occurrences of '<* sample_name *>' in template_text
            # with self.info['sample name']
            template_text = template_text.replace(
                '<* analysis_name *>', self.analysis_name)
            self.template['body'] = self.template['body'].replace(
                '<* data_preview *>', template_text)
        elif self.data_type == 'SmartSEM TIFF':
            self.template['body'] = self.template['body'].replace(
                '<* data_preview *>', f'![[{self.analysis_name}.jpg]]')
        elif self.data_type == 'Horiba TXT':
            template_text = self.get_data_preview_template()
            # replace all occurrences of '<* sample_name *>' in template_text
            # with self.info['sample name']
            template_text = template_text.replace(
                '<* analysis_name *>', self.analysis_name)
            self.template['body'] = self.template['body'].replace(
                '<* data_preview *>', template_text)
            
    def get_data_preview_template(self):
        """
        Get data preview of the analysis file.

        Parameters
        ----------
        analysis_name: str
            Name of the analysis.
        """
        # read chartsview template file
        if self.method == 'GCPL':
            chartsview_template_file = os.path.join(
                'resources', 'gcpl_data_preview.md')
            chartsview_template_data = pkgutil.get_data(
                __main_package__, chartsview_template_file)
            if chartsview_template_data is not None:
                chartsview_template = chartsview_template_data.decode('utf-8')
        elif self.method == 'Raman Spectroscopy':
            chartsview_template_file = os.path.join(
                'resources', 'raman_data_preview.md')
            chartsview_template_data = pkgutil.get_data(
                __main_package__, chartsview_template_file)
            if chartsview_template_data is not None:
                chartsview_template = chartsview_template_data.decode('utf-8')
        else:
            chartsview_template = None

        return chartsview_template
            
    def insert_settings_view(self):
        """
        Insert settings view into body of analysis file.
        """
        if self.data_type == 'Biologic MPT':
            self.template['body'] = self.template['body'].replace(
                '<* settings_view *>', self.analysis.get_settings_table_template())
        else:
            self.template['body'] = self.template['body'].replace(
                '<* settings_view *>', '')

    def create_md_report(self, file_path: str = None):
        """
        Create markdown report of analysis file.
        """
        if self.template is None:
            self.load_analysis_template()
        self.update_yaml()
        self.update_body()

        if file_path is None:
            if self.analysis_folder is None:
                self.set_analysis_folder()
            if not os.path.isdir(self.analysis_folder):
                try:
                    os.makedirs(self.analysis_folder)
                except OSError as error:
                    print(error)

            file_path = os.path.join(self.analysis_folder, self.analysis_name + '.md')

        fm.save_as_markdown(
            file_path, self.template['yaml'], self.template['body'])

    def set_analysis_base_name(self, analysis_base_name: str = None):
        """
        Set analysis base name.
        """
        if analysis_base_name is not None:
            self.analysis_base_name = analysis_base_name
        else:
            if self.info['sample name'] is not None:
                sample_name = self.info['sample name']
                if self.method is not None:
                    method = self.method.replace(' ', '_')
                else:
                    raise ValueError('No method specified.')
                self.analysis_base_name = f'{sample_name} - {method}'
            else:
                self.analysis_base_name = os.path.basename(self.file_path).split('.')[0]

    def set_analysis_name(self, analysis_folder: str = None):
        """
        Set analysis name.
        """
        if self.analysis_base_name is None:
            self.set_analysis_base_name()

        # if analysis_folder is not specified, set analysis folder
        # either to the folder of the analysis file or if an obsidian
        # ELN base folder is provided, to the analyses folder of the
        # obsidian ELN vault
        if analysis_folder is None:
            if self.obsidian_base_folder is None:
                analysis_base_folder = os.path.dirname(self.file_path)
            else:
                if self.analysis_base_folder is None:
                    self.set_analysis_base_folder()
                analysis_base_folder = self.analysis_base_folder
        else:
            analysis_base_folder = analysis_folder

        if os.path.isdir(analysis_base_folder):
            dir_content = os.listdir(analysis_base_folder)
            existing_analysis_folders = list(filter(lambda item: os.path.isdir(
                f'{analysis_base_folder}/{item}') and item.startswith(
                self.analysis_base_name), dir_content))
            
            logging.debug(existing_analysis_folders)
            # get max increment number from existing analysis folders
            if len(existing_analysis_folders) > 0:
                analysis_numbers = [int(folder.split('_')[-1]) 
                                    for folder 
                                    in existing_analysis_folders]
                counter = max(analysis_numbers) + 1
            else:
                counter = 1

            analysis_name = ''
            # increment file_name
            if counter < 10:
                analysis_name = f'{self.analysis_base_name}_0{counter}'
            else:
                analysis_name = f'{self.analysis_base_name}_{counter}'
        else:
            analysis_name = f'{self.analysis_base_name}_01'

        logging.debug(f'self.analysis_name will be set to: {analysis_name}')
        self.analysis_name = analysis_name

    def set_analysis_folder(self, analysis_folder: str = None):
        """
        Set analysis folder.
        """
        if analysis_folder is not None:
            self.analysis_folder = analysis_folder
        else:
            if self.obsidian_base_folder is None:
                self.analysis_folder = os.path.dirname(self.file_path)
            else:
                if self.analysis_base_folder is None:
                    self.set_analysis_base_folder()
                if self.analysis_name is None:
                    self.set_analysis_name()
                analysis_base_folder = self.analysis_base_folder
                analysis_name = self.analysis_name
                self.analysis_folder = os.path.join(analysis_base_folder, analysis_name)

    def get_analysis_name(self):
        """
        Get analysis name.
        """
        if self.analysis_name is None:
            self.set_analysis_name()
        return self.analysis_name

    def set_analysis_base_folder(self):
        """
        Set analysis folder.
        """
        if self.obsidian_base_folder is None:
            self.analysis_base_folder = os.path.dirname(self.file_path)
        else:
            eln_analyses_folder = self.eln_settings['folder']['analyses']
            self.analysis_base_folder = os.path.join(
                self.obsidian_base_folder, eln_analyses_folder,
                self.project_name, self.sample_name)

    def get_eln_settings(self):
        """
        Get settings for Obsidian ELN.
        """
        # read yaml frontmatter from obsidian_base_folder/assets/ELN_settings.md
        if self.obsidian_base_folder is not None:
            settings_file = os.path.join(
                self.obsidian_base_folder, 'assets', 'ELN settings.md')
            settings = fm.get_yaml_frontmatter(settings_file)
        else:
            settings = None
        return settings

    def get_export_parameters(self) -> dict:
        """
        Prepare dictionary with parameters for export.
        """
        # Look up parameters for export in biologic_mpt.yaml.
        # Use keys of yaml dictionary in biologic_mpt.yaml to rename parameters
        # for export.

        method_settings = None
        # Read export settings from data type settings file
        if self.data_type == 'Biologic MPT':
            export_settings_file = os.path.join('resources', 'biologic_mpt.yaml')
        elif self.data_type == 'SmartSEM TIFF':
            export_settings_file = os.path.join('resources', 'smartsem_tiff.yaml')
        elif self.data_type == 'Horiba TXT':
            export_settings_file = os.path.join('resources', 'labspec_txt.yaml')
        else:
            raise ValueError('Data type not supported.')

        export_settings_data = pkgutil.get_data(__main_package__, export_settings_file)
        if export_settings_data is not None:

            export_settings = yaml.safe_load(export_settings_data.decode('utf-8'))

        if self.method not in export_settings['export parameters']:
            raise ValueError(
                f"Technique '{self.method}' is not defined in ",
                f"{export_settings_file}.\n",
                "Supported techniques are:\n",
                f"{list(export_settings['export parameters'].keys())}\n",
                f"Update {export_settings_file} to add another technique."
            )
        else:
            if self.data_type == 'Biologic MPT':
                parameters = export_settings['export parameters'][self.method]['parameters']
                method_settings = export_settings['export parameters'][self.method]['settings']
            elif self.data_type == 'SmartSEM TIFF':
                parameters = export_settings['export parameters'][self.method]
            elif self.data_type == 'Horiba TXT':
                parameters = export_settings['export parameters'][self.method]

        # Create dictionary with parameters for export
        export_dict = {}
        for key, value in parameters.items():
            if value in self.analysis.header:
                export_dict[key] = self.analysis.header[value]

        # Add BioLogic technique settings for export
        # method_settings is None if data type is not Biologic MPT
        # if method_settings is not None:
        #     export_dict['settings'] = {}
        #     for key, value in method_settings.items():
        #         if value['name'] in self.analysis.parameter_table.columns:
        #             export_dict['settings'][key] = self.analysis.parameter_table[value['name']].tolist()

        return export_dict
