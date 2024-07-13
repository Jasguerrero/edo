FINAL_COLUMNS_MAP = {
    "EIN": "edo_ein",
    "CITY": "city",
    "ICO": "contact",
    "NAME": "edo_name",
    "NTEE_CD": "ntee_tax_code",
    "Phone": "phone",
    "STATE": "state",
    "STREET": "street",
    "ZIP": "zip",
    "email": "email"
}


def format_final_df(final_df):
    df = final_df.loc[:, ~final_df.columns.str.contains('^Unnamed')]
    df = df.rename(columns=FINAL_COLUMNS_MAP)
    return df
