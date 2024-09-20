
import geopandas as gpd
import plotly.express as px


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
        


    def plotLine_accpeted_over_time_by_source(self, source: str):
        """
        Plots a line chart showing the total accepted and maximum export capacity over time 
        for a specified energy source. The data is aggregated by 'Target Energisation Date' 
        and the selected source, with both accepted and maximum export capacities displayed.

        Args:
            source (str): The name of the energy source to plot.

        Returns:
            fig (plotly.graph_objects.Figure): The line chart figure.
        """
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
     
    
    def plot_sunburst_LA_2_FSP(self):
        """
        Plots a sunburst chart representing the capacity distribution by Licence Area, 
        Bulk Supply Point, Primary, and FSP (Final Supply Point) count. The chart displays
        accepted and already connected capacities at each level in a hierarchical structure.

        The data is grouped by 'Licence Area', 'Bulk Supply Point', and 'Primary', 
        and the 'Export MPAN_MSID' is renamed to 'FSP Count'. The capacities are aggregated 
        and displayed in a sunburst chart, with colors representing different Licence Areas.

        Returns:
            fig (plotly.graph_objects.Figure): The sunburst chart figure.
        """
        grouped_data = self.gdf.groupby(['Licence Area', 'Bulk Supply Point', 'Primary']).agg({'Accepted to Connect Registered Capacity (MW)': 'sum',
                                                                                                'Already connected Registered Capacity (MW)': 'sum',
                                                                                                'Export MPAN_MSID': 'count'}).reset_index()

        # Rename the column 'Export MPAN_MSID' to 'FSP Count'
        grouped_data.rename(columns={'Export MPAN_MSID': 'FSP Count'}, inplace=True)

        # Melt the dataframe to create a hierarchical structure
        melted_data = pd.melt(grouped_data,
                            id_vars=['Licence Area', 'Bulk Supply Point', 'Primary', 'FSP Count'],
                            var_name='Capacity Type',
                            value_name='Capacity (MW)')

        # Create a new column for the total (used for sorting)
        melted_data['Total'] = melted_data.groupby(['Licence Area', 'Bulk Supply Point', 'Primary'])['Capacity (MW)'].transform('sum')

        # Sort the dataframe
        melted_data = melted_data.sort_values(['Total', 'Licence Area', 'Bulk Supply Point', 'Primary', 'Capacity Type'],
                                            ascending=[False, True, True, True, True])

        # Create the sunburst chart with color based on 'Licence Area'
        fig = px.sunburst(melted_data, 
                        path=['Licence Area', 'Bulk Supply Point', 'Primary', 'Capacity Type'], 
                        values='Capacity (MW)',
                        color='Licence Area',  # Color by 'Licence Area'
                        hover_data={'Capacity (MW)': True, 'FSP Count': True},
                        color_discrete_sequence=px.colors.qualitative.Bold  # Color palette for Licence Area
                        )

        # Update layout with title, width, and height
        fig.update_layout(title='Capacity Distribution by Licence Area, Bulk Supply Point, Primary, and FSP Count',
                        width=1000,
                        height=1000)

        # Show the plot
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
        import folium
        selected_features = ['Export MPAN_MSID', 'Town_City', 'Primary', 'Bulk Supply Point', 'Grid Supply Point', 'Licence Area', 'Eastings', 'Northings', 'geometry', 'Accepted to Connect Registered Capacity (MW)', 'Connection Status']
        selected_dates = ['Date Connected', 'Last Updated', 'Date Accepted', 'Target Energisation Date']

        bounds = self.gdf.total_bounds

        layers = (self.gdf.drop(selected_dates, axis=1)[selected_features].explore(column='Licence Area',
                                                                                   tiles="CartoDB dark_matter",
                                                                                   vmin=bounds[1], vmax=bounds[3],
                                                                                   scheme='JenksCaspallForced'))

        return layers
