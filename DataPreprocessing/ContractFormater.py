import re
from ContractCleaner import SourceCodeCleaner


class SourceCodeFormater:
    def __init__(self, source_code, parsed_code, deleted_lines):
        self.source_code = source_code
        self.parsed_code = parsed_code
        self.deleted_lines = deleted_lines
        self.contract_mapping = {}
        self.inheritance_link = {}
        self.counters = {
            'contract_counters': 0,
            'function_counters': 0,
            'variable_counters': 0,
            'modifier_counters': 0
        }

    def replace_in_range(self, key, replacement, r):

        # Split the source code into lines
        lines = self.source_code.split('\n')

        if r is None:
            r = [0, len(lines)]

        # Use regex with word boundaries to perform a strict replacement
        pattern = r'\b' + re.escape(key) + r'\b'
        for line_number in range(r[0] - 1, r[1]):
            try:
                # Perform the pattern replacement for the current line
                lines[line_number] = re.sub(
                    pattern, replacement, lines[line_number])
            except Exception as e:
                print(
                    f"An exception occurred at line {line_number}: {str(e)}")
                # Handle the exception as needed, e.g., logging, error reporting, etc.

        # Join the modified lines back into a string
        self.source_code = '\n'.join(lines)
    
    def format_inheritance(self):

        #Add the inheritance sub links

        for contract in self.inheritance_link.keys():
            links = self.inheritance_link[contract]['links']
            sub_link = set()
            for link in links:
               if link in self.inheritance_link:
                sub_link.update(self.inheritance_link[link]['links'])
            self.inheritance_link[contract]['links'].update(sub_link)
            
        # Format with the complete inheritance links

        for contract in self.inheritance_link.keys():
            loc = self.inheritance_link[contract]['loc']
            links = self.inheritance_link[contract]['links']
            for link in links:
                if link in self.contract_mapping:
                    for component in self.contract_mapping[link]:
                        self.replace_in_range(component[0], component[1], r=loc)

    def format_source(self, node, parent_node=None, grandparent_node=None):
        if isinstance(node, dict):
            # Recursively traverse the child nodes
            if 'type' in node:
                if 'loc' in node:
                    node_type = node['type']

                    if node_type == 'ContractDefinition':
                        if node['loc']['start']['line'] not in self.deleted_lines and node['loc']['end']['line'] not in self.deleted_lines:
                            self.counters['contract_counters'] += 1
                            new_contract_name = f'CONT{self.counters["contract_counters"]}'
                            if 'name' in node and (node['name'] is not None and node['name'].strip() != ''):
                                node_name = node['name']
                                self.replace_in_range(node_name, new_contract_name, r=None)

                                self.inheritance_link.setdefault(node_name, {})['loc'] = (
                                    node['loc']['start']['line'],
                                    node['loc']['end']['line']
                                )

                                links = set()

                                if 'baseContracts' in node and len(node['baseContracts']) > 0:
                                    for base_contract in node['baseContracts']:
                                        if base_contract['type'] == 'InheritanceSpecifier':
                                            links.add(base_contract['baseName']['namePath'])

                                self.inheritance_link[node_name]['links'] = links


                    if node_type == 'VariableDeclaration':
                        if node['loc']['start']['line'] not in self.deleted_lines and node['loc']['end']['line'] not in self.deleted_lines:
                            self.counters['variable_counters'] += 1
                            new_variable_name = f'VAR{self.counters["variable_counters"]}'
                            if 'name' in node and (node['name'] is not None and node['name'].strip() != ''):
                                node_name = node['name']
                        
                                if parent_node is not None and 'type' in parent_node:
                                    if parent_node['type'] == 'StateVariableDeclaration' or parent_node['type'] == 'VariableDeclarationStatement':
                                        if grandparent_node is not None and 'type' in grandparent_node:
                                            if 'loc' in grandparent_node:
                                                grandparent_start = grandparent_node["loc"]["start"]["line"]
                                                grandparent_end = grandparent_node["loc"]["end"]["line"]
                                                self.replace_in_range(node_name, new_variable_name, r=[grandparent_start, grandparent_end])

                                                if 'name' in grandparent_node:
                                                    self.contract_mapping.setdefault(grandparent_node['name'], []).append((node_name, new_variable_name))
                                    else: 
                                        if 'loc' in parent_node:
                                            parent_start = parent_node["loc"]["start"]["line"]
                                            parent_end = parent_node["loc"]["end"]["line"]
                                            self.replace_in_range(node_name, new_variable_name, r=[parent_start, parent_end])
                                            
                    if node_type == 'ModifierDefinition':
                        if node['loc']['start']['line'] not in self.deleted_lines and node['loc']['end']['line'] not in self.deleted_lines:
                            if 'name' in node and (node['name'] is not None and node['name'].strip() != ''):
                                self.counters['modifier_counters'] += 1
                                new_modifier_name = f'MOD{self.counters["modifier_counters"]}'
                                node_name = node['name']
                                if parent_node is not None and 'type' in parent_node:
                                    if 'loc' in parent_node:
                                        self.contract_mapping.setdefault(parent_node['name'], []).append((node_name, new_modifier_name))
                                        parent_start = parent_node["loc"]["start"]["line"]
                                        parent_end = parent_node["loc"]["end"]["line"]
                                        self.replace_in_range(node_name, new_modifier_name, r=[parent_start, parent_end])

                    if node_type == 'FunctionDefinition':
                        if node['loc']['start']['line'] not in self.deleted_lines and node['loc']['end']['line'] not in self.deleted_lines:
                            if 'name' in node and (node['name'] is not None and node['name'].strip() != ''):
                                self.counters['function_counters'] += 1
                                new_function_name = f'FUN{self.counters["function_counters"]}'
                                node_name = node['name']
                                if parent_node is not None and 'type' in parent_node:
                                    if 'loc' in parent_node:
                                        self.contract_mapping.setdefault(parent_node['name'], []).append((node_name, new_function_name))
                                        parent_start = parent_node["loc"]["start"]["line"]
                                        parent_end = parent_node["loc"]["end"]["line"]
                                        self.replace_in_range(node_name, new_function_name, r=[parent_start, parent_end])

            for key, value in node.items():
                if key != 'loc':
                    # Pass the parent and grandparent nodes when recursively calling format_source
                    self.format_source(value, parent_node=node, grandparent_node=parent_node)
        elif isinstance(node, list):
            # Recursively traverse each element in the list
            for item in node:
                # Pass the parent and grandparent nodes when recursively calling format_source
                self.format_source(item, parent_node=parent_node, grandparent_node=grandparent_node)


cleaner = SourceCodeCleaner('sample-input.sol', 'sample-output.json')
cleaner.read_input_file()
deleted_lines = cleaner.removal()
formatter = SourceCodeFormater(cleaner.source_code, cleaner.parsed_source, deleted_lines)

formatter.format_source(formatter.parsed_code)
formatter.format_inheritance()

cleaner = SourceCodeCleaner(source_code=formatter.source_code)
cleaner.clean_source_code()

print(cleaner.source_code)