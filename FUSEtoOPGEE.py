import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import pandas as pd
import math

import os

# Function to extract data from the Excel sheet based on the specified ranges
def extract_field_data(sheet, col):
    """
    Extracts data for each field from OPGEE excel

    Parameters:
        sheet (pandas dataframe): Pandas dataframe containing the "Inputs" sheet of the OPGEE excel file
        col (integer): Used to identify the column that data is collected from.

    Returns:
        list: list with data collected from OPGEE excel
    """
    ranges = [
        (8, 16), (19, 30), (33, 33), (35, 41), (45, 50),
        (57, 58), (61, 67), (69, 71), (76, 76),
        (85, 87), (91, 93), (95, 97),
        (101, 105), (107, 112), (114, 114)
    ] # rows that contains data (skipped rows are blank)
    data = []
    for start, end in ranges:
        data.extend(sheet.iloc[start-1:end, col].tolist())
    return data

# Function to apply conversion mappings
def apply_conversions(field_updates, mappings):
    """
    Applies conversion mappings to specific field values in the `field_updates` dictionary.

    This function replaces numerical values in the `field_updates` dictionary with their corresponding 
    string representations based on the provided `mappings`. It handles special cases for 
    `ecosystem_richness` and `field_development_intensity`, where the values are lists of integers. 
    The function identifies which element in the list is set to 1 and maps that index to the corresponding 
    string value in the mapping. For other keys, if the value is a digit and exists in the mapping, 
    it will be replaced by the corresponding string.

    Parameters:
    field_updates (dict): A dictionary containing field values that may need conversion.
    mappings (dict): A dictionary where the keys are variable names and the values are nested dictionaries, 
                    which maps integers to their corresponding string representations.

    Returns:
    dictionary: The updated `field_updates` dictionary with the converted values.
    """
    for key, mapping in mappings.items():
        if key in field_updates:
            value = field_updates[key]
            if key in ['ecosystem_richness', 'field_development_intensity']:
                # value = [i for i, val in enumerate(value, 1) if val == '1']
                # Enumerate the list to find which value is set to 1
                value_enumerated =  enumerate(value, 1)
                
                for index, val in value_enumerated:
                    if val == 1:
                            value = index
                if value:
                    field_updates[key] = mapping[value]
            elif value.isdigit() and int(value) in mapping:
                field_updates[key] = mapping[int(value)]
    return field_updates

def create_field_element(field_name, field_updates):
    """
    Creates an XML element representing a field with its associated data.

    This function generates an XML `<Field>` element with the provided `field_name` and populates it 
    with sub-elements based on the `field_updates` dictionary. Each key-value pair in `field_updates` 
    becomes a sub-element under the `<Field>` element. Special handling is applied for the keys 
    `fraction_diluent` and `heater_treater`, where these keys are nested under `<Process>` elements 
    with their respective classes.

    Parameters:
    field_name (str): The name of the field. To be used as the `name` attribute in the `<Field>` element.
    field_updates (dict): A dictionary containing field data where the keys are variable names and the values are their corresponding data. 
                        This data will be converted into XML sub-elements.

    Returns:
    xml.etree.ElementTree.Element: An XML element representing the field, including all sub-elements as specified by the `field_updates` dictionary.
    """
    new_field = ET.Element('Field', {'name': field_name, 'modifies': 'template'})
    group_element = ET.SubElement(new_field, 'Group')
    group_element.text = 'all'

    for key, value in field_updates.items():
        value = '' if pd.isna(value) else str(value)  # Replace NaN with an empty string, otherwise convert to string

        if key in ('GOR', 'WOR'):                              # When we're handling the GOR variable
            try:
                # try to parse it as a float
                gor_val = float(value)
            except ValueError:
                gor_val = 0.0                        # Non-numeric fall-back

            if gor_val in (0.0, 0, 0.00):            # If it's exactly zero
                value = '0.00001'                    # Enforce a small minimum value

        if key in ['fraction_diluent', 'heater_treater']:
            # Handle special case for fraction_diluent and heater_treater
            process_class = 'HeavyOilDilution' if key == 'fraction_diluent' else 'CrudeOilDewatering' # A conditional expression to choose between HeavyOilDilution or CrudeOilDewatering
            ET.SubElement(new_field, 'Process', {'class': process_class, 'enabled' : 'false'})        # Create a sub element titled 'Process', used to temporarily disable the process to avoid dublicate error in OPGEEv4 
            process_element = ET.SubElement(new_field, 'Process', {'class': process_class})           # Create a sub element titled 'Process'
            a_element = ET.SubElement(process_element, 'A', {'name': key})                            # Print variable nad value to the 'Process' sub element
        else:
            a_element = ET.SubElement(new_field, 'A', {'name' : key})                                 

        a_element.text = value
    return new_field

