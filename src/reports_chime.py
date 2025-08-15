import pandas as pd
from decimal import Decimal
from helpers import create_directory, write_totals_to_csv



def get_chime_transfers_report(df, account_type, direction, source_or_destination, start_date=None, end_date=None):
    transaction_type = "Transfer"
    directory = create_directory("Chime", account_type.capitalize(), f"{transaction_type}s")
    csv_file = (f"{directory}/Chime {account_type.capitalize()} Account {transaction_type}s {direction.capitalize()} {source_or_destination}.csv")
    df = df[(df["Description"].str.contains(f'{transaction_type} {direction} {source_or_destination}')) & (df["Type"] == transaction_type)]
    if (start_date and end_date):
        csv_file = csv_file.replace(".csv", f" Between {start_date} and {end_date}.csv")
        df = df[(df["Transaction Date"] >= start_date) & (df["Transaction Date"] <= end_date)]
    elif (start_date and not end_date):
        csv_file = csv_file.replace(".csv", f" After {start_date}.csv")
        df = df[(df["Transaction Date"] >= start_date)]
    elif (not start_date and end_date):
        csv_file = csv_file.replace(".csv", f" Before {end_date}.csv")
        df = df[(df["Transaction Date"] <= end_date)]
    df = df[["Transaction Date", "Description", "Type", "Amount"]]
    df["Amount"] = pd.to_numeric(df["Amount"]).apply(lambda x: Decimal(f"{x:.2f}")).abs()
    df = df.sort_values(by="Transaction Date", ascending=False)
    print(f"Chime {transaction_type}s {direction} {source_or_destination}")
    print(df)
    count = len(df)
    count_total = [f"Total Number of {transaction_type}s", count]
    print(f"{count_total[0]} {direction} {source_or_destination} = {count}")
    amount = df["Amount"].sum()
    amount_total = [f"Total Amount of {transaction_type}s", amount] 
    print(f"{amount_total[0]} {direction} {source_or_destination} = {amount}")
    print(f"Report Output File: {csv_file}")
    print()
    df.to_csv(csv_file, index=False)
    write_totals_to_csv(csv_file, count_total, amount_total)
    return df

def get_chime_purchases_report(df, account_type, purchase_description, start_date=None, end_date=None):
    transaction_type = "Purchase"
    directory = create_directory("Chime", account_type.capitalize(), f"{transaction_type}s")
    csv_file = (f"{directory}/Chime {account_type.capitalize()} Account {transaction_type}s Made at {purchase_description}.csv")
    df = df[(df["Description"].str.contains(purchase_description)) & (df["Type"] == transaction_type)]
    if (start_date and end_date):
        csv_file = csv_file.replace(".csv", f" Between {start_date} and {end_date}.csv")
        df = df[(df["Transaction Date"] >= start_date) & (df["Transaction Date"] <= end_date)]
    elif (start_date and not end_date):
        csv_file = csv_file.replace(".csv", f" After {start_date}.csv")
        df = df[(df["Transaction Date"] >= start_date)]
    elif (not start_date and end_date):
        csv_file = csv_file.replace(".csv", f" Before {end_date}.csv")
        df = df[(df["Transaction Date"] <= end_date)]
    df = df[["Transaction Date", "Description", "Type", "Amount"]]
    df["Amount"] = pd.to_numeric(df["Amount"]).apply(lambda x: Decimal(f"{x:.2f}")).abs()
    df = df.sort_values(by="Transaction Date", ascending=False)
    print(f"Chime {account_type} Account {transaction_type}s Made at {purchase_description}")
    print(df)
    count = len(df)
    count_total = [f"Total Number of {transaction_type}s", count]
    print(f"{count_total[0]} = {count}")
    amount = df["Amount"].sum()
    amount_total = [f"Total Amount of {transaction_type}s", amount] 
    print(f"{amount_total[0]} = {amount}")
    print(f"Report Output File: {csv_file}")
    print()
    df.to_csv(csv_file, index=False)
    write_totals_to_csv(csv_file, count_total, amount_total)
    return df


def main():
    df_chime_checking_transactions = pd.read_csv("data/processed/Chime/Checking/Combined/Transactions/Chime Checking Account Transactions.csv")
    df_chime_credit_transactions = pd.read_csv("data/processed/Chime/Credit/Combined/Transactions/Chime Credit Account Transactions.csv")

    df_chime_transfers_report = get_chime_transfers_report(df_chime_checking_transactions, "Checking", "to", "source_or_destination")
    df_chime_transfers_report = get_chime_transfers_report(df_chime_checking_transactions, "checking", "from", "source_or_destination")
    df_chime_transfers_report = get_chime_transfers_report(df_chime_checking_transactions, "Checking", "To", "source_or_destination", "2023-01-03", "2023-01-05")
    df_chime_transfers_report = get_chime_transfers_report(df_chime_checking_transactions, "Checking", "to", "source_or_destination", "2023-01-03")
    df_chime_transfers_report = get_chime_transfers_report(df_chime_checking_transactions, "Checking", "to", "source_or_destination", end_date="2023-01-03")

    df_chime_checking_purchases_report = get_chime_purchases_report(df_chime_checking_transactions, "Checking", "purchase_description")
    df_chime_checking_purchases_report = get_chime_purchases_report(df_chime_checking_transactions, "Checking", "purchase_description", "2022-10-31", "2022-12-20")
    df_chime_checking_purchases_report = get_chime_purchases_report(df_chime_checking_transactions, "Checking", "purchase_description", "2022-10-31")
    df_chime_checking_purchases_report = get_chime_purchases_report(df_chime_checking_transactions, "Checking", "purchase_description",end_date="2023-01-27")

    df_chime_checking_purchases_report = get_chime_purchases_report(df_chime_credit_transactions, "Credit", "purchase_description")
    df_chime_checking_purchases_report = get_chime_purchases_report(df_chime_credit_transactions, "credit", "purchase_description", "2022-10-31", "2022-12-20")
    df_chime_checking_purchases_report = get_chime_purchases_report(df_chime_credit_transactions, "Credit", "purchase_description", "2022-10-31")
    df_chime_credit_purchases_report = get_chime_purchases_report(df_chime_credit_transactions, "Credit", "purchase_description", end_date="2023-01-27")


if __name__ == '__main__':
    main()