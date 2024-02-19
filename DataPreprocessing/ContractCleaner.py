import re
import os
import shutil
import chardet
import json


class SourceCodeCleaner:
    def __init__(self, input_file=None, parsed_file=None, source_code=None):
        self.input_file = input_file
        self.parsed_file = parsed_file
        self.source_code = source_code
        self.parsed_source = None
        self.delete_ranges = []

    def read_input_file(self):
        try:
            with open(self.input_file, 'rb') as file:
                raw_data = file.read()
                detected_encoding = chardet.detect(raw_data)['encoding']
                if detected_encoding:
                    self.source_code = raw_data.decode(detected_encoding)
                else:
                    # If encoding detection fails, fall back to UTF-8
                    self.source_code = raw_data.decode('utf-8')
        except UnicodeDecodeError:
            # Handle the case where decoding still fails
            print(f"Error: Unable to decode file '{self.input_file}'")
            self.source_code = None  # Set the source_code to None to indicate an error

        try:
            with open(self.parsed_file, "r") as json_file:
                self.parsed_source = json.load(json_file)

        except FileNotFoundError:
            print(f"Error: {self.parsed_file} not found")
            exit(1)

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            # Log the JSON parsing error to the log file
            with open("error.log", "a") as log_file:
                log_file.write(f"Error parsing JSON:\n{e}\n")

    def remove_comments(self):
        # remove all occurrences streamed comments (/*COMMENT */) from string
        self.source_code = re.sub(re.compile(
            "/\*.*?\*/", re.DOTALL), "", self.source_code)
        # remove all occurrence single-line comments (//COMMENT\n ) from string
        self.source_code = re.sub(re.compile("//.*?\n"), "", self.source_code)

    def remove_multiple_spaces(self):
        self.source_code = re.sub(r' +', ' ', self.source_code)

    def format_within_parentheses(self):
        pattern = r'\(([^()]*((?:\([^()]*\))[^()]*)*)\)'
        self.source_code = re.sub(pattern, lambda match: '(' + re.sub(
            r' {2,}', ' ', match.group(1).replace('\n', '')) + ')', self.source_code)

    def remove_redundant_line_breaks(self):
        lines = self.source_code.split('\n')
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        self.source_code = '\n'.join(cleaned_lines)

    def clean_source_code(self):
        self.remove_comments()
        self.format_within_parentheses()
        self.remove_redundant_line_breaks()
        self.remove_multiple_spaces()

    def delete_lines_in_ranges(self, lines):
        # Create a set of line numbers to be deleted
        lines_to_delete = set()
        for start, end in self.delete_ranges:
            for line_num in range(start, end + 1):
                lines_to_delete.add(line_num)

        # Create a list of lines with blank lines for the ones to be deleted
        cleaned_lines = []
        for line_num, line in enumerate(lines, start=1):
            if line_num in lines_to_delete:
                # Add a blank line for the line to be deleted
                cleaned_lines.append('')
            else:
                # Add the original line
                cleaned_lines.append(line)

        return cleaned_lines, lines_to_delete

    def traverse_ast(self, node):
        if isinstance(node, dict):
            # Check if the node has a 'type' key
            if 'type' in node:

                if 'loc' in node:
                    start = node["loc"]["start"]["line"]
                    end = node["loc"]["end"]["line"]

                    node_type = node['type']

                    # Check if the node is of type 'ContractDefinition' and has a 'kind' key
                    if node_type == 'ContractDefinition' and 'kind' in node:
                        node_kind = node['kind']

                        # Check if the node is of kind 'library' or 'interface'
                        if node_kind == 'library' or node_kind == 'interface':
                            # Process the node as needed
                            self.delete_ranges.append((start, end))
                    if node_type == 'FunctionDefinition':
                        if 'stateMutability' in node:
                            node_state = node['stateMutability']

                            if node_state == 'view' or node_state == 'pure':
                                self.delete_ranges.append((start, end))
                        if "body" in node:
                            node_body = node['body']

                            if node_body is None:
                                self.delete_ranges.append((start, end))
                            elif 'statements' in node_body and not len(node_body['statements']):
                                self.delete_ranges.append((start, end))

                    # Add more conditions for other node types as needed
                    elif node_type == 'PragmaDirective':
                        # Process PragmaDirective nodes
                        self.delete_ranges.append((start, end))
                    elif node_type == 'ImportDirective':
                        # Process ImportDirective nodes
                        self.delete_ranges.append((start, end))
                    elif node_type == 'EmitStatement':
                        self.delete_ranges.append((start, end))
                    elif node_type == 'EventDefinition':
                        self.delete_ranges.append((start, end))


            # Recursively traverse the child nodes
            for key, value in node.items():
                if key != 'loc':
                    self.traverse_ast(value)
        elif isinstance(node, list):
            # Recursively traverse each element in the list
            for item in node:
                self.traverse_ast(item)
    def removal(self):
        self.traverse_ast(self.parsed_source)
        lines = self.source_code.split('\n')
        cleaned_lines, lines_to_delete = self.delete_lines_in_ranges(lines)
        self.source_code = '\n'.join(cleaned_lines)
        return lines_to_delete
