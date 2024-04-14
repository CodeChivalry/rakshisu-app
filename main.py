import pandas as pd
import numpy as np
import streamlit as st
import time
import base64
from typing import Optional
from google.auth import credentials as auth_credentials
from google.cloud import aiplatform

#------------------------------------------------------------------------------------------------------------
key = "a4aded933c7e444899170460bddf323f"
endpoint = "https://pii-detection-rakshisu.cognitiveservices.azure.com/"
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client


client = authenticate_client()

# Example method for detecting sensitive information (PII) from text 
def pii_recognition(client, documents_array):
    response = client.recognize_pii_entities(documents_array, language="kn")
    result = [doc for doc in response if not doc.is_error]
    return result
#-----------------------------------------------------------------------------------------------------------------
# Rowdy Sheeter Details Masking Variables 

rowdy_sheeter_variables_object = {
    "rs_district_name_mask" : {
        "value": False,
        "maps_with_key": "District_Name"
    },

    "rs_unit_name_mask": {
        "value": False,
        "maps_with_key": "Unit_Name"
    },

    "rs_rowdy_sheet_no_mask" : {
        "value": False,
        "maps_with_key": "Rowdy_Sheet_No"
    },

    "rs_name" : {
        "value": False,
        "maps_with_key": "Name"
    },

    "rs_alias_name" : {
        "value": False,
        "maps_with_key": "AliasName"
    },

    "rs_open_date" : {
        "value": False,
        "maps_with_key": "RS_Open_Date"
    },

    "rs_rowdy_classification_details" : {
        "value": False,
        "maps_with_key": "Rowdy_Classification_Details"
    },

    "rs_activities_description" : {
        "value": False,
        "maps_with_key": "Activities_Description"
    },

    "rs_rowdy_category" : {
        "value": False,
        "maps_with_key": "Rowdy_Category"
    },

    "rs_prev_case_details" : {
        "value": False,
        "maps_with_key": "PrevCase_Details"
    },

    "rs_address" : {
        "value": False,
        "maps_with_key": "Address"
    },

    "rs_age" : {
        "value": False,
        "maps_with_key": "Age"
    },

    "rs_father_name" : {
        "value": False,
        "maps_with_key": "Father_Name"
    },

    "rs_source_of_income" :{
        "value": False,
        "maps_with_key": "Source_Of_Income"
    },

    "rs_last_updated_date" : {
        "value": False,
        "maps_with_key": "LastUpdatedDate"
    },

    "rs_present_whereabout" : {
        "value": False,
        "maps_with_key": "PresentWhereabout"
    }
}
class RowdySheeterVariables:
    def __init__(self, variables_object):
        self.variables_object = variables_object

    def set_mask_value(self, key, value):
        if key in self.variables_object:
            self.variables_object[key]["value"] = value
        else:
            print(f"Key '{key}' not found.")

    def get_mask_value(self, key):
        if key in self.variables_object:
            return self.variables_object[key]["value"]
        else:
            print(f"Key '{key}' not found.")

# Create an instance of the RowdySheeterVariables class
rowdy_sheeter_variables = RowdySheeterVariables({
"rs_district_name_mask" : {
 "value": False,
 "maps_with_key": "District_Name"
},
"rs_unit_name_mask": {
        "value": False,
        "maps_with_key": "Unit_Name"
},

    "rs_rowdy_sheet_no_mask" : {
        "value": False,
        "maps_with_key": "Rowdy_Sheet_No"
},

    "rs_name" : {
        "value": False,
        "maps_with_key": "Name"
},

    "rs_alias_name" : {
        "value": False,
        "maps_with_key": "AliasName"
},

    "rs_open_date" : {
        "value": False,
        "maps_with_key": "RS_Open_Date"
},

    "rs_rowdy_classification_details" : {
        "value": False,
        "maps_with_key": "Rowdy_Classification_Details"
},

    "rs_activities_description" : {
        "value": False,
        "maps_with_key": "Activities_Description"
},

    "rs_rowdy_category" : {
        "value": False,
        "maps_with_key": "Rowdy_Category"
},

    "rs_prev_case_details" : {
        "value": False,
        "maps_with_key": "PrevCase_Details"
},

    "rs_address" : {
        "value": False,
        "maps_with_key": "Address"
},

    "rs_age" : {
        "value": False,
        "maps_with_key": "Age"
},

    "rs_father_name" : {
        "value": False,
        "maps_with_key": "Father_Name"
},

    "rs_source_of_income" :{
        "value": False,
        "maps_with_key": "Source_Of_Income"
},

    "rs_last_updated_date" : {
        "value": False,
        "maps_with_key": "LastUpdatedDate"
},

    "rs_present_whereabout" : {
        "value": False,
        "maps_with_key": "PresentWhereabout"
}
})

# Example usage:
rowdy_sheeter_variables.set_mask_value("rs_district_name_mask", True) # Modify value for "rs_district_name_mask"

