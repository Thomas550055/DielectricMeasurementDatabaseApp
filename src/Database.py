import sqlite3
from typing import MutableMapping
import pandas as pd
from Measurement import Measurement


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('Materialien.db')
        self.measurement_headers = [
            'ID', 'Name', 'Temperature [°C]', 'Humidity [%]', 'Material type',
            'Serial number', 'PDC output voltage (DC) [V]', 'FDS output voltage (AC) [V]',
            'c0', 'Sample thickness [m]', 'Measurement started'
        ]
        self.fds_result_headers = [
            'ID', 'measurement_id', 'Frequency [Hz]', 'Tanδ', "εr'", "εr''", '|Z| [Ω]', 'Phase of Z [°]', '|Y| [S]',
            'Phase of Y [°]', 'Cp [F]', 'Rp [Ω]', "c' [F]", "c'' [F]", 'R [Ω]', 'X [Ω]'
        ]

    def db_store_measurement(self, measurement: Measurement):
        self.db_create_measurements_table()
        self.db_create_fds_results_table()
        name_of_measurement = measurement.get_name()
        self.db_get_measurement_by(name_of_measurement)
        # drop id because we want to autogenerate
        material = measurement.material.drop(columns=['ID'])
        material.to_sql("Measurements", self.connection,
                        index=False, if_exists='append')

        measurement_df = self.db_get_measurement_by(measurement.get_name())

        database_id = measurement_df.iat[0, 0]
        fds_results = measurement.fds_results

        # fds_results = fds_results.drop(columns=['Frequency [Hz]'])
        # print(frequencies)
        # fds_results['Frequency [Hz]'] = frequencies

        fds_results = fds_results.drop(columns=['ID'])
        fds_results.insert(0, 'measurement_id', database_id)

        fds_results.to_sql("FDSResults", self.connection,
                           index=False, if_exists='append')

        # Commit changes
        self.connection.commit()

    def db_get_all_measured_frequencies(self) -> [float]:
        c = self.connection.cursor()
        try:
            result = c.execute(
                'SELECT DISTINCT "Frequency [Hz]" FROM FDSResults'
            )
        except:
            return [0.0]

        database_frequencies = []
        for row in result:
            database_frequencies.append(row[0])
        c.close()
        return database_frequencies

    def db_get_all_measurements(self) -> pd.DataFrame:
        c = self.connection.cursor()
        c.execute(
            "SELECT * FROM Measurements"
        )
        df = pd.DataFrame(c.fetchall(), columns=self.measurement_headers)
        c.close()
        return df

    def db_get_measurement_by(self, name_of_measurement: str) -> pd.DataFrame:
        c = self.connection.cursor()
        c.execute(
            "SELECT * FROM Measurements WHERE Name = " + '"' + name_of_measurement + '"'
        )
        measurements_df = pd.DataFrame(
            c.fetchall(), columns=self.measurement_headers)
        c.close()
        return measurements_df

    def db_get_fds_results_of(self, measurement_id: int) -> pd.DataFrame:
        c = self.connection.cursor()
        c.execute(
            "SELECT * FROM FDSResults WHERE measurement_id = " +
            str(measurement_id)
        )
        fds_df = pd.DataFrame(c.fetchall(), columns=self.fds_result_headers)
        c.close()
        return fds_df

    def db_get_measurements(self) -> MutableMapping[str, Measurement]:
        measurements: MutableMapping[str, Measurement] = {}
        db_measurements: pd.DataFrame = pd.DataFrame()
        try:
            db_measurements = self.db_get_all_measurements()
        except:
            print("Unable to fetch measurements")
            return measurements

        for index, row in db_measurements.iterrows():
            fds_results = self.db_get_fds_results_of(row['ID'])
            measurement = Measurement(pd.DataFrame([row]), fds_results)
            measurements[measurement.get_name()] = measurement

        return measurements

    def db_create_measurements_table(self):
        c = self.connection.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS Measurements (
            ID INTEGER PRIMARY KEY        AUTOINCREMENT,
            Name                          TEXT UNIQUE,
            "Temperature [°C]"            REAL,
            "Humidity [%]"                REAL,
            "Material type"               TEXT,
            "Serial number"               TEXT,
            "PDC output voltage (DC) [V]" TEXT,
            "FDS output voltage (AC) [V]" TEXT,
            c0                            REAL,
            "Sample thickness [m]"        REAL,
            "Measurement started"         TEXT
            );""")
        c.close()

    def db_create_fds_results_table(self):
        c = self.connection.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS FDSResults (
            ID INTEGER PRIMARY KEY        AUTOINCREMENT,
            measurement_id INTEGER,
            "Frequency [Hz]" REAL,
            Tanδ             REAL,
            "εr'"            REAL,
            "εr''"           REAL,
            "|Z| [Ω]"        REAL,
            "Phase of Z [°]" REAL,
            "|Y| [S]"        REAL,
            "Phase of Y [°]" TEXT,
            "Cp [F]"         REAL,
            "Rp [Ω]"         REAL,
            "c' [F]"         REAL,
            "c'' [F]"        REAL,
            "R [Ω]"          REAL,
            "X [Ω]"          REAL,
            FOREIGN KEY(measurement_id) REFERENCES Measurements(id)
            );""")
        c.close()

    # def delete(self):
        # # Create a database or connect to existing one
        # c = self.connection.cursor()
        #
        # c.execute("DELETE from Materialien WHERE oid= " + )
        #
        # self.connection.commit()
        # self.connection.close()