# Financial Reports
A collection of Python files for preprocessing financial bank and billing statements, facilitate bank and billing statement transaction queries, and generate reports of historical financial transactions.

## Purpose
The intended purpose of this project is to assist in gathering evidence of transactions that occured during marriage. However, it can be used to gather such data for any specified peried of time, for any reason.

## Current Bank Account Statements and Sections
### Preprocesing
* Chime Bank Statments
    * Checking Account
        * Summary
        * Transactions
    * Credit Builder Card 
        * Summary (Includes: Your Payment)
        * Transactions
    * Credit Builder Secured
        * Summary
        * Transactions

### Report Generation

## Features
* Correction of errors that arise when using the [Tabula Application](https://tabula.technology/) to extract and convert pdf data to csv format
* Preprocess a single csv file or a collection of csv files
* Combine a collection of csv files into a single csv file
* Read preprocesed csv files
* Save preprocessed csv files by writing to a new csv file

## Documentation and Instructions
### Directory-File-Structure
#### Input Directory-File-Structure
CSV files shall be placed in the "data/raw" folder using the following hierachy:

    data/                       data/
      raw/                        raw/
        Bank Name/                  Chime/
          Statement Year/             2025/
            Account/                    Checking/
              Statement Portion/          Summary/
                Input CSV Files             tabula-2025-01-25.csv

#### Output Directory-File-Structure
The output directory will follow the same structure as the input directory, however "raw" will be replaced with "prepocessed":

    data/
        preprocessed/

#### Single or Multiple File Outputs
Individually preprocessed file ouputs will be stored in the folder respecful to the input directory format:

    data/                       data/
      preprocessed/               preprocessed/
        Bank Name/                  Chime/
          Statement Year/             2025/
            Account/                    Checking/
              Statement Portion/          Summary/
                Output CSV Files            tabula-2025-01-25.csv

#### Combined File Outputs
Combined preprocessed file oupts will be stored in the combined folder: 

    data/                       data/
      prepocessed/                preprocessed/
        Bank Name/                  Chime/
          Combined/                   2025/
            Combined CSV File           combined_chime_transactions.csv

### Preprocessing - Options
Using the 'r' or 'w' options with preprocess_statements() will combine all csv files into a single output.

Using the 'r' or 'w' options with preprocess_statment() will produce single output of the csv file.

#### read only ('r')
* returns the preprocessed csv file/files as a single dataframe
#### write only ('w')
* writes the preprocessed csv file/files to a single csv file
#### read write ('rw')
* returns the preprocessed file/files and writes the preprocessed file/files as a csv file
#### write all files ('wa') - only for preprocess_statements()
* saves all preprocesed files as individual csv files
* saves the combined preprocessed files as a single csv file
#### read write all files ('rwa') - only for preprocess_statements()
* returns the preprocessed files combined into a single dataframe
* saves all preprocesed files as individual csv files
* saves the combined preprocessed files as a single csv file


### Single File Preprocessing Example
#### preprocess_statement(year, month, account, statement, option)
    preprocess_statement(2024, "september", "checking", "summary", 'r')
    preprocess_statement(2024, "sept", "checking", "transactions", 'w')
    preprocess_statement(2024, "sep", "credit builder card", "summary", "rw")
    preprocess_statement(2024, 9, "credit builder card", "transactions", "rw")
    preprocess_statement(2024, "09", "credit builder secured", "summary", "rw")
    preprocess_statement(2024, "09", "credit builder secured", "transactions", "rw")

### Multiple File Prerocessing Example
#### preprocess_statements(start_year, end_year, account, statement, option)
    preprocess_statements(2021, 2025, "checking", "summary", 'r')
    preprocess_statements(2021, 2025, "checking", "transactions", 'w')
    preprocess_statements(2021, 2025, "credit builder card", "summary", "rw")
    preprocess_statements(2021, 2025, "credit builder card", "transactions", "wa")
    preprocess_statements(2021, 2025, "credit builder secured", "summary", "rwa")
    preprocess_statements(2021, 2025, "credit builder secured", "transactions", "rwa")

## Dependencies
This project relies on the following package:
* pandas (version 2.3.1)

## Version History
* 0.1 (Initial Release)
    * preprocessing of Chime bank statements

## License
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
