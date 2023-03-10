# This code has been developed by Fundació Privada Internet i Innovació Digital a Catalunya (i2CAT)
import pandas as pd
import json
import AI_Engine.core.utils as utils
from typing import List

"""
    matchers = ['Application Log: Application Log Content', 'Firewall: Firewall Rule Modification', 'Firewall: Firewall Disable',
            'Firewall: Firewall Metadata ', 'Firewall: Firewall Enumeration', 'Network Traffic: Network Traffic Content', 
            'Network Traffic: Network Traffic Flow', "Network Traffic: Network Connection Creation",
            "Domain Name: Active DNS", "Certificate: Certificate Registration", "User Account: User Account Authentication", 
            "User Account: User Account Creation", "User Account: User Account Deletion", 
            "User Account: User Account Modification", "User Account: User Account Metadata", 
            "User Account: User Account Modification", "Process: OS API Execution", "Process: Process Access", 
            "Process: Process Creation", "Process: Process Metadata", "Process: Process Modification", 
            "Process: Process Termination", "Windows Registry: Windows Registry Key Access", 
            "Windows Registry: Windows Registry Key Creation", "Windows Registry: Windows Registry Key Deletion", 
            "Windows Registry: Windows Registry Key Modification"]
"""

def dataSources2techniques(used_data_sources: List) -> dict: 
    print(used_data_sources)
    matchers = [matcher.split(': ')[1] for matcher in used_data_sources]
    techniques_to_use = []
    data_sources = pd.read_csv("data/mapping/data_sources.csv")

    for _, row in data_sources.iterrows():
        if row['data_component'] in matchers:
            techniques_to_use.append(row['technique_id'])
    
    complete, partial, missing = [], [], []
    techniques_dict = {}
   
    for _, technique in data_sources['technique_id'].iteritems():
        tech_used_count = techniques_to_use.count(technique)
        tech_count = (data_sources["technique_id"] == technique).sum()
        if  tech_used_count == 0: missing.append(technique) 
        elif tech_used_count < tech_count: partial.append(technique) # Aquí és on potser es pot usar el gradient
        elif tech_used_count == tech_count: complete.append(technique) 
    
    techniques_dict["#8cdd69"] = list(set(sorted(complete))) # Complete
    techniques_dict["#ffd966"] = list(set(sorted(partial))) # Partial
    techniques_dict["#ed4f4f"] = list(set(sorted(missing))) # Missing

    techniques_dict = utils.exchange_key_value(techniques_dict)

    return techniques_dict
    










