import tkinter as tk
import pandas as pd
from pandastable import Table


class FrequencyFrame:
    def __init__(self, main_window: tk.Tk, frequency_comparison_df: pd.DataFrame):
        self.frequency_comparison_df = frequency_comparison_df
        self.frame = tk.Frame(main_window, bd=2, height=900,
                              width=1680, background="whitesmoke")
        self.frame.grid(row=1, column=0, sticky='nsew')
        print(frequency_comparison_df)
        self.ui_draw_frequencies()

    def ui_draw_frequencies(self):
        f = tk.Frame(self.frame)
        f.pack(fill=tk.BOTH, expand=True)
        pt = Table(f, dataframe=self.frequency_comparison_df,
                   showtoolbar=True, showstatusbar=True)
        pt.show()
