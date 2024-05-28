# pip3 install streamlit

import streamlit as st
import json
from collections import defaultdict


def content2columns(content):
    columns_data = defaultdict(dict)
    columns_info = content['modes']
    variables = content['variables']
    for variable in variables:
        for value in variable['resolvedValuesByMode']:
            langague = columns_info[str(value)]
            id_name = variable['name']
            lang_name = variable['resolvedValuesByMode'][value]['resolvedValue']
            columns_data[langague][id_name] = lang_name
    return columns_data

st.markdown("# Figma JSON to I18n JSON")
if 'json_data' not in st.session_state or st.session_state['json_data'] == "":
    st.markdown("""
    ## Get JSON file using Figma Extension "Export/Import Variables"
    1. Open your Figma project.
    2. Go to Plugins and search for ["Export/Import Variables"](https://www.figma.com/community/plugin/1256972111705530093).
    3. Use the extension to export your variables into a JSON file.
    4. Ensure the exported JSON matches the required input format for this project.""")
uploaded_file = st.file_uploader("Choose a JSON file", type="json",accept_multiple_files=False)
if uploaded_file is not None:
    # Read the file and convert to JSON
    input_data = json.load(uploaded_file)
    # Use st.session_state to cache the data
    st.session_state['json_data'] = input_data
else:
    st.session_state['json_data'] = ""
    st.warning("Please upload a JSON file.")



# You must check outside of the button press event if the session state has data to show it persistently.
if 'json_data' in st.session_state:
    if st.session_state['json_data'] != "":
        columns_data = content2columns(st.session_state['json_data'])
        tabs = st.tabs(columns_data.keys())
        for index, lang in enumerate(columns_data.keys()):
            with tabs[index]:
                data = json.dumps(columns_data[lang],indent=4,ensure_ascii=False)
                st.download_button("Download JSON File",data,lang+".json")
                st.json(columns_data[lang])

