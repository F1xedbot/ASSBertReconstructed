# ASSBertReconstructed

## Overview
ASSBertReconstructed is a project dedicated to implementing the proposed model from the paper [ASSBert: Active and semi-supervised BERT for smart contract vulnerability detection](https://www.sciencedirect.com/science/article/abs/pii/S221421262300008X).

### Project Goals
1. **Create Vocabulary for BERT:**
   - Generate a vocabulary for the NLP model BERT from the Solidity programming language.

2. **Normalize Smart Contract Source Code:**
   - Clean unwanted blank spaces, breaklines, and comments from the dataset.
   - Normalize contract names, modifier names, function names, and variable names with scope awareness. Standardize to a consistent format (VAR1, VAR2, FUN1, FUN2, ...).
   - Note: Normalization with scope awareness involves using the solidity-parser module to create an AST for a contract source code, facilitating easier scope access.

3. **Implement Sliding Window Technique:**
   - Use the sliding window technique to feed long/short contract source code into the BERT model for training.
   - Note: Due to BERT's limitation of handling only 512 tokens at a time, the contract source code is divided into meaningful chunks, stacked, and fed to BERT for training.

### Project Structure
Inside the project, two main folders are present: ASSBERT and DataPreprocessing.

#### ASSBERT Folder
- Contains code for end-to-end model implementation and training using an existing normalized smart contract dataset.
- Notebook: `ASSBERT/Training/ASSBERT_TRAIN.ipynb`

#### DataPreprocessing Folder
- Contains code to create a normalized dataset from an existing dataset, such as smartbugs. This dataset can be used to train a custom model.

## Usage
1. **BERT Vocabulary Creation:**
   - Execute code to generate a vocabulary for BERT from Solidity.

2. **Smart Contract Source Code Normalization:**
   - Utilize the provided normalization steps to clean and standardize the dataset.

3. **Sliding Window Technique:**
   - Implement the sliding window technique for feeding contract source code into the BERT model.

4. **Training (ASSBERT Folder):**
   - Refer to the notebook (`ASSBERT/Training/ASSBERT_TRAIN.ipynb`) for end-to-end model implementation and training.

5. **Data Preprocessing (DataPreprocessing Folder):**
   - Use the code in the DataPreprocessing folder to create a normalized dataset from an existing dataset like smartbugs.

This project is geared towards advancing smart contract vulnerability detection through active and semi-supervised learning with BERT. Contributions, feedback, and collaboration from the community are welcome to enhance and refine ASSBertReconstructed. Thank you for your interest and support!
