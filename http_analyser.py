import os
import re
import csv
from urllib.parse import urlparse, parse_qs
from tkinter import filedialog, Tk
import os

def extract_log_data_all(line, search_param='rhsearch'):
    """
    Extracts the requested data from a log line if it contains the specified parameter.
    This function uses regular expressions to parse the log line and extract the IP address,
    HTTP method, and URL. If the URL contains the specified parameter, it further parses to get
    the base URL, the value of the parameter, and returns this data as a tuple.

    Args:
        line (str): The log line to extract data from.
        search_param (str): The parameter to search for in the URL (default is 'rhsearch').

    Returns:
        tuple or None: A tuple containing URL, base URL, parameter value, and IP address if found,
        or None if not found.
    """
    pattern = r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[.*\] "(?P<method>GET|POST) (?P<url>.+?) HTTP/.*" .*'
    match = re.match(pattern, line)
    if match:
        data = match.groupdict()
        url = data['url']

        if f'{search_param}=' in url:
            parsed_url = urlparse(url)
            path_segments = parsed_url.path.strip('/').split('/')
            if len(path_segments) >= 2:
                base_url = path_segments[1]
            else:
                base_url = ''
            query_params = parse_qs(parsed_url.query)
            param_value = query_params.get(search_param, [''])[0]
            ip = data['ip']
            return (url, base_url, param_value, ip)

    return None


def extract_search_data(file_paths, output_search_file = "search_logs_filtered.csv"):
    """
    Extracts the logs tht represent the action of searching in a RoboHelp help file, based on the 'rhsearch' keyword.
    Stores the result in one or many files depending on value of output_search_file.

    Args:
        file_paths (str): The list of files.
        output_search_file (str): The name of the file to store the result. If empty, the result will be stored in the same file with a different name.

    """
    output_search_file = "search_logs_filtered.csv"
    #output_search_file = ""

    for file_path in file_paths:
        # Create the 'filtered' subdirectory if it doesn't exist
        output_directory = os.path.join(os.path.dirname(file_path), "search_filter")
        os.makedirs(output_directory, exist_ok=True)

        # Process the file again with the adjusted criteria
        extracted_data_all_rhsearch = []
        seen_param_values = set()  # A set to keep track of unique parameter values

        with open(file_path, 'r') as file:
            for line in file:
                extracted = extract_log_data_all(line, rhsearch_param='rhsearch')
                if extracted:
                    # Check if the parameter value has already been seen
                    param_value = extracted[2]  # Extracting the parameter value from the tuple
                    if param_value not in seen_param_values:
                        seen_param_values.add(param_value)
                        extracted_data_all_rhsearch.append(extracted)

        if output_search_file == "":
            # Extract the base filename and its suffix (if any)
            base_filename, suffix = os.path.splitext(os.path.basename(file_path))

            # Split the base filename at the '-' character
            parts = suffix.split('-')

            # Reform the filename including the part after '-' if it exists
            if len(parts) > 1:
                csv_filename = f"{base_filename}-{parts[1]}.csv"
            else:
                csv_filename = f"{base_filename}.csv"
        else:
            csv_filename = output_search_file
        # Construct the full path for the CSV file
        csv_file_path_all_rhsearch = os.path.join(output_directory, csv_filename)

            # Delete the file if it already exists
        mode = 'w' if output_search_file == "" else 'a'

        # Writing data to the CSV file
        with open(csv_file_path_all_rhsearch, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')  # Set delimiter to semicolon
            writer.writerow(['Base URL', 'Parameter Value', 'Calling IP', 'URL'])  # Adjusted column order

            for data in extracted_data_all_rhsearch:
                # Rearranging the data according to the new column order
                reordered_data = (data[1], data[2], data[3], data[0])
                writer.writerow(reordered_data)

        print(f"Filtered log search data saved to: {csv_file_path_all_rhsearch}")
        


def extract_index_data(file_paths):

    output_search_file = "index_logs_filtered.csv"
    #output_search_file = ""

    for file_path in file_paths:
        # Create the 'filtered' subdirectory if it doesn't exist
        output_directory = os.path.join(os.path.dirname(file_path), "index_filter")
        os.makedirs(output_directory, exist_ok=True)

        # Process the file again with the adjusted criteria
        extracted_data_all_index = []
        seen_param_values = set()  # A set to keep track of unique parameter values

        with open(file_path, 'r') as file:
            for line in file:
                extracted = extract_log_data_all(line, search_param ='agt')
                if extracted:
                    extracted_data_all_index.append(extracted)
                    # Check if the parameter value has already been seen
                    # param_value = extracted[2]  # Extracting the parameter value from the tuple
                    # if param_value not in seen_param_values:
                    #     seen_param_values.add(param_value)
                    #     extracted_data_all_index.append(extracted)

        if output_search_file == "":
            # Extract the base filename and its suffix (if any)
            base_filename, suffix = os.path.splitext(os.path.basename(file_path))

            # Split the base filename at the '-' character
            parts = suffix.split('-')

            # Reform the filename including the part after '-' if it exists
            if len(parts) > 1:
                csv_filename = f"{base_filename}-{parts[1]}.csv"
            else:
                csv_filename = f"{base_filename}.csv"
        else:
            csv_filename = output_search_file
        # Construct the full path for the CSV file
        csv_file_path_all_index = os.path.join(output_directory, csv_filename)

            # Delete the file if it already exists
        mode = 'w' if output_search_file == "" else 'a'

        # Writing data to the CSV file
        with open(csv_file_path_all_index, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')  # Set delimiter to semicolon
            writer.writerow(['Base URL', 'Parameter Value', 'Calling IP', 'URL'])  # Adjusted column order

            for data in extracted_data_all_index:
                # Rearranging the data according to the new column order
                reordered_data = (data[1], data[2], data[3], data[0])
                writer.writerow(reordered_data)

        print(f"Filtered log index data saved to: {csv_file_path_all_index}")
        

        
# Ask for input files
root = Tk()
root.withdraw()  # We don't want a full GUI, so keep the root window from appearing
file_paths = filedialog.askopenfilenames(
    initialdir=r"C:\svnroot\oxyprj_1102\IA\memsoft_docs\Aides\logs", title="Select log files",
    filetypes=(("Log files", "*.log"), ("all files", "*.*"))
)
root.destroy()

if not file_paths:
    print("No file selected. Exiting.")
    exit()

extract_search_data(file_paths)
#extract_index_data(file_paths)