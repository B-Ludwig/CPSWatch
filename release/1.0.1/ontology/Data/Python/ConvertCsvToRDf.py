import tkinter as tk
from tkinter import filedialog
import pandas as pd
import rdflib
import sys


def load_numeric_csv_file():
    # Initialize Tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Set the title for the file dialog window
    root.title("Choose csv numeric data file")

    # Open file dialog and get the file path
    file_path = filedialog.askopenfilename(parent=root, filetypes=[("CSV files", "*.csv")], title="Choose csv numeric data file")
    if file_path:  # If a file was selected
        # Read the CSV file
        df = pd.read_csv(file_path, dtype={'datetime': str, 'unsigned_int': 'UInt32', 'float': float})
        df['dateTime'] = pd.to_datetime(df['dateTime'])
        print(df.head())
        root.destroy()  # Close the Tkinter instance
        file_path = '/'.join(file_path.split('/')[:-1]) + '/'
        return df, file_path
    else:
        print("No file selected, exiting programm.")
        root.destroy()  # Close the Tkinter instance
        return 1
    
def load_status_csv_file():
    # Initialize Tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Set the title for the file dialog window
    root.title("Choose csv status file")

    # Open file dialog and get the file path
    file_path = filedialog.askopenfilename(parent=root, filetypes=[("CSV files", "*.csv")], title="Choose csv status file")
    if file_path:  # If a file was selected
        # Read the CSV file
        df = pd.read_csv(file_path, dtype={'datetime': str, 'unsigned_int': 'UInt32', 'status': str})
        df['dateTime'] = pd.to_datetime(df['dateTime'])
        print(df.head())
        root.destroy()  # Close the Tkinter instance
        return df
    else:
        print("No file selected, exiting programm.")
        root.destroy()  # Close the Tkinter instance
        return 1

def load_rdf_file():
    # Initialize Tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.title("Choose RDF file")

    # Open file dialog and get the file path
    file_path = filedialog.askopenfilename(parent=root, filetypes=[("RDF files", "*.rdf")], title="Choose RDF file")
    if file_path:  # If a file was selected
        # Load and parse the RDF file
        g = rdflib.Graph()
        g.parse(file_path)
        print(f"{len(g)} triples in the graph.")
        root.destroy()  # Close the Tkinter instance
        return g
    else:
        print("No file selected, exiting programm.")
        root.destroy()  # Close the Tkinter instance
        sys.exit()

def get_all_classes(graph):
    query = """
    SELECT DISTINCT ?class WHERE {
        ?class rdf:type owl:Class .
    }
    """
    return set(str(row[0]) for row in graph.query(query))

def get_instances_of_class(graph, class_uri):
    query = f"""
    SELECT DISTINCT ?instance WHERE {{
        ?instance rdf:type <{class_uri}> .
    }}
    """
    return set(str(row.instance) for row in graph.query(query))

def get_data_properties_of_instance(graph, instance_uri):
    query = f"""
    SELECT DISTINCT ?property ?value WHERE {{
        <{instance_uri}> ?property ?value .
        FILTER (isLiteral(?value))
    }}
    """
    return {(str(row.property), str(row.value)) for row in graph.query(query)}

def get_base_uri(instance_uri):
    # Check if the URI contains a hash (#)
    if '#' in instance_uri:
        # Split at the hash and return the part before it, including the hash
        return instance_uri.split('#')[0] + '#'
    else:
        # Split at the last slash and return the part before it, including the slash
        return '/'.join(instance_uri.split('/')[:-1]) + '/'
    
datagraph = load_rdf_file()
data, filepath = load_numeric_csv_file()
status = load_status_csv_file()

# Combine status and numeric data
data['isNumeric'] = True
status['isNumeric'] = False
data = pd.concat([data, status], ignore_index=True)

# Get unique sensor IDs
unique_sensor_ids = data['id'].unique()

# Assuming datagraph is already defined and loaded
ontology_classes = get_all_classes(datagraph)

print("Classes in the ontology:")
for cls in ontology_classes:
    print(cls)

# List to store (instance, hasID value) tuples
hasID_data = []

# Assuming ontology_classes and get_data_properties_of_instance are already defined
for cls in ontology_classes:
    instances = get_instances_of_class(datagraph, cls)
    for instance in instances:
        data_properties = get_data_properties_of_instance(datagraph, instance)
        for property, value in data_properties:
            if 'hasID' in property:
                hasID_data.append((instance, get_base_uri(instance), value))

# Create a DataFrame from the collected data
df_hasID = pd.DataFrame(hasID_data, columns=['Instance', 'base', 'hasID'])

# Convert the 'Instance' and 'base' columns to string, and 'hasID' to int
df_hasID['Instance'] = df_hasID['Instance'].astype(str)
df_hasID['base'] = df_hasID['base'].astype(str)
df_hasID['hasID'] = df_hasID['hasID'].astype(int)


# Open a file to write RDF entries
with open(filepath + "ConvertCsvToRdfOutput.rdf", "w") as rdf_file:
    # Loop over the data dataframe
    for index, row in data.iterrows():
        # Find the corresponding instance for the id in df_hasID
        instance = df_hasID[df_hasID['hasID'] == row['id']]['Instance'].item()
        base = df_hasID[df_hasID['hasID'] == row['id']]['base'].item()
        isNumeric = row['isNumeric']

        # Extract dateTime and value
        dateTime = row['dateTime'].strftime("%Y-%m-%dT%H:%M:%S")
        value = row['value']

        if isNumeric:
            # Create the RDF-style entry
            rdf_entry = f"""
            <!-- {base}Observation_{index} -->

            <NamedIndividual rdf:about="{base}Observation_{index}">
                <rdf:type rdf:resource="https://w3id.org/CPSWatch#NumericObservation"/>
                <sosa:madeBySensor rdf:resource="{instance}"/>
                <sosa:hasSimpleResult rdf:datatype="http://www.w3.org/2001/XMLSchema#decimal">{value}</sosa:hasSimpleResult>
                <sosa:resultTime rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">{dateTime}</sosa:resultTime>
            </NamedIndividual>
            """
        else:
            # Create the RDF-style entry
            rdf_entry = f"""
            <!-- {base}Observation_{index} -->

            <NamedIndividual rdf:about="{base}Observation_{index}">
                <rdf:type rdf:resource="https://w3id.org/CPSWatch#StatusObservation"/>
                <sosa:madeBySensor rdf:resource="{instance}"/>
                <CPSWatch:hasStatus rdf:resource="https://w3id.org/CPSWatch#{value}"/>
                <sosa:resultTime rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">{dateTime}</sosa:resultTime>
            </NamedIndividual>
            """

        # Write the entry to the file
        rdf_file.write(rdf_entry + "\n")

print('Done')