import mitreattack.attackToExcel.attackToExcel as attackToExcel
import mitreattack.attackToExcel.stixToDf as stixToDf
import attackcti as attck
import pandas as pd
from pandas import json_normalize
import csv
from collections import Counter
import matplotlib.pyplot as plt
import json
import sys
from attackcti import attack_client


def get_attck_from_stix(matrix = 'enterprise'):
    if  (matrix.lower() == 'enterprise'):
        # Instantiating attack_client class
        lift = attack_client()
        # Getting techniques for windows platform - enterprise matrix
        attck = lift.get_enterprise_techniques(stix_format = False)
        # Removing revoked techniques
        attck = lift.remove_revoked_deprecated(attck)
        return attck
    else:
        sys.exit('ERROR: Only Enterprise available!!')


def get_attack_dataframe (matrix = 'enterprise'):
    if  (matrix.lower() == 'enterprise'):
        # Getting ATT&CK techniques
        attck = get_attck_from_stix(matrix = matrix)
        # Generating a dataframe with information collected
        attck = json_normalize(attck)
        # Selecting columns
        attck = attck[['technique_id','technique','tactic','platform','data_sources']]
        # Splitting data_sources field
        attck = attck.explode('data_sources').reset_index(drop=True)
        attck[['data_source','data_component']] = attck.data_sources.str.split(pat = ": ", expand = True)
        attck = attck.drop(columns = ['data_sources'])
        return attck
    else:
        sys.exit('ERROR: Only Enterprise available!!')

# attackToExcel.export("enterprise-attack", "v8.1", "data") 
# download and parse ATT&CK STIX data
attackdata = attackToExcel.get_stix_data("enterprise-attack", "v8.1")

attack = get_attack_dataframe()
attack.loc[0:,['technique_id', 'data_source', 'data_component']].to_csv("data_sources.csv")

aux = attackToExcel.build_dataframes(attackdata, "enterprise-attack")

# get Pandas DataFrames for techniques, associated relationships, and citations
t=techniques_data = stixToDf.techniquesToDf(attackdata, "enterprise-attack")
ss=software_data = stixToDf.softwareToDf(attackdata)


# show T1102 and sub-techniques of T1102
tt=techniques_df = techniques_data['techniques']
software_data_df = software_data['techniques used']


techniques_df.loc[0:, ["ID","data sources"]].to_csv("./dataframe_technique.csv")
software_data_df.to_csv("./dataframe_software.csv")


aux=[]
p_aux = []
phishing = []
matchers = ['Application Log: Application Log Content', 'Network Traffic: Network Traffic Content', 
            'Network Traffic: Network Traffic Flow', "Network Traffic: Network Connection Creation",
            "Domain Name: Active DNS", "Certificate: Certificate Registration", "User Account: User Account Authentication", 
            "User Account: User Account Creation", "User Account: User Account Deletion", 
            "User Account: User Account Modification", "User Account: User Account Metadata", 
            "User Account: User Account Modification", "Process: OS API Execution", "Process: Process Access", 
            "Process: Process Creation", "Process: Process Metadata", "Process: Process Modification", 
            "Process: Process Termination", "Windows Registry: Windows Registry Key Access", 
            "Windows Registry: Windows Registry Key Creation", "Windows Registry: Windows Registry Key Deletion", 
            "Windows Registry: Windows Registry Key Modification"]

matchers = [{'data source' : matcher.split(':')[0], 'data component' : matcher.split(':')[1]} for matcher in matchers]

with open('data-sources.json', 'w') as file:
    json.dump(matchers, file, indent=4)

##For every tool
for technique in software_data_df['target ID']:
    try:
        matching = []
        sources = [x.strip() for x in (tt.loc[tt['ID'] == technique]['data sources'].values[0].split(','))]
        # print('src identified:',technique, sources)
        matching = [s for s in sources if any(xs in s for xs in matchers)]
        if len(matching)>0:
            print('---SOURCES---\n',sources)            
    except:
        pass
    aux.extend(sources)

ttp_counter = Counter(aux)


with open("testfile", 'w') as f:
    for k,v in  ttp_counter.most_common():
        f.write( "{} {}\n".format(k,v) )
plt.bar(ttp_counter.keys(), ttp_counter.values())
# plt.show()
print(len(aux))
# get data sources given a ttp
print(tt.loc[tt['ID'] == 'T1102']['data sources'].values[0])