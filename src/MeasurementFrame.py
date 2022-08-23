import pandas as pd
from pandastable import Table
import tkinter as tk
from turtle import color
import matplotlib
import matplotlib.pyplot as plt
from typing import Dict, MutableMapping
from Measurement import Measurement
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class MeasurementFrame:
    def __init__(self, main_window: tk.Tk, measurement: Measurement):
        self.measurement = measurement
        self.frame = tk.Frame(main_window, bd=2, height=900,
                              width=1680, background="whitesmoke")
        self.frame.grid(row=1, column=0, sticky='nsew')
        self.ui_draw_measurement_details()

    def ui_draw_measurement_details(self):
        fds_results = self.measurement.fds_results

        self.ui_draw_permittitvity_plot(fds_results)
        self.ui_draw_fds_results_table(fds_results)

    def ui_draw_permittitvity_plot(self, fds_results: pd.DataFrame):
        color1 = 'tab:red'
        color2 = 'darkmagenta'
        fig, ax = plt.subplots()
        ax.set_xlabel('Frequency [Hz]', fontsize=14)
        ax.set_ylabel("εr'", color=color1, fontsize=16)
        ax.plot(fds_results['Frequency [Hz]'], fds_results["εr'"],
                color=color1, linewidth=2, )
        ax.set_xscale('log')
        ax.set_xticks([0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000])
        ax.get_xaxis().set_major_formatter(
            matplotlib.ticker.LogFormatterSciNotation())
        ax.grid()
        # define second y-axis that shares x-axis with current plot
        ax2 = ax.twinx()
        ax2.plot(fds_results['Frequency [Hz]'], fds_results["εr''"],
                 color=color2, linewidth=2, )
        ax2.set_ylabel("εr''", color=color2, fontsize=16)
        ax2.grid()

        plot1 = FigureCanvasTkAgg(fig.get_figure(), self.frame)
        plot1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def ui_draw_fds_results_table(self, fds_results: pd.DataFrame):
        f = tk.Frame(self.frame)
        f.pack(fill=tk.BOTH, expand=True)
        pt = Table(f, dataframe=fds_results,
                   showtoolbar=False, showstatusbar=True)
        pt.show()
