
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import geopandas as gpd
import os, ast
from dotenv import load_dotenv
from plotter import Plotter
from preprocessor import run_preprocessor


# ++++++++++++++++++++++++++++++++++++++++++ Configure page and Properties +++++++++++++++++++++++++++++++++++++++++
st.set_page_config(
    page_title="📊ECR Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": "mailto:john.e.omage@gmail.com",
        "Report a bug": "mailto:john.e.omage@gmail.com",
        "About": "# Want to reach out?",
    },
)


# set page title
st.title(":bulb: NGED Embedded Capacity Register: 2023 - 2028")

# ++++++++++++++++++++++++++++++++++++++++++ Cache and Load Data +++++++++++++++++++++++++++++++++++++++++

@st.cache_data
def load_data(filename='processed_ecr'):
    run_preprocessor()
    return gpd.read_file(f'./datastore/{filename}.geojson')

data = load_data('processed_ecr')


print(data.columns)





st.write('\n\n\n\n\n++++++++++++++++++++++++++++++++++++++++++')






st.dataframe(data)

#