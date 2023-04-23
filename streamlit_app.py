import streamlit as st
from annotated_text import annotated_text
import difflib
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import requests

API_URL = "https://api-inference.huggingface.co/models/team-writing-assistant/t5-base-c4jfleg"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def diff_strings(a, b):
    result = []
    diff = difflib.Differ().compare(a.split(), b.split())
    replacement = ""
    
    for line in diff:
        if line.startswith("  "):
            if len(replacement) == 0:
                result.append(" ")
                result.append(line[2:])
            else:
                result.append(" ")
                result.append(("", replacement, "#ffd"))
                replacement = ""
                result.append(line[2:])
        elif line.startswith("- "):
            if len(replacement) == 0:
                replacement = line[2:]
            else:
                result.append(" ")
                result.append(("", replacement, "#fdd"))
                replacement = ""
        elif line.startswith("+ "):
            if len(replacement) == 0:
                result.append((line[2:], "", "#dfd"))
            else:
                result.append(" ")
                result.append((line[2:], replacement, "#ddf"))
                replacement = ""
                
    return result
  
st.set_page_config(
        page_title="Replicating Grammarly",
)

st.markdown("# Replicating Grammarly <img src=\"https://imgs.search.brave.com/EYFiTdavQZV6Nf2kfIm7zvJvzKisli4smRZPbjYZ-P8/rs:fit:667:667:1/g:ce/aHR0cHM6Ly9jYXBp/Y2hlLmNvbS9yYWls/cy9hY3RpdmVfc3Rv/cmFnZS9ibG9icy9l/eUpmY21GcGJITWlP/bnNpYldWemMyRm5a/U0k2SWtKQmFIQkJj/MmRDSWl3aVpYaHdJ/anB1ZFd4c0xDSndk/WElpT2lKaWJHOWlY/MmxrSW4xOS0tMDA0/MzMzY2IzN2I4NjEy/MzgyNzNjNjcwNGY3/OTc4N2NkYTUyOTkx/YS9HcmFtbWFybHku/cG5n\" alt=\"logo\" height=\"50px\" width=\"50px\" />", unsafe_allow_html=True)
st.markdown("## GECToR – Grammatical Error Correction: Tag, Not Rewrite \n This project is PyTorch implementation of the following paper: \n> [GECToR – Grammatical Error Correction: Tag, Not Rewrite](https://aclanthology.org/2020.bea-1.16/)")
st.markdown("Grammarly is a writing assistant that detects 🔍 and corrects ✍️ grammatical mistakes for you!")
st.subheader("Example text: ")

col1, col2 = st.columns([1, 1])

with col1:
    example_1 = st.button("Speed of light is fastest then speed of sound")
with col2:
    example_2 = st.button("Who are the president?")
    
input_text = st.text_area('Enter your text here')
button = st.button('Submit')

def output(text):
    with st.spinner('Detecting 🔍..'):
        text = "grammar: " + text
        result = query({"inputs": text, "wait_for_model":True})
        
        diff = diff_strings(text[9:], result[0]['generated_text'])
        annotated_text(*diff)
        
        copy_button = Button(label="Copy the Result")
        copy_button.js_on_event("button_click", CustomJS(args=dict(result=result[0]['generated_text']), code="""
            navigator.clipboard.writeText(result);
            """))
        
        streamlit_bokeh_events(
            copy_button,
            events="GET_TEXT",
            key="get_text",
            refresh_on_update=True,
            override_height=75,
            debounce_time=0)
        
if example_1:
    output("Speed of light is fastest then speed of sound")
elif example_2:
    output("Who are the president?")
elif input_text:
    output(input_text)