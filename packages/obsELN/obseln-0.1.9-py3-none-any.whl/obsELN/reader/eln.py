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

The Obsidian ELN class creates an object to access the structure and meta data
of an Obsidian ELN vault.
"""
import os
from . import frontmatter as fm


class ObsidianELN:
    """
    Obsidian ELN class to access ELN structure and meta data
    """
    def __init__(self, obsidian_base_folder):
        self.obsidian_base_folder = obsidian_base_folder
        self.settings = None
        self.folders = None
        self.operators = None
        self.projects = None
        self.samples = None
        self.analyses = None
        self.instruments = None
        self.devices = None
        self.processes = None
        self.load()

    def load(self):
        """
        Load ELN structure and meta data
        """
        self.settings = self.load_settings()
        if self.settings is None:
            return
        self.folders = self.load_folders()
        if self.folders is None:
            return
        self.operators = self.load_operators()
        self.projects = self.load_projects()
        self.samples = self.load_samples()
        # print('Samples: ', self.samples)
        self.analyses = self.load_analyses()
        # print('Analyses: ', self.anlayses)
        self.instruments = self.load_instruments()
        # print('Instruments: ', self.instruments)
        self.devices = self.load_devices()
        # print('Devices: ', self.devices)
        self.processes = self.load_processes()
        # print('Processes: ', self.processes)

    def load_settings(self):
        """
        Get settings from "ELN settings.md"
        """
        settings = None
        settings_file = os.path.join(self.obsidian_base_folder, 'assets/ELN settings.md')
        if os.path.isfile(settings_file):
            settings = fm.get_yaml_frontmatter(settings_file)
        else:
            # throw error if settings file is not found
            print('ELN settings file not found')
            return None
        
        return settings

    def load_folders(self):
        """
        Get folders from settings
        """
        if 'folder' in self.settings:
            return self.settings['folder']
        elif 'folders' in self.settings:
            return self.settings['folders']
        else:
            print('No folders found in settings. Make sure your vault has a valid ELN settings file.')
            return None

    def load_operators(self):
        """
        Get operators from settings
        """
        if 'operators' in self.settings:
            return self.settings['operators']
        else:
            return None

    def load_projects(self):
        """
        Get projects from projects folder
        """
        project_dict = {}
        if 'projects' in self.folders:
            projects_folder = os.path.join(self.obsidian_base_folder, self.folders['projects'])
        elif 'project' in self.folders:
            projects_folder = os.path.join(self.obsidian_base_folder, self.folders['project'])
        else:
            print('No projects folder found in settings. Make sure your vault has a valid ELN settings file.')
            return None
        if os.path.isdir(projects_folder):
            # loop though subfolders in projects folder
            projects = [item for item
                        in os.listdir(projects_folder)
                        if os.path.isdir(os.path.join(projects_folder, item))]
            for project in projects:
                project_file = os.path.join(projects_folder, project, f'{project}.md')
                if os.path.isfile(project_file):
                    frontmatter = fm.get_yaml_frontmatter(project_file)
                    if (frontmatter is not None and 'note type' in frontmatter
                        and frontmatter['note type'] == 'project'
                        and 'project' in frontmatter and 'type' in frontmatter['project']
                        and frontmatter['project']['type'] == 'science'):
                        project_dict[project] = frontmatter
        return project_dict

    def load_samples(self):
        """
        Get samples from samples folder
        """
        samples = {}
        samples_folder = os.path.join(self.obsidian_base_folder, self.folders['samples'])
        if os.path.isdir(samples_folder):
            # get folders in samples folder
            project_list = [item
                            for item in os.listdir(samples_folder)
                            if os.path.isdir(os.path.join(samples_folder, item))]
            # loop though subfolders in samples folder
            for project in project_list:
                # each folder should be a project name
                if project in self.projects:
                    # project folder contains subfolders for each sample type
                    project_folder = os.path.join(samples_folder, project)
                    sample_types = [item for item
                                    in os.listdir(project_folder)
                                    if os.path.isdir(os.path.join(project_folder, item))]
                    # loop though sample types to get samples
                    for sample_type in sample_types:
                        sample_type_folder = os.path.join(project_folder, sample_type)
                        samples_in_type = [os.path.splitext(file)[0] for file
                                           in os.listdir(sample_type_folder)
                                           if os.path.isfile(
                                               os.path.join(sample_type_folder, file))]
                        for sample in samples_in_type:
                            sample_file = os.path.join(sample_type_folder, f'{sample}.md')
                            if os.path.isfile(sample_file):
                                frontmatter = fm.get_yaml_frontmatter(sample_file)
                                if (frontmatter is not None and 'sample' in frontmatter):
                                    samples[sample] = {}
                                    samples[sample]['meta'] = frontmatter
                                    samples[sample]['project'] = project
                                    samples[sample]['type'] = sample_type
                                    
        return samples

    def load_analyses(self):
        """
        Get analyses from analyses folder
        """
        analyses = {}
        if 'analyses' in self.folders:
            analyses_folder = os.path.join(self.obsidian_base_folder, self.folders['analyses'])
        elif 'analysis' in self.folders:
            analyses_folder = os.path.join(self.obsidian_base_folder, self.folders['analysis'])
        else:
            print('No analyses folder found in settings. Make sure your vault has a valid ELN settings file.')
            return None
        if os.path.isdir(analyses_folder):
            # get folders in analyses folder
            project_list = [item
                            for item in os.listdir(analyses_folder)
                            if os.path.isdir(os.path.join(analyses_folder, item))]
            # loop though subfolders in analyses folder
            for project in project_list:
                # each folder should be a project name
                if project in self.projects:
                    # project folder contains subfolders for each sample type
                    project_folder = os.path.join(analyses_folder, project)
                    sample_list = [item
                                   for item in os.listdir(project_folder)
                                   if os.path.isdir(os.path.join(project_folder, item))]
                    # loop though samples to get analyses
                    for sample in sample_list:
                        sample_folder = os.path.join(project_folder, sample)
                        analysis_list = [item
                                         for item in os.listdir(sample_folder)
                                         if os.path.isdir(os.path.join(sample_folder, item))]
                        for analysis in analysis_list:
                            analysis_file = os.path.join(sample_folder, analysis, f'{analysis}.md')
                            if os.path.isfile(analysis_file):
                                frontmatter = fm.get_yaml_frontmatter(analysis_file)
                                if (frontmatter is not None and 'analysis' in frontmatter):
                                    analyses[analysis] = {}
                                    analyses[analysis]['meta'] = frontmatter
                                    analyses[analysis]['project'] = project
                                    analyses[analysis]['sample'] = sample
        return analyses

    def load_instruments(self):
        """
        Get instruments from instruments folder
        """
        instruments = {}
        instruments_folder = os.path.join(self.obsidian_base_folder, self.folders['instruments'])
        if os.path.isdir(instruments_folder):
            # get files in instruments folder
            instrument_list = [os.path.splitext(file)[0]
                               for file in os.listdir(instruments_folder)
                               if os.path.isfile(os.path.join(instruments_folder, file))]
            # loop though instruments in instruments folder
            for instrument in instrument_list:
                instrument_file = os.path.join(instruments_folder, f'{instrument}.md')
                if os.path.isfile(instrument_file):
                    frontmatter = fm.get_yaml_frontmatter(instrument_file)
                    if (frontmatter is not None and 'instrument' in frontmatter):
                        instruments[instrument] = frontmatter
        return instruments

    def load_devices(self):
        """
        Get devices from devices folder
        """
        devices = {}
        devices_folder = os.path.join(self.obsidian_base_folder, self.folders['devices'])
        if os.path.isdir(devices_folder):
            # get files in devices folder
            device_list = [os.path.splitext(file)[0]
                           for file in os.listdir(devices_folder)
                           if os.path.isfile(os.path.join(devices_folder, file))]
            # loop though devices in devices folder
            for device in device_list:
                device_file = os.path.join(devices_folder, f'{device}.md')
                if os.path.isfile(device_file):
                    frontmatter = fm.get_yaml_frontmatter(device_file)
                    if (frontmatter is not None and 'device' in frontmatter):
                        devices[device] = frontmatter
        return devices

    def load_processes(self):
        """
        Get processes from processes folder
        """
        processes = {}
        processes_folder = os.path.join(self.obsidian_base_folder, self.folders['processes'])
        if os.path.isdir(processes_folder):
            # get files in processes folder
            process_list = [os.path.splitext(file)[0]
                            for file in os.listdir(processes_folder)
                            if os.path.isfile(os.path.join(processes_folder, file))]
            # loop though processes in processes folder
            for process in process_list:
                process_file = os.path.join(processes_folder, f'{process}.md')
                if os.path.isfile(process_file):
                    frontmatter = fm.get_yaml_frontmatter(process_file)
                    if (frontmatter is not None and 'process' in frontmatter):
                        processes[process] = frontmatter
        return processes

    # def import_data(
    #     self, file_path=None, project_name=None, sample_name=None,
    #         operator=None, instrument=None):
    #     """
    #     Import analysis data into Obsidian ELN
    #     """
    #     # detect file type
    #     file_type = detect_file_type(file_path)
    #     # call import function for file type
    #     if file_type == 'SmartSEM TIFF':
    #         smartsem_tiff_to_md(
    #             file_path, project_name, sample_name, operator,
    #             instrument, self.obsidian_base_folder)
    #     elif file_type == 'Biologic MPT':
    #         import_biologic_mpt(
    #             file_path, project_name, sample_name, operator,
    #             instrument, self.obsidian_base_folder)
    #     else:
    #         print(f'File type {file_type} not supported')

    def get_samples(self, project=None, sample_type=None):
        """
        Filter samples by project and/or sample type
        """
        samples = None
        if project is not None and sample_type is None:
            samples = [sample for sample in self.samples
                       if self.samples[sample]['project'] == project]
        elif project is not None and sample_type is not None:
            samples = [sample for sample in self.samples
                       if self.samples[sample]['project'] == project
                       and self.samples[sample]['type'] == sample_type]
        elif project is None and sample_type is not None:
            samples = [sample for sample in self.samples
                       if self.samples[sample]['type'] == sample_type]
        else:
            samples = [sample for sample in self.samples]
        # sort list alphabetically
        samples.sort()
        return samples

    def get_analyses(self, project=None, sample=None):
        """
        Filter analyses by project and/or sample
        """
        analyses = None
        if project is not None and sample is None:
            analyses = [analysis for analysis in self.analyses
                        if self.analyses[analysis]['project'] == project]
        elif project is not None and sample is not None:
            analyses = [analysis for analysis in self.analyses
                        if self.analyses[analysis]['project'] == project
                        and self.analyses[analysis]['sample'] == sample]
        elif project is None and sample is not None:
            analyses = [analysis for analysis in self.analyses
                        if self.analyses[analysis]['sample'] == sample]
        else:
            analyses = [analysis for analysis in self.analyses]
        # sort list alphabetically
        analyses.sort()
        return analyses

    def get_instruments(self, instrument_type=None):
        """
        Filter instruments by type
        """
        instruments = None
        if instrument_type is not None:
            instruments = [
                instrument for instrument in self.instruments
                if self.instruments[instrument]['instrument']['type'] == instrument_type
            ]
        else:
            instruments = [instrument for instrument in self.instruments]
        # sort list alphabetically
        instruments.sort()
        return instruments

    def get_devices(self, device_type=None):
        """
        Filter devices by type
        """
        devices = None
        if device_type is not None:
            devices = [device for device in self.devices
                       if self.devices[device]['device']['type'] == device_type]
        else:
            devices = [device for device in self.devices]
        # sort list alphabetically
        devices.sort()
        return devices

    def get_processes(self, process_type=None):
        """
        Filter processes by type
        """
        processes = None
        if process_type is not None:
            processes = [process for process in self.processes
                         if self.processes[process]['process']['type'] == process_type]
        else:
            processes = [process for process in self.processes]
        # sort list alphabetically
        processes.sort()
        return processes

    def get_sample_types(self, project=None):
        """
        Get sample types for project
        """
        sample_types = None
        if project is not None:
            sample_types = [self.samples[sample]['type'] for sample in self.samples
                            if self.samples[sample]['project'] == project]
        else:
            sample_types = [self.samples[sample]['type'] for sample in self.samples]
        # remove duplicates
        sample_types = list(dict.fromkeys(sample_types))
        # sort list alphabetically
        sample_types.sort()
        return sample_types

    def get_projects(self):
        """
        Get projects
        """
        projects = [project for project in self.projects]
        # sort list alphabetically
        projects.sort()
        return projects
