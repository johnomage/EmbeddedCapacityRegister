
# ECR Dashboard

## Overview
The **ECR Dashboard** is a dynamic data visualization tool designed to provide insights into the **Embedded Capacity Register (ECR)** for **National Grid Electricity Distribution (NGED)** regions in the UK. The dashboard allows users to filter data, explore connection points, and view metrics related to **connected capacities**, **voltage levels**, and **distribution network operators (DNOs)** across various licence areas.

This dashboard integrates **Streamlit** for interactive data visualizations, **Plotly** for charting and mapping, and **GeoPandas** for geospatial data handling.

## Features
- **Interactive filters**: Filter the data based on **Licence Area** and **Voltage Levels**.
- **Geospatial visualization**: Visualize connection points on an interactive map using Plotly and Mapbox.
- **Capacity metrics**: View summary statistics of already connected and accepted capacities in **MW** and **GW**.
- **Sunburst Charts**: Visualize hierarchical relationships between Licence Areas and connection capacities.
- **Energy Source Insights**: Explore capacities by **Energy Source** and corresponding **Conversion Technology** using tree maps and line charts.
- **Data Table**: View a filtered data table that shows the underlying dataset.
  
## Technologies Used
- **Python**: Core programming language.
- **Pandas**: For data manipulation and processing.
- **GeoPandas**: For handling geospatial data (shapefiles, GeoJSON).
- **Plotly**: For creating charts and maps.
- **Streamlit**: For building the interactive web app.
- **Matplotlib**: Supplementary plotting.
- **dotenv**: For environment variable management.



## Installation

### 1. Clone the repository
 - `git clone https://github.com/johnomage/EmbeddedCapacityRegister.git`
 - `cd EmbeddedCapacityRegister`

### 2. Set up the Python environment
 - `python -m venv venv`
 - `source venv/bin/activate`

### 3. Install required dependencies
 - `pip install -r requirements.txt`


## Running the Dashboard
To start the Streamlit dashboard, use the following command:
- `streamlit run ECRapp.py`
<br>or</br>
 - `python.exe -m streamlit streamlit run ECRapp.py`


<br></br>

## Lastly
- Latest Embedded Capacity Regiister: [Embedded Capacity Regiister](https://www.nationalgrid.co.uk/our-network/embedded-capacity-register)
- Contributor: [**Praise**](https://www.linkedin.com/in/praizerema/)