import sys
sys.path.insert(0, '../../DataPreprocessing')
from ContractFormater import SourceCodeFormater
import re

# We only want to extract functions and modifiers as the main code gadget from the contract


class CodeExtractor:
    def __init__(self):
        self.formatter = SourceCodeFormater(None)

    def extract_blocks_range(self, parsed_code):
        blocks_range = []
        accumulate_blocks = []

        for contract in parsed_code:
            if contract != 'vars':
                for item in parsed_code[contract]:
                    if item not in ['end', 'start', 'vars']:
                        new_block = (
                            parsed_code[contract][item]['start'], parsed_code[contract][item]['end'])
                        blocks_range.append([new_block, contract])
                        accumulate_blocks.append(new_block)

                new_block = (parsed_code[contract]['start'],
                             parsed_code[contract]['end'])
                blocks_range.append([new_block, accumulate_blocks])
                accumulate_blocks = []

        return blocks_range

    def extract_contracts_range(self, parsed_code):
        blocks_range = []

        for contract in parsed_code:
            if contract != 'vars':
                new_block = (parsed_code[contract]['start'],
                             parsed_code[contract]['end'])
                blocks_range.append([new_block, None])

        return blocks_range

    def extract_code_gadgets(self, blocks_range, source):
        code_gadgets = []

        for (start, end), item in blocks_range:
            try:
                code_block = "\n".join(source.splitlines()[start:end + 1])
                # Process the code_block here
            except Exception as e:
                continue

            if isinstance(item, list):
                lines = source.splitlines()
                total_deleted = 0
                # Delete the lines specified in the list of line ranges
                for substart, subend in reversed(item):
                    total_deleted += (subend - substart) + 1
                    del lines[substart:subend + 1]

                # Join the lines within the variable range back into a single string
                code_block = '\n'.join(lines[start:end - total_deleted + 1])

            if isinstance(item, str):
                code_block = item + '\n' + code_block

            code_gadgets.append(code_block)

        return code_gadgets

    def run(self, filename):
        source, parsed = self.formatter.formatted_and_parsed_source(filename)
        blocks_range = self.extract_contracts_range(parsed)
        code_gadgets = self.extract_code_gadgets(blocks_range, source)
        return code_gadgets


# extractor = CodeExtractor()
# code_gadgets = extractor.run("../../Data_preprocessing/input.sol")
# for gadget in code_gadgets:
#     print(gadget + '\n')
