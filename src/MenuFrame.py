import tkinter as tk
from typing import MutableMapping

from PIL import ImageTk, Image

from Measurement import Measurement


class MenuFrame:
    def __init__(self, main_window: tk.Tk):
        self.frame = tk.Frame(main_window, bd=0, height=50,
                              width=1680, bg="whitesmoke", relief=tk.SUNKEN)
        self.configure_menu_grid()
        self.frame.grid(row=0, column=0, sticky='nsew')

    def configure_menu_grid(self):
        self.frame.columnconfigure(0, weight=1, minsize=280)
        self.frame.columnconfigure(1, weight=1, minsize=280)
        self.frame.columnconfigure(2, weight=1, minsize=280)
        self.frame.columnconfigure(3, weight=1, minsize=280)
        self.frame.columnconfigure(4, weight=1, minsize=280)
        self.frame.columnconfigure(5, weight=1, minsize=280)
        self.frame.rowconfigure(0, weight=1, minsize=56)

    def ui_draw_read_csv_button(self, read_csv_function):
        # Create Add-CSV-Data Button
        add_csv_button = tk.Button(
            self.frame,
            height=2,
            text="Add measurement",
            command=read_csv_function,
        )
        add_csv_button.grid(row=0, column=0, sticky="ew", padx=10)

    def ui_draw_material_dropdown(self, measurements_dict: MutableMapping[str, Measurement], selected_material):
        measurements = ["loading"]
        if len(measurements_dict) > 0:
            measurements = measurements_dict

        opt = tk.OptionMenu(
            self.frame, selected_material,
            *measurements
        )
        opt.grid(row=0, column=1, sticky="ew", padx=10)

    def ui_draw_display_measurement_button(self, display_data_function):
        add_csv_button = tk.Button(
            self.frame,
            height=2,
            text="Show measurement",
            command=display_data_function,
        )
        add_csv_button.grid(row=0, column=2, sticky="ew", padx=10)

    def ui_draw_logo(self):
        print('No Logo selected')
        # canvas = tk.Canvas(self.frame, width=280, height=56, background="white")
        # canvas.grid(row=0, column=3, pady=0, sticky="ew", padx=0)
        # img = ImageTk.PhotoImage(Image.open(""))
        # canvas.create_image(200, 56, anchor=tk.CENTER, image=img)

    def ui_draw_frequency_dropdown(self, frequencies, selected_frequency):
        opt = tk.OptionMenu(
            self.frame, selected_frequency,
            *frequencies
        )
        opt.grid(row=0, column=4, sticky="ew", padx=10)

    def ui_draw_frequency_button(self, ui_draw_frequencies):
        add_csv_button = tk.Button(
            self.frame,
            height=2,
            text="Frequency comparison [Hz]",
            command=ui_draw_frequencies
        )
        add_csv_button.grid(row=0, column=5, sticky="ew", padx=10)
