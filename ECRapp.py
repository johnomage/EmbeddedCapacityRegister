
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



# ++++++++++++++++++++++++++++++++++++++++++ Cache and Load Data +++++++++++++++++++++++++++++++++++++++++

@st.cache_data
def load_data(filename='processed_ecr'):
    run_preprocessor()
    return gpd.read_file(f'./datastore/{filename}.geojson')

raw_data = load_data('processed_ecr')

# set page title
st.title(f":bulb: Live NGED Embedded Capacity Register Dashboard: 2023 - 2028 \n\tLast Updated: {raw_data['Last Updated'].max().strftime('%A, %d/%m/%Y')}")

def make_subheader(subheader):
    st.markdown(
    f"""
    <div style="text-align: center;">
        <b>++++++++++++++++++++ {subheader} ++++++++++++++++++++++++</b>
    </div>
    """, 
    unsafe_allow_html=True
)


# ++++++++++++++++++++++++++++++++++++++++++ Sidebar Filters +++++++++++++++++++++++++++++++++++++++++
def create_sidebar(label, feature, placeholder):
    df = raw_data[~raw_data[feature].isna()] 
    return st.sidebar.multiselect(
                                label=label,
                                options=df[feature].unique(),
                                default=df[feature].unique(),
                                placeholder=placeholder)

st.sidebar.header("Global Sliders")


# Licence Area silcer
licence_area_silcer = create_sidebar('Select DNO', 'Licence Area', 'Select DNO')

# Voltage Level Slicer
voltage_slicer = create_sidebar('Select Voltage', 'PoC Voltage (KV)', 'Voltage (KV)')


data = raw_data[(raw_data["Licence Area"].isin(licence_area_silcer) & raw_data["PoC Voltage (KV)"].isin(voltage_slicer))]

plotter = Plotter(data)



# ++++++++++++++++++++++++++++++++++++++++++ Metrics Container +++++++++++++++++++++++++++++++++++++++++
"---"
def format_MW_GW(capacity: float, feature):
    """
    Format and display capacity in KW or MW using based on capacity's value.

    Converts the input value to MW if it's 1000 or greater,
    otherwise displays it in KW. Uses Streamlit to render
    the formatted capacity with HTML styling.

    Args:
        value (float): Capacity value in KW
        feature (string): Name of capacity feature to convert
    """
    cap_value = capacity / 1000
    if cap_value < 1:  # Display in MW
        st.markdown(f"<b>{feature}</b><h3>{capacity:.2f}MW</h3>", unsafe_allow_html=True,)
    else:  # Display in MW
        st.markdown(f"<b>{feature}</b><h3>{cap_value:.4f}GW</h3>", unsafe_allow_html=True)


capacity_containers = st.columns(7)

with capacity_containers[0]:
    total_mpans = data.shape[0]
    st.markdown(f"<b>MPANs Count<h3>{total_mpans}</b></h3>", unsafe_allow_html=True)

with capacity_containers[1]:
    total_registered = data['Already connected Registered Capacity (MW)'].sum()
    format_MW_GW(total_registered, 'Already Connected')

with capacity_containers[2]:
    format_MW_GW(data['Accepted to Connect Registered Capacity (MW)'].sum(), 'Accepted to Connect')

with capacity_containers[3]:
    format_MW_GW(data['Maximum Export Capacity (MW)'].sum(), 'Max Export Capacity')

with capacity_containers[4]:
    format_MW_GW(data['Maximum Import Capacity (MW)'].sum(), 'Max Import Capacity')

with capacity_containers[5]:
    format_MW_GW(data['Change to Maximum Export Capacity (MW)'].astype('float').sum(), 'Change to Maximum Export')

with capacity_containers[6]:
    format_MW_GW(data['Change to Maximum Import Capacity (MW)'].astype('float').sum(), 'Change to Maximum Import')
"---"


# ++++++++++++++++++++++++++++++++++++++++++ Map Container +++++++++++++++++++++++++++++++++++++++++
st.plotly_chart(plotter.plotMap_of_MPANs())
"---"
st.markdown("\n")


# ++++++++++++++++++++++++++++++++++++++++++ Sunburst Container +++++++++++++++++++++++++++++++++++++++++
st.plotly_chart(plotter.plot_sunburst_LA_2_FSP(), use_container_width=True)
st.markdown("\n\n")




# ++++++++++++++++++++++++++++++++++++++++++ Energy Source Charts +++++++++++++++++++++++++++++++++++++++++


def show_source_cap_plots(source: str, source_number: int):
    make_subheader(f'{source} Capacities')
    st.plotly_chart(plotter.plot_energy_source_by_cap(source), use_container_width=True)

    source_containers = st.columns(2)
    with source_containers[0]:
        st.plotly_chart(plotter.plotTreeMap_energy_source_by_conv_tech(source, f'Energy Conversion Technology {source_number}', f'Reg_Cap_Energy_Source_Conv_Tech_{source_number}'))
    with source_containers[1]:
        st.plotly_chart(plotter.plotLineScatter_accpeted_over_time_by_source(f'Energy Source {source_number}', 'line'))
    st.write('\n')


show_source_cap_plots('Energy Source 1', 1)
show_source_cap_plots('Energy Source 2', 2)
show_source_cap_plots('Energy Source 3', 3)

"---"

make_subheader("Accepted Connect Capacity for All Sources")
st.plotly_chart(plotter.plotLineScatter_accpeted_over_time_by_source('', 'scatter'), use_container_width=True)




#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ Empty Data +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if data.empty:
    st.warning(f"Tabula rasa ⚠️\nFill thy content from the sidebar 🧙‍♂️")
    st.stop()
else:
    st.write(f'Register showing {data.shape[0]} records')
    st.dataframe(data)