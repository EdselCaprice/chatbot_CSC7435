import os
from dotenv import load_dotenv
load_dotenv()
state_listing = ['Alabama',	'Alaska',	'Arizona',	'Arkansas',	'California',	'Colorado',	'Connecticut',	'Delaware',	'District of Columbia',	'Florida',	'Georgia',	'Hawaii',	'Idaho',	'Illinois',	'Indiana',	'Iowa',	'Kansas',	'Kentucky',	'Louisiana',	'Maine',	'Maryland',	'Massachusetts',	'Michigan',	'Minnesota',	'Mississippi',	'Missouri',	'Montana',	'Nebraska',	'Nevada',	'New Hampshire',	'New Jersey',	'New Mexico',	'New York',	'North Carolina',	'North Dakota',	'Ohio',	'Oklahoma',	'Oregon',	'Pennsylvania',	'Rhode Island',	'South Carolina',	'South Dakota',	'Tennessee',	'Texas',	'Utah',	'Vermont',	'Virginia',	'Washington',	'West Virginia',	'Wisconsin', 'Wyoming',	'Foreign',	'Other']
import requests

def import_exclusion_rates_from_ss(tax_year):
    url = os.environ['ss_url'] + os.environ['exclusions_sheet']
    header = {"Authorization": "Bearer " + os.environ['ss_token']}
    r = requests.get(url, headers=header)
    response = r.json()
    results = {}
    for state in state_listing:
        results[state.lower()] = {}
    for column in response["columns"]:
        if column['title'] == tax_year:
            column_index = int(column['index'])
            for row in response["rows"]:
                category = row["cells"][1]["value"]
                exclusion_rate = row["cells"][column_index]["value"]
                state = row["cells"][0]["value"]
                results[state].update({category: exclusion_rate})
    return results

def import_nexus_thresholds_from_ss():
    url = os.environ['ss_url'] + os.environ['nexus_sheet']
    header = {"Authorization": "Bearer " + os.environ['ss_token']}
    temp_table = {"Table": {}}
    r = requests.get(url, headers=header)
    response = r.json()
    for row in response["rows"]:
      state = row["cells"][0]["value"]
      try:
        dollar_threshold = row["cells"][1]["value"] if row["cells"][1]["value"] != 'n/a' else 0
        transaction_threshold = row["cells"][2]["value"] if row["cells"][2]["value"] != 'n/a' else 0
        and_or = row["cells"][3]["value"]
        thresholds = {'dollar_threshold':dollar_threshold, 'transaction_threshold':transaction_threshold, 'and_or':and_or}
      except:
        print(f'Error importing economic threshold {state}')
        thresholds = {'dollar_threshold':0, 'transaction_threshold':0, 'and_or':0}
      temp_table["Table"].update({state: thresholds})
    return temp_table['Table']

def import_pre_post_nol_from_ss():
    url = os.environ['ss_url'] + os.environ['pre_post_sheet']
    header = {"Authorization": "Bearer " + os.environ['ss_token']}
    temp_table = {"Table": {}}
    r = requests.get(url, headers=header)
    response = r.json()
    for row in response["rows"]:
      state = row["cells"][0]["value"]
      try:
        imported_data = row["cells"][1]["value"]
      except:
        imported_data = 'Post'
      temp_table["Table"].update({state: imported_data})
    return temp_table['Table']

def import_tax_rates_from_ss(tax_year):
    url = os.environ['ss_url'] + os.environ['tax_rates_sheet']
    header = {"Authorization": "Bearer " + os.environ['ss_token']}
    r = requests.get(url, headers=header)
    response = r.json()
    compliance_table = {"compliance": {}}
    current_table = {"current_provision": {}}
    deferred_table = {"deferred_provision": {}}
    for column in response['columns']: #column represents a json object/python dictionary
       if column['title'] == tax_year:
            column_index = int(column['index'])
    for row in response["rows"]:
        state = row["cells"][0]["value"]
        state = state[0:len(state)-5]
        if row['cells'][1]["value"] == 'compliance':
            compliance_rate = row["cells"][column_index]["value"]
            compliance_table["compliance"].update({state: compliance_rate})
        elif row['cells'][1]["value"] == 'current':
            current_provision_rate = row["cells"][column_index]["value"]
            current_table["current_provision"].update({state: current_provision_rate})
        elif row['cells'][1]["value"] == 'deferred':
            deferred_provision_rate = row["cells"][column_index]["value"]
            deferred_table["deferred_provision"].update({state: deferred_provision_rate})
    #print(compliance_table['compliance'])
    return [compliance_table['compliance'], current_table['current_provision'], deferred_table['deferred_provision']]

def import_cfp_from_ss():
    url = os.environ['ss_url'] + os.environ['cfp_sheet']
    header = {"Authorization": "Bearer " + os.environ['ss_token']}
    r = requests.get(url, headers=header)
    response = r.json()
    full_table={}
    for column in response["columns"]:
      if column['index'] != 0:
        full_table[column["title"]] = {}
        for row in response["rows"]:
          year = row["cells"][0]["value"]
          try:
            data = row["cells"][column["index"]]["value"]
          except:
            data =0
          full_table[column["title"]].update({year: data})
    return full_table

def import_limitations_from_ss():
    url = os.environ['ss_url'] + os.environ['limitations_sheet']
    header = {"Authorization": "Bearer " + os.environ['ss_token']}
    r = requests.get(url, headers=header)
    response = r.json()
    full_table={}
    for column in response["columns"]:
      if column['index'] != 0:
        full_table[column["title"]] = {}
        for row in response["rows"]:
          year = row["cells"][0]["value"]
          try:
            data = row["cells"][column["index"]]["value"]
          except:
            data =0
          full_table[column["title"]].update({year: data})
    return full_table

def import_smartsheets_methodologies(tax_year):
    url = os.environ['ss_url'] + os.environ['methods_sheet']
    header = {"Authorization": "Bearer " + os.environ['ss_token']}
    r = requests.get(url, headers=header)
    print(r.status_code)
    response = r.json()
    for column in response['columns']: #column represents a json object/python dictionary
       if column['title'] == tax_year:
            column_index = int(column['index'])
    #column index 6 is deferred, column index 5 is 2023 and so on (response['cells'][5]). If column index changes in smartsheets when new columsn are added this will have to be revised. Consider using column ID intead of index.
    #state = response['rows'][0]['cells'][0]['value']
    method_listing = [] #will be formatted as list of dictionaries: [{state: 'alabama', method: 'single sales factor', year: 'current'}, {state: 'alabama', method:'single sales factor', year: 'deferred'}]
    for row in response["rows"]:
        state = row["cells"][0]["value"]
        state = state[0:len(state)-5]
        year = row['cells'][1]['value']
        method = row['cells'][column_index]["value"]
        method_listing.append({'state': state, 'method': method, 'year':year })
    return method_listing