# Function to remove excessive newlines from the pretty-printed XML
def remove_excessive_newlines(xml_str):
    """
    Removes excessive newlines from a given XML string.

    This function removes any empty lines that contain only whitespace. 
    It returns a cleaned-up version of the XML string where only meaningful lines with content are retained, 
    reducing unnecessary spacing.

    Parameters:
    xml_str (str): The XML string from which excessive newlines are to be removed.

    Returns:
    str: The cleaned XML string with excessive newlines removed.
    """
    lines = xml_str.split('\n')
    filtered_lines = [line for line in lines if line.strip() != '']
    return '\n'.join(filtered_lines)

def export_name_api(root, csv_path):
    """
    Extracts each Field’s ‘name’ and ‘API’ values and writes them
    in two rows: the first row starts with ‘name’ followed by all field names,
    the second row starts with ‘API’ followed by all API values.
    """
    names = []
    apis  = []

    # Collect the values
    for field in root.findall('.//Field[@modifies="template"]'):
        name_elem = field.find('A[@name="name"]')
        api_elem  = field.find('A[@name="API"]')
        if name_elem is not None and api_elem is not None:
            names.append(name_elem.text)
            apis.append(api_elem.text)
            # print(f"{field.get('name')} ready for exporting")

    # Build a DataFrame with two rows and write it out horizontally
    df = pd.DataFrame([names, apis], index=['name', 'API'])
    df.to_csv(csv_path, header=False)

    print(f"Exported {len(names)} field names and {len(apis)} APIs to {csv_path}")

