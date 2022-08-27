# this is the key datastructure for a single measurement object
# one measurement always contains:
# * material specifications dataframe (just first row is important here)
# * a fds results dataframe
#
from dataclasses import dataclass
import pandas as pd

# headers measurement [
#   'ID', 'Name', 'Temperature [°C]', 'Humidity [%]', 'Material type',
#   'Serial number', 'PDC output voltage (DC) [V]', 'FDS output voltage (AC) [V]',
#   'c0', 'Sample thickness [m]', 'Measurement started'
# ]
# headers fds results [
#   'ID', 'Frequency [Hz]', 'Tanδ', "εr'", "εr''", '|Z| [Ω]', 'Phase of Z [°]', '|Y| [S]',
#   'Phase of Y [°]', 'Cp [F]', 'Rp [Ω]', "c' [F]", "c'' [F]", 'R [Ω]', 'X [Ω]'
# ]

# Define "Measurement"-class (datastructure)
@dataclass(order=True, frozen=True)
class Measurement:
    material: pd.DataFrame
    fds_results: pd.DataFrame

    def __init__(self, measurements_df: pd.DataFrame, fds_results_df: pd.DataFrame):
        measurements_df = measurements_df.astype({
            'ID': int,
            'Name': str,
            'Temperature [°C]': float,
            'Humidity [%]': float,
            'Material type': str,
            'Serial number': str,
            # TODO: handle optional values
            'PDC output voltage (DC) [V]': str,
            'FDS output voltage (AC) [V]': str,
            'c0': float,
            'Sample thickness [m]': float,
            'Measurement started': str,
        })
        headers_fds_df = fds_results_df.head()
        # print(fds_results_df)
        fds_results_df = fds_results_df.astype({
            'ID': int,
            'Frequency [Hz]': float,
            'Tanδ': float,
            "εr'": float,
            "εr''": float,
            '|Z| [Ω]': float,
            'Phase of Z [°]': float,
            '|Y| [S]': float,
            'Cp [F]': float,
            'Rp [Ω]': float,
            "c' [F]": float,
            "c'' [F]": float,
            'R [Ω]': float,
            'X [Ω]': float
        })
        object.__setattr__(self, 'material', measurements_df)
        object.__setattr__(self, 'fds_results', fds_results_df)

    def get_name(self):
        if self.material.empty:
            return

        # name is at first row second column in material dataframe
        return self.material.iat[0, 1]

    def get_serial_number(self):
        if self.material.empty:
            return

        # name is at first row sixth column in material dataframe
        return self.material.iat[0, 5]

    def get_frequency_row(self, frequency: float) -> pd.DataFrame:
        fds_results_at_frequency = self.get_fds_row_by(frequency)
        # fds_results_at_frequency = fds_results_at_frequency.drop(
        #     columns=['measurement_id'])
        fds_results_at_frequency = fds_results_at_frequency.drop(columns=[
                                                                 'ID'])
        fds_results_at_frequency.insert(0, "Name", [self.get_name()])
        return fds_results_at_frequency

    def get_fds_row_by(self, frequency: float) -> pd.DataFrame:
        return self.fds_results.loc[self.fds_results['Frequency [Hz]'] == frequency]
