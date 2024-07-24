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

The ObsidianImportGUI class is the main class of the Obsidian ELN Import package.
It provides a graphical user interface to import data and metadata from various
analytical instruments into Obsidian ELN. The class is a subclass of the QWidget
class of the PyQt5.QtWidgets module and contains methods to initialize the GUI,
load settings from settings.yaml, import data into Obsidian ELN, confirm import,
show success and error dialogs, and update the Obsidian ELN structure.
"""

import os
import pkgutil
import logging
import yaml

from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure as MplFigure

from obsELN.reader.eln import ObsidianELN
from obsELN.note.analysis import AnalysisNote


__main_package__ = 'obsELN'
logging.basicConfig(level=logging.INFO)


class ObsidianImportGUI(QtWidgets.QWidget):
    """
    Class definition of main GUI window
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Obsidian Import')
        self.setGeometry(100, 100, 700, 350)
        self.obsidian_eln = None
        self.analysis_note = None
        self.settings = None
        self.preview_window = None
        self.load_settings()
        self.initUI()

    def load_settings(self):
        """
        Load settings from settings.yaml
        """
        settings_file = os.path.join('resources', 'settings.yaml')
        settings_data = pkgutil.get_data(__main_package__, settings_file)
        if settings_data:
            try:
                settings_data = settings_data.decode('utf-8')
                self.settings = yaml.load(settings_data, Loader=yaml.SafeLoader)
            except yaml.YAMLError as exc:
                print(exc)
        else:
            logging.info('No settings file not found.')

    def initUI(self):
        """
        Initialize GUI
        """
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)

        if self.settings:
            if 'vault parent folder' in self.settings:
                vault_parent_folder = self.settings['vault parent folder']
                # check if vault parent folder exists
                if not os.path.isdir(vault_parent_folder):
                    vault_parent_folder = ''
            else:
                vault_parent_folder = ''
            if 'vault folder' in self.settings:
                default_vault = self.settings['vault folder']
                # check if default vault exists
                if not os.path.isdir(default_vault):
                    default_vault = ''
            else:  
                default_vault = ''
            if 'data folder' in self.settings:
                data_folder = self.settings['data folder']
                # check if data folder exists
                if not os.path.isdir(data_folder):
                    data_folder = ''
            else:
                data_folder = ''
        else:
            vault_parent_folder = ''
            default_vault = ''
            data_folder = ''

        self.folder = SelectObsidianVaultWidget(
            master=self,
            default_folder=vault_parent_folder,
            default_value=default_vault)

        self.file = SelectPathWidget(
            master=self,
            label_text='Select analysis data file',
            selection_type='file',
            default_folder=data_folder,
            file_types="Supported files (*.tif *.tiff *.mpt *.txt);;"
                       "SmartSEM TIFF files (*.tif *.tiff);;"
                       "BioLogic MPT files (*.mpt *.txt);;"
                       "LabSpec 6 files (*.txt)",
            button_label='Select file')

        self.parameter_frame = ParameterFrame(master=self)
        self.file_options_tab = QtWidgets.QTabWidget()
        self.mpt_options_frame = OptionsFrame(master=self, data_type='Biologic MPT')
        self.tiff_options_frame = OptionsFrame(master=self, data_type='SmartSEM TIFF')
        self.file_options_tab.addTab(self.mpt_options_frame, 'MPT options')
        self.file_options_tab.addTab(self.tiff_options_frame, 'TIFF options')
        self.folder.update_eln()

        self.import_button = QtWidgets.QPushButton(
            'Import',
            clicked=self.import_data)
        self.import_button.setStyleSheet(
            "background-color: purple; color: white;"
            "border-radius: 5px; width: 100px; height: 25px;")
        # shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        # shadow.setBlurRadius(8)
        # shadow.setColor(QtGui.QColor(100, 100, 100).lighter())
        # shadow.setXOffset(0)
        # shadow.setYOffset(1)
        # self.import_button.setGraphicsEffect(shadow)

        layout.addWidget(self.folder, 0, 0, 1, 2)
        layout.addWidget(self.file, 1, 0, 1, 2)
        layout.addWidget(self.parameter_frame, 2, 0, 1, 2)
        layout.addWidget(self.file_options_tab, 3, 0, 1, 2)
        layout.addWidget(self.import_button, 4, 1, 1, 1, alignment=QtCore.Qt.AlignRight)

    def import_data(self):
        """
        Import data into Obsidian ELN
        """
        note_author = self.parameter_frame.get('author')
        file_path = self.file.get()
        if file_path:
            project_name = self.parameter_frame.get('project_name')
            sample_name = self.parameter_frame.get('sample_name')
            sample_type = self.obsidian_eln.samples[sample_name]['meta']['sample']['type']
            sample_description = self.obsidian_eln.samples[sample_name]['meta']['sample']['description']
            operator = self.parameter_frame.get('operator')
            instrument = self.parameter_frame.get('instrument_id')
            instrument_type = self.obsidian_eln.instruments[instrument]['instrument']['type']
            status = 'completed'
            analysis_info = {
                'author': note_author,
                'project name': project_name,
                'sample name': sample_name,
                'sample type': sample_type,
                'sample description': sample_description,
                'instrument': instrument,
                'instrument type': instrument_type,
                'operator': operator,
                'status': status,
            }
            obsidian_base_folder = self.folder.get()
            # get data type from file extension
            extension = os.path.splitext(file_path)[1]
            if extension in ['.tif', '.tiff']:
                data_type = 'SmartSEM TIFF'
            elif extension == '.mpt':
                data_type = 'Biologic MPT'
            elif extension == '.txt':
                # read first line of data file to determine data type
                encoding = 'windows-1252'
                with open(file_path, 'r', encoding=encoding) as file:
                    first_line = file.readline()
                if first_line.startswith('#'):
                    data_type = 'LabSpec 6 TXT'
                elif first_line.startswith('EC-Lab ASCII FILE'):
                    data_type = 'Biologic MPT'
            else:
                data_type = None
            if data_type == 'Biologic MPT':
                # get options
                first_cycle_number = self.mpt_options_frame.first_cycle_number.get()
                if first_cycle_number:
                    first_cycle_number = int(first_cycle_number)
                else:
                    first_cycle_number = 1
                negative_charge_current = self.mpt_options_frame.charge_current.get()
                if negative_charge_current == 'negative':
                    negative_charge_current = True
                else:
                    negative_charge_current = False
                cycle_starts_with = self.mpt_options_frame.cycle_start.get()
                if cycle_starts_with == 'charge':
                    cycle_starts_with = 'charge'
                else:
                    cycle_starts_with = 'discharge'
                offset = None
                options = {
                    'first_cycle_number': first_cycle_number,
                    'negative_charge_current': negative_charge_current,
                    'cycle_starts_with': cycle_starts_with,
                    'offset': offset,
                    'process': True
                }
            else:
                options = None
            # create AnalysisNote object with prameters above
            print('Analysis note will be called with the following parameters:')
            print(f'file_path: {file_path}')
            print(f'analysis_info: {analysis_info}')
            print(f'obsidian_base_folder: {obsidian_base_folder}')
            print(f'options: {options}')
            self.analysis_note = AnalysisNote(
                file_path=file_path,
                analysis_info=analysis_info,
                obsidian_base_folder=obsidian_base_folder,
                options=options
            )
            if data_type == 'Biologic MPT':
                # create new window to preview plots
                self.preview_window = QtWidgets.QMainWindow()
                self.preview_window.setWindowTitle('Plot preview')
                self.preview_window.setGeometry(100, 100, 800, 600)
                self.preview_window.setWindowIcon(
                    QtGui.QIcon('obsidian_import_icon.png'))
                self.preview_window.setWindowFlags(
                    self.preview_window.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
                self.preview_window.setWindowModality(QtCore.Qt.ApplicationModal)
                self.preview_window.setCentralWidget(
                    PlotPreviewWidget(master=self, analysis_note=self.analysis_note))
                self.preview_window.show()
                self.preview_window.raise_()
                self.preview_window.activateWindow()
            elif data_type == 'SmartSEM TIFF':
                self.analysis_note.export_analysis_data()
                self.analysis_note.create_md_report()
                self.show_success_dialog(f'{file_path} successfully impoted into Obsidian ELN')
            elif data_type == 'LabSpec 6 TXT':
                self.analysis_note.export_analysis_data()
                self.analysis_note.create_md_report()
                self.show_success_dialog(f'{file_path} successfully impoted into Obsidian ELN')
            else:
                self.show_error_dialog(f'File type {extension} not supported')
        else:
            # show error dialog
            self.show_error_dialog('No file selected')

    def confirm_import(self, file_path, file_name, project_name, sample_name, sample_type, sample_description, operator, instrument, instrument_type, status, obsidian_base_folder):
        # Display confirmation dialog
        confirmation_dialog = QtWidgets.QMessageBox()
        confirmation_dialog.setWindowTitle('Confirm import')
        confirmation_dialog.setText(
            f'Import {file_name} into Obsidian ELN?')
        confirmation_dialog.setStandardButtons(
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        confirmation_dialog.setDefaultButton(QtWidgets.QMessageBox.No)
        # confirmation_dialog.setStyleSheet(
        #     "QLabel {font-weight: bold;}")
        # confirmation_dialog.setWindowIcon(
        #     QtWidgets.QIcon('obsidian_import_icon.png'))
        confirmation_dialog.setIcon(QtWidgets.QMessageBox.Question)
        confirmation_dialog.setWindowFlags(
            confirmation_dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        confirmation_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        confirmation_dialog.setEscapeButton(QtWidgets.QMessageBox.No)
        # confirmation_dialog.setButtonText(
        #     QtWidgets.QMessageBox.Yes, 'Import')
        # confirmation_dialog.setButtonText(
        #     QtWidgets.QMessageBox.No, 'Cancel')
        confirmation_dialog.setInformativeText(
            'This will overwrite any existing data with the same name.')
        confirmation_dialog.setDetailedText(
            f'Project name: {project_name}\n'
            f'Sample name: {sample_name}\n'
            f'Sample type: {sample_type}\n'
            f'Operator: {operator}\n'
            f'Instrument: {instrument}\n'
            f'Instrument type: {instrument_type}\n'
            f'Status: {status}\n'
            f'Obsidian vault: {obsidian_base_folder}')
        confirmation_dialog.show()
        confirmation_dialog.raise_()
        confirmation_dialog.activateWindow()
        confirmation = confirmation_dialog.exec_()
        if confirmation == QtWidgets.QMessageBox.Yes:
            # Import data
            analysis_info = {
                'author': 'Frieder Scheiba',
                'project name': project_name,
                'sample name': sample_name,
                'sample type': sample_type,
                'sample description': sample_description,
                'instrument': instrument,
                'instrument type': instrument_type,
                'operator': operator,
                'status': status,
            }
            options = {
                'first_cycle_number': 1,
                'negative_charge_current': None,
                'cycle_starts_with': None,
                'offset': None
            }
            analysis_note = AnalysisNote(
                file_path=file_path,
                analysis_info=analysis_info,
                obsidian_base_folder=obsidian_base_folder,
                options=options
            )

            analysis_note.export_analysis_data()
            analysis_note.create_md_report()
            return True
        else:
            return False

    def show_success_dialog(self, message):
        # Display success dialog
        success_dialog = QtWidgets.QMessageBox()
        success_dialog.setWindowTitle('Import successful')
        success_dialog.setText(message)
        success_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
        success_dialog.setDefaultButton(QtWidgets.QMessageBox.Ok)
        success_dialog.setStyleSheet(
            "QLabel {font-weight: bold;}")
        # success_dialog.setWindowIcon(
        #     QtWidgets.QIcon('obsidian_import_icon.png'))
        success_dialog.setIcon(QtWidgets.QMessageBox.Information)
        success_dialog.setWindowFlags(
            success_dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        success_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        success_dialog.setEscapeButton(QtWidgets.QMessageBox.Ok)
        success_dialog.show()
        success_dialog.raise_()
        success_dialog.activateWindow()
        success_dialog.exec_()

    def show_error_dialog(self, message):
        # Display error dialog
        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setWindowTitle('Import failed')
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
        error_dialog.setDefaultButton(QtWidgets.QMessageBox.Ok)
        error_dialog.setStyleSheet(
            "QLabel {font-weight: bold;}")
        # error_dialog.setWindowIcon(
        #     QtWidgets.QIcon('obsidian_import_icon.png'))
        error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
        error_dialog.setWindowFlags(
            error_dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        error_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        error_dialog.setEscapeButton(QtWidgets.QMessageBox.Ok)
        error_dialog.show()
        error_dialog.raise_()
        error_dialog.activateWindow()
        error_dialog.exec_()


class PlotPreviewWidget(QtWidgets.QWidget):
    """
    Widget to preview matplotlib plots of analysis data
    """

    def __init__(self, master=None, analysis_note: AnalysisNote = None):
        super().__init__()
        self.master = master
        if analysis_note:
            self.analysis_note = analysis_note
        else:
            self.analysis_note = master.analysis_note
        self.figures = None
        self.canvases = None
        self.figure_titles = None
        self.tab_widget = None

        self.initUI()

    def initUI(self):
        """
        Initialize UI
        """
        # set layout mode to grid layout
        layout = QtWidgets.QGridLayout()
        # configure layout
        layout.setColumnMinimumWidth(0, 800)
        layout.setColumnMinimumWidth(1, 300)
        # fix width of 2nd column
        # layout.setColumnStretch(1, 0)
        self.setLayout(layout)

        self.setStyleSheet(
            "QFrame#PlotPreviewWidgetFrame "
            "{border: 1px solid rgba(125, 125, 125, 0.3); border-radius: 3px;"
            "padding: 5px; background-color: rgba(125, 125, 125, 0.1);}")

        self.plot = QtWidgets.QLabel()

        # create matplotlib canvas for each figure

        self.canvases = []
        self.figures = []
        self.figure_titles = None
        if self.analysis_note.data_type == 'Biologic MPT':
            self.figure_titles = ['Capacity', 'Energy', 'Efficiency',
                                  'IR Drop', 'IR Rise',
                                  'V_vs_Cap', 'dQ/dV']

        for title in self.figure_titles:
            canvas = MplCanvas(master=self, parent=self, title=title)
            self.canvases.append(canvas)
            self.figures.append(canvas.figure)
        # create matplotlib figures of analysis data
        self.analysis_note.analysis.create_plots(canvases=self.canvases)

        # create tab widget
        self.tab_widget = QtWidgets.QTabWidget()
        for i, canvas in enumerate(self.canvases):
            if self.figure_titles:
                self.tab_widget.addTab(canvas, self.figure_titles[i])
            else:
                self.tab_widget.addTab(canvas, f'Figure {i+1}')
        
        # create frame for options
        self.options_frame = PlotOptionsFrame(master=self)

        # add tab widget for plots to first column of layout
        layout.addWidget(self.tab_widget, 0, 0, 1, 1)
        # add options frame to second column of layout
        layout.addWidget(self.options_frame, 0, 1, 1, 1)


class PlotOptionsFrame(QtWidgets.QFrame):
    """
    Widget to select options for plot preview
    """

    def __init__(self, master=None):
        super().__init__()
        self.master = master
        first_cycle_number = self.master.analysis_note.analysis.cycle_info['first cycle number']
        last_cycle_number = first_cycle_number + \
            self.master.analysis_note.analysis.cycle_info['number of cycles'] - 1
        plot_cycles_vvsq = [1, 2, 3, 4, 5, 10, 25, 50, 100, 250, 500, 750, 1000,
                            1250, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000,
                            5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000]
        # slice plot_cycles_vvsq to elements smaller than last_cycle_number
        plot_cycles_vvsq = [cycle for cycle in plot_cycles_vvsq if cycle <= last_cycle_number]
        plot_cycles_dqdv = [1, 3, 5]
        # slice plot_cycles_dqdv to elements smaller than last_cycle_number
        plot_cycles_dqdv = [cycle for cycle in plot_cycles_dqdv if cycle <= last_cycle_number]
        self.plot_options = {
            'first cycle number': first_cycle_number,
            'last cycle number': last_cycle_number,
            'exclude cycles': [],
            'cycles to plot v vs q': plot_cycles_vvsq,
            'voltage step': 5,
            'cycles to plot dqdv': plot_cycles_dqdv
        }
        self.initUI()

    def initUI(self):
        # set layout mode to grid layout
        options_layout = QtWidgets.QGridLayout()
        # configure layout
        # set fixed row height for rows 0, 1, 2, 3, 4, 5 and 6
        rows = range(0, 13)
        for row in rows:
            options_layout.setRowMinimumHeight(row, 20)
            # disable row stretch for rows
            options_layout.setRowStretch(row, 0)

        options_layout.setRowMinimumHeight(rows[-1]+1, 30)
        options_layout.setRowStretch(rows[-1]+2, 1)
        options_layout.setRowMinimumHeight(rows[-1]+3, 25)

        self.setLayout(options_layout)
        # add title to options frame
        self.title = QtWidgets.QLabel('Plot options')
        self.title.setStyleSheet("QLabel {font-weight: bold; font-size: 14px;}")
        # add section for cycle based plots
        self.cycle_based_label = QtWidgets.QLabel('Plots vs cycle number')
        self.cycle_based_label.setStyleSheet("QLabel {font-weight: bold; font-size: 12px;}")
        # get first and last cycle number from analysis note
        first_cycle_number = self.master.analysis_note.analysis.cycle_info['first cycle number']
        last_cycle_number = first_cycle_number + \
            self.master.analysis_note.analysis.cycle_info['number of cycles'] - 1
        # add label "first cycle" to options frame
        self.first_cycle_label = QtWidgets.QLabel('First cycle')
        # add spin box field for first cycle number to options frame
        self.first_cycle_number = QtWidgets.QSpinBox()
        self.first_cycle_number.setRange(first_cycle_number, last_cycle_number)
        self.first_cycle_number.setValue(first_cycle_number)
        self.first_cycle_number.setAlignment(QtCore.Qt.AlignRight)
        # add label "last cycle" to options frame
        self.last_cycle_label = QtWidgets.QLabel('Last cycle')
        # add spin box field for last cycle number to options frame
        self.last_cycle_number = QtWidgets.QSpinBox()
        self.last_cycle_number.setRange(first_cycle_number, last_cycle_number)
        self.last_cycle_number.setValue(last_cycle_number)
        self.last_cycle_number.setAlignment(QtCore.Qt.AlignRight)
        # add exclude cycles label and line edit field to options frame
        self.exclude_cycles_label = QtWidgets.QLabel('Exclude cycles')
        self.exclude_cycles = QtWidgets.QLineEdit()
        self.exclude_cycles.setPlaceholderText('Enter list of cycle numbers to exclude')
        self.exclude_cycles.setAlignment(QtCore.Qt.AlignRight)
        # set validator to only allow comma separated list of integers
        self.exclude_cycles.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'^\d+(,\s\d+)*$')))
        # add horizontal line to options frame
        self.hline = QtWidgets.QFrame()
        self.hline.setFrameShape(QtWidgets.QFrame.HLine)
        self.hline.setFrameShadow(QtWidgets.QFrame.Sunken)
        # add section vor voltage vs. capacity plot options
        self.voltage_capacity_label = QtWidgets.QLabel('V vs. Q')
        self.voltage_capacity_label.setStyleSheet("QLabel {font-weight: bold; font-size: 12px;}")
        # add widget to select list of cycles to plot
        self.cycles_to_plot_vvsq_label = QtWidgets.QLabel('Cycles to plot')
        self.cycles_to_plot_vvsq = QtWidgets.QLineEdit()
        # set default values
        self.cycles_to_plot_vvsq.setText('1, 2, 3, 5, 10, 20, 50, 100')
        self.cycles_to_plot_vvsq.setAlignment(QtCore.Qt.AlignRight)
        # set validator to only allow comma separated list of integers
        self.cycles_to_plot_vvsq.setValidator(
            QtGui.QRegExpValidator(QtCore.QRegExp(r'^\d+(,\s\d+)*$')))
        # add horizontal line to options frame
        self.hline2 = QtWidgets.QFrame()
        self.hline2.setFrameShape(QtWidgets.QFrame.HLine)
        self.hline2.setFrameShadow(QtWidgets.QFrame.Sunken)
        # add section for dQ/dV plot options
        self.dqdv_label = QtWidgets.QLabel('dQ/dV')
        # self.dqdv_label.setFixedHeight(20)
        self.dqdv_label.setStyleSheet("QLabel {font-weight: bold; font-size: 12px;}")
        # add widget for voltage step size
        self.voltage_step_label = QtWidgets.QLabel('Voltage step (mV)')
        self.voltage_step = QtWidgets.QLineEdit()
        self.voltage_step.setText('5')
        self.voltage_step.setAlignment(QtCore.Qt.AlignRight)
        # add widget for dQ/dV cycles to plot
        self.cycles_to_plot_dqdv_label = QtWidgets.QLabel('Cycles to plot')
        self.cycles_to_plot_dqdv = QtWidgets.QLineEdit()
        self.cycles_to_plot_dqdv.setText('1, 3, 5')
        self.cycles_to_plot_dqdv.setAlignment(QtCore.Qt.AlignRight)
        # set validator to only allow comma separated list of integers
        self.cycles_to_plot_dqdv.setValidator(
            QtGui.QRegExpValidator(QtCore.QRegExp(r'^\d+(,\s\d+)*$')))
        # add horizontal line to options frame
        self.hline3 = QtWidgets.QFrame()
        self.hline3.setFrameShape(QtWidgets.QFrame.HLine)
        self.hline3.setFrameShadow(QtWidgets.QFrame.Sunken)
        # add button to update plot preview
        self.update_button = QtWidgets.QPushButton(
            'Update plots', clicked=self.update_plot_preview)
        # create import button
        self.import_button = QtWidgets.QPushButton('Import', clicked=self.import_data)
        self.import_button.setStyleSheet(
            "background-color: purple; color: white;"
            "border-radius: 5px; width: 100px; height: 25px;")
        
        # add widgets to options frame
        row = 0
        # add title to the first row of the frame
        options_layout.addWidget(self.title, row, 0)
        # add cycle based plots label to the second row of the frame
        # let the label span two columns
        row += 1
        options_layout.addWidget(self.cycle_based_label, row, 0, 1, 2)
        # add first cycle label and spin box to the second row of the frame
        row += 1
        options_layout.addWidget(self.first_cycle_label, row, 0)
        options_layout.addWidget(self.first_cycle_number, row, 1)
        # add last cycle label and spin box to the third row of the frame
        row += 1
        options_layout.addWidget(self.last_cycle_label, row, 0)
        options_layout.addWidget(self.last_cycle_number, row, 1)
        # add  exclude cycles label and input field to the fourth row of the frame
        row += 1
        options_layout.addWidget(self.exclude_cycles_label, row, 0)
        options_layout.addWidget(self.exclude_cycles, row, 1)
        # add horizontal line to the fifth row of the frame
        row += 1
        options_layout.addWidget(self.hline, row, 0, 1, 2)
        # add voltage vs. capacity label to the sixth row of the frame
        row += 1
        options_layout.addWidget(self.voltage_capacity_label, row, 0, 1, 2)
        # add cycles to plot label and input field to the seventh row of the frame
        row += 1
        options_layout.addWidget(self.cycles_to_plot_vvsq_label, row, 0)
        options_layout.addWidget(self.cycles_to_plot_vvsq, row, 1)
        # add horizontal line to the eighth row of the frame
        row += 1
        options_layout.addWidget(self.hline2, row, 0, 1, 2)
        # add dQ/dV label to the eighth row of the frame
        row += 1
        options_layout.addWidget(self.dqdv_label, row, 0, 1, 2)
        # add voltage step label and input field to the ninth row of the frame
        row += 1
        options_layout.addWidget(self.voltage_step_label, row, 0)
        options_layout.addWidget(self.voltage_step, row, 1)
        # add cycles to plot label and input field to the tenth row of the frame
        row += 1
        options_layout.addWidget(self.cycles_to_plot_dqdv_label, row, 0)
        options_layout.addWidget(self.cycles_to_plot_dqdv, row, 1)
        # add horizontal line to the tenth row of the frame
        row += 1
        options_layout.addWidget(self.hline3, row, 0, 1, 2)
        
        # add update button to the fifth row of the frame in the 10th row of the frame
        options_layout.addWidget(self.update_button, rows[-1]+1, 1)
        # add empty row to the sixth row of the frame

        # add import button to the last row of the frame in the 11th row of the frame
        options_layout.addWidget(self.import_button, rows[-1]+3, 1)

    def get_exclude_cycles(self):
        """
        Get list of cycles to exclude
        """
        # get first and last cycle number from analysis note
        first_cycle = self.master.analysis_note.analysis.cycle_info['first cycle number']
        last_cycle = (
            first_cycle +
            self.master.analysis_note.analysis.cycle_info['number of cycles'] - 1
        )
        debug_msg = f'First cycle: {first_cycle}, Last cycle: {last_cycle}'
        logging.debug(debug_msg)
        first_cycle_plot_options = self.get_first_cycle_number()
        last_cycle_plot_options = self.get_last_cycle_number()
        exclude_cycles_text = self.exclude_cycles.text()
        if exclude_cycles_text == '':
            exclude_cycles = []
        else:
            exclude_cycles = exclude_cycles_text.split(',')
        exclude_cycles = [int(cycle) for cycle in exclude_cycles]
        if first_cycle_plot_options > first_cycle:
            exclude_first_cycles = list(range(first_cycle, first_cycle_plot_options))
            # check if cycles in exclude_cycles are in exclude_first_cycles
            exclude_cycles = [
                cycle for cycle in exclude_cycles if cycle not in exclude_first_cycles
            ]
            exclude_cycles = exclude_first_cycles + exclude_cycles
        if last_cycle_plot_options < last_cycle:
            exclude_last_cycles = list(range(last_cycle_plot_options + 1, last_cycle + 1))
            # check if cycles in exclude_cycles are in exclude_last_cycles
            exclude_cycles = [
                cycle for cycle in exclude_cycles if cycle not in exclude_last_cycles
            ]
            exclude_cycles = exclude_cycles + exclude_last_cycles
        return exclude_cycles

    def get_first_cycle_number(self):
        """
        Get first cycle number
        """
        return self.first_cycle_number.value()

    def get_last_cycle_number(self):
        """
        Get last cycle number
        """
        return self.last_cycle_number.value()

    def get_cycles_to_plot_vvsq(self):
        """
        Get list of cycles to plot for V vs. Q plot
        """
        cycles_to_plot = self.cycles_to_plot_vvsq.text()
        cycles_to_plot = cycles_to_plot.split(',')
        cycles_to_plot = [int(cycle) for cycle in cycles_to_plot]
        return cycles_to_plot

    def get_voltage_step(self):
        """
        Get voltage step size for dQ/dV plot
        """
        return int(self.voltage_step.text())

    def get_cycles_to_plot_dqdv(self):  
        """
        Get list of cycles to plot for dQ/dV plot
        """
        cycles_to_plot = self.cycles_to_plot_dqdv.text()
        cycles_to_plot = cycles_to_plot.split(',')
        cycles_to_plot = [int(cycle) for cycle in cycles_to_plot]
        return cycles_to_plot

    def import_data(self):
        """
        Import data into Obsidian ELN
        """
        master = self.master.master
        plot_options = self.plot_options
        master.analysis_note.export_analysis_data(plot_options=plot_options)
        master.analysis_note.create_md_report()
        # close preview window
        master.preview_window.close()
        master.show_success_dialog(f'{master.analysis_note.file_path} successfully impoted into Obsidian ELN')

    def update_plot_preview(self):
        """
        Update plot preview
        """
        # get list of plot canvases
        canvases = self.master.canvases
        # get exclude cycles
        exclude_cycles = self.get_exclude_cycles()
        exclude_cycles_last = self.plot_options['exclude cycles']
        if exclude_cycles != exclude_cycles_last:
            self.plot_options['exclude cycles'] = exclude_cycles
            info_msg = f'Excluding cycles: {exclude_cycles}'
            logging.info(info_msg)
            # get first cycle number of mpt options
            # first_cycle_number = int(self.master.master.mpt_options_frame.first_cycle_number.get())
            # exclude_indices = [cycle - first_cycle_number for cycle in exclude_cycles]
            # update figures capacity, efficiency, voltage drop and voltage rise
            figure_titles = ['Capacity', 'Energy', 'Efficiency', 'IR Drop', 'IR Rise']
            for canvas in canvases:
                title = canvas.title
                figure = canvas.figure
                if title in figure_titles:
                    self.master.analysis_note.analysis.remove_plot_data_points(
                        figure, exclude_x_values=exclude_cycles)
                else:
                    pass
        # update voltage vs. capacity plot
        self.update_v_vs_cap_plot()
        # update dQ/dV plot
        self.update_dqdv_plot()

    def update_v_vs_cap_plot(self):
        """
        Update Voltage vs. Capacity plot
        """
        # get cycles to plot
        cycles_to_plot = self.get_cycles_to_plot_vvsq()
        cycles_to_plot_last = self.plot_options['cycles to plot v vs q']

        def get_canvas_vvsq():
            """
            Get canvas for V vs. Q plot
            """
            for canvas in self.master.canvases:
                if canvas.title == 'V_vs_Cap':
                    return canvas
            return None

        if cycles_to_plot != cycles_to_plot_last:
            # update plot options
            self.plot_options['cycles to plot v vs q'] = cycles_to_plot
            # update V vs. Q plot
            canvas = get_canvas_vvsq()
            if canvas:
                # clear plot
                canvas.axis.clear()
                self.master.analysis_note.analysis.plot_voltage_vs_capacity(
                    cycles=cycles_to_plot, canvas=canvas)
                # refresh canvas
                # canvas.draw()
                canvas.figure.canvas.draw()

    def update_dqdv_plot(self):
        """
        Update dQ/dV plot
        """
        # get voltage step size
        voltage_step = self.get_voltage_step()
        voltage_step_last = self.plot_options['voltage step']
        # get cycles to plot
        cycles_to_plot = self.get_cycles_to_plot_dqdv()
        cycles_to_plot_last = self.plot_options['cycles to plot dqdv']

        def get_canvas_dqdv():
            """
            Get canvas for dQ/dV plot
            """
            for canvas in self.master.canvases:
                if canvas.title == 'dQ/dV':
                    return canvas
            return None

        if voltage_step != voltage_step_last:
            # update plot options
            self.plot_options['voltage step'] = voltage_step
            # update the dQ/dV column in the analysis data
            self.master.analysis_note.analysis.add_column_dq_dv(
                dv_step=voltage_step, update=True)
            # update dQ/dV plot
            canvas = get_canvas_dqdv()
            if canvas:
                # clear plot
                canvas.axis.clear()
                self.master.analysis_note.analysis.plot_dq_dv_vs_voltage(
                    cycles=cycles_to_plot, canvas=canvas)
                # refresh canvas
                # canvas.draw()
                canvas.figure.canvas.draw()
        elif cycles_to_plot != cycles_to_plot_last:
            # update plot options
            self.plot_options['cycles to plot dqdv'] = cycles_to_plot
            # update dQ/dV plot
            canvas = get_canvas_dqdv()
            if canvas:
                # clear plot
                canvas.axis.clear()
                self.master.analysis_note.analysis.plot_dq_dv_vs_voltage(
                    cycles=cycles_to_plot, canvas=canvas)
                # refresh canvas
                # canvas.draw()
                canvas.figure.canvas.draw()


class MplCanvas(FigureCanvasQTAgg):
    """
    Matplotlib canvas
    """
    def __init__(self, master=None, parent=None, title=None,
                 width=4, height=3, dpi=120):
        self.master = master
        self.parent = parent
        self.title = title
        # create figure
        self.figure = MplFigure(figsize=(width, height), dpi=dpi)
        # create axes
        self.axis = self.figure.subplots()
        # initialize canvas
        super(MplCanvas, self).__init__(self.figure)


class SelectPathWidget(QtWidgets.QFrame):
    """
    Widget to select a path. Subclasses QFrame and contains a label, a line
    edit and a button. Clicking the button opens a file dialog.
    """
    def __init__(self,
                 master: QtWidgets.QWidget = None,
                 label_text: str = '',
                 selection_type: str = 'file',
                 default_value: str = None,
                 default_folder: str = None,
                 file_types: str = 'All files (*.*);;',
                 button_label: str = 'Select path'):
        super().__init__()
        self.master = master
        self.setObjectName('SelectPathWidgetFrame')
        self.label_text = label_text
        self.selection_type = selection_type
        self.default_value = default_value
        self.default_folder = default_folder
        self.file_types = file_types
        if button_label == 'Select path' and self.selection_type == 'folder':
            button_label = 'Select folder'
        elif button_label == 'Select path' and self.selection_type == 'file':
            button_label = 'Select file'
        self.button_label = button_label
        self.initUI()

    def initUI(self):
        """
        Initialize UI
        """
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        self.setStyleSheet(
            "QFrame#SelectPathWidgetFrame "
            "{border: 1px solid rgba(125, 125, 125, 0.3); border-radius: 3px;"
            "padding: 5px; background-color: rgba(125, 125, 125, 0.1);}")

        self.label = QtWidgets.QLabel(self.label_text)
        self.label.setObjectName('label')
        self.label.setStyleSheet("QLabel#label {font-weight: bold;}")
        self.button = QtWidgets.QPushButton(self.button_label, clicked=self.select_path)
        self.entry = QtWidgets.QLineEdit()
        self.entry.setPlaceholderText('Selected path will appear here')
        if self.default_value:
            self.entry.setText(self.default_value)
        self.entry.setReadOnly(True)

        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addWidget(self.button)

    def select_path(self):
        """
        Open file dialog to select path
        """
        if self.selection_type == 'folder':
            path = QtWidgets.QFileDialog.getExistingDirectory(
                self, 'Select folder', self.default_folder, QFileDialog.ShowDirsOnly)
        else:
            path, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, 'Select file', self.default_folder, self.file_types)
        if path:
            self.entry.setText(path)
            if self.selection_type == 'file':
                # check if file is a supported analysis file
                extension = os.path.splitext(path)[1]
                if extension in ['.tif', '.tiff', '.mpt', '.txt']:
                    if extension == '.mpt':
                        # make mpt options tab the active tab
                        self.master.file_options_tab.setCurrentIndex(0)
                        # open MPT file
                        self.master.analysis_note = AnalysisNote(file_path=path)
                        print('Analysis file loaded')
                        # get mass of active material and characterisitic mass from analysis note
                        active_mass = str(
                            self.master.analysis_note.analysis.header['Mass of active material']['value'])
                        characteristic_mass = str(
                            self.master.analysis_note.analysis.header['Characteristic mass']['value'])
                        # get battery capacity from analysis note
                        battery_capacity = str(
                            self.master.analysis_note.analysis.header['Battery capacity']['value'])
                        # get cycle starts with from analysis note
                        cycle_starts_with = str(
                            self.master.analysis_note.analysis.cycle_info['cycle starts with'])
                        # get sign of charge current from analysis note
                        negative_charge_current = self.master.analysis_note.analysis.cycle_info['negative charge current']
                        # update mpt options
                        self.master.mpt_options_frame.active_material_mass.update(active_mass)
                        self.master.mpt_options_frame.characteristic_mass.update(characteristic_mass)
                        self.master.mpt_options_frame.battery_capacity.update(battery_capacity)
                        if cycle_starts_with == 'charge':
                            self.master.mpt_options_frame.cycle_start.combobox.setCurrentText('charge')
                        else:
                            self.master.mpt_options_frame.cycle_start.combobox.setCurrentText('discharge')
                        if negative_charge_current:
                            self.master.mpt_options_frame.charge_current.combobox.setCurrentText('negative')
                    elif extension == '.tif' or extension == '.tiff':
                        # make tiff options tab the active tab
                        self.master.file_options_tab.setCurrentIndex(1)
                    elif extension == '.txt':
                        # make txt options tab the active tab
                        # self.master.file_options_tab.setCurrentIndex(2)
                        pass
                else:
                    # show error dialog
                    self.master.show_error_dialog(f'File type {extension} not supported')
                    self.entry.setText('')

    def get(self):
        """
        Get path
        """
        return self.entry.text()


class SelectObsidianVaultWidget(SelectPathWidget):
    """
    Widget to select Obsidian vault. Subclasses SelectPathWidget and overrides
    select_path() method to open a folder dialog
    """

    def __init__(self, master=None, default_folder=None, default_value=None):
        super().__init__(
            master=master,
            label_text='Select Obsidian vault',
            selection_type='folder',
            button_label='Select vault',
            default_folder=default_folder,
            default_value=default_value,
        )

    def select_path(self):
        """
        Open folder dialog to select Obsidian vault
        """
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select folder', self.default_folder, QtWidgets.QFileDialog.ShowDirsOnly)
        if path:
            self.entry.setText(path)
            # update Obsidian ELN structure
            self.update_eln()

    def update_eln(self):
        """
        Update Obsidian ELN structure
        """
        path = self.entry.text()
        if path:
            self.master.obsidian_eln = ObsidianELN(path)
            # get list of projects
            projects = self.master.obsidian_eln.projects.keys()
            # update project name combobox
            self.master.parameter_frame.project_name.update(projects)
            # get list of samples
            if len(projects) > 0:
                project_name = self.master.parameter_frame.project_name.get()
                samples = self.master.obsidian_eln.get_samples(project_name)
            else:
                samples = self.master.obsidian_eln.samples.keys()
            # update sample name combobox
            self.master.parameter_frame.sample_name.update(samples)
            # get list of operators
            operators = self.master.obsidian_eln.operators.keys()
            # update operator combobox
            self.master.parameter_frame.operator.update(operators)
            # get list of instruments
            instruments = self.master.obsidian_eln.instruments.keys()
            # update instrument combobox
            self.master.parameter_frame.instrument_id.update(instruments)
            # get list of authors
            authors = self.master.obsidian_eln.settings['note']['author']
            # if authors is a string, convert to list
            if isinstance(authors, str):
                authors = [authors]
            # update author combobox
            self.master.parameter_frame.author.update(authors)
            # get list of status
            status = self.master.obsidian_eln.settings['analysis']['status']
            # update status combobox
            self.master.parameter_frame.status.update(status)
            if 'completed' in status:
                self.master.parameter_frame.status.combobox.setCurrentText('completed')


class ParameterFrame(QtWidgets.QFrame):
    """
    Widget to select parameters for import
    """

    def __init__(self,  master=None):
        super().__init__()
        self.master = master
        self.setObjectName('ParameterFrame')
        self.create_widgets()
        self.set_layout()

    def create_widgets(self):
        """
        Create widgets
        """
        self.frame_label = QtWidgets.QLabel('Analysis parameters')
        self.frame_label.setStyleSheet(
            "QLabel {font-weight: bold; font-size: 14px;}")
        self.project_name = LabeledComboBox(
            label_text='Project name', options=[])
        self.sample_name = LabeledComboBox(
            label_text='Sample name', options=[])
        self.operator = LabeledComboBox(label_text='Operator', options=[])
        self.instrument_id = LabeledComboBox(label_text='Instrument ID', options=[])
        self.author = LabeledComboBox(label_text='Note author', options=[])
        self.status = LabeledComboBox(label_text='Status', options=['completed', 'in progress', 'aborted', 'failed'])

        self.project_name.combobox.currentTextChanged.connect(self.project_changed)

    def set_layout(self):
        """
        Set layout
        """
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)

        self.setStyleSheet(
            "QFrame#ParameterFrame "
            "{border: 1px solid rgba(125, 125, 125, 0.3); border-radius: 3px;"
            "padding: 5px; background-color: rgba(125, 125, 125, 0.1);}")

        layout.setColumnMinimumWidth(0, 200)
        layout.setColumnMinimumWidth(1, 200)
        layout.setColumnMinimumWidth(2, 200)
        # addWidgets(self, QWidget, row, column, rowSpan, columnSpan, alignment)
        layout.addWidget(self.frame_label, 0, 0)
        layout.addWidget(self.project_name, 1, 0)
        layout.addWidget(self.sample_name, 1, 1)
        layout.addWidget(self.instrument_id, 1, 2)
        layout.addWidget(self.operator, 2, 0)
        layout.addWidget(self.status, 2, 1)
        layout.addWidget(self.author, 2, 2)

    def get(self, field):
        """
        Get value of parameter
        """
        if field == 'project_name':
            return self.project_name.get()
        elif field == 'sample_name':
            return self.sample_name.get()
        elif field == 'operator':
            return self.operator.get()
        elif field == 'instrument_id':
            return self.instrument_id.get()
        elif field == 'status':
            return self.status.get()
        elif field == 'author':
            return self.author.get()
        else:
            raise ValueError('Invalid field')
        
    def project_changed(self):
        """
        Update sample name combobox when project name is changed
        """
        project_name = self.project_name.get()
        if project_name:
            samples = self.master.obsidian_eln.get_samples(project_name)
            self.sample_name.update(samples)


class OptionsFrame(QtWidgets.QFrame):
    """
    Widget to select parameters for import
    """

    def __init__(self,  master=None, data_type=None):
        super().__init__()
        self.master = master
        self.data_type = data_type
        self.setObjectName('OptionsFrame')
        if self.data_type == 'Biologic MPT':
            self.create_widgets_mpt()
            self.set_layout_mpt()
        elif self.data_type == 'SmartSEM TIFF':
            self.create_widgets_tiff()
            self.set_layout_tiff()
        else:
            self.create_default_widgets()
            self.set_default_layout()

    def create_widgets_mpt(self):
        """
        Create widgets
        """
        self.options_label = QtWidgets.QLabel('MPT import options')
        self.options_label.setStyleSheet("QLabel {font-weight: bold; font-size: 14px;}")
        self.cycle_start = LabeledComboBox(
            label_text='Cycle starts with', options=['charge', 'discharge'])
        self.cycle_start.combobox.currentIndexChanged.connect(self.cycle_start_changed)
        self.charge_current = LabeledComboBox(
            label_text='Sign of charge current', options=['positive', 'negative'])
        self.first_cycle_number = LabeledEntryField(
            label_text='First cycle number', defaultValue='1', alignment='right',
            valiator='int')
        self.active_material_mass = LabeledEntryField(
            label_text='Mass of active material (mg)', defaultValue='', alignment='right',
            valiator='float')
        self.characteristic_mass = LabeledEntryField(
            label_text='Characteristic mass (mg)', defaultValue='', alignment='right',
            valiator='float')
        self.battery_capacity = LabeledEntryField(
            label_text='Battery capacity (mAh)', defaultValue='', alignment='right',
            valiator='float')

    def set_layout_mpt(self):
        """
        Set layout
        """
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)

        self.setStyleSheet(
            "QFrame#OptionsFrame "
            "{border: 1px solid rgba(125, 125, 125, 0.3); border-radius: 3px;"
            "padding: 5px; background-color: rgba(125, 125, 125, 0.1);}")

        layout.setColumnMinimumWidth(0, 200)
        layout.setColumnMinimumWidth(1, 200)
        layout.setColumnMinimumWidth(2, 200)
        # addWidgets(self, QWidget, row, column, rowSpan, columnSpan, alignment)
        layout.addWidget(self.options_label, 0, 0)
        layout.addWidget(self.cycle_start, 1, 0)
        layout.addWidget(self.active_material_mass, 1, 1)
        layout.addWidget(self.first_cycle_number, 1, 2)
        layout.addWidget(self.charge_current, 2, 0)
        layout.addWidget(self.characteristic_mass, 2, 1)
        layout.addWidget(self.battery_capacity, 2, 2)

    def cycle_start_changed(self):
        """
        Update charge current combobox when cycle start combobox is changed
        """
        charge_current = self.charge_current.get()
        if charge_current == 'positive':
            # change charge current selection to negative
            self.charge_current.combobox.setCurrentText('negative')
        else:
            self.charge_current.combobox.setCurrentText('positive')

    def create_widgets_tiff(self):
        """
        Create widgets
        """
        self.options_label = QtWidgets.QLabel('SmartSEM TIFF import options')
        self.options_label.setStyleSheet("QLabel {font-weight: bold; font-size: 14px;}")
        self.display_text = QtWidgets.QLabel('No options available for TIFF files')
        self.display_text.setStyleSheet("QLabel {font-style: italic; color: grey;}")
        self.display_text.setAlignment(QtCore.Qt.AlignCenter)

    def set_layout_tiff(self):
        """
        Set layout
        """
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.setStyleSheet(
            "QFrame#OptionsFrame "
            "{border: 1px solid rgba(125, 125, 125, 0.3); border-radius: 3px;"
            "padding: 5px; background-color: rgba(125, 125, 125, 0.1);}")

        layout.addWidget(self.options_label)
        layout.addWidget(self.display_text)

    def create_default_widgets(self):
        """
        Create widgets
        """
        self.options_label = QtWidgets.QLabel(self.data_type + ' import options')
        self.options_label.setStyleSheet("QLabel {font-weight: bold; font-size: 14px;}")
        self.display_text = QtWidgets.QLabel('No options available for this file type')
        self.display_text.setStyleSheet("QLabel {font-style: italic; color: grey;}")
        self.display_text.setAlignment(QtCore.Qt.AlignCenter)

    def set_default_layout(self):
        """
        Set layout
        """
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.setStyleSheet(
            "QFrame#OptionsFrame "
            "{border: 1px solid rgba(125, 125, 125, 0.3); border-radius: 3px;"
            "padding: 5px; background-color: rgba(125, 125, 125, 0.1);}")

        layout.addWidget(self.options_label)
        layout.addWidget(self.display_text)

class LabeledEntryField(QtWidgets.QWidget):
    """
    Widget with a label and a line edit
    """

    def __init__(self,
                 master=None,
                 label_text='',
                 defaultValue=None,
                 alignment='left',
                 valiator=None,
                 input_mask=None):
        super().__init__()
        self.master = master
        self.label_text = label_text
        self.defaultValue = defaultValue
        self.alignment = alignment
        self.valiator = valiator
        self.input_mask = input_mask
        self.initUI()

    def initUI(self):
        """
        Initialize UI
        """
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.label = QtWidgets.QLabel(self.label_text)
        self.entry = QtWidgets.QLineEdit(self.defaultValue)
        if self.input_mask:
            self.entry.setInputMask(self.input_mask)
        if self.alignment == 'right':
            self.entry.setAlignment(QtCore.Qt.AlignRight)
        else:
            self.entry.setAlignment(QtCore.Qt.AlignLeft)
        if self.valiator == 'float':
            self.entry.setValidator(QtGui.QDoubleValidator())
        elif self.valiator == 'int':
            self.entry.setValidator(QtGui.QIntValidator())
        else:
            pass

        layout.addWidget(self.label)
        layout.addWidget(self.entry)

    def get(self):
        """
        Get value of entry field
        """
        return self.entry.text()

    def update(self, text):
        """
        Update entry field
        """
        self.entry.setText(text)


class LabeledComboBox(QtWidgets.QWidget):
    """
    Widget with a label and a combo box
    """

    def __init__(self, master=None, label_text='', options=None):
        super().__init__()
        self.master = master
        self.label_text = label_text
        self.options = options
        self.create_widgets()
        self.set_layout()

    def create_widgets(self):
        """
        Create widgets
        """
        self.label = QtWidgets.QLabel(self.label_text)
        self.combobox = QtWidgets.QComboBox()
        self.combobox.addItems(self.options)

    def set_layout(self):
        """
        Set layout
        """
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.label)
        layout.addWidget(self.combobox)

    def get(self):
        """
        Get value of combo box
        """
        return self.combobox.currentText()

    def update(self, options):
        """
        Update combo box options
        """
        self.combobox.clear()
        self.combobox.addItems(options)
