import pandas as pd
from constants import rename_columns


def map_role(row):
    if row['role'] == 1:
        return "Developer / Software Engineer"
    elif row['role'] == 2:
        return "QA / Test Engineer"
    elif row['role'] == 3:
        return "Researcher / Academic"
    elif row['role'] == 4:
        return row['text_role_other']
    else:
        return row['role']  # keep original value if not 1–4


def map_familiarity(row):
    if row['bva_familiarity'] == 1:
        return "Not at all familiar"
    elif row['bva_familiarity'] == 2:
        return "Somewhat familiar"
    elif row['bva_familiarity'] == 3:
        return "Quite familiar"
    elif row['bva_familiarity'] == 4:
        return "Expert"
    else:
        return row['bva_familiarity']


def preprocess_raw_data(input_filename, output_filename):
    # Read the Excel file
    df = pd.read_excel(input_filename)

    # rename the columns to shorter names
    df = df.rename(columns=rename_columns)
    # drop the column name because it does not contain any information
    df = df.drop(columns="name")
    # add a column to sort out incomplete answers later if needed
    df['completed'] = df['time_completed'].apply(lambda x: 1 if pd.notna(x) and str(x).strip() != '' else 0)
    # drop test data (and one record without any answers)
    df = df[~df['id'].isin([411488791, 411595601])]
    # convert numeric values to text
    df['role'] = df.apply(map_role, axis=1)
    df['bva_familiarity'] = df.apply(map_familiarity, axis=1)

    df.to_csv(output_filename, index=False)


