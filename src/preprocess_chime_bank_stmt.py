import csv
import os
import pandas as pd
from decimal import Decimal



read = 'r'
write = 'w'
read_write = "rw"
write_all = "wa"
read_write_all = "rwa"

bank = "Chime"
checking = "checking"
credit_builder_card = "credit builder card"
credit_builder_secured = "credit builder secured"
summary = "summary"
transactions = "transactions"

checking_transaction_column_names = ["Transaction Date", "Description", "Type", "Amount", "Net Amount", "Settlement Date"]
credit_builder_transaction_column_names = ["Transaction Date", "Description", "Type", "Amount", "Settlement Date"]
checking_summary_column_names = ["Statement Period", "Beginning Balance", "Deposits", "ATM Withdrawals", "Purchases", "Adjustments", "Transfers", "Round Up Transfers", "Fees", "SpotMe Tips", "Ending Balance"]
credit_builder_summary_column_names = ["Statement Period", "Last Month's Balance", "Payments/Credits", "New Spending", "Fees", "New Balance", "Payment Due Date", "Total Due"]
credit_builder_secured_summary_column_names = ["Statement Period", "Beginning Balance", "Deposits", "Transfers", "Ending Balance"]

months = {"01": ['1', "01", "jan", "january"],
               "02": ['2', "02", "feb", "february"],
               "03": ['3', "03", "mar", "march"],
               "04": ['4', "04", "apr", "april"],
               "05": ['5', "05", "may"],
               "06": ['6', "06", "jun", "june"],
               "07": ['7', "07", "jul", "july"],
               "08": ['8', "08", "aug", "august"],
               "09": ['9', "09", "sep", "sept", "september"],
               "10": ["10", "oct", "october"],
               "11": ["11", "nov", "november"],
               "12": ["12", "dec", "december"]}


def rename_columns(df, account, statement):
    if account.lower() == checking:
        if statement.lower() == transactions: 
            df.columns = checking_transaction_column_names
        elif statement.lower() == summary:
            df.columns = checking_summary_column_names
    elif account.lower() == credit_builder_card:
        if statement.lower() == transactions:
            df.columns = credit_builder_transaction_column_names
        elif statement.lower() == summary:
            df.columns = credit_builder_summary_column_names
    elif account.lower() == credit_builder_secured:
        if statement.lower() == transactions:
            df.columns = credit_builder_transaction_column_names
        elif statement.lower() == summary:
            df.columns = credit_builder_secured_summary_column_names
    return df

def create_dataframe(csv_file):
    with open(csv_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        row_1 = next(reader)
        row_2 = next(reader)
        row_1.append(row_2[0])
        row_dict = {row_1[0]: row_1[1]}
        for row in reader:
            row_dict = {**row_dict, row[0]: row[1]}
    df = pd.DataFrame([row_dict])
    return df

def correct_tabula_data_extraction_errors(df):
    for i in range(len(df)):
        if df.isnull().iloc[i, 0]:
            df.iloc[i - 1, 1] = df.iloc[i - 1, 1] + " " + df.iloc[i, 1]
    df = df.dropna(subset=df.columns[0])
    return df

def format_data(df, account, statement):
    if statement.lower() == summary:
        for i in range(len(df.columns)):
            if (i == 0) or (i == 6 and account.lower() == credit_builder_card):
                df[df.columns[i]] = df[df.columns[i]].astype('string')
            else:
                df[df.columns[i]] = pd.to_numeric(df[df.columns[i]].str.replace('$', '').str.replace(',','')).apply(lambda x: Decimal(f"{x:.2f}"))
    if statement.lower() == transactions:
        df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], format='%m/%d/%Y')
        df["Description"] = df["Description"].astype("string")
        df["Type"] = df["Type"].astype("string")
        df["Amount"] = pd.to_numeric(df["Amount"].str.replace('$', '', regex=False).str.replace(',', '')).apply(lambda x: Decimal(f"{x:.2f}"))
        df["Settlement Date"] = pd.to_datetime(df["Settlement Date"], format='%m/%d/%Y')
        if account.lower() == checking:
            df["Net Amount"] = pd.to_numeric(df["Net Amount"].str.replace('$', '', regex=False).str.replace(',', '')).apply(lambda x: Decimal(f"{x:.2f}"))
    return df

