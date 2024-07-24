"""
Universal plot function to plot and style xy data with matplotlib
or plotly using a style dictionary.
"""
import os
import re
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import yaml


class UPlot:
    def __init__(
            self, plot_type: str = 'line', data: (dict, pd.DataFrame) = None,
            xcolumn: str = None, ycolumns: list = None, style_dict=None,
            plotly=False):
        """
        Plot xy data with matplotlib or plotly using a style dictionary.

        Parameters
        ----------
        data : pandas.DataFrame or dict
            pandas DataFrame or dictionary containing data to be plotted.
        style_dict : dict
            Dictionary containing style information.
        plotly : bool, optional
            If True, plot with plotly, else plot with matplotlib, by default False
        """
        self.plot_type = plot_type
        self.data = data
        self.xcolumn = xcolumn
        self.ycolumns = ycolumns
        self.style_dict = style_dict
        self.fig = None
        self.ax = None
        self.plotly = plotly

        if plotly:
            self.renderer = 'plotly'
        else:
            self.renderer = 'matplotlib'

        if os.path.exists('resources/plot_styles.yaml'):
            self.plot_styles = yaml.load(
                open('resources/plot_styles.yaml', 'r', encoding='utf8'),
                Loader=yaml.FullLoader)
        else:
            self.plot_styles = {
                'line-chart': {
                    'chart': {
                        'background-color': '#ffffff',
                        'title': {
                            'visible': False,
                            'text': 'Title',
                            'font-size': 20,
                            'font-family': 'Arial',
                            'font-weight': 'bold',
                            'color': '#000000',
                            'position': 'top',
                        },
                        'xlabel': {
                            'visible': True,
                            'text': 'x-axis',
                            'font-size': 16,
                            'font-family': 'Arial',
                            'font-weight': 'bold',
                            'color': '#000000',
                            'position': 'bottom'},
                        'ylabel': {
                            'visible': True,
                            'text': 'y-axis',
                            'font-size': 16,
                            'font-family': 'Arial',
                            'font-weight': 'bold',
                            'color': '#000000',
                            'position': 'left'},
                    },
                    'lines': {
                        'colors': {
                            'apply': 'list',
                            'list': [
                                '#ff0000',
                                '#00ff00',
                                '#0000ff'],
                            'map': {
                                'style': 'hsv',
                                'n-color': 5},
                        },
                        'style': [
                            'solid',
                            'dashed',
                            'dotted',
                            'dash-dotted'],
                        'width': 2,
                        'cycler': 'multiply',
                    },
                    'markers': {
                        'edge': {
                            'visible': True,
                            'colors': {
                                'apply': 'line',
                                'list': [
                                  '#ff0000',
                                  '#00ff00',
                                  '#0000ff'],
                                'map': {
                                    'style': 'hsv',
                                    'n-color': 5},
                            },
                            'style': [
                              'circle',
                              'square',
                              'triangle',
                              'star'],
                            'width': 2,
                        },
                        'face': {
                            'visible': 'true',
                            'style': 'solid',
                            'colors': 'same',
                        },
                    },
                    'axes': {
                        'limits': {
                            'xmin': 'min - 10 %',
                            'xmax': 'max + 10 %',
                            'ymin': 'min - 10 %',
                            'ymax': 'max + 10 %',
                        },
                        'scale': {
                            'x': 'linear',
                            'y': 'linear',
                        },
                        'style': {
                            'bottom': {
                                'visible': True,
                                'color': '#aaaaaa',
                                'line-width': 2},
                            'top': {
                                'visible': True,
                                'color': '#aaaaaa',
                                'line-width': 2},
                            'left': {
                                'visible': True,
                                'color': '#aaaaaa',
                                'line-width': 2},
                            'right': {
                                'visible': True,
                                'color': '#aaaaaa',
                                'line-width': 2},
                        },
                        'ticks': {
                            'x-axes': {
                                'major': {
                                    'visible': True,
                                    'position': 'bottom',
                                    'direction': 'inwards',
                                    'length': 3},
                                'minor': {
                                    'visible': False,
                                    'position': 'bottom',
                                    'direction': 'inwards'},
                            },
                            'y-axes': {
                                'major': {
                                    'visible': True,
                                    'position': 'bottom',
                                    'direction': 'inwards',
                                    'length': 3},
                                'minor': {
                                    'visible': False,
                                    'position': 'bottom',
                                    'direction': 'inwards'},
                            },
                        },
                    },
                },
            }

        if self.plot_type == 'line' and 'line-chart' in self.plot_styles:
            self.plot_styles = self.plot_styles['line-chart']
        elif self.plot_type == 'scatter' and 'scatter-chart' in self.plot_styles:
            self.plot_styles = self.plot_styles['scatter-chart']
        elif self.plot_type == 'bar' and 'bar-chart' in self.plot_styles:
            self.plot_styles = self.plot_styles['bar-chart']

        if style_dict is not None:
            self.plot_styles.update(style_dict)

    def uplot(self):
        """
        Plot xy data with matplotlib or plotly using a style dictionary.
        """
        if self.renderer == 'plotly':
            if self.plot_type == 'line':
                self.uplot_line_plotly()
        else:
            if self.plot_type == 'line':
                self.uplot_line_matplotlib()
            elif self.plot_type == 'scatter':
                self.uplot_scatter_matplotlib()
            elif self.plot_type == 'bar':
                self.uplot_bar_matplotlib()

    def uplot_line_matplotlib(self):
        """
        Plot xy data with matplotlib using a style dictionary.
        """
        if self.xcolumn is None:
            self.xcolumn = self.data.columns[0]
        if self.ycolumns is None:
            self.ycolumns = self.data.columns[1:]

        self.fig, self.ax = plt.subplots()
        for ycolumn in self.ycolumns:
            self.ax.plot(
                self.data[self.xcolumn], self.data[ycolumn])
        self.format_axes_matplotlib()

    def format_axes_matplotlib(self):
        """
        Format axes of matplotlib plot using a style dictionary.
        """

        if self.plot_styles['chart']['title']['visible']:
            self.ax.set_title(self.plot_styles['chart']['title']['text'])
            # format title
            self.ax.title.set_fontsize(
                self.plot_styles['chart']['title']['font-size'])
            self.ax.title.set_fontfamily(
                self.plot_styles['chart']['title']['font-family'])
            self.ax.title.set_fontweight(
                self.plot_styles['chart']['title']['font-weight'])
            self.ax.title.set_color(
                self.plot_styles['chart']['title']['color'])
            # set title position
            if self.plot_styles['chart']['title']['position'] == 'top':
                self.ax.title.set_position([.5, 1.05])
            elif self.plot_styles['chart']['title']['position'] == 'bottom':
                self.ax.title.set_position([.5, -.15])
            elif self.plot_styles['chart']['title']['position'] == 'left':
                self.ax.title.set_position([-.15, .5])
            elif self.plot_styles['chart']['title']['position'] == 'right':
                self.ax.title.set_position([1.05, .5])

        if self.plot_styles['chart']['xlabel']['visible']:
            self.ax.set_xlabel(self.plot_styles['chart']['xlabel']['text'])
            # format xlabel
            self.ax.xaxis.label.set_fontsize(
                self.plot_styles['chart']['xlabel']['font-size'])
            self.ax.xaxis.label.set_fontfamily(
                self.plot_styles['chart']['xlabel']['font-family'])
            self.ax.xaxis.label.set_fontweight(
                self.plot_styles['chart']['xlabel']['font-weight'])
            self.ax.xaxis.label.set_color(
                self.plot_styles['chart']['xlabel']['color'])
            # set xlabel position
            if self.plot_styles['chart']['xlabel']['position'] == 'top':
                self.ax.xaxis.label.set_position([.5, 1.05])
            elif self.plot_styles['chart']['xlabel']['position'] == 'bottom':
                self.ax.xaxis.label.set_position([.5, -.15])
                
        if self.plot_styles['chart']['ylabel']['visible']:
            self.ax.set_ylabel(self.plot_styles['chart']['ylabel']['text'])
            # format ylabel
            self.ax.yaxis.label.set_fontsize(
                self.plot_styles['chart']['ylabel']['font-size'])
            self.ax.yaxis.label.set_fontfamily(
                self.plot_styles['chart']['ylabel']['font-family'])
            self.ax.yaxis.label.set_fontweight(
                self.plot_styles['chart']['ylabel']['font-weight'])
            self.ax.yaxis.label.set_color(
                self.plot_styles['chart']['ylabel']['color'])
            # set ylabel position
            if self.plot_styles['chart']['ylabel']['position'] == 'left':
                self.ax.yaxis.label.set_position([-.15, .5])
            elif self.plot_styles['chart']['ylabel']['position'] == 'right':
                self.ax.yaxis.label.set_position([1.05, .5])

        # set background color
        self.ax.set_facecolor(
            self.plot_styles['chart']['background-color'])
        
        # set axes limits
        if self.plot_styles['axes']['limits']['xmin'] == 'min':
            self.plot_styles['axes']['limits']['xmin'] = self.data[self.xcolumn].min()
        elif self.plot_styles['axes']['limits']['xmin'] == 'max':
            self.plot_styles['axes']['limits']['xmin'] = self.data[self.xcolumn].max()
        # use regular expression to match xaxes limits offset from min or max string
        match = re.match(r'min\s*([-+])\s*(\d+)\s*%',
                         self.plot_styles['axes']['limits']['xmin'])
        if match:
            sign = match.group(1)
            offset = float(match.group(2))
            if sign == '+':
                self.plot_styles['axes']['limits']['xmin'] = (
                    self.data[self.xcolumn].min() * (1 + offset / 100))
            elif sign == '-':
                self.plot_styles['axes']['limits']['xmin'] = (
                    self.data[self.xcolumn].min() * (1 - offset / 100))

        elif self.plot_styles['axes']['limits']['xmin'] == 'min + 10 %':
            self.plot_styles['axes']['limits']['xmin'] = self.data[self.xcolumn].min() * 1.1


        ax.grid(plot_styles['grid']['show'])
        ax.set_xscale(plot_styles['xaxis']['scale'])
        ax.set_yscale(plot_styles['yaxis']['scale'])
        ax.legend(plot_styles['legend']['show'])
        ax.legend(plot_styles['legend']['location'])

    def format_lines_matplotlib(self):
        """
        Format lines of matplotlib plot using a style dictionary.
        """
        if plot_styles is None:
            plot_styles = yaml.load(open('resources/plot_styles.yaml', 'r'), Loader=yaml.FullLoader)

        for line in ax.get_lines():
            line.set_linestyle(plot_styles['line']['style'])
            line.set_linewidth(plot_styles['line']['width'])
            line.set_color(plot_styles['line']['color'])
            line.set_alpha(plot_styles['line']['alpha'])

    def format_markers_matplotlib(self):
        """
        Format markers of matplotlib plot using a style dictionary.
        """
        for line in self.ax.get_lines():
            line.set_marker(plot_styles['marker']['style'])
            line.set_markersize(plot_styles['marker']['size'])
            line.set_markerfacecolor(plot_styles['marker']['color'])
            line.set_markeredgecolor(plot_styles['marker']['color'])
            line.set_markeredgewidth(plot_styles['marker']['width'])
            line.set_alpha(plot_styles['marker']['alpha'])


    