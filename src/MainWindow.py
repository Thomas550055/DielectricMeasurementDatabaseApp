import tkinter as tk
from tkinter.filedialog import askopenfile
from functools import partial
from typing import MutableMapping

import pandas as pd

from CSVReader import create_data_frame_with
from Measurement import Measurement
from MenuFrame import MenuFrame
from Database import Database
from tkinter import messagebox
from MeasurementFrame import MeasurementFrame
from FrequencyFrame import FrequencyFrame


class MainWindow:
    def __init__(self):
        self.database = Database()
        self.window = self.ui_configure_window()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        # create empty measurement's dictionary
        # this contains instances of measurements by key -> value
        self.measurements_dict: MutableMapping[str,
                                               Measurement] = self.database.db_get_measurements()
        self.selected_material = tk.StringVar(self.window)
        self.selected_material.set("Select measurement...")
        if len(self.measurements_dict) > 0:
            self.selected_material.set(list(self.measurements_dict.keys())[0])

        self.frequencies: [
            float] = self.database.db_get_all_measured_frequencies()
        self.selected_frequency = tk.DoubleVar(self.window)
        self.selected_frequency.set(1.0)

        self.content_frame = type('obj', (object,), {"frame": tk.Frame(
            self.window, bd=2, bg="whitesmoke", height=900, width=1680)})
        self.menu = None
        self.ui_draw_menu()

        self.window.mainloop()

    def ui_configure_window(self):
        window = tk.Tk()
        window.title('Dielectric measurement database APP')
        window.geometry("1680x950")

        window.rowconfigure(0, minsize=50, weight=1)
        window.rowconfigure(1, minsize=900, weight=1)
        window.columnconfigure(0, minsize=1680, weight=1)
        return window

    def ui_draw_menu(self):
        if self.menu is not None:
            self.menu.frame.destroy()

        menu = MenuFrame(self.window)
        menu.ui_draw_read_csv_button(self.read_csv)
        menu.ui_draw_material_dropdown(
            self.measurements_dict, self.selected_material)

        menu.ui_draw_display_measurement_button(self.ui_draw_measurement_frame)

        menu.ui_draw_logo()
        menu.ui_draw_frequency_dropdown(
            self.frequencies, self.selected_frequency)
        menu.ui_draw_frequency_button(self.ui_draw_frequency_frame)

        self.menu = menu

    def ui_draw_measurement_frame(self):
        if len(self.measurements_dict) == 0:
            return

        if self.content_frame is not None:
            self.content_frame.frame.destroy()

        measurement = self.measurements_dict[self.selected_material.get()]
        self.content_frame = MeasurementFrame(self.window, measurement)

    def ui_draw_frequency_frame(self):
        if self.content_frame is not None:
            self.content_frame.frame.destroy()
        frequency_comparison_df = self.get_frequency_df_at(
            self.selected_frequency.get())
        self.content_frame = FrequencyFrame(
            self.window, frequency_comparison_df)

    # Open CSV and initialize dataframe
    def read_csv(self):
        # Chose File to open
        file = askopenfile(mode='r', filetypes=[("csv files", "*.csv")])
        if not file:
            print('Unable to access file')
            return None
        # print(file.name)

        measurements_df = create_data_frame_with('MEASUREMENTS', file.name)
        fds_results_df = create_data_frame_with('FDS RESULTS', file.name)

        # drop first two unnecessary rows
        measurements_df = measurements_df.drop([0, 1], axis=0)

        # create new measurement class
        measurement = Measurement(measurements_df, fds_results_df)

        data = pd.DataFrame()
        try:
            data = self.database.db_get_measurement_by(measurement.get_name())
        except:
            print("")

        if data.size > 0:
            tk.messagebox.showerror(
                title=None, message="Measurement already existing!")
            return

        self.database.db_store_measurement(measurement)
        self.refresh_data()
        self.selected_material.set(measurement.get_name())
        self.ui_draw_menu()

    def get_frequency_df_at(self, frequency: float) -> pd.DataFrame:
        measurement_frequency_frames = []
        for key, value in self.measurements_dict.items():
            measurement_frequency_frames.append(
                value.get_frequency_row(frequency)
            )

        merged_frame = pd.concat(measurement_frequency_frames)
        merged_frame = merged_frame.dropna()

        return merged_frame

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.destroy()

    def refresh_data(self):
        self.measurements_dict = self.database.db_get_measurements()
        self.frequencies = self.database.db_get_all_measured_frequencies()

        has_measurements = len(self.measurements_dict) > 0
        if has_measurements:
            self.selected_material.set(list(self.measurements_dict.keys())[0])
