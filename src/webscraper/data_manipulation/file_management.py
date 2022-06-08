import pandas as pd


def data_dict_to_pandas(generator_json):
    obj = []
    for each in generator_json:
        df = pd.DataFrame.from_dict(each.items(), orient="columns")
        df = df.rename(columns={0: "data", 1: "data_value"})
        df = df.set_index("data").T
        obj.append(df)
    return pd.concat(obj, ignore_index=True)


def read_excel_get_url_series(excel_file):
    df = pd.read_excel(excel_file)
    return df["url"]


def output_excel_file(file_name, data_frame: pd.DataFrame):
    data_frame.to_excel(f"{file_name}", index=False)
    return None