def main():

    # Load the existing XML file
    script_dir = os.path.dirname(os.path.dirname(__file__))  # Go up one directory level
    script_path = os.path.join(script_dir, 'OPGEEv4/opgee/etc/fuse.xml') # Prepare the relative path to the XML file
    
    if not os.path.exists(script_path) or os.stat(script_path).st_size == 0: # check for missing/empty file
        root = ET.Element('Model') # create a <Model> element as root                                        
        tree = ET.ElementTree(root) # wrap it in an ElementTree
    else:
        tree = ET.parse(script_path)  # Parse the XML file into an ElementTree object
        root = tree.getroot() # Get the root element of the XML tree

    # Dictionary with keys and values to be updated in the Analysis element
    analysis_updates = {
        'functional_unit': 'oil',
        'GWP_horizon': '100',
        'GWP_version': 'AR5'
    }

    # Predefined parameters for the dictionary keys
    parameters = [
        'downhole_pump', 'water_reinjection', 'natural_gas_reinjection', 'water_flooding', 'gas_lifting', 
        'gas_flooding', 'steam_flooding', 'oil_sands_mine_upgrader', 'oil_sands_mine_no_upgrader',
        'country', 'name', 'age', 'depth', 'oil_prod',
        'num_prod_wells', 'num_water_inj_wells', 'well_diam', 
        'prod_index', 'res_press', 'res_temp', 'offshore',
        'API', 'gas_comp_N2', 'gas_comp_CO2', 'gas_comp_C1', 'gas_comp_C2', 'gas_comp_C3', 'gas_comp_C4', 
        'gas_comp_H2S', 'GOR', 'WOR', 'WIR', 'GLIR', 'GFIR',
        'flood_gas_type', 'frac_CO2_breakthrough', 'FILLER_source_of_CO2', 'FILLER_perc_seq_credit', 'SOR', 'fraction_elec_onsite',
        'fraction_remaining_gas_inj', 'fraction_water_reinjected', 'fraction_steam_cogen',
        'fraction_steam_solar', 'heater_treater', 'stabilizer_column', 'upgrader_type',
        'gas_processing_path', 'FOR', 'frac_venting', 'fraction_diluent', 'ecosystem_richness',
        'field_development_intensity', 'frac_transport_tanker', 'frac_transport_barge',
        'frac_transport_pipeline', 'frac_transport_rail', 'frac_transport_truck',
        'transport_dist_tanker', 'transport_dist_barge', 'transport_dist_pipeline', 'transport_dist_rail',
        'transport_dist_truck', 'ocean_tanker_size', 'small_sources_emissions', 'common_gas_process_choice', 'oil_processing_path'
    ]
    # print(len(parameters))

    # Variables to be removed from each field dictionary
    variables_to_remove = [
        'ocean_tanker_size', 'small_sources_emissions', 'FILLER_source_of_CO2', 
        'FILLER_perc_seq_credit', 'oil_sands_mine_no_upgrader', 'oil_sands_mine_upgrader'
    ]

    # Mappings for conversion of numerical values to strings
    conversion_mappings = {
        'flood_gas_type': {1: 'NG', 2: 'N2', 3: 'CO2'},
        'upgrader_type': {0: 'None', 1: 'Delayed Coking', 2: 'Hydroconvention', 3: 'Combined Hydroconversion and Fluid Coking'},
        'gas_processing_path': {1: 'None', 2: 'Minimal', 3: 'Acid Gas', 4: 'Wet Gas', 5: 'Acid Wet Gas', 6: 'Sour Gas Reinjection', 7: 'CO2-EOR Membrane', 8: 'CO2-EOR Ryan Holmes'},
        'ecosystem_richness': {1: 'Low carbon', 2: 'Med carbon', 3: 'High carbon'},
        'field_development_intensity': {1: 'Low', 2: 'Med', 3: 'High'},
        'common_gas_process_choice': {1: 'All'},
        'oil_processing_path': {1: 'Stabilization', 2: 'Storage', 3: 'Upgrading', 4: 'Dilution', 5: 'Dilution and Upgrading'}
    }

    # Read the text file containing the project name
    script_dir = os.path.dirname(os.path.dirname(__file__))  # Go up one directory level
    script_path_2 = os.path.join(script_dir, 'FUSE/project_name.txt')
    with open(script_path_2, 'r') as file:                   # open file in read only mode
        # Read the current contents
        content = file.read()
        # Remove all spaces from the content
        content_without_spaces = content.replace(" ", "")
        project_name  = str(content_without_spaces)

    # Read the Excel file and extract data from the "inputs" tab
    # excel_file = 'FUSE_py3/Project Data/OPGEE/COEA - OPGEE/OPGEE_3.0c_TestProject copy.xlsm'  # Replace with The OPGEE Excel file path
    script_dir = os.path.dirname(os.path.dirname(__file__))  # Go up one directory level
    script_path_3 = os.path.join(script_dir, 'FUSE/FUSE_py3/Project Data/OPGEE/COEA - OPGEE/OPGEE_3.0c_') # Construct directory of excel file
    excel_file = script_path_3 + project_name + '.xlsm'      # Append the project name and file extension to complete the Excel file path
    print(excel_file) # Used for Debugging
    df = pd.read_excel(excel_file, sheet_name='Inputs')      # Load the 'Inputs' sheet from the specified Excel file into a Pandas DataFrame

    # Create the field_updates_dicts based on the extracted values
    field_updates_dicts = {}
    i = 0
    for col in range(7, df.shape[1]):                      # Start from column H (index 7)

        field_name = df.iloc[3, col]                       # Field name in row 5 (index 4)
        
        # Ensures that Field names after 500 are not left blank
        if pd.isna(field_name):
            i += 1
            field_name = 'Field ' + str(500 + i)
        # print(field_name)

        values = extract_field_data(df, col)

        # Extract lists for special cases
        ecosystem_richness_values = values[51:54]           # one of these 3 indices contains a number that will be mapped onto the conversion_mappings dictionary
        field_development_intensity_values = values[54:57]  # one of these 3 indices contains a number that will be mapped onto the conversion_mappings dictionary

        indexes_to_pop = [52,53,54,55]                      # Remove 4 of the 6 indices in 51:57, leave 2 because there are 2 variables (i.e. ecosystem_richness_values and field_development_intensity_values)                        
        for index in sorted(indexes_to_pop, reverse=True):
            values.pop(index)

        # print(field_development_intensity_values)
        if any(pd.notna(values)):                           # Check if there are any non-NaN values
            print(values)
            
            if 'common_gas_process_choice' in parameters and 'oil_processing_path' in parameters: # additional parameters required by OPGEEv4 that was not included in the Excel version of OPGEE
                values.extend([1,1])

            field_updates = {
                parameters[i]: '' if pd.isna(values[i]) else str(values[i])
                for i in range(min(len(parameters), len(values)))
            }
            
            # Add lists for special cases
            field_updates['ecosystem_richness'] = ecosystem_richness_values
            field_updates['field_development_intensity'] = field_development_intensity_values
            
            # Remove specified variables in the list variables_to_remove, these variables do not exist in OPGEEv4 but existed in Excel version of OPGEE
            for var in variables_to_remove:
                if var in field_updates:
                    del field_updates[var]
            
            # Apply conversion mappings
            field_updates = apply_conversions(field_updates, conversion_mappings)
            field_updates_dicts[field_name] = field_updates

    # Update or create Analysis element
    # analysis = root.find('.//Analysis[@name="SSE_test"]') # Find the Analysis element with the name "SSE_test"
    # if analysis is not None:
    #     group_element = ET.SubElement(analysis, 'Group')
    #     group_element.text = 'all'
    #     for a in analysis.findall('A'):
    #         # If the "name" attribute of an >A< element matches a key in analysis_updates, update its text
    #         if a.get('name') in analysis_updates:
    #             a.text = analysis_updates[a.get('name')]

    # Update or create Analysis element
    analysis = root.find('.//Analysis[@name="FUSE_run"]')                                # Find the Analysis element with the name "FUSE_run"

    # If the Analysis element does not exist, create it
    if analysis is None:
        analysis = ET.SubElement(root, 'Analysis', {'name': 'FUSE_run'})

    # Check if <Group>all</Group> already exists within the Analysis element
    group_exists = any(group.text == 'all' for group in analysis.findall('Group'))
    if not group_exists:
        group_element = ET.SubElement(analysis, 'Group')
        group_element.text = 'all'