#ROWDY FUNCTION
def process_rowdy_sheeter_data(rowdy_sheeter_df):
    rowdy_sheeter_input = []
    rowdy_sheeter_pii_output = []
    #print(rowdy_sheeter_df)
    # Iterate through the rows
    row_dict=None
    for index in range(len(rowdy_sheeter_df)):
        row_dict = rowdy_sheeter_df.iloc[index].to_dict()
        row_values = [str(value) for value in row_dict.values()]

        # Split row values into chunks of 5
        for i in range(0, len(row_values), 5):
            row_chunk = row_values[i:i+5]
            rowdy_sheeter_row_detection = pii_recognition(client, row_chunk)
            rowdy_sheeter_input.append(row_chunk)
            rowdy_sheeter_pii_output.append(rowdy_sheeter_row_detection)

    for index, result in enumerate(rowdy_sheeter_pii_output): 
        for document in result:
            if len(document.entities) > 0: 
                # PII is detected
                key_to_modify = list(rowdy_sheeter_variables_object.keys())[index]
                inner_dict = rowdy_sheeter_variables_object[key_to_modify]
                inner_dict["value"] = True
            else: 
                continue


    combined_list = [item for sublist in rowdy_sheeter_input for item in sublist]

    rowdy_sheeter_input=combined_list

    rowdy_sheeter_list=rowdy_sheeter_input

    from fpdf import FPDF
    import base64
    import os
    def generate_pdf(all_masked_values, file_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('NotoSansKannada', '','/Users/MEHAK SHARMA/Documents/KSP HACK/NotoSansKannada_Condensed-Black.ttf', uni=True)
        pdf.set_font('NotoSansKannada', size=12)
        #index_name = rowdy_sheeter_df.index[0]
        index_name = rowdy_sheeter_df.index[0]
        pdf.cell(200,10,txt="Sheet: Rowdy Sheeter Details",align='C',ln=True)
        pdf.cell(200,10,txt=f"Row Number: {index_name}",align='C',border='B',ln=True)
        for key, value in all_masked_values:
            if(len(value)<50):
                pdf.cell(200, 10, txt=f'{key}: {value}', ln=True)
            else:
                numrows= int(len(value)/50)+1
                numspaces=len(key)+2
                #st.write(key,len(value),numrows)
                x=0
                spaces=' '
                spaces*=numspaces
                for i in range (0,numrows):
                    if(i==0):
                        pdf.cell(200, 10, txt=f'{key}: {value[x:x+50]}',ln=True)
                    else:
                        pdf.cell(200, 10, txt=f'{spaces}{value[x:x+50]}',ln=True)
                    x=x+50
        pdf.output(file_name)
        # Initialize a list to store masked values for all rows
        # Initialize a list to store masked values for all rows
    all_masked_values = []
    # Iterate over each index in the input data
    gem=1
    for i, string in enumerate(rowdy_sheeter_list):
        st.write(f"Title {i+1}: {string}")
        # PII detection for each value
        result = pii_recognition(client, [string])
        print(result)

        # Check if any PII entities are detected in the string
        pii_detected = any(len(document.entities) > 0 for document in result)

        # Display string details and PII detection status
        print(f"String Details: {string}")
        
        # Display PII detection status and prompt user for masking preference
        if pii_detected:
            st.write("PII Detected")
            for document in result:
                for entity in document.entities:
                    pii_type = entity.category
                    subcategory = entity.subcategory if hasattr(entity, 'subcategory') else None
            #gemini(pii_type,gem)
            gem=gem+1
            st.write("Protection from further harm: Masking PII's of victims helps protect them from further victimization, harassment, or stalking.")
            st.write("Compliance with the Indian Evidence Act, 1872: Section 27 of the Indian Evidence Act allows for the production of evidence to rebut the presumption of innocence, but it also protects the privacy of victims.")
            # Add action dropdown for PII detection
            #st.write(f"Title: {i+1}")
            #st.write(f"Value: {string}")
            action = st.selectbox("Action", ["Mask", "Not Mask"], key=f"Action_{i}_{string}")   
            # Prompt user for masking preference for the string
            #mask_preference = input(f"Do you want to mask the detected PII '{string}'? (yes/no): ")
            # Apply masking only if the user wants to mask the detected PII
            if action == "Mask":
                # Mask the string with asterisks if PII is detected
                st.markdown(f"Action: <font color='red'>{action}</font>", unsafe_allow_html=True)
                masked_string = "*" * len(string)
                st.write(f"PII in '{string}' Masked: {masked_string}")
            else:
                st.markdown(f"Action: <font color='green'>{action}</font>", unsafe_allow_html=True)
                masked_string = string
                st.write(f"PII in '{string}' Not Masked: {string}")
            # Get the corresponding key based on the index
            key = list(rowdy_sheeter_variables.variables_object.keys())[rowdy_sheeter_list.index(string)]
            # Store masked value for this string along with the corresponding key
            all_masked_values.append((key, masked_string))
            # Display string details after masking
        else:
            st.write("No PII Detected")
            # Get the corresponding key based on the index
            key = list(rowdy_sheeter_variables.variables_object.keys())[rowdy_sheeter_list.index(string)]

            # Store original value along with the corresponding key
            all_masked_values.append((key, string))


    unique_keys = set()
    unique_tuples = []

    for tuple_item in all_masked_values:

        key = tuple_item[0]  # Access the key of each tuple
        if key not in unique_keys:
            unique_tuples.append(tuple_item)
            unique_keys.add(key)
    all_masked_values=unique_tuples

    # Generate PDF from the obtained masked values
    def get_binary_file_downloader_html(bin_file, file_label='File'):
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download the {file_label}</a>'
        return href

# Assuming `st` is Streamlit's library object for UI components
    if st.button("Export PDF"):
        # Generate PDF from the obtained masked values
        index_name = rowdy_sheeter_df.index[0]
        generate_pdf(all_masked_values, f"rowdy_{index_name}.pdf")
        st.write("PDF exported successfully!")

    # Adding a downloadable link
        download_link = get_binary_file_downloader_html(f"rowdy_{index_name}.pdf", file_label="PDF")
        st.markdown(download_link, unsafe_allow_html=True) 

# accused data 
accused_data_variables_object = {
    "ad_district_name_mask": {
        "value": False,
        "maps_with_key": "District_Name"
    },

    "ad_unit_name_mask": {
        "value": False,
        "maps_with_key": "UnitName"
    },

    "ad_fir_no_mask": {
        "value": False,
        "maps_with_key": "FIRNo"
    },

    "ad_year": {
        "value": False,
        "maps_with_key": "Year"
    },

    "ad_month": {
        "value": False,
        "maps_with_key": "Month"
    },

    "ad_accused_name": {
        "value": False,
        "maps_with_key": "AccusedName"
    },

    "ad_person_name": {
        "value": False,
        "maps_with_key": "Person_Name"
    },

    "ad_age": {
        "value": False,
        "maps_with_key": "age"
    },

    "ad_caste": {
        "value": False,
        "maps_with_key": "Caste"
    },

    "ad_profession": {
        "value": False,
        "maps_with_key": "Profession"
    },

    "ad_present_city": {
        "value": False,
        "maps_with_key": "PresentCity"
    },

    "ad_present_state": {
        "value": False,
        "maps_with_key": "PresentState"
    },

    "ad_permanent_address": {
        "value": False,
        "maps_with_key": "PermanentAddress"
    },

    "ad_permanent_city": {
        "value": False,
        "maps_with_key": "PermanentCity"
    },

    "ad_permanent_state": {
        "value": False,
        "maps_with_key": "PermanentState"
    },

    "ad_nationality_name": {
        "value": False,
        "maps_with_key": "Nationality_Name"
    },

    "ad_dob": {
        "value": False,
        "maps_with_key": "DOB"
    },

    "ad_person_no": {
        "value": False,
        "maps_with_key": "Person_No"
    },

    "ad_arr_id": {
        "value": False,
        "maps_with_key": "Arr_ID"
    },

    "ad_crime_no": {
        "value": False,
        "maps_with_key": "crime_no"
    }
}

class AccusedDataVariables:
    def __init__(self, variables_object):
        self.variables_object = variables_object

    def set_mask_value(self, key, value):
        if key in self.variables_object:
            self.variables_object[key]["value"] = value
        else:
            print(f"Key '{key}' not found.")

    def get_mask_value(self, key):
        if key in self.variables_object:
            return self.variables_object[key]["value"]
        else:
            print(f"Key '{key}' not found.")

# Create an instance of the AccusedDataVariables class
accused_data_variables = AccusedDataVariables(accused_data_variables_object)

# Example usage:
accused_data_variables.set_mask_value("ad_district_name_mask", True)  # Modify value for "ad_district_name_mask"

#ACCUSED FUNCTION
def process_accused_data(accused_df):
    accused_input = []
    accused_pii_output = []

    # Iterate through the rows
    for index in range(len(accused_df)):
        row_dict = accused_df.iloc[index].to_dict()
        row_values = [str(value) for value in row_dict.values()]

        # Split row values into chunks of 5
        for i in range(0, len(row_values), 5):
            row_chunk = row_values[i:i+5]
            accused_row_detection = pii_recognition(client, row_chunk)
            accused_input.append(row_chunk)
            accused_pii_output.append(accused_row_detection)

    # Update mask values based on PII detection results
    for index, result in enumerate(accused_pii_output): 
        for document in result:
            if len(document.entities) > 0: 
                # PII is detected
                key_to_modify = list(accused_data_variables_object.keys())[index]
                inner_dict = accused_data_variables_object[key_to_modify]
                inner_dict["value"] = True
            else: 
                continue

    combined_list = [item for sublist in accused_input for item in sublist]
    accused_input = combined_list
    accused_list = accused_input

    from fpdf import FPDF
    import base64
    import os

    def generate_pdf(all_masked_values, file_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('NotoSansKannada', '','/Users/MEHAK SHARMA/Documents/KSP HACK/NotoSansKannada_Condensed-Black.ttf', uni=True)
        pdf.set_font('NotoSansKannada', size=12)
        index_name = accused_df.index[0]
        pdf.cell(200,10,txt="Sheet: Accused Data Details",align='C',ln=True)
        pdf.cell(200,10,txt=f"Row Number: {index_name}",align='C',border='B',ln=True)
        for key, value in all_masked_values:
            if(len(value)<50):
                pdf.cell(200, 10, txt=f'{key}: {value}', ln=True)
            else:
                numrows= int(len(value)/50)+1
                numspaces=len(key)+2
                #st.write(key,len(value),numrows)
                x=0
                spaces=' '
                spaces*=numspaces
                for i in range (0,numrows):
                    if(i==0):
                        pdf.cell(200, 10, txt=f'{key}: {value[x:x+50]}',ln=True)
                    else:
                        pdf.cell(200, 10, txt=f'{spaces}{value[x:x+50]}',ln=True)
                    x=x+50
        pdf.output(file_name)

    # Initialize a list to store masked values for all rows
    all_masked_values = []
    gem=1
    # Iterate over each index in the input data
    for i, string in enumerate(accused_list):
        st.write(f"Title {i+1}: {string}")
        # PII detection for each value
        result = pii_recognition(client, [string])
        print(result)

        # Check if any PII entities are detected in the string
        pii_detected = any(len(document.entities) > 0 for document in result)

        # Display string details and PII detection status
        print(f"String Details: {string}")
        
        # Display PII detection status and prompt user for masking preference
        if pii_detected:
            st.write("PII Detected")
            for document in result:
                for entity in document.entities:
                    pii_type = entity.category
                    subcategory = entity.subcategory if hasattr(entity, 'subcategory') else None
                    #gemini(pii_type,gem)
                    gem=gem+1
            action = st.selectbox("Action", ["Mask", "Not Mask"], key=f"Action_{i}_{string}")   
            if action == "Mask":
                st.markdown(f"Action: <font color='red'>{action}</font>", unsafe_allow_html=True)
                masked_string = "*" * len(string)
                st.write(f"PII in '{string}' Masked: {masked_string}")
            else:
                st.markdown(f"Action: <font color='green'>{action}</font>", unsafe_allow_html=True)
                masked_string = string
                st.write(f"PII in '{string}' Not Masked: {string}")
            
            # Get the corresponding key based on the index
            key = list(accused_data_variables.variables_object.keys())[accused_list.index(string)]
            # Store masked value for this string along with the corresponding key
            all_masked_values.append((key, masked_string))
            # Display string details after masking
        else:
            st.write("No PII Detected")
            # Get the corresponding key based on the index
            key = list(accused_data_variables.variables_object.keys())[accused_list.index(string)]
            # Store original value along with the corresponding key
            all_masked_values.append((key, string))

    unique_keys = set()
    unique_tuples = []

    for tuple_item in all_masked_values:
        key = tuple_item[0]  # Access the key of each tuple
        if key not in unique_keys:
            unique_tuples.append(tuple_item)
            unique_keys.add(key)
    all_masked_values = unique_tuples

    # Generate PDF from the obtained masked values
    def get_binary_file_downloader_html(bin_file, file_label='File'):
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download th {file_label}</a>'
        return href

    # Assuming `st` is Streamlit's library object for UI components
    if st.button("Export PDF"):
        # Generate PDF from the obtained masked values
        index_name=accused_df.index[0]
        generate_pdf(all_masked_values, f"accused_{index_name}.pdf")
        st.write("PDF exported successfully!")

        # Adding a downloadable link
        download_link = get_binary_file_downloader_html(f"accused_{index_name}.pdf", file_label="PDF")
        st.markdown(download_link, unsafe_allow_html=True)

# accident reports
accident_reports_variables_object = {
    "ar_district_name_mask": {
        "value": False,
        "maps_with_key": "DISTRICTNAME"
    },

    "ar_unit_name_mask": {
        "value": False,
        "maps_with_key": "UNITNAME"
    },

    "ar_crime_no_mask": {
        "value": False,
        "maps_with_key": "Crime_No"
    },

    "ar_year": {
        "value": False,
        "maps_with_key": "Year"
    },

    "ar_ri": {
        "value": False,
        "maps_with_key": "RI"
    },

    "ar_no_of_vehicle_involved": {
        "value": False,
        "maps_with_key": "Noofvehicle_involved"
    },

    "ar_accident_classification": {
        "value": False,
        "maps_with_key": "Accident_Classification"
    },

    "ar_accident_spot": {
        "value": False,
        "maps_with_key": "Accident_Spot"
    },

    "ar_accident_location": {
        "value": False,
        "maps_with_key": "Accident_Location"
    },

    "ar_accident_sub_location": {
        "value": False,
        "maps_with_key": "Accident_SubLocation"
    },

    "ar_accident_spot_b": {
        "value": False,
        "maps_with_key": "Accident_SpotB"
    },

    "ar_main_cause": {
        "value": False,
        "maps_with_key": "Main_Cause"
    },

    "ar_hit_run": {
        "value": False,
        "maps_with_key": "Hit_Run"
    },

    "ar_severity": {
        "value": False,
        "maps_with_key": "Severity"
    },

    "ar_collision_type": {
        "value": False,
        "maps_with_key": "Collision_Type"
    },

    "ar_junction_control": {
        "value": False,
        "maps_with_key": "Junction_Control"
    },

    "ar_road_character": {
        "value": False,
        "maps_with_key": "Road_Character"
    },

    "ar_road_type": {
        "value": False,
        "maps_with_key": "Road_Type"
    },

    "ar_surface_type": {
        "value": False,
        "maps_with_key": "Surface_Type"
    },

    "ar_surface_condition": {
        "value": False,
        "maps_with_key": "Surface_Condition"
    },

    "ar_road_condition": {
        "value": False,
        "maps_with_key": "Road_Condition"
    },

    "ar_weather": {
        "value": False,
        "maps_with_key": "Weather"
    },

    "ar_lane_type": {
        "value": False,
        "maps_with_key": "Lane_Type"
    },

    "ar_road_markings": {
        "value": False,
        "maps_with_key": "Road_Markings"
    },

    "ar_spot_conditions": {
        "value": False,
        "maps_with_key": "Spot_Conditions"
    },

    "ar_side_walk": {
        "value": False,
        "maps_with_key": "Side_Walk"
    },

    "ar_road_junction": {
        "value": False,
        "maps_with_key": "RoadJunction"
    },

    "ar_collision_type_b": {
        "value": False,
        "maps_with_key": "Collision_TypeB"
    },

    "ar_accident_road": {
        "value": False,
        "maps_with_key": "Accident_Road"
    },

    "ar_landmark_first": {
        "value": False,
        "maps_with_key": "Landmark_first"
    },

    "ar_landmark_second": {
        "value": False,
        "maps_with_key": "landmark_second"
    },

    "ar_distance_landmark_first": {
        "value": False,
        "maps_with_key": "Distance_LandMark_First"
    },

    "ar_distance_landmark_second": {
        "value": False,
        "maps_with_key": "Distance_LandMark_Second"
    },

    "ar_accident_description": {
        "value": False,
        "maps_with_key": "Accident_Description"
    },

    "ar_latitude": {
        "value": False,
        "maps_with_key": "Latitude"
    },

    "ar_longitude": {
        "value": False,
        "maps_with_key": "Longitude"
    }
}

class AccidentReportsVariables:
    def __init__(self, variables_object):
        self.variables_object = variables_object

    def set_mask_value(self, key, value):
        if key in self.variables_object:
            self.variables_object[key]["value"] = value
        else:
            print(f"Key '{key}' not found.")

    def get_mask_value(self, key):
        if key in self.variables_object:
            return self.variables_object[key]["value"]
        else:
            print(f"Key '{key}' not found.")

# Create an instance of the AccidentReportsVariables class
accident_reports_variables = AccidentReportsVariables(accident_reports_variables_object)

# Example usage:
accident_reports_variables.set_mask_value("ar_district_name_mask", True)  # Modify value for "ar_district_name_mask"
#ACCIDENT FUNCTION
def process_accident_reports_data(accident_reports_df):
    accident_reports_input = []
    accident_reports_pii_output = []

    # Iterate through the rows
    for index in range(len(accident_reports_df)):
        row_dict = accident_reports_df.iloc[index].to_dict()
        row_values = [str(value) for value in row_dict.values()]

        # Split row values into chunks of 5
        for i in range(0, len(row_values), 5):
            row_chunk = row_values[i:i+5]
            accident_reports_row_detection = pii_recognition(client, row_chunk)
            accident_reports_input.append(row_chunk)
            accident_reports_pii_output.append(accident_reports_row_detection)

    # Update mask values based on PII detection results
    for index, result in enumerate(accident_reports_pii_output): 
        for document in result:
            if len(document.entities) > 0: 
                # PII is detected
                key_to_modify = list(accident_reports_variables_object.keys())[index]
                inner_dict = accident_reports_variables_object[key_to_modify]
                inner_dict["value"] = True
            else: 
                continue

    combined_list = [item for sublist in accident_reports_input for item in sublist]
    accident_reports_input = combined_list
    accident_reports_list = accident_reports_input

    from fpdf import FPDF
    import base64
    import os

    def generate_pdf(all_masked_values, file_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('NotoSansKannada', '','/Users/MEHAK SHARMA/Documents/KSP HACK/NotoSansKannada_Condensed-Black.ttf', uni=True)
        pdf.set_font('NotoSansKannada', size=12)
        index_name = accident_reports_df.index[0]
        pdf.cell(200,10,txt="Sheet: Accident Report Details",align='C',ln=True)
        pdf.cell(200,10,txt=f"Row Number: {index_name}",align='C',border='B',ln=True)
        for key, value in all_masked_values:
            if(len(value)<50):
                pdf.cell(200, 10, txt=f'{key}: {value}', ln=True)
            else:
                numrows= int(len(value)/50)+1
                numspaces=len(key)+2
                #st.write(key,len(value),numrows)
                x=0
                spaces=' '
                spaces*=numspaces
                for i in range (0,numrows):
                    if(i==0):
                        pdf.cell(200, 10, txt=f'{key}: {value[x:x+50]}',ln=True)
                    else:
                        pdf.cell(200, 10, txt=f'{spaces}{value[x:x+50]}',ln=True)
                    x=x+50
        pdf.output(file_name)

    # Initialize a list to store masked values for all rows
    all_masked_values = []
    gem=1
    # Iterate over each index in the input data
    for i, string in enumerate(accident_reports_list):
        st.write(f"Title {i+1}: {string}")
        # PII detection for each value
        result = pii_recognition(client, [string])
        print(result)

        # Check if any PII entities are detected in the string
        pii_detected = any(len(document.entities) > 0 for document in result)

        # Display string details and PII detection status
        print(f"String Details: {string}")
        
        # Display PII detection status and prompt user for masking preference
        if pii_detected:
            st.write("PII Detected")
            for document in result:
                for entity in document.entities:
                    pii_type = entity.category
                    subcategory = entity.subcategory if hasattr(entity, 'subcategory') else None
                    #gemini(pii_type,gem)
                    gem=gem+1
            action = st.selectbox("Action", ["Mask", "Not Mask"], key=f"Action_{i}_{string}")   
            if action == "Mask":
                st.markdown(f"Action: <font color='red'>{action}</font>", unsafe_allow_html=True)
                masked_string = "*" * len(string)
                st.write(f"PII in '{string}' Masked: {masked_string}")
            else:
                st.markdown(f"Action: <font color='green'>{action}</font>", unsafe_allow_html=True)
                masked_string = string
                st.write(f"PII in '{string}' Not Masked: {string}")
            
            # Get the corresponding key based on the index
            key = list(accident_reports_variables.variables_object.keys())[accident_reports_list.index(string)]
            # Store masked value for this string along with the corresponding key
            all_masked_values.append((key, masked_string))
            # Display string details after masking
        else:
            st.write("No PII Detected")
            # Get the corresponding key based on the index
            key = list(accident_reports_variables.variables_object.keys())[accident_reports_list.index(string)]
            # Store original value along with the corresponding key
            all_masked_values.append((key, string))

    unique_keys = set()
    unique_tuples = []

    for tuple_item in all_masked_values:
        key = tuple_item[0]  # Access the key of each tuple
        if key not in unique_keys:
            unique_tuples.append(tuple_item)
            unique_keys.add(key)
    all_masked_values = unique_tuples

    # Generate PDF from the obtained masked values
    def get_binary_file_downloader_html(bin_file, file_label='File'):
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download the  {file_label}</a>'
        return href

    # Assuming `st` is Streamlit's library object for UI components
    if st.button("Export PDF"):
        # Generate PDF from the obtained masked values
        index_name=accident_reports_df.index[0]
        generate_pdf(all_masked_values, f"accident_{index_name}.pdf")
        st.write("PDF exported successfully!")

        # Adding a downloadable link
        download_link = get_binary_file_downloader_html(f"accident_{index_name}.pdf", file_label="PDF")
        st.markdown(download_link, unsafe_allow_html=True)


#FIR 
fir_details_data_variables_object = {
    "fd_district_name_mask": {
        "value": False,
        "maps_with_key": "District_Name"
    },

    "fd_unit_name_mask": {
        "value": False,
        "maps_with_key": "UnitName"
    },

    "fd_fir_no_mask": {
        "value": False,
        "maps_with_key": "FIRNo"
    },

    "fd_ri": {
        "value": False,
        "maps_with_key": "RI"
    },

    "fd_year": {
        "value": False,
        "maps_with_key": "Year"
    },

    "fd_month": {
        "value": False,
        "maps_with_key": "Month"
    },

    "fd_offence_from_date": {
        "value": False,
        "maps_with_key": "Offence_From_Date"
    },

    "fd_offence_to_date": {
        "value": False,
        "maps_with_key": "Offence_To_Date"
    },

    "fd_fir_reg_datetime": {
        "value": False,
        "maps_with_key": "FIR_Reg_DateTime"
    },

    "fd_fir_date": {
        "value": False,
        "maps_with_key": "FIR_Date"
    },

    "fd_fir_type": {
        "value": False,
        "maps_with_key": "FIR Type"
    },

    "fd_fir_stage": {
        "value": False,
        "maps_with_key": "FIR_Stage"
    },

    "fd_complaint_mode": {
        "value": False,
        "maps_with_key": "Complaint_Mode"
    },

    "fd_crimegroup_name": {
        "value": False,
        "maps_with_key": "CrimeGroup_Name"
    },

    "fd_crimehead_name": {
        "value": False,
        "maps_with_key": "CrimeHead_Name"
    },

    "fd_latitude": {
        "value": False,
        "maps_with_key": "Latitude"
    },

    "fd_longitude": {
        "value": False,
        "maps_with_key": "Longitude"
    },

    "fd_actsection": {
        "value": False,
        "maps_with_key": "ActSection"
    },

    "fd_ioname": {
        "value": False,
        "maps_with_key": "IOName"
    },

    "fd_kgid": {
        "value": False,
        "maps_with_key": "KGID"
    },

    "fd_ioassigned_date": {
        "value": False,
        "maps_with_key": "IOAssigned_Date"
    },

    "fd_internal_io": {
        "value": False,
        "maps_with_key": "Internal_IO"
    },

    "fd_place_of_offence": {
        "value": False,
        "maps_with_key": "Place of Offence"
    },

    "fd_distance_from_ps": {
        "value": False,
        "maps_with_key": "Distance from PS"
    },

    "fd_beat_name": {
        "value": False,
        "maps_with_key": "Beat_Name"
    },

    "fd_village_area_name": {
        "value": False,
        "maps_with_key": "Village_Area_Name"
    },

    "fd_male": {
        "value": False,
        "maps_with_key": "Male"
    },

    "fd_female": {
        "value": False,
        "maps_with_key": "Female"
    },

    "fd_boy": {
        "value": False,
        "maps_with_key": "Boy"
    },

    "fd_girl": {
        "value": False,
        "maps_with_key": "Girl"
    },

    "fd_age_0": {
        "value": False,
        "maps_with_key": "Age 0"
    },

    "fd_victim_count": {
        "value": False,
        "maps_with_key": "VICTIM COUNT"
    },

    "fd_accused_count": {
        "value": False,
        "maps_with_key": "Accused Count"
    },

    "fd_arrested_male": {
        "value": False,
        "maps_with_key": "Arrested Male"
    },

    "fd_arrested_female": {
        "value": False,
        "maps_with_key": "Arrested Female"
    },

    "fd_arrested_count": {
        "value": False,
        "maps_with_key": "Arrested Count\tNo."
    },

    "fd_accused_chargesheeted_count": {
        "value": False,
        "maps_with_key": "Accused_ChargeSheeted Count"
    },

    "fd_conviction_count": {
        "value": False,
        "maps_with_key": "Conviction Count"
    },

    "fd_fir_id": {
        "value": False,
        "maps_with_key": "FIR_ID"
    },

    "fd_unit_id": {
        "value": False,
        "maps_with_key": "Unit_ID"
    },

    "fd_crime_no": {
        "value": False,
        "maps_with_key": "Crime_No"
    }
}

class FIR_Details_Data_Variables:
    def __init__(self, variables_object):
        self.variables_object = variables_object

    def set_mask_value(self, key, value):
        if key in self.variables_object:
            self.variables_object[key]["value"] = value
        else:
            print(f"Key '{key}' not found.")

    def get_mask_value(self, key):
        if key in self.variables_object:
            return self.variables_object[key]["value"]
        else:
            print(f"Key '{key}' not found.")

# Create an instance of the FIR_Details_Data_Variables class
fir_details_data_variables = FIR_Details_Data_Variables(fir_details_data_variables_object)

# Example usage:
fir_details_data_variables.set_mask_value("fd_district_name_mask", True)  # Modify value for "fd_district_name_mask"

#FIR FUNCTION
def process_fir_details_data(fir_details_df):
    fir_details_input = []
    fir_details_pii_output = []

    # Iterate through the rows
    for index in range(len(fir_details_df)):
        row_dict = fir_details_df.iloc[index].to_dict()
        row_values = [str(value) for value in row_dict.values()]

        # Split row values into chunks of 5
        for i in range(0, len(row_values), 5):
            row_chunk = row_values[i:i+5]
            fir_details_row_detection = pii_recognition(client, row_chunk)
            fir_details_input.append(row_chunk)
            fir_details_pii_output.append(fir_details_row_detection)

    # Update mask values based on PII detection results
    for index, result in enumerate(fir_details_pii_output): 
        for document in result:
            if len(document.entities) > 0: 
                # PII is detected
                key_to_modify = list(fir_details_data_variables_object.keys())[index]
                inner_dict = fir_details_data_variables_object[key_to_modify]
                inner_dict["value"] = True
            else: 
                continue

    combined_list = [item for sublist in fir_details_input for item in sublist]
    fir_details_input = combined_list
    fir_details_list = fir_details_input

    from fpdf import FPDF
    import base64
    import os

    def generate_pdf(all_masked_values, file_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('NotoSansKannada', '','/Users/MEHAK SHARMA/Documents/KSP HACK/NotoSansKannada_Condensed-Black.ttf', uni=True)
        pdf.set_font('NotoSansKannada', size=12)
        index_name = fir_details_df.index[0]
        pdf.cell(200,10,txt="Sheet: FIR Data Details",align='C',ln=True)
        pdf.cell(200,10,txt=f"Row Number: {index_name}",align='C',border='B',ln=True)
        for key, value in all_masked_values:
            if(len(value)<50):
                pdf.cell(200, 10, txt=f'{key}: {value}', ln=True)
            else:
                numrows= int(len(value)/50)+1
                numspaces=len(key)+2
                #st.write(key,len(value),numrows)
                x=0
                spaces=' '
                spaces*=numspaces
                for i in range (0,numrows):
                    if(i==0):
                        pdf.cell(200, 10, txt=f'{key}: {value[x:x+50]}',ln=True)
                    else:
                        pdf.cell(200, 10, txt=f'{spaces}{value[x:x+50]}',ln=True)
                    x=x+50
        pdf.output(file_name)

    # Initialize a list to store masked values for all rows
    all_masked_values = []
    gem=1
    # Iterate over each index in the input data
    for i, string in enumerate(fir_details_list):
        st.write(f"Title {i+1}: {string}")
        # PII detection for each value
        result = pii_recognition(client, [string])
        print(result)

        # Check if any PII entities are detected in the string
        pii_detected = any(len(document.entities) > 0 for document in result)

        # Display string details and PII detection status
        print(f"String Details: {string}")
        
        # Display PII detection status and prompt user for masking preference
        if pii_detected:
            st.write("PII Detected")
            for document in result:
                for entity in document.entities:
                    pii_type = entity.category
                    subcategory = entity.subcategory if hasattr(entity, 'subcategory') else None
                    #gemini(pii_type,gem)
                    gem=gem+1
            action = st.selectbox("Action", ["Mask", "Not Mask"], key=f"Action_{i}_{string}")   
            if action == "Mask":
                st.markdown(f"Action: <font color='red'>{action}</font>", unsafe_allow_html=True)
                masked_string = "*" * len(string)
                st.write(f"PII in '{string}' Masked: {masked_string}")
            else:
                st.markdown(f"Action: <font color='green'>{action}</font>", unsafe_allow_html=True)
                masked_string = string
                st.write(f"PII in '{string}' Not Masked: {string}")
            
            # Get the corresponding key based on the index
            key = list(fir_details_data_variables.variables_object.keys())[fir_details_list.index(string)]
            # Store masked value for this string along with the corresponding key
            all_masked_values.append((key, masked_string))
            # Display string details after masking
        else:
            st.write("No PII Detected")
            # Get the corresponding key based on the index
            key = list(fir_details_data_variables.variables_object.keys())[fir_details_list.index(string)]
            # Store original value along with the corresponding key
            all_masked_values.append((key, string))

    unique_keys = set()
    unique_tuples = []

    for tuple_item in all_masked_values:
        key = tuple_item[0]  # Access the key of each tuple
        if key not in unique_keys:
            unique_tuples.append(tuple_item)
            unique_keys.add(key)
    all_masked_values = unique_tuples

    # Generate PDF from the obtained masked values
    def get_binary_file_downloader_html(bin_file, file_label='File'):
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download the {file_label}</a>'
        return href

    # Assuming `st` is Streamlit's library object for UI components
    if st.button("Export PDF"):
        # Generate PDF from the obtained masked values
        index_name=fir_details_df.index[0]
        generate_pdf(all_masked_values, f"fir_{index_name}.pdf")
        st.write("PDF exported successfully!")

        # Adding a downloadable link
        download_link = get_binary_file_downloader_html(f"fir_{index_name}.pdf", file_label="PDF")
        st.markdown(download_link, unsafe_allow_html=True)

#Complainant
complainant_details_data_variables_object = {
    "cd_district_name_mask": {
        "value": False,
        "maps_with_key": "District_Name"
    },

    "cd_unit_name_mask": {
        "value": False,
        "maps_with_key": "UnitName"
    },

    "cd_fir_no_mask": {
        "value": False,
        "maps_with_key": "FIRNo"
    },

    "cd_year": {
        "value": False,
        "maps_with_key": "Year"
    },

    "cd_month": {
        "value": False,
        "maps_with_key": "Month"
    },

    "cd_complainant_name": {
        "value": False,
        "maps_with_key": "ComplainantName"
    },

    "cd_relation": {
        "value": False,
        "maps_with_key": "Relation"
    },

    "cd_relationship_name": {
        "value": False,
        "maps_with_key": "RelationshipName"
    },

    "cd_date_of_birth": {
        "value": False,
        "maps_with_key": "DateOfBirth"
    },

    "cd_age": {
        "value": False,
        "maps_with_key": "Age"
    },

    "cd_sex": {
        "value": False,
        "maps_with_key": "Sex"
    },

    "cd_nationality": {
        "value": False,
        "maps_with_key": "Nationality"
    },

    "cd_occupation": {
        "value": False,
        "maps_with_key": "Occupation"
    },

    "cd_address": {
        "value": False,
        "maps_with_key": "Address"
    },

    "cd_city": {
        "value": False,
        "maps_with_key": "City"
    },

    "cd_state": {
        "value": False,
        "maps_with_key": "State"
    },

    "cd_pincode": {
        "value": False,
        "maps_with_key": "Pincode"
    },

    "cd_caste": {
        "value": False,
        "maps_with_key": "Caste"
    },

    "cd_religion": {
        "value": False,
        "maps_with_key": "Religion"
    },

    "cd_fir_id": {
        "value": False,
        "maps_with_key": "FIR_ID"
    },

    "cd_unit_id": {
        "value": False,
        "maps_with_key": "Unit_ID"
    },

    "cd_complaint_id": {
        "value": False,
        "maps_with_key": "Complaint_ID"
    }
}

class Complainant_Details_Data_Variables:
    def __init__(self, variables_object):
        self.variables_object = variables_object

    def set_mask_value(self, key, value):
        if key in self.variables_object:
            self.variables_object[key]["value"] = value
        else:
            print(f"Key '{key}' not found.")

    def get_mask_value(self, key):
        if key in self.variables_object:
            return self.variables_object[key]["value"]
        else:
            print(f"Key '{key}' not found.")

# Create an instance of the Complainant_Details_Data_Variables class
complainant_details_data_variables = Complainant_Details_Data_Variables(complainant_details_data_variables_object)

# Example usage:
complainant_details_data_variables.set_mask_value("cd_district_name_mask", True)  # Modify value for "cd_district_name_mask"

#COMPLAINANT FUNCTION

def process_complainant_details_data(complainant_details_df):
    complainant_details_input = []
    complainant_details_pii_output = []

    # Iterate through the rows
    for index in range(len(complainant_details_df)):
        row_dict = complainant_details_df.iloc[index].to_dict()
        row_values = [str(value) for value in row_dict.values()]

        # Split row values into chunks of 5
        for i in range(0, len(row_values), 5):
            row_chunk = row_values[i:i+5]
            complainant_details_row_detection = pii_recognition(client, row_chunk)
            complainant_details_input.append(row_chunk)
            complainant_details_pii_output.append(complainant_details_row_detection)

    # Update mask values based on PII detection results
    for index, result in enumerate(complainant_details_pii_output): 
        for document in result:
            if len(document.entities) > 0: 
                # PII is detected
                key_to_modify = list(complainant_details_data_variables_object.keys())[index]
                inner_dict = complainant_details_data_variables_object[key_to_modify]
                inner_dict["value"] = True
            else: 
                continue

    combined_list = [item for sublist in complainant_details_input for item in sublist]
    complainant_details_input = combined_list
    complainant_details_list = complainant_details_input

    from fpdf import FPDF
    import base64
    import os

    def generate_pdf(all_masked_values, file_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('NotoSansKannada', '','/Users/MEHAK SHARMA/Documents/KSP HACK/NotoSansKannada_Condensed-Black.ttf', uni=True)
        pdf.set_font('NotoSansKannada', size=12)
        index_name = complainant_details_df.index[0]
        pdf.cell(200,10,txt="Sheet: Complainant Details",align='C',ln=True)
        pdf.cell(200,10,txt=f"Row Number: {index_name}",align='C',border='B',ln=True)
        for key, value in all_masked_values:
            if(len(value)<50):
                pdf.cell(200, 10, txt=f'{key}: {value}', ln=True)
            else:
                numrows= int(len(value)/50)+1
                numspaces=len(key)+2
                #st.write(key,len(value),numrows)
                x=0
                spaces=' '
                spaces*=numspaces
                for i in range (0,numrows):
                    if(i==0):
                        pdf.cell(200, 10, txt=f'{key}: {value[x:x+50]}',ln=True)
                    else:
                        pdf.cell(200, 10, txt=f'{spaces}{value[x:x+50]}',ln=True)
                    x=x+50
        pdf.output(file_name)

    # Initialize a list to store masked values for all rows
    all_masked_values = []
    gem=1
    # Iterate over each index in the input data
    for i, string in enumerate(complainant_details_list):
        st.write(f"Title {i+1}: {string}")
        # PII detection for each value
        result = pii_recognition(client, [string])
        print(result)

        # Check if any PII entities are detected in the string
        pii_detected = any(len(document.entities) > 0 for document in result)

        # Display string details and PII detection status
        print(f"String Details: {string}")
        
        # Display PII detection status and prompt user for masking preference
        if pii_detected:
            st.write("PII Detected")
            for document in result:
                for entity in document.entities:
                    pii_type = entity.category
                    subcategory = entity.subcategory if hasattr(entity, 'subcategory') else None
                    #gemini(pii_type,gem)
                    gem=gem+1
            action = st.selectbox("Action", ["Mask", "Not Mask"], key=f"Action_{i}_{string}")   
            if action == "Mask":
                st.markdown(f"Action: <font color='red'>{action}</font>", unsafe_allow_html=True)
                masked_string = "*" * len(string)
                st.write(f"PII in '{string}' Masked: {masked_string}")
            else:
                st.markdown(f"Action: <font color='green'>{action}</font>", unsafe_allow_html=True)
                masked_string = string
                st.write(f"PII in '{string}' Not Masked: {string}")
            
            # Get the corresponding key based on the index
            key = list(complainant_details_data_variables.variables_object.keys())[complainant_details_list.index(string)]
            # Store masked value for this string along with the corresponding key
            all_masked_values.append((key, masked_string))
            # Display string details after masking
        else:
            st.write("No PII Detected")
            # Get the corresponding key based on the index
            key = list(complainant_details_data_variables.variables_object.keys())[complainant_details_list.index(string)]
            # Store original value along with the corresponding key
            all_masked_values.append((key, string))

    unique_keys = set()
    unique_tuples = []

    for tuple_item in all_masked_values:
        key = tuple_item[0]  # Access the key of each tuple
        if key not in unique_keys:
            unique_tuples.append(tuple_item)
            unique_keys.add(key)
    all_masked_values = unique_tuples

    # Generate PDF from the obtained masked values
    def get_binary_file_downloader_html(bin_file, file_label='File'):
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download the {file_label}</a>'
        return href

    # Assuming `st` is Streamlit's library object for UI components
    if st.button("Export PDF"):
        # Generate PDF from the obtained masked values
        index_name=complainant_details_df.index[0]
        generate_pdf(all_masked_values, f"complainant_{index_name}.pdf")
        st.write("PDF exported successfully!")

        # Adding a downloadable link
        download_link = get_binary_file_downloader_html(f"complainant_{index_name}.pdf", file_label="PDF")
        st.markdown(download_link, unsafe_allow_html=True)

#victim
victim_info_details_variables_object = {
    "vid_district_name_mask": {
        "value": False,
        "maps_with_key": "District_Name"
    },

    "vid_unit_name_mask": {
        "value": False,
        "maps_with_key": "UnitName"
    },

    "vid_fir_no_mask": {
        "value": False,
        "maps_with_key": "FIRNo"
    },

    "vid_year": {
        "value": False,
        "maps_with_key": "Year"
    },

    "vid_month": {
        "value": False,
        "maps_with_key": "Month"
    },

    "vid_victim_name": {
        "value": False,
        "maps_with_key": "VictimName"
    },

    "vid_age": {
        "value": False,
        "maps_with_key": "age"
    },

    "vid_caste": {
        "value": False,
        "maps_with_key": "Caste"
    },

    "vid_profession": {
        "value": False,
        "maps_with_key": "Profession"
    },

    "vid_sex": {
        "value": False,
        "maps_with_key": "Sex"
    },

    "vid_present_address": {
        "value": False,
        "maps_with_key": "PresentAddress"
    },

    "vid_present_city": {
        "value": False,
        "maps_with_key": "PresentCity"
    },

    "vid_present_state": {
        "value": False,
        "maps_with_key": "PresentState"
    },

    "vid_permanent_address": {
        "value": False,
        "maps_with_key": "PermanentAddress"
    },

    "vid_permanent_city": {
        "value": False,
        "maps_with_key": "PermanentCity"
    },

    "vid_permanent_state": {
        "value": False,
        "maps_with_key": "PermanentState"
    },

    "vid_nationality_name": {
        "value": False,
        "maps_with_key": "Nationality_Name"
    },

    "vid_dob": {
        "value": False,
        "maps_with_key": "DOB"
    },

    "vid_person_type": {
        "value": False,
        "maps_with_key": "PersonType"
    },

    "vid_injury_type": {
        "value": False,
        "maps_with_key": "InjuryType"
    },

    "vid_injury_nature": {
        "value": False,
        "maps_with_key": "Injury_Nature"
    },

    "vid_crime_no": {
        "value": False,
        "maps_with_key": "Crime_No"
    },

    "vid_arr_id": {
        "value": False,
        "maps_with_key": "Arr_ID"
    },

    "vid_victim_id": {
        "value": False,
        "maps_with_key": "Victim_ID"
    }
}

class Victim_Info_Details_Variables:
    def __init__(self, variables_object):
        self.variables_object = variables_object

    def set_mask_value(self, key, value):
        if key in self.variables_object:
            self.variables_object[key]["value"] = value
        else:
            print(f"Key '{key}' not found.")

    def get_mask_value(self, key):
        if key in self.variables_object:
            return self.variables_object[key]["value"]
        else:
            print(f"Key '{key}' not found.")

# Create an instance of the Victim_Info_Details_Variables class
victim_info_details_variables = Victim_Info_Details_Variables(victim_info_details_variables_object)

# Example usage:
victim_info_details_variables.set_mask_value("vid_district_name_mask", True)  # Modify value for "vid_district_name_mask"

#VICTIM FUNCTION
def process_victim_info_data(victim_info_df):
    victim_info_input = []
    victim_info_pii_output = []

    # Iterate through the rows
    for index in range(len(victim_info_df)):
        row_dict = victim_info_df.iloc[index].to_dict()
        row_values = [str(value) for value in row_dict.values()]

        # Split row values into chunks of 5
        for i in range(0, len(row_values), 5):
            row_chunk = row_values[i:i+5]
            victim_info_row_detection = pii_recognition(client, row_chunk)
            victim_info_input.append(row_chunk)
            victim_info_pii_output.append(victim_info_row_detection)

    # Update mask values based on PII detection results
    for index, result in enumerate(victim_info_pii_output): 
        for document in result:
            if len(document.entities) > 0: 
                # PII is detected
                key_to_modify = list(victim_info_details_variables_object.keys())[index]
                inner_dict = victim_info_details_variables_object[key_to_modify]
                inner_dict["value"] = True
            else: 
                continue

    combined_list = [item for sublist in victim_info_input for item in sublist]
    victim_info_input = combined_list
    victim_info_list = victim_info_input

    from fpdf import FPDF
    import base64
    import os

    def generate_pdf(all_masked_values, file_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('NotoSansKannada', '','/Users/MEHAK SHARMA/Documents/KSP HACK/NotoSansKannada_Condensed-Black.ttf', uni=True)
        pdf.set_font('NotoSansKannada', size=12)
        index_name = victim_info_df.index[0]
        pdf.cell(200,10,txt="Sheet: Victim Info Details",align='C',ln=True)
        pdf.cell(200,10,txt=f"Row Number: {index_name}",align='C',border='B',ln=True)
        for key, value in all_masked_values:
            if(len(value)<50):
                pdf.cell(200, 10, txt=f'{key}: {value}', ln=True)
            else:
                numrows= int(len(value)/50)+1
                numspaces=len(key)+2
                #st.write(key,len(value),numrows)
                x=0
                spaces=' '
                spaces*=numspaces
                for i in range (0,numrows):
                    if(i==0):
                        pdf.cell(200, 10, txt=f'{key}: {value[x:x+50]}',ln=True)
                    else:
                        pdf.cell(200, 10, txt=f'{spaces}{value[x:x+50]}',ln=True)
                    x=x+50
        pdf.output(file_name)

    # Initialize a list to store masked values for all rows
    all_masked_values = []
    gem=1
    # Iterate over each index in the input data
    for i, string in enumerate(victim_info_list):
        st.write(f"Title {i+1}: {string}")
        # PII detection for each value
        result = pii_recognition(client, [string])
        print(result)

        # Check if any PII entities are detected in the string
        pii_detected = any(len(document.entities) > 0 for document in result)

        # Display string details and PII detection status
        print(f"String Details: {string}")
        
        # Display PII detection status and prompt user for masking preference
        if pii_detected:
            st.write("PII Detected")
            for document in result:
                for entity in document.entities:
                    pii_type = entity.category
                    subcategory = entity.subcategory if hasattr(entity, 'subcategory') else None
                    #gemini(pii_type,gem)
                    gem=gem+1
            action = st.selectbox("Action", ["Mask", "Not Mask"], key=f"Action_{i}_{string}")   
            if action == "Mask":
                st.markdown(f"Action: <font color='red'>{action}</font>", unsafe_allow_html=True)
                masked_string = "*" * len(string)
                st.write(f"PII in '{string}' Masked: {masked_string}")
            else:
                st.markdown(f"Action: <font color='green'>{action}</font>", unsafe_allow_html=True)
                masked_string = string
                st.write(f"PII in '{string}' Not Masked: {string}")
            
            # Get the corresponding key based on the index
            key = list(victim_info_details_variables.variables_object.keys())[victim_info_list.index(string)]
            # Store masked value for this string along with the corresponding key
            all_masked_values.append((key, masked_string))
            # Display string details after masking
        else:
            st.write("No PII Detected")
            # Get the corresponding key based on the index
            key = list(victim_info_details_variables.variables_object.keys())[victim_info_list.index(string)]
            # Store original value along with the corresponding key
            all_masked_values.append((key, string))

    unique_keys = set()
    unique_tuples = []

    for tuple_item in all_masked_values:
        key = tuple_item[0]  # Access the key of each tuple
        if key not in unique_keys:
            unique_tuples.append(tuple_item)
            unique_keys.add(key)
    all_masked_values = unique_tuples

    # Generate PDF from the obtained masked values
    def get_binary_file_downloader_html(bin_file, file_label='File'):
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download the {file_label}</a>'
        return href

    # Assuming `st` is Streamlit's library object for UI components
    if st.button("Export PDF"):
        # Generate PDF from the obtained masked values
        index_name=victim_info_df.index[0]
        generate_pdf(all_masked_values, f"victim_{index_name}.pdf")
        st.write("PDF exported successfully!")

        # Adding a downloadable link
        download_link = get_binary_file_downloader_html(f"victim_{index_name}.pdf", file_label="PDF")
        st.markdown(download_link, unsafe_allow_html=True)

#charge sheeted details
charge_sheeted_details_variables_object = {
    "csd_district_name_mask": {
        "value": False,
        "maps_with_key": "District_Name"
    },

    "csd_unit_name_mask": {
        "value": False,
        "maps_with_key": "UnitName"
    },

    "csd_fir_no_mask": {
        "value": False,
        "maps_with_key": "FIRNo"
    },

    "csd_ri": {
        "value": False,
        "maps_with_key": "RI"
    },

    "csd_year": {
        "value": False,
        "maps_with_key": "Year"
    },

    "csd_month": {
        "value": False,
        "maps_with_key": "Month"
    },

    "csd_fir_date": {
        "value": False,
        "maps_with_key": "FIR_Date"
    },

    "csd_report_date": {
        "value": False,
        "maps_with_key": "Report_Date"
    },

    "csd_final_report_date": {
        "value": False,
        "maps_with_key": "Final_Report_Date"
    },

    "csd_report_type": {
        "value": False,
        "maps_with_key": "Report_Type"
    },

    "csd_fir_id": {
        "value": False,
        "maps_with_key": "FIR_ID"
    },

    "csd_unit_id": {
        "value": False,
        "maps_with_key": "Unit_ID"
    },

    "csd_crime_no": {
        "value": False,
        "maps_with_key": "Crime_No"
    },

    "csd_fr_id": {
        "value": False,
        "maps_with_key": "FR_ID"
    }
}

class Charge_Sheeted_Details_Variables:
    def __init__(self, variables_object):
        self.variables_object = variables_object

    def set_mask_value(self, key, value):
        if key in self.variables_object:
            self.variables_object[key]["value"] = value
        else:
            print(f"Key '{key}' not found.")

    def get_mask_value(self, key):
        if key in self.variables_object:
            return self.variables_object[key]["value"]
        else:
            print(f"Key '{key}' not found.")

# Create an instance of the Charge_Sheeted_Details_Variables class
charge_sheeted_details_variables = Charge_Sheeted_Details_Variables(charge_sheeted_details_variables_object)

# Example usage:
charge_sheeted_details_variables.set_mask_value("csd_district_name_mask", True)  # Modify value for "csd_district_name_mask"

#CHARGE FUNCTION
def process_charge_sheeted_data(charge_sheeted_df):
    charge_sheeted_input = []
    charge_sheeted_pii_output = []

    # Iterate through the rows
    for index in range(len(charge_sheeted_df)):
        row_dict = charge_sheeted_df.iloc[index].to_dict()
        row_values = [str(value) for value in row_dict.values()]

        # Split row values into chunks of 5
        for i in range(0, len(row_values), 5):
            row_chunk = row_values[i:i+5]
            charge_sheeted_row_detection = pii_recognition(client, row_chunk)
            charge_sheeted_input.append(row_chunk)
            charge_sheeted_pii_output.append(charge_sheeted_row_detection)

    # Update mask values based on PII detection results
    for index, result in enumerate(charge_sheeted_pii_output): 
        for document in result:
            if len(document.entities) > 0: 
                # PII is detected
                key_to_modify = list(charge_sheeted_details_variables_object.keys())[index]
                inner_dict = charge_sheeted_details_variables_object[key_to_modify]
                inner_dict["value"] = True
            else: 
                continue

    combined_list = [item for sublist in charge_sheeted_input for item in sublist]
    charge_sheeted_input = combined_list
    charge_sheeted_list = charge_sheeted_input

    from fpdf import FPDF
    import base64
    import os

    def generate_pdf(all_masked_values, file_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('NotoSansKannada', '','/Users/MEHAK SHARMA/Documents/KSP HACK/NotoSansKannada_Condensed-Black.ttf', uni=True)
        pdf.set_font('NotoSansKannada', size=12)
        index_name = charge_sheeted_df.index[0]
        pdf.cell(200,10,txt="Sheet: Charge Sheeted Details",align='C',ln=True)
        pdf.cell(200,10,txt=f"Row Number: {index_name}",align='C',border='B',ln=True)
        for key, value in all_masked_values:
            if(len(value)<50):
                pdf.cell(200, 10, txt=f'{key}: {value}', ln=True)
            else:
                numrows= int(len(value)/50)+1
                numspaces=len(key)+2
                #st.write(key,len(value),numrows)
                x=0
                spaces=' '
                spaces*=numspaces
                for i in range (0,numrows):
                    if(i==0):
                        pdf.cell(200, 10, txt=f'{key}: {value[x:x+50]}',ln=True)
                    else:
                        pdf.cell(200, 10, txt=f'{spaces}{value[x:x+50]}',ln=True)
                    x=x+50
        pdf.output(file_name)

    # Initialize a list to store masked values for all rows
    all_masked_values = []
    gem=1
    # Iterate over each index in the input data
    for i, string in enumerate(charge_sheeted_list):
        st.write(f"Title {i+1}: {string}")
        # PII detection for each value
        result = pii_recognition(client, [string])
        print(result)

        # Check if any PII entities are detected in the string
        pii_detected = any(len(document.entities) > 0 for document in result)

        # Display string details and PII detection status
        print(f"String Details: {string}")
        
        # Display PII detection status and prompt user for masking preference
        if pii_detected:
            st.write("PII Detected")
            for document in result:
                for entity in document.entities:
                    pii_type = entity.category
                    subcategory = entity.subcategory if hasattr(entity, 'subcategory') else None
                    #gemini(pii_type,gem)
                    gem=gem+1
            action = st.selectbox("Action", ["Mask", "Not Mask"], key=f"Action_{i}_{string}")   
            if action == "Mask":
                st.markdown(f"Action: <font color='red'>{action}</font>", unsafe_allow_html=True)
                masked_string = "*" * len(string)
                st.write(f"PII in '{string}' Masked: {masked_string}")
            else:
                st.markdown(f"Action: <font color='green'>{action}</font>", unsafe_allow_html=True)
                masked_string = string
                st.write(f"PII in '{string}' Not Masked: {string}")
            
            # Get the corresponding key based on the index
            key = list(charge_sheeted_details_variables.variables_object.keys())[charge_sheeted_list.index(string)]
            # Store masked value for this string along with the corresponding key
            all_masked_values.append((key, masked_string))
            # Display string details after masking
        else:
            st.write("No PII Detected")
            # Get the corresponding key based on the index
            key = list(charge_sheeted_details_variables.variables_object.keys())[charge_sheeted_list.index(string)]
            # Store original value along with the corresponding key
            all_masked_values.append((key, string))

    unique_keys = set()
    unique_tuples = []

    for tuple_item in all_masked_values:
        key = tuple_item[0]  # Access the key of each tuple
        if key not in unique_keys:
            unique_tuples.append(tuple_item)
            unique_keys.add(key)
    all_masked_values = unique_tuples

    # Generate PDF from the obtained masked values
    def get_binary_file_downloader_html(bin_file, file_label='File'):
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download the {file_label}</a>'
        return href

    # Assuming `st` is Streamlit's library object for UI components
    if st.button("Export PDF"):
        # Generate PDF from the obtained masked values
        index_name=charge_sheeted_df.index[0]
        generate_pdf(all_masked_values, f"charge_{index_name}.pdf")
        st.write("PDF exported successfully!")

        # Adding a downloadable link
        download_link = get_binary_file_downloader_html(f"charge_{index_name}.pdf", file_label="PDF")
        st.markdown(download_link, unsafe_allow_html=True)

#arrest person details
arrest_person_details_variables_object = {
    "apd_district_name_mask": {
        "value": False,
        "maps_with_key": "District_Name"
    },

    "apd_unit_name_mask": {
        "value": False,
        "maps_with_key": "UnitName"
    },

    "apd_fir_no_mask": {
        "value": False,
        "maps_with_key": "FIRNo"
    },

    "apd_year": {
        "value": False,
        "maps_with_key": "Year"
    },

    "apd_month": {
        "value": False,
        "maps_with_key": "Month"
    },

    "apd_name": {
        "value": False,
        "maps_with_key": "Name"
    },

    "apd_age": {
        "value": False,
        "maps_with_key": "age"
    },

    "apd_caste": {
        "value": False,
        "maps_with_key": "Caste"
    },

    "apd_profession": {
        "value": False,
        "maps_with_key": "Profession"
    },

    "apd_sex": {
        "value": False,
        "maps_with_key": "Sex"
    },

    "apd_present_address": {
        "value": False,
        "maps_with_key": "PresentAddress"
    },

    "apd_present_city": {
        "value": False,
        "maps_with_key": "PresentCity"
    },

    "apd_present_state": {
        "value": False,
        "maps_with_key": "PresentState"
    },

    "apd_permanent_address": {
        "value": False,
        "maps_with_key": "PermanentAddress"
    },

    "apd_permanent_city": {
        "value": False,
        "maps_with_key": "PermanentCity"
    },

    "apd_permanent_state": {
        "value": False,
        "maps_with_key": "PermanentState"
    },

    "apd_nationality_name": {
        "value": False,
        "maps_with_key": "Nationality_Name"
    },

    "apd_dob": {
        "value": False,
        "maps_with_key": "DOB"
    },

    "apd_person_no": {
        "value": False,
        "maps_with_key": "Person_No"
    },

    "apd_crime_no": {
        "value": False,
        "maps_with_key": "Crime_No"
    },

    "apd_arr_id": {
        "value": False,
        "maps_with_key": "Arr_ID"
    },

    "apd_charge_sheeted": {
        "value": False,
        "maps_with_key": "Charge_Sheeted"
    },

    "apd_charge_sheet_number": {
        "value": False,
        "maps_with_key": "Charge_Sheet_Number"
    }
}

class Arrest_Person_Details_Variables:
    def __init__(self, variables_object):
        self.variables_object = variables_object

    def set_mask_value(self, key, value):
        if key in self.variables_object:
            self.variables_object[key]["value"] = value
        else:
            print(f"Key '{key}' not found.")

    def get_mask_value(self, key):
        if key in self.variables_object:
            return self.variables_object[key]["value"]
        else:
            print(f"Key '{key}' not found.")

# Create an instance of the Arrest_Person_Details_Variables class
arrest_person_details_variables = Arrest_Person_Details_Variables(arrest_person_details_variables_object)

# Example usage:
arrest_person_details_variables.set_mask_value("apd_district_name_mask", True)  # Modify value for "apd_district_name_mask"

#ARREST FUNCTION
def process_arrest_person_data(arrest_person_df):
    arrest_person_input = []
    arrest_person_pii_output = []

    # Iterate through the rows
    for index in range(len(arrest_person_df)):
        row_dict = arrest_person_df.iloc[index].to_dict()
        row_values = [str(value) for value in row_dict.values()]

        # Split row values into chunks of 5
        for i in range(0, len(row_values), 5):
            row_chunk = row_values[i:i+5]
            arrest_person_row_detection = pii_recognition(client, row_chunk)
            arrest_person_input.append(row_chunk)
            arrest_person_pii_output.append(arrest_person_row_detection)

    # Update mask values based on PII detection results
    for index, result in enumerate(arrest_person_pii_output): 
        for document in result:
            if len(document.entities) > 0: 
                # PII is detected
                key_to_modify = list(arrest_person_details_variables_object.keys())[index]
                inner_dict = arrest_person_details_variables_object[key_to_modify]
                inner_dict["value"] = True
            else: 
                continue

    combined_list = [item for sublist in arrest_person_input for item in sublist]
    arrest_person_input = combined_list
    arrest_person_list = arrest_person_input

    from fpdf import FPDF
    import base64
    import os

    def generate_pdf(all_masked_values, file_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('NotoSansKannada', '','/Users/MEHAK SHARMA/Documents/KSP HACK/NotoSansKannada_Condensed-Black.ttf', uni=True)
        pdf.set_font('NotoSansKannada', size=12)
        index_name = arrest_person_df.index[0]
        pdf.cell(200,10,txt="Sheet: Arrest Person Details",align='C',ln=True)
        pdf.cell(200,10,txt=f"Row Number: {index_name}",align='C',border='B',ln=True)
        for key, value in all_masked_values:
            if(len(value)<50):
                pdf.cell(200, 10, txt=f'{key}: {value}', ln=True)
            else:
                numrows= int(len(value)/50)+1
                numspaces=len(key)+2
                #st.write(key,len(value),numrows)
                x=0
                spaces=' '
                spaces*=numspaces
                for i in range (0,numrows):
                    if(i==0):
                        pdf.cell(200, 10, txt=f'{key}: {value[x:x+50]}',ln=True)
                    else:
                        pdf.cell(200, 10, txt=f'{spaces}{value[x:x+50]}',ln=True)
                    x=x+50
        pdf.output(file_name)

    # Initialize a list to store masked values for all rows
    all_masked_values = []
    gem=1
    # Iterate over each index in the input data
    for i, string in enumerate(arrest_person_list):
        st.write(f"Title {i+1}: {string}")
        # PII detection for each value
        result = pii_recognition(client, [string])
        print(result)

        # Check if any PII entities are detected in the string
        pii_detected = any(len(document.entities) > 0 for document in result)

        # Display string details and PII detection status
        print(f"String Details: {string}")
        
        # Display PII detection status and prompt user for masking preference
        if pii_detected:
            st.write("PII Detected")
            for document in result:
                for entity in document.entities:
                    pii_type = entity.category
                    subcategory = entity.subcategory if hasattr(entity, 'subcategory') else None
                    #gemini(pii_type,gem)
                    gem=gem+1
            action = st.selectbox("Action", ["Mask", "Not Mask"], key=f"Action_{i}_{string}")   
            if action == "Mask":
                st.markdown(f"Action: <font color='red'>{action}</font>", unsafe_allow_html=True)
                masked_string = "*" * len(string)
                st.write(f"PII in '{string}' Masked: {masked_string}")
            else:
                st.markdown(f"Action: <font color='green'>{action}</font>", unsafe_allow_html=True)
                masked_string = string
                st.write(f"PII in '{string}' Not Masked: {string}")
            
            # Get the corresponding key based on the index
            key = list(arrest_person_details_variables.variables_object.keys())[arrest_person_list.index(string)]
            # Store masked value for this string along with the corresponding key
            all_masked_values.append((key, masked_string))
            # Display string details after masking
        else:
            st.write("No PII Detected")
            # Get the corresponding key based on the index
            key = list(arrest_person_details_variables.variables_object.keys())[arrest_person_list.index(string)]
            # Store original value along with the corresponding key
            all_masked_values.append((key, string))

    unique_keys = set()
    unique_tuples = []

    for tuple_item in all_masked_values:
        key = tuple_item[0]  # Access the key of each tuple
        if key not in unique_keys:
            unique_tuples.append(tuple_item)
            unique_keys.add(key)
    all_masked_values = unique_tuples

    # Generate PDF from the obtained masked values
    def get_binary_file_downloader_html(bin_file, file_label='File'):
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download the {file_label}</a>'
        return href

    # Assuming `st` is Streamlit's library object for UI components
    if st.button("Export PDF"):
        # Generate PDF from the obtained masked values
        index_name=arrest_person_df.index[0]
        generate_pdf(all_masked_values, f"arrest_{index_name}.pdf")
        st.write("PDF exported successfully!")

        # Adding a downloadable link
        download_link = get_binary_file_downloader_html(f"arrest_{index_name}.pdf", file_label="PDF")
        st.markdown(download_link, unsafe_allow_html=True)

#MOB's
mob_details_variables_object = {
    "mob_district_name_mask": {
        "value": False,
        "maps_with_key": "District_Name"
    },

    "mob_unit_name_mask": {
        "value": False,
        "maps_with_key": "Unit_Name"
    },

    "mob_name": {
        "value": False,
        "maps_with_key": "Name"
    },

    "mob_person_no": {
        "value": False,
        "maps_with_key": "Person_No"
    },

    "mob_mob_number": {
        "value": False,
        "maps_with_key": "MOB_Number"
    },

    "mob_mob_open_date": {
        "value": False,
        "maps_with_key": "MobOpenDate"
    },

    "mob_mob_open_year": {
        "value": False,
        "maps_with_key": "MOB_Open_Year"
    },

    "mob_arrested_by": {
        "value": False,
        "maps_with_key": "Arrested_By"
    },

    "mob_kgid": {
        "value": False,
        "maps_with_key": "KGID"
    },

    "mob_caste": {
        "value": False,
        "maps_with_key": "Caste"
    },

    "mob_grading": {
        "value": False,
        "maps_with_key": "Grading"
    },

    "mob_occupation": {
        "value": False,
        "maps_with_key": "Occupation"
    },

    "mob_ps_native": {
        "value": False,
        "maps_with_key": "PS_Native"
    },

    "mob_ps_district": {
        "value": False,
        "maps_with_key": "PS_District"
    },

    "mob_offender_class": {
        "value": False,
        "maps_with_key": "Offender_Class"
    },

    "mob_crime_no": {
        "value": False,
        "maps_with_key": "Crime_No"
    },

    "mob_actsection": {
        "value": False,
        "maps_with_key": "ActSection"
    },

    "mob_brief_fact": {
        "value": False,
        "maps_with_key": "Brief_Fact"
    },

    "mob_present_whereabouts": {
        "value": False,
        "maps_with_key": "Present_WhereAbouts"
    },

    "mob_gang_strength": {
        "value": False,
        "maps_with_key": "Gang_Strength"
    },

    "mob_ident_officer": {
        "value": False,
        "maps_with_key": "Ident_Officer"
    },

    "mob_officer_rank": {
        "value": False,
        "maps_with_key": "officer_rank"
    },

    "mob_crime_group1": {
        "value": False,
        "maps_with_key": "Crime_Group1"
    },

    "mob_crime_head2": {
        "value": False,
        "maps_with_key": "Crime_Head2"
    },

    "mob_class": {
        "value": False,
        "maps_with_key": "class"
    },

    "mob_age": {
        "value": False,
        "maps_with_key": "AGE"
    },

    "mob_present_age": {
        "value": False,
        "maps_with_key": "PresentAge"
    },

    "mob_dob": {
        "value": False,
        "maps_with_key": "DOB"
    },

    "mob_address": {
        "value": False,
        "maps_with_key": "Address"
    },

    "mob_sex": {
        "value": False,
        "maps_with_key": "SEX"
    },

    "mob_locality": {
        "value": False,
        "maps_with_key": "Locality"
    },

    "mob_last_updated_date": {
        "value": False,
        "maps_with_key": "LastUpdatedDate"
    }
}

class MOB_Details_Variables:
    def __init__(self, variables_object):
        self.variables_object = variables_object

    def set_mask_value(self, key, value):
        if key in self.variables_object:
            self.variables_object[key]["value"] = value
        else:
            print(f"Key '{key}' not found.")

    def get_mask_value(self, key):
        if key in self.variables_object:
            return self.variables_object[key]["value"]
        else:
            print(f"Key '{key}' not found.")

# Create an instance of the MOB_Details_Variables class
mob_details_variables = MOB_Details_Variables(mob_details_variables_object)

# Example usage:
mob_details_variables.set_mask_value("mob_district_name_mask", True)  # Modify value for "mob_district_name_mask"

#MOB FUNCTION
def process_mob_data(mob_df):
    mob_input = []
    mob_pii_output = []

    # Iterate through the rows
    for index in range(len(mob_df)):
        row_dict = mob_df.iloc[index].to_dict()
        row_values = [str(value) for value in row_dict.values()]

        # Split row values into chunks of 5
        for i in range(0, len(row_values), 5):
            row_chunk = row_values[i:i+5]
            mob_row_detection = pii_recognition(client, row_chunk)
            mob_input.append(row_chunk)
            mob_pii_output.append(mob_row_detection)

    # Update mask values based on PII detection results
    for index, result in enumerate(mob_pii_output): 
        for document in result:
            if len(document.entities) > 0: 
                # PII is detected
                key_to_modify = list(mob_details_variables_object.keys())[index]
                inner_dict = mob_details_variables_object[key_to_modify]
                inner_dict["value"] = True
            else: 
                continue

    combined_list = [item for sublist in mob_input for item in sublist]
    mob_input = combined_list
    mob_list = mob_input

    from fpdf import FPDF
    import base64
    import os

    def generate_pdf(all_masked_values, file_name):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('NotoSansKannada', '','/Users/MEHAK SHARMA/Documents/KSP HACK/NotoSansKannada_Condensed-Black.ttf', uni=True)
        pdf.set_font('NotoSansKannada', size=12)
        index_name = mob_df.index[0]
        pdf.cell(200,10,txt="Sheet: MOBs Details",align='C',ln=True)
        pdf.cell(200,10,txt=f"Row Number: {index_name}",align='C',border='B',ln=True)
        for key, value in all_masked_values:
            if(len(value)<50):
                pdf.cell(200, 10, txt=f'{key}: {value}', ln=True)
            else:
                numrows= int(len(value)/50)+1
                numspaces=len(key)+2
                #st.write(key,len(value),numrows)
                x=0
                spaces=' '
                spaces*=numspaces
                for i in range (0,numrows):
                    if(i==0):
                        pdf.cell(200, 10, txt=f'{key}: {value[x:x+50]}',ln=True)
                    else:
                        pdf.cell(200, 10, txt=f'{spaces}{value[x:x+50]}',ln=True)
                    x=x+50
        pdf.output(file_name)

    # Initialize a list to store masked values for all rows
    all_masked_values = []
    gem=1
    # Iterate over each index in the input data
    for i, string in enumerate(mob_list):
        st.write(f"Title {i+1}: {string}")
        # PII detection for each value
        result = pii_recognition(client, [string])
        print(result)

        # Check if any PII entities are detected in the string
        pii_detected = any(len(document.entities) > 0 for document in result)

        # Display string details and PII detection status
        print(f"String Details: {string}")
        
        # Display PII detection status and prompt user for masking preference
        if pii_detected:
            st.write("PII Detected")
            for document in result:
                for entity in document.entities:
                    pii_type = entity.category
                    subcategory = entity.subcategory if hasattr(entity, 'subcategory') else None
                    #gemini(pii_type,gem)
                    gem=gem+1
            action = st.selectbox("Action", ["Mask", "Not Mask"], key=f"Action_{i}_{string}")   
            if action == "Mask":
                st.markdown(f"Action: <font color='red'>{action}</font>", unsafe_allow_html=True)
                masked_string = "*" * len(string)
                st.write(f"PII in '{string}' Masked: {masked_string}")
            else:
                st.markdown(f"Action: <font color='green'>{action}</font>", unsafe_allow_html=True)
                masked_string = string
                st.write(f"PII in '{string}' Not Masked: {string}")
            
            # Get the corresponding key based on the index
            key = list(mob_details_variables.variables_object.keys())[mob_list.index(string)]
            # Store masked value for this string along with the corresponding key
            all_masked_values.append((key, masked_string))
            # Display string details after masking
        else:
            st.write("No PII Detected")
            # Get the corresponding key based on the index
            key = list(mob_details_variables.variables_object.keys())[mob_list.index(string)]
            # Store original value along with the corresponding key
            all_masked_values.append((key, string))

    unique_keys = set()
    unique_tuples = []

    for tuple_item in all_masked_values:
        key = tuple_item[0]  # Access the key of each tuple
        if key not in unique_keys:
            unique_tuples.append(tuple_item)
            unique_keys.add(key)
    all_masked_values = unique_tuples

    # Generate PDF from the obtained masked values
    def get_binary_file_downloader_html(bin_file, file_label='File'):
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download the {file_label}</a>'
        return href

    # Assuming `st` is Streamlit's library object for UI components
    if st.button("Export PDF"):
        # Generate PDF from the obtained masked values
        index_name = mob_df.index[0]
        generate_pdf(all_masked_values, f"mob_{index_name}.pdf")
        st.write("PDF exported successfully!")

        # Adding a downloadable link
        download_link = get_binary_file_downloader_html(f"mob_{index_name}.pdf", file_label="PDF")
        st.markdown(download_link, unsafe_allow_html=True)
#---------------------------------------------------------------------------------------------------------------
def rowdy_sheeter_details_page():
    st.title("Rowdy Sheeter Details")
    # Add content specific to Rowdy Sheeter Details page
    # File uploader for CSV file
    st.write("Upload Rowdy Sheeter CSV file:")
    uploaded_file = st.file_uploader("", type=["csv"])
    
    # Add disclaimer
    st.write("*If file size is greater than the 200 MB limit, try making chunks of the file and uploading smaller files.")
    
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the DataFrame
        st.write("Preview of uploaded data:")
        st.write(df)
        
        # Dropdown to select FIRNo
        if 'Rowdy_Sheet_No' in df.columns:
            fir_numbers = df['Rowdy_Sheet_No'].unique()
            selected_fir = st.selectbox("Rowdy Sheet No.", fir_numbers)
            
            # Find the rows corresponding to the selected FIR Number
            selected_rows = df[df['Rowdy_Sheet_No'] == selected_fir]
            if not selected_rows.empty:
                # Display selected documents
                st.subheader("Selected Documents:")
                st.write(selected_rows)
                
                if len(selected_rows) > 1:
                    # If there are multiple rows, ask user to select one
                    row_numbers = selected_rows.index.tolist()  # Get the index (actual row numbers) of selected rows
                    selected_row_number = st.selectbox("Select Row Number:", row_numbers)
                    selected_row = selected_rows.loc[[selected_row_number]]
                    st.subheader("Selected Document:")
                    st.write(selected_row)

                else:
                    selected_row = selected_rows.iloc[0:1].copy()   # Only one row, so select it directly
                    
                # Pass the row to rowdysheeter_piidetect function
                process_rowdy_sheeter_data(selected_row)

def accused_details_page():
    st.title("Accused Details")
    # Add content specific to Accused Details page
    # File uploader for CSV file
    st.write("Upload Accused CSV file:")
    uploaded_file = st.file_uploader("", type=["csv"])
    
    # Add disclaimer
    st.write("*If file size is greater than the 200 MB limit, try making chunks of the file and uploading smaller files.")
    
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the DataFrame
        st.write("Preview of uploaded data:")
        st.write(df)
        
        # Dropdown to select Accused ID
        if 'Accused_ID' in df.columns:
            accused_ids = df['Accused_ID'].unique()
            selected_accused_id = st.selectbox("Accused ID", accused_ids)
            
            # Find the row corresponding to the selected Accused ID
            selected_rows = df[df['Accused_ID'] == selected_accused_id]
            
            if not selected_rows.empty:
                # Display selected documents
                st.subheader("Selected Documents:")
                st.write(selected_rows)
                if len(selected_rows) > 1:
                    # If there are multiple rows, ask user to select one
                    row_numbers = selected_rows.index.tolist()  # Get the index (actual row numbers) of selected rows
                    selected_row_number = st.selectbox("Select Row Number:", row_numbers)
                    selected_row = selected_rows.loc[[selected_row_number]]
                    st.subheader("Selected Document:")
                    st.write(selected_row)

                else:
                    selected_row = selected_rows.iloc[0:1].copy()   # Only one row, so select it directly
                # Pass the row to process_accused_data function
                process_accused_data(selected_row)

def accident_reports_page():
    st.title("Accident Reports")
    # Add content specific to Accident Reports page
    # File uploader for CSV file
    st.write("Upload Accident Reports CSV file:")
    uploaded_file = st.file_uploader("", type=["csv"])
    
    # Add disclaimer
    st.write("*If file size is greater than the 200 MB limit, try making chunks of the file and uploading smaller files.")
    
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the DataFrame
        st.write("Preview of uploaded data:")
        st.write(df)
        
        # Dropdown to select Crime No.
        if 'Crime_No' in df.columns:
            crime_numbers = df['Crime_No'].unique()
            selected_crime_no = st.selectbox("Crime No.", crime_numbers)
            
            # Find the row corresponding to the selected Crime No.
            selected_rows = df[df['Crime_No'] == selected_crime_no]
            
            if not selected_rows.empty:
                # Display selected documents
                st.subheader("Selected Documents:")
                st.write(selected_rows)
                if len(selected_rows) > 1:
                    # If there are multiple rows, ask user to select one
                    row_numbers = selected_rows.index.tolist()  # Get the index (actual row numbers) of selected rows
                    selected_row_number = st.selectbox("Select Row Number:", row_numbers)
                    selected_row = selected_rows.loc[[selected_row_number]]
                    st.subheader("Selected Document:")
                    st.write(selected_row)

                else:
                    selected_row = selected_rows.iloc[0:1].copy()   # Only one row, so select it directly
                # Pass the row to process_accident_reports_data function
                process_accident_reports_data(selected_row)

def fir_details_page():
    st.title("FIR Details")
    # Add content specific to FIR Details page
    # File uploader for CSV file
    st.write("Upload FIR Details CSV file:")
    uploaded_file = st.file_uploader("", type=["csv"])
    
    # Add disclaimer
    st.write("*If file size is greater than the 200 MB limit, try making chunks of the file and uploading smaller files.")
    
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the DataFrame
        st.write("Preview of uploaded data:")
        st.write(df)
        
        # Dropdown to select FIRNo
        if 'FIRNo' in df.columns:
            fir_numbers = df['FIRNo'].unique()
            selected_fir = st.selectbox("FIR No.", fir_numbers)
            
            # Find the row corresponding to the selected FIR Number
            selected_rows = df[df['FIRNo'] == selected_fir]
            
            if not selected_rows.empty:
                # Display selected documents
                st.subheader("Selected Documents:")
                st.write(selected_rows)
                if len(selected_rows) > 1:
                    # If there are multiple rows, ask user to select one
                    row_numbers = selected_rows.index.tolist()  # Get the index (actual row numbers) of selected rows
                    selected_row_number = st.selectbox("Select Row Number:", row_numbers)
                    selected_row = selected_rows.loc[[selected_row_number]]
                    st.subheader("Selected Document:")
                    st.write(selected_row)

                else:
                    selected_row = selected_rows.iloc[0:1].copy()   # Only one row, so select it directly
                # Pass the row to process_fir_details_data function
                process_fir_details_data(selected_row)

def complainant_details_page():
    st.title("Complainant Details")
    # Add content specific to Complainant Details page
    # File uploader for CSV file
    st.write("Upload Complainant Details CSV file:")
    uploaded_file = st.file_uploader("", type=["csv"])
    
    # Add disclaimer
    st.write("*If file size is greater than the 200 MB limit, try making chunks of the file and uploading smaller files.")
    
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the DataFrame
        st.write("Preview of uploaded data:")
        st.write(df)
        
        # Dropdown to select Complaint ID
        if 'Complaint_ID' in df.columns:
            complaint_ids = df['Complaint_ID'].unique()
            selected_complaint = st.selectbox("Complaint ID", complaint_ids)
            
            # Find the row corresponding to the selected Complaint ID
            selected_rows = df[df['Complaint_ID'] == selected_complaint]
            
            if not selected_rows.empty:
                # Display selected documents
                st.subheader("Selected Documents:")
                st.write(selected_rows)
                if len(selected_rows) > 1:
                    # If there are multiple rows, ask user to select one
                    row_numbers = selected_rows.index.tolist()  # Get the index (actual row numbers) of selected rows
                    selected_row_number = st.selectbox("Select Row Number:", row_numbers)
                    selected_row = selected_rows.loc[[selected_row_number]]
                    st.subheader("Selected Document:")
                    st.write(selected_row)

                else:
                    selected_row = selected_rows.iloc[0:1].copy()   # Only one row, so select it directly
                # Pass the row to process_complainant_details_data function
                process_complainant_details_data(selected_row)

def mob_details_page():
    st.title("MOB Details")
    # Add content specific to MOB Details page
    # File uploader for CSV file
    st.write("Upload MOB Details CSV file:")
    uploaded_file = st.file_uploader("", type=["csv"])
    
    # Add disclaimer
    st.write("*If file size is greater than the 200 MB limit, try making chunks of the file and uploading smaller files.")
    
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the DataFrame
        st.write("Preview of uploaded data:")
        st.write(df)
        
        # Dropdown to select MOB ID
        if 'Mob_ID' in df.columns:
            mob_ids = df['Mob_ID'].unique()
            selected_mob = st.selectbox("MOB ID", mob_ids)
            
            # Find the row corresponding to the selected MOB ID
            selected_rows = df[df['Mob_ID'] == selected_mob]
            
            if not selected_rows.empty:
                # Display selected documents
                st.subheader("Selected Documents:")
                st.write(selected_rows)
                # Pass the row to process_mob_data function
                if len(selected_rows) > 1:
                    # If there are multiple rows, ask user to select one
                    row_numbers = selected_rows.index.tolist()  # Get the index (actual row numbers) of selected rows
                    selected_row_number = st.selectbox("Select Row Number:", row_numbers)
                    selected_row = selected_rows.loc[[selected_row_number]]
                    st.subheader("Selected Document:")
                    st.write(selected_row)

                else:
                    selected_row = selected_rows.iloc[0:1].copy()   # Only one row, so select it directly
                process_mob_data(selected_row)

def arrest_person_details_page():
    st.title("Arrest Person Details")
    # Add content specific to Arrest Person Details page
    # File uploader for CSV file
    st.write("Upload Arrest Person Details CSV file:")
    uploaded_file = st.file_uploader("", type=["csv"])
    
    # Add disclaimer
    st.write("*If file size is greater than the 200 MB limit, try making chunks of the file and uploading smaller files.")
    
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the DataFrame
        st.write("Preview of uploaded data:")
        st.write(df)
        
        # Dropdown to select Person ID
        if 'Person_ID' in df.columns:
            person_ids = df['Person_ID'].unique()
            selected_person = st.selectbox("Person ID", person_ids)
            
            # Find the row corresponding to the selected Person ID
            selected_rows = df[df['Person_ID'] == selected_person]
            
            if not selected_rows.empty:
                # Display selected documents
                st.subheader("Selected Documents:")
                st.write(selected_rows)
                if len(selected_rows) > 1:
                    # If there are multiple rows, ask user to select one
                    row_numbers = selected_rows.index.tolist()  # Get the index (actual row numbers) of selected rows
                    selected_row_number = st.selectbox("Select Row Number:", row_numbers)
                    selected_row = selected_rows.loc[[selected_row_number]]
                    st.subheader("Selected Document:")
                    st.write(selected_row)

                else:
                    selected_row = selected_rows.iloc[0:1].copy()   # Only one row, so select it directly
                # Pass the row to process_arrest_person_data function
                process_arrest_person_data(selected_row)

def charge_sheeted_details_page():
    st.title("Charge Sheeted Details")
    # Add content specific to Charge Sheeted Details page
    # File uploader for CSV file
    st.write("Upload Charge Sheeted Details CSV file:")
    uploaded_file = st.file_uploader("", type=["csv"])
    
    # Add disclaimer
    st.write("*If file size is greater than the 200 MB limit, try making chunks of the file and uploading smaller files.")
    
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the DataFrame
        st.write("Preview of uploaded data:")
        st.write(df)
        
        # Dropdown to select Crime No
        if 'Crime_No' in df.columns:
            crime_numbers = df['Crime_No'].unique()
            selected_crime = st.selectbox("Crime No.", crime_numbers)
            
            # Find the row corresponding to the selected Crime No
            selected_rows = df[df['Crime_No'] == selected_crime]
            
            if not selected_rows.empty:
                # Display selected documents
                st.subheader("Selected Documents:")
                st.write(selected_rows)
                if len(selected_rows) > 1:
                    # If there are multiple rows, ask user to select one
                    row_numbers = selected_rows.index.tolist()  # Get the index (actual row numbers) of selected rows
                    selected_row_number = st.selectbox("Select Row Number:", row_numbers)
                    selected_row = selected_rows.loc[[selected_row_number]]
                    st.subheader("Selected Document:")
                    st.write(selected_row)

                else:
                    selected_row = selected_rows.iloc[0:1].copy()   # Only one row, so select it directly
                # Pass the row to process_charge_sheeted_data function
                process_charge_sheeted_data(selected_row)


def victim_info_details_page():
    st.title("Victim Info Details")
    # Add content specific to Victim Info Details page
    # File uploader for CSV file
    st.write("Upload Victim Info Details CSV file:")
    uploaded_file = st.file_uploader("", type=["csv"])
    
    # Add disclaimer
    st.write("*If file size is greater than the 200 MB limit, try making chunks of the file and uploading smaller files.")
    
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the DataFrame
        st.write("Preview of uploaded data:")
        st.write(df)
        
        # Dropdown to select Victim ID
        if 'Victim_ID' in df.columns:
            victim_ids = df['Victim_ID'].unique()
            selected_victim = st.selectbox("Victim ID", victim_ids)
            
            # Find the row corresponding to the selected Victim ID
            selected_rows = df[df['Victim_ID'] == selected_victim]
            
            if not selected_rows.empty:
                # Display selected documents
                st.subheader("Selected Documents:")
                st.write(selected_rows)
                if len(selected_rows) > 1:
                    # If there are multiple rows, ask user to select one
                    row_numbers = selected_rows.index.tolist()  # Get the index (actual row numbers) of selected rows
                    selected_row_number = st.selectbox("Select Row Number:", row_numbers)
                    selected_row = selected_rows.loc[[selected_row_number]]
                    st.subheader("Selected Document:")
                    st.write(selected_row)

                else:
                    selected_row = selected_rows.iloc[0:1].copy()   # Only one row, so select it directly
                # Pass the row to process_victim_info_data function
                process_victim_info_data(selected_row)

#MAIN------------------------------------------------------------------------------------------------------------
def main():
    st.title("RAKSHISU")
    st.write("Choose the file types you want to work with:")

    # Define options for file types
    file_types = {
        "FIR Details": fir_details_page,
        "Rowdy Sheeter Details": rowdy_sheeter_details_page,
        "Arrest Person": arrest_person_details_page,
        "MOB Data": mob_details_page,
        "Victim Info Details": victim_info_details_page,
        "Complainant Details": complainant_details_page,
        "Charge Sheeted Details": charge_sheeted_details_page,
        "Accused Data": accused_details_page,
        "Accident Reports": accident_reports_page
    }

    # Multiselect widget to select file types
    selected_file_type = st.selectbox("", list(file_types.keys()))

    # Render selected file type pages
    # Render selected file type page
    file_types[selected_file_type]()

if __name__ == "__main__":
    main()
