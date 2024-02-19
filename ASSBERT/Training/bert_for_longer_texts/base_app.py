"""

    Simple Streamlit webserver application for serving developed classification
	models.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within this directory for guidance on how to use this script
    correctly.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend the functionality of this script
	as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st
import joblib,os

# Data dependencies
import pandas as pd
from belt_nlp.bert_truncated import BertClassifierTruncated
# Load your raw data
raw = pd.read_csv("sample_data\ExperimentalModelDataset.csv")
MODEL_PARAMS = {
    "batch_size": 4,
    "learning_rate": 5e-5,
    "epochs": 1,
}
model = BertClassifierTruncated(**MODEL_PARAMS, device="cpu")
# The main function where we will build the actual app
def main():
	"""Smart Contract Vulnerabilities Detection """
	model.load("model_test", "cpu")
	# Creates a main title and subheader on your page -
	# these are static across all pages
	st.title("Smart Contract Classifer")
	st.subheader("Smart Contract Vulnerabilities classification")

	# Creating sidebar with selection box -
	# you can create multiple pages this way
	options = ["Prediction"]
	selection = st.sidebar.selectbox("Choose Option", options)
	
	# Building out the predication page
	if selection == "Prediction":
		st.info("Prediction with ML Models")
		# Creating a text box for user input
		contract_source = st.text_area("Enter Text","Type Here")

		if st.button("Classify"):
			prediction = model.predict_classes([contract_source])
			# When model has successfully run, will print prediction
			# You can use a dictionary or similar structure to make this output
			# more human interpretable.
			output = None
			if prediction[0] is False: output = "Vulnerable" 
			else: output = "Safe"
			st.success("Source code Categorized as: {}".format(output))

# Required to let Streamlit instantiate our web app.  
if __name__ == '__main__':
	main()
