import json
import random

json_file = 'experimental_contracts.json'

def load_json_data(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    vulnerabilities = []
    contracts_lists = []
    
    for item in data:
        vulnerability = item["vulnerability"]
        contracts = item["contracts"]
        
        vulnerabilities.append(vulnerability)
        contracts_lists.append(contracts)
    
    return vulnerabilities, contracts_lists

vulnerabilities, contracts_lists = load_json_data(json_file)

vul_type_mapping = {
    'access_control': 0,
    'arithmetic': 1,
    'denial_service': 2,
    'front_running': 3,
    'reentrancy': 4,
    'time_manipulation': 5,
    'unchecked_low_calls': 6,
    'non_vulnerable': 7
}


def load_contracts_data(vulnerabilities, contract_lists):
    labels = []
    type_labels = []
    contracts = []
    
    for i, vulnerability in enumerate(vulnerabilities):
        contracts.extend(contract_lists[i])
        type_labels.extend([vul_type_mapping[vulnerability]] * len(contract_lists[i]))
        labels.extend([1 if vulnerability == "non_vulnerable" else 0] * len(contract_lists[i]))
    
    return labels, type_labels, contracts

labels, type_labels, contracts = load_contracts_data(vulnerabilities, contracts_lists)

# Combine contracts, labels, and type_labels into a single list of tuples
data = list(zip(contracts, labels, type_labels))

# Shuffle the data while keeping the correspondence
random.shuffle(data)

# Unzip the shuffled data back into separate lists
shuffled_contracts, shuffled_labels, shuffled_type_labels = zip(*data)