def save_file(df, directory, file):
    directory = directory.replace("raw", "processed")
    os.makedirs(directory, exist_ok=True)
    if file.startswith("tabula-"):
        file = file.replace("tabula-", '')
    csv_file = os.path.join(directory, file)
    df.to_csv(csv_file, index=False)
    print(f"CSV Output File: {csv_file}\n")

def save_combined_file(df, bank, account, statement):
    directory = f"data/processed/{bank}/{account.title()}/Combined/{statement.title()}"
    os.makedirs(directory, exist_ok=True)
    file = (f"{bank} {account.title()} Account {statement.title()}.csv")
    csv_file = os.path.join(directory, file)
    df.to_csv(csv_file, index=False)
    print(f"Combined CSV Output File: {csv_file}\n")

def preprocess(csv_file, account, statement):
    if statement.lower() == summary:
        df = create_dataframe(csv_file)
    else:
        df = pd.read_csv(csv_file)
        df = df.infer_objects()
        df = correct_tabula_data_extraction_errors(df)
    df = rename_columns(df, account, statement)
    df = format_data(df, account, statement)
    return df

def preprocess_statement(year, month, account, statement, option):
    for key, value_list in months.items():
        if str(month).lower() in value_list:
            csv_directory = (f"data/raw/{bank}/{account.title()}/{year}/{statement.title()}")
            file = (f"tabula-{year}-{key}.csv")
            csv_file = os.path.join(csv_directory, file)
            break
    print(f"Input File: {csv_file}\n")
    df = preprocess(csv_file, account, statement)
    if option.lower() == write or option.lower() == read_write:
        save_file(df, csv_directory, file)
    if option.lower() == read or option.lower() == read_write:
        return df
        
def preprocess_statements(start_year, end_year, account, statement, option):
    dataframes = []
    for i in range(start_year, end_year + 1):
        csv_directory = (f"data/raw/{bank}/{account.title()}/{i}/{statement.title()}")
        csv_files = [f for f in os.listdir(csv_directory) if f.endswith(".csv")]
        csv_files.sort()
        for file in csv_files:
            csv_file = os.path.join(csv_directory, file)
            print(f"CSV Input File: {csv_file}")
            df = preprocess(csv_file, account, statement)
            if option.lower() == write_all or option.lower() == read_write_all:
                save_file(df, csv_directory, file)
            dataframes.append(df)
    df = pd.concat(dataframes, ignore_index=True)
    if option.lower() == write or option.lower() == read_write or option.lower() == write_all or option.lower() == read_write_all:
        save_combined_file(df, bank, account, statement)
    if option.lower() == read or option.lower() == read_write or option.lower() == read_write_all:
        print()
        return df


def main():
    df = preprocess_statement(2024, "september", "checking", "summary", 'r')
    preprocess_statement(2024, "sept", "checking", "transactions", 'w')
    df = preprocess_statement(2024, "sep", "credit builder card", "summary", "rw")
    df = preprocess_statement(2024, 9, "credit builder card", "transactions", "rw")
    df = preprocess_statement(2024, "09", "credit builder secured", "summary", "rw")
    df = preprocess_statement(2024, "09", "credit builder secured", "transactions", "rw")
    

    df = preprocess_statements(2021, 2025, "checking", "summary", 'r')
    preprocess_statements(2021, 2025, "checking", "transactions", 'w')
    df = preprocess_statements(2021, 2025, "credit builder card", "summary", "rw")
    preprocess_statements(2021, 2025, "credit builder card", "transactions", "wa")
    df = preprocess_statements(2021, 2025, "credit builder secured", "summary", "rwa")
    df = preprocess_statements(2021, 2025, "credit builder secured", "transactions", "rwa")


if __name__ == '__main__':
    main()
