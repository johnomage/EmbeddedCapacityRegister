
import geopandas as gpd
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os, ast

class Plotter:
    """
    A class for visualizing energy capacity data using Plotly.

    This class provides methods to create various types of plots, such as
    sunburst charts, line plots, treemaps, and bar charts. It is designed
    to work with a GeoDataFrame that contains information about energy
    sources, capacities, and related attributes.

    Attributes:
        gdf (gpd.GeoDataFrame): A GeoDataFrame containing energy capacity
        data, including information on licence areas, bulk supply points,
        and various capacity metrics.
    """

    def __init__(self, gdf: gpd.GeoDataFrame) -> None:
        self.gdf = gdf

    
    def plot_energy_source_by_cap(self, energy_source: str):
        """
        Plots stacked bar chart of capacities by energy source, including
        accepted, connected, maximum export, and maximum import capacities.

        Args:
            energy_source (str): The name of the energy source to plot.

        Returns:
            fig (plotly.express.bar): The bar chart figure showing capacities.
        """

        # Group and sum capacities by the specified energy source
        energy_cap_sources_group = (
            self.gdf.groupby(energy_source)[['Accepted to Connect Registered Capacity (MW)', 'Already connected Registered Capacity (MW)',
                                                'Maximum Export Capacity (MW)', 'Maximum Import Capacity (MW)',
                                                'Change to Maximum Export Capacity (MW)', 'Change to Maximum Import Capacity (MW)']]
                        .sum()
                        .reset_index())
        
        # Calculate total capacities for sorting
        energy_cap_sources_group['Total Capacity'] = energy_cap_sources_group[['Accepted to Connect Registered Capacity (MW)',
                                                                                'Already connected Registered Capacity (MW)',
                                                                                'Maximum Export Capacity (MW)',
                                                                                'Maximum Import Capacity (MW)']].sum(axis=1)
        # Sort by Total Capacity in descending order
        energy_cap_sources_group.sort_values(by='Total Capacity', ascending=False, inplace=True)

        # Create a bar chart
        fig = px.bar(
            data_frame=energy_cap_sources_group,
            x=energy_source,
            y=['Accepted to Connect Registered Capacity (MW)', 'Already connected Registered Capacity (MW)',
                'Maximum Export Capacity (MW)', 'Maximum Import Capacity (MW)'],
            barmode='stack',
            title=f'Registered Capacities, Import and Export for {energy_source}',
            height=600,
            color_discrete_sequence=['#000099', '#90109f', '#0000ff', '#2200ee']
        )

        # Update layout
        fig.update_layout(
            xaxis_title='Energy Source', 
            yaxis_title='Capacity (MW)',
            legend_title='Capacity Type', legend=dict(
                                                        orientation="h",
                                                        yanchor="bottom", y=1.02, 
                                                        xanchor="center", x=0.5  # Centered on the x-axis
                                                    ),
            bargap=0.2, bargroupgap=0.5, margin=dict(b=150))

        # Add total capacity text on top of bars
        total_capacity = energy_cap_sources_group[['Accepted to Connect Registered Capacity (MW)',
                                                    'Already connected Registered Capacity (MW)',
                                                    'Maximum Export Capacity (MW)',
                                                    'Maximum Import Capacity (MW)']].sum(axis=1)

        for i, row in energy_cap_sources_group.iterrows():
            fig.add_annotation(x=row[energy_source], y=total_capacity[i],
                text=f"{total_capacity[i]:.2f} MW", showarrow=False,
                font=dict(size=10), yshift=10)  # Shift the text above the bar

        
        return fig
        


    def plotTreeMap_energy_source_by_conv_tech(self, source: str, tech: str, values: str):
        """
        Creates a treemap visualization of energy source capacity based on specified 
        energy conversion technology. The data is aggregated into a pivot table 
        and filtered to include only positive capacities.

        Args:
            source (str): The name of the energy source to use as the main category.
            tech (str): The name of the energy conversion technology to use as the sub-category.
            values (str): The column name containing capacity values to be aggregated.

        Returns:
            fig (plotly.express.treemap): The treemap figure, or None if no valid data is available.
        """
        # Create a pivot table
        source_tech_pivot = self.gdf.pivot_table(columns=tech, index=source, values=values, fill_value=0, aggfunc='sum').reset_index()

        # Melt the pivot table for treemap plotting
        melted_data = source_tech_pivot.melt(id_vars=source, var_name=tech, value_name='Capacity')

        # Filter out rows where Capacity is zero
        melted_data = melted_data[melted_data['Capacity'] > 0]

        # Check if there are any valid entries left for plotting
        if melted_data.empty:
            print("No valid data.")
            return

        # Plotting with Plotly using a treemap
        fig = px.treemap(
            melted_data,
            path=[source, tech],
            values='Capacity',
            color='Capacity',
            color_continuous_scale='turbo',
            title=f'Energy Source Capacity by {tech}',
            labels={source: 'Energy Source', tech: 'Energy Conversion Technology', 'Capacity': 'Registered Capacity'}
        )

        # Show the plot
        return fig
        


    def plotLineScatter_accpeted_over_time_by_source(self, source: str, plot: str):
        """
        Plots a line chart showing the total accepted and maximum export capacity over time 
        for a specified energy source. The data is aggregated by 'Target Energisation Date' 
        and the selected source, with both accepted and maximum export capacities displayed.

        Args:
            source (str): The name of the energy source to plot.

        Returns:
            fig (plotly.graph_objects.Figure): The line chart figure.
        """
        match plot:
            case 'line':
                fig = px.line(data_frame=self.gdf.groupby(['Target Energisation Date', source])[['Accepted to Connect Registered Capacity (MW)',
                                                                                                'Maximum Export Capacity (MW)']].agg(
                                                                                                    {'Accepted to Connect Registered Capacity (MW)': 'sum',
                                                                                                    'Maximum Export Capacity (MW)': 'sum'}
                                                ).reset_index(), 
                    x='Target Energisation Date', 
                    y=['Accepted to Connect Registered Capacity (MW)', 'Maximum Export Capacity (MW)'],
                    title=f'Total Accepted Capacity Over Time for {source}',
                    markers='line+circle',
                    color=source,
                    # labels={'Target Energisation Date': 'Date', 'Accepted to Connect Registered Capacity (MW)': 'Capacity (MW)'},
                    color_discrete_sequence=px.colors.carto.Agsunset
                )
                return fig
            
            case 'scatter':
                data_sorted = self.gdf.sort_values('Target Energisation Date')
                # Ensure 'Accepted to Connect Registered Capacity (MW)' has no NaN values
                data_sorted['Accepted to Connect Registered Capacity (MW)'] = data_sorted['Accepted to Connect Registered Capacity (MW)'].fillna(1)

                # Filter out rows with missing 'Target Energisation Date'
                data_sorted = data_sorted.dropna(subset=['Target Energisation Date'])

                # Extract the year from 'Target Energisation Date' and cast it as a string for animation
                data_sorted['Year'] = data_sorted['Target Energisation Date'].dt.year.astype(str)

                # Create the scatter plot
                fig = px.scatter(
                    data_frame=data_sorted,
                    x='Target Energisation Date',
                    y='Accepted to Connect Registered Capacity (MW)',
                    title='Accepted to Connect Registered Capacity for all Sources Over Time',
                    labels={
                        'Target Energisation Date': 'Date',
                        'Accepted to Connect Registered Capacity (MW)': 'Capacity (MW)',
                        'Licence Area': 'Licence Area'
                    },
                    color='Licence Area',  # Color points by Licence Area
                    color_discrete_sequence=px.colors.qualitative.Plotly,  # Use a discrete color sequence
                    size='Accepted to Connect Registered Capacity (MW)',  # Size points by capacity
                    size_max=30,  # Set maximum marker size
                    hover_data=['Energy Source 1', 'Energy Conversion Technology 1', 'Energy Source 2', 'Energy Conversion Technology 2',
                                'Energy Source 3', 'Energy Conversion Technology 3', 'PoC Voltage (KV)'],
                    # animation_frame='Year',y
                )

                # Customize the layout to reposition the animator inside the figure
                fig.update_layout(
                    xaxis_title='Target Energisation Date',
                    yaxis_title='Accepted to Connect Registered Capacity (MW)',
                    hovermode='closest',
                    legend_title_text='Licence Area',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1 ),
                )
                return fig
            case _:
                return f'plot must be one of ["line", "scatter"] but got {plot}'
     
    
    def plot_sunburst_LA_2_FSP(self):
        # Reshape the data for sunburst chart
        load_dotenv(find_dotenv('.env'))

        blue_purple = ast.literal_eval(os.getenv('blue_purple'))

        cols = ['Maximum Export Capacity (MW)', 'Maximum Import Capacity (MW)', 'Change to Maximum Export Capacity (MW)', 'Change to Maximum Import Capacity (MW)']
        self.gdf[cols] = self.gdf[cols].apply(pd.to_numeric, errors='coerce')
        dno_voltage_energy_group = self.gdf.groupby(['Licence Area', 'PoC Voltage (KV)'])[cols].sum().reset_index()

        sunburst_data = pd.melt(dno_voltage_energy_group, 
                                id_vars=['Licence Area', 'PoC Voltage (KV)'], 
                                value_vars=['Maximum Export Capacity (MW)',
                                            'Maximum Import Capacity (MW)',
                                            'Change to Maximum Export Capacity (MW)',
                                            'Change to Maximum Import Capacity (MW)'],
                                var_name='Capacity Type', 
                                value_name='Capacity (MW)',
                                )

        # Create the sunburst chart
        fig = px.sunburst(sunburst_data, 
                        path=['Licence Area', 'PoC Voltage (KV)', 'Capacity Type'], 
                        values='Capacity (MW)',
                        color='Licence Area',
                        color_discrete_sequence=blue_purple,
                        hover_data={'Capacity (MW)': ':.2f'},
                        branchvalues='total',
                        height=600)

        fig.update_layout(title='Import Export Capacity Distribution by Licence Area and Voltage',
                        margin=dict(t=30, l=0, r=0, b=0))

        return fig


    

    def plotMap_of_MPANs(self):
        """
        Creates an interactive map layer visualization of the GeoDataFrame.

        This method selects specific features and date columns from the GeoDataFrame,
        then generates an interactive map using Folium. The map visualizes the
        geographical distribution of energy connection data, with layers colored
        by Licence Area. The visualization uses a dark-themed tile layer.

        Returns:
            folium.Map: An interactive map object displaying the selected features
            from the GeoDataFrame, with color coding based on Licence Area.
        """
        
        self.gdf = self.gdf.to_crs(epsg=4326)

        self.gdf['Accepted to Connect Registered Capacity (MW)'].fillna(0, inplace=True)
        self.gdf['Already connected Registered Capacity (MW)'].fillna(0, inplace=True)

        
        fig = px.scatter_mapbox(data_frame=self.gdf,
                                lat=self.gdf.geometry.y,
                                lon=self.gdf.geometry.x,
                                hover_name='Licence Area',
                                hover_data={
                                    'Town_City': True, 
                                    'County': True,
                                    'Accepted to Connect Registered Capacity (MW)': True, 
                                    'Already connected Registered Capacity (MW)': True
                                },
                                color='Licence Area', 
                                color_discrete_sequence=['#0000FF', '#FFF700', '#80ff80', '#FF0000'],  
                                size='Accepted to Connect Registered Capacity (MW)',  
                                size_max=100, 
                                zoom=6,
                                mapbox_style="carto-darkmatter", 
                                title="MPAN Locations by Licence Area"
        )

        # Update layout to adjust the size, title, etc.
        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},  # Adjust margins
            height=500,
            title={'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'}
        )

        return fig
