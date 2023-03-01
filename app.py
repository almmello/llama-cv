import openai
import os
from llama_index import GPTTreeIndex, GPTListIndex, GPTKeywordTableIndex, GPTSimpleVectorIndex, SimpleDirectoryReader, MockLLMPredictor

import streamlit as st

from dotenv import load_dotenv

# Authenticate with OpenAI
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

## Build a siedebar

# Add a title
st.sidebar.title("Settings")

# Add a combobox to select the LLM Model
selected_model = st.sidebar.selectbox("Select the LLM Model", ["text-davinci-003", "text-babbage-001"])

# Add a text box to input the temperature
temperature = st.sidebar.text_input("Temperature", value="0.5")

# Add a text box to input the max tokens
max_tokens = st.sidebar.text_input("Max Tokens", value="2048")

## Build a main page *** This is where the user will interact with the app not the sidebar ***

# Add a title
st.title("OpenAI Text Search")

# Add a button to check if there are indexes saved
check_indexes_button = st.button("Check if there are indexes saved")

# Add a button to load from saved indexes and it is disabled by default
load_indexes_button = st.button("Load from Saved Indexes")

# Add a button to build new indexes and it is disabled by default.
build_index_button = st.button("Build Indexes")

# Add a button to save the indexes, it is disabled by default
save_index_button = st.button("Save Indexes")

# Add a text box to input the query
query_txt = st.text_input("Enter a search query_txt")

# add a button to predict the query cost. It is enalbed by default
predict_query_cost_button = st.button("Predict Cost of Query")

# Add a button to execute the query and it is disabled by default
query_button = st.button("Search")


# Create global variables to store the indexes and use on the methods
global resume_index, projects_index, opportunity_index

# Create a method to check if there are indexes saved
if check_indexes_button:
    resume_index_exists = os.path.exists('index/resume_index.json')
    project_index_exists = os.path.exists('index/project_index.json')
    opportunity_index_exists = os.path.exists('index/opportunity_index.json')

    # if resume_index_exists and project_index_exists and opportunity_index_exists enable button to load from saved indexes
    #if resume_index_exists and project_index_exists and opportunity_index_exists:
        # Enable the button to load from saved indexes
        #load_indexes_button.diabled = False

        
# Create a method to load from saved indexes
if load_indexes_button:

    # Load the indexes from the saved files
    resume_index = GPTSimpleVectorIndex.load("index/resume_index.json")
    projects_index = GPTSimpleVectorIndex.load("index/project_index.json")
    opportunity_index = GPTSimpleVectorIndex.load("index/opportunity_index.json")

    # Enable search button
    #query_button.diabled = False


# Line 79: Predict the new indexes building costs.

# Add a method to build the new indexes
if build_index_button:
    # Load the data from the folders
    resume_data = SimpleDirectoryReader("data/resume").load_data()
    project_data = SimpleDirectoryReader("data/projects").load_data()
    opportunity_data = SimpleDirectoryReader("data/opportunity").load_data()

    # Create the indexes
    resume_index = GPTSimpleVectorIndex(documents=resume_data)
    projects_index = GPTSimpleVectorIndex(documents=project_data)
    opportunity_index = GPTSimpleVectorIndex(documents=opportunity_data)


    # Build the indexes
    resume_index.save_to_disk("index/resume_index.json")
    resume_index = GPTSimpleVectorIndex.load_from_disk("index/resume_index.json")
    projects_index.save_to_disk("index/project_index.json")
    projects_index = GPTSimpleVectorIndex.load_from_disk("index/project_index.json")
    opportunity_index.save_to_disk("index/opportunity_index.json")
    opportunity_index = GPTSimpleVectorIndex.load_from_disk("index/opportunity_index.json")

    # Enable the button to save the indexes
    #if save_index_button:
    #    st.session_state.disabled = False


    # Disable the button to load from saved indexes
    #if load_indexes_button:
    #    st.session_state.disabled = True

    # Enable the predict query cost button
    #if predict_query_cost_button:
     #   st.session_state.disabled = False


# Add a method to save the new indexes
if save_index_button:

    # Save the indexes to files
    resume_index.save("index/resume_index.json")
    projects_index.save("index/project_index.json")
    opportunity_index.save("index/opportunity_index.json")

    # Disable the button to save the indexes
    #save_index_button.diabled = True

    # Enable the button to build new indexes
    #build_index_button.diabled = False


# Add a method to estimate the cost of the query
if predict_query_cost_button:

    # Predict the cost of the query
    query_cost = opportunity_index.query_cost(query_txt)

    # Display the predicted cost to the user
    st.write("The predicted cost of the query is:", query_cost)

    # Enable the search button
    #query_button.diabled = False

# Add a method to execute the query
if query_button:

    # Search the opportunity index using the resume and projects indexes as context
    results = opportunity_index.query(query_txt, [resume_index, projects_index])

    # Display the results to the user
    #for result in results:
    st.write(results)

