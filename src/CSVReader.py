import pandas as pd
import csv

# Read CSV-File into dataframe
def create_data_frame_with(measurement, path_to_csv):
    with open(path_to_csv, 'r', newline='', encoding='utf8') as csvfile:
        raw_csv = csv.reader(csvfile, delimiter=';')

        read_index = -1
        data_array = []
        for i, row in enumerate(raw_csv):
            is_reading_data = len(data_array) != 0
            is_empty_row = len(row) == 0

            key_word = '[' + str(measurement) + ']'
            is_at_key_word = not is_reading_data and not is_empty_row and row[0] == key_word

            if is_at_key_word:
                # init readIndex
                read_index = i + 1

            is_at_end_of_data = is_reading_data and is_empty_row
            if is_at_end_of_data:
                break

            if read_index == i:
                row = [value.replace(',', '.') for value in row]
                row = [value.strip() for value in row]
                data_array.append(row)
                read_index = read_index + 1

    headers = data_array[:1][0]
    # print(headers)
    data = data_array[1:]

    return pd.DataFrame(data=data, columns=headers)