# Update or create the <A> elements within the Analysis element
    for key, value in analysis_updates.items():
        # Check if the <A> element already exists
        a_element = analysis.find(f'A[@name="{key}"]')
        if a_element is not None:
            # Update existing element's text
            a_element.text = value
        else:
            # Create the element if it does not exist
            ET.SubElement(analysis, 'A', {'name': key}).text = value


    # Get all existing field names from the current XML structure
    existing_fields = root.findall('.//Field[@modifies="template"]')

    # Extract the names of fields that should be present based on the current run
    required_field_names = set(field_updates_dicts.keys())

    # Remove fields that are not part of the current run
    for field in existing_fields:
        field_name = field.get('name')
        if field_name not in required_field_names:
            root.remove(field)                                                                             # Remove fields that are not in the required list

    # Update or create Field elements
    for field_name, field_updates in field_updates_dicts.items():
        field = root.find(f'.//Field[@name="{field_name}"][@modifies="template"]')                         # Find the Field element with the required field name and the "modifies" attribute set to "template"
        if field is not None:
            root.remove(field)                                                                             # Remove field if it exists, this enables accurate reprinting of the field elements if sub-elements are removed by user

        new_field = create_field_element(field_name, field_updates)
        root.append(new_field) # Append the new Field element to the root

    # Used for Debugging
    # print(xml_str)

    # Debug print to verify field updates
    # print(field_updates_dicts)
    # print(df.head())

    # Write the properly formatted XML back to the file
    script_dir = os.path.dirname(os.path.dirname(__file__))                                                 # Go up one directory level
    script_path_4 = os.path.join(script_dir, 'OPGEEv4/opgee/etc/fuse.xml')                                  # Prepare the relative path to the XML file

    csv_path_name_api = os.path.join(script_dir, 'FUSE/FUSE_py3/OPGEE post processing/field_name_api.csv')  # directroy of API and field name csv file
    export_name_api(root, csv_path_name_api)                                                                # used to export API and field name to csv fil in the OPGEE post processing folder

    rough = ET.tostring(root, encoding='UTF-8')                                                             # dump tree to raw bytes (no declaration)                                       
    reparsed = minidom.parseString(rough)                                                                   # parse into DOM for pretty‐print   

    # produce a UTF-8-encoded pretty XML with declaration                                      
    pretty_bytes = reparsed.toprettyxml(indent='    ', encoding='UTF-8')  

    # remove any blank lines that toprettyxml might have inserted
    lines = [line for line in pretty_bytes.splitlines() if line.strip()]                   
    final = b'\n'.join(lines)       

    # write bytes (including XML declaration) back to the file                                                       
    with open(script_path_4, 'wb') as f:                                                    
        f.write(final)    
    print('Functional unit and fields updated successfully.')


if __name__ == "__main__": 
    main()