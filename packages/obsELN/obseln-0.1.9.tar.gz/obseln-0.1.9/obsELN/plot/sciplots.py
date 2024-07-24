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

This file defines custom plotting functions for scientific plots.
"""

import os
import pkgutil
import logging
import yaml
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.legend as mlegend
from matplotlib import font_manager
import pandas as pd
import numpy as np

__main_package__ = 'obsELN'


def single_axis_plot(data, exclude: list = None,
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
    data_label : str, optifonal
        Label of the data. The default is None.
    """
    if exclude is not None:
        # trim exclude list to only include indices that are in data
        exclude_indices = [index for index in exclude
                           if index in data.index.to_list()]
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
            color = default_colors[0]
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
            marker = marker
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
            linestyle = linestyle
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
        color = rgb_color_tuple_from_array(color)
        axis_obj.plot(x_data, y_data, linestyle=linestyle, color=color,
                      marker=marker, markersize=4,  markeredgecolor=color,
                      markeredgewidth=0.5, fillstyle='full',
                      markerfacecolor=color + (0.2,),
                      label=data_label)
    elif length > 0:
        for i in range(length):
            line_color = rgb_color_tuple_from_array(color[i])
            marker_style = marker[i]
            axis_obj.plot(x_data[i], y_data[i], linestyle=linestyle, color=line_color,
                          marker=marker_style, markersize=4,  markeredgecolor=line_color,
                          markeredgewidth=0.5, fillstyle='full',
                          markerfacecolor=line_color + (0.2,),
                          label=data_label[i])

    axis_obj.set_title(title)
    axis_obj.set_xlabel(xlabel)
    axis_obj.set_ylabel(ylabel)
    axis_obj.legend(loc='upper right')
    format_plot(figure_obj, [axis_obj])

    return figure_obj


def create_doulbe_yaxis_plot(canvas=None):
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


def multi_line_plot(data: pd.DataFrame = None,
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
        line_gradient = color_gradient(
            rgb1=line_gradients[d_index][0], rgb2=line_gradients[d_index][1], steps=n_lines)
        for index, line in enumerate(line_selector_values):
            mindex = (dataset, line)
            # check if data_index is in data
            if mindex in plot_data.index:
                info_msg = f'Creating plot for dataset {
                    dataset} and line {line}'
                logging.info(info_msg)
                x_data = plot_data.loc[mindex, x_data_column]
                y_data = plot_data.loc[mindex, y_data_column]
                line_handles[d_index][index] = axis_obj.plot(
                    x_data, y_data, color=line_gradient[index])
            else:
                warning_msg = f'No data found for dataset {
                    dataset} and line {line}'
                logging.warning(warning_msg)

    axis_obj.set_xlabel(xlabel)
    axis_obj.set_ylabel(ylabel)
    axis_obj.set_title(title)

    # expand x axis to the right by 20% to make room for legend
    axis_obj.set_xlim(left=0.95 * axis_obj.get_xlim()
                      [0], right=1.2 * axis_obj.get_xlim()[1])

    # make concatenate lists in line_handles
    line_handles_flat = [
        item for sublist in line_handles for item in sublist]
    # line_handels_flat is now a nested list where each handle is stored in its own list
    # make line_handles_flat a flat list
    line_handles_flat = [
        item for sublist in line_handles_flat for item in sublist]
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
    format_plot(figure_obj, axis_obj)
    return figure_obj


def color_gradient(rgb1: tuple = (255, 0, 0),
                   rgb2: tuple = (0, 0, 255), steps: int = 10):
    """
    Create color gradient between rgb1 and rgb2.
    """
    # create color gradient
    gradient = []
    gradient = [tuple(rgb1[j]/255 + (rgb2[j] - rgb1[j])/255 * i / steps for j in range(3))
                for i in range(steps)]
    return gradient


def rgb_color_tuple_from_array(color):
    """
    Return normalized RGB color tuple from an array of RGB colors.
    """
    # convert color to normalized RGB color tuple
    return tuple([x/255 for x in color])


def format_plot(figure_obj, axis_objects):
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
        title_color = rgb_color_tuple_from_array(
            plot_colors['text']['colors'][0])
        axes_color = rgb_color_tuple_from_array(
            plot_colors['axes']['colors'][0])
        axes_label_color = rgb_color_tuple_from_array(
            plot_colors['text']['colors'][0])
        grid_color = rgb_color_tuple_from_array(
            plot_colors['grid']['colors'][0])
        tick_color = axes_color
    else:
        axes_color = rgb_color_tuple_from_array([55, 53, 47])
        axes_label_color = rgb_color_tuple_from_array([55, 53, 47])
        grid_color = rgb_color_tuple_from_array([99, 95, 84])
        tick_color = rgb_color_tuple_from_array([55, 53, 47])

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
        axis_obj.set_xticklabels(
            xlabels,
            fontname=font_name, fontsize=8, fontweight='medium',
            color=axes_label_color)
        yticks_loc = axis_obj.get_yticks()
        ylabels = axis_obj.get_yticklabels()
        axis_obj.yaxis.set_major_locator(mticker.FixedLocator(yticks_loc))
        axis_obj.set_yticklabels(
            ylabels,
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
        axis_obj.grid(
            axis='y', linestyle='-',
            color=yaxis_color, linewidth=0.4, alpha=0.3)
        axis_obj.grid(
            axis='x', linestyle='-',
            color=grid_color, linewidth=0.4, alpha=0.3)

        axis_obj.set_facecolor((1, 1, 1, 0))

        # format axis legend
        legends = [item for item in axis_obj.get_children(
        ) if isinstance(item, mlegend.Legend)]
        for legend in legends:
            # set legend frame color
            legend_frame_color = rgb_color_tuple_from_array(
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
