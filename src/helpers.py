import csv
import os

def create_directory(bank, account_type, report_type):
    directory = (f"reports/csv/{bank}/{account_type}/{report_type}")
    os.makedirs(directory, exist_ok=True)
    return directory

def write_to_csv(csv_file, data):
    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

def write_totals_to_csv(csv_file, count_total, amount_total):
    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([])
        writer.writerow(count_total)
        writer.writerow(amount_total)