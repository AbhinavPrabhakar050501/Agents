import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.genai import upload,get
import google.genai as genai
import time
from pathlib import Path

import tempfile

from dotenv import load_dotenv
load_dotenv()

import os
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

st.set_page_config(
    page_title = ""
    page_icon = 

)

st.title
st.header

@st.cache_resource
def initialise_agent():
    return Agent(
        name = "Video AI Summarizer",
    )