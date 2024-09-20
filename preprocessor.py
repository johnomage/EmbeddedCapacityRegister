# Import packages
import requests
import numpy as np
import pandas as pd
import geopandas as gpd
import os
import warnings

# configure warnnings
warnings.simplefilter('ignore')
pd.set_option('future.no_silent_downcasting', True)



class DataDownloader:
    def __init__(self, url: str, file_path: str) -> None:
        self.url = url
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def download_data(self) -> None:
        """Downloads data from the specified URL and saves it to the file path."""
        print('downloading data ...')
        response = requests.get(self.url)
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        with open(self.file_path, 'wb') as f:
            if response:
                f.write(response.content)



class DataProcessor:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.raw_data = None

    def load_data(self) -> None:
        """Loads data from the Excel file and concatenates specified sheets."""
        df_dict = pd.read_excel(self.file_path, sheet_name=[2, 3], header=1)
        self.raw_data = pd.concat([df_dict[2], df_dict[3]])
        self.clean_data()

    def clean_data(self) -> None:
        """Cleans and preprocesses the raw data."""
        print('cleaning data ...')
        # Remove extra space from feature names
        self.raw_data.columns = [col.strip() for col in self.raw_data.columns]
        
        # Rename columns
        self.raw_data.rename(columns={
            'Location (X-coordinate):Eastings (where data is held)': 'Eastings',
            'Export MPAN / MSID': 'Export MPAN_MSID',
            'Location (y-coordinate):Northings (where data is held)': 'Northings',
            'Point of Connection (POC)\nVoltage (kV)': 'PoC Voltage (KV)',
            'Energy Source & Energy Conversion Technology 1 - Registered Capacity (MW)': 'Reg_Cap_Energy_Source_Conv_Tech_1',
            'Energy Source & Energy Conversion Technology 2 - Registered Capacity (MW)': 'Reg_Cap_Energy_Source_Conv_Tech_2',
            'Town/ City': 'Town_City',
            'Import MPAN / MSID': 'Import MPAN_MSID',
            'Energy Source & Energy Conversion Technology 3 - Registered Capacity (MW)': 'Reg_Cap_Energy_Source_Conv_Tech_3'
        }, inplace=True)

        # Rename Licence Area fields
        self.raw_data['Licence Area'] = self.raw_data['Licence Area'].apply(self.rename_LA_fields)

        # Set index and strip whitespace
        self.raw_data.set_index('Export MPAN_MSID', inplace=True)
        self.raw_data = self.raw_data.map(lambda x: x.strip() if isinstance(x, str) else x)

        # Replace specific values
        self.raw_data.replace(r'(?i)--REDACTED--', np.nan, inplace=True, regex=True)
        self.raw_data.replace({'data not available': np.nan}, inplace=True)

        # Redefine data types
        self.redefine_data_types()

    def rename_LA_fields(self, area: str) -> str:
        """Maps Licence Area names to standardized names."""
        match area:
            case 'National Grid Electricity Distribution (East Midlands) Plc':
                return 'East Midlands'
            case 'National Grid Electricity Distribution (West Midlands) Plc':
                return 'West Midlands'
            case 'National Grid Electricity Distribution (South West) Plc':
                return 'South West'
            case 'National Grid Electricity Distribution (South Wales) Plc':
                return 'South Wales'
            case _:
                return pd.NA

    def redefine_data_types(self) -> None:
        """Converts columns to appropriate data types."""
        selected_floats = [
            'PoC Voltage (KV)', 'Maximum Export Capacity (MW)', 'Maximum Import Capacity (MW)',
            'Maximum Export Capacity (MVA)', 'Maximum Import Capacity (MVA)',
            'Already connected Registered Capacity (MW)', 'Accepted to Connect Registered Capacity (MW)',
            'Reg_Cap_Energy_Source_Conv_Tech_2', 'Reg_Cap_Energy_Source_Conv_Tech_3'
        ]
        selected_ints = ['Eastings', 'Northings']
        selected_dates = ['Date Connected', 'Last Updated', 'Date Accepted', 'Target Energisation Date']

        self.raw_data[selected_floats] = self.raw_data[selected_floats].replace({'data not applicable': np.nan})
        self.raw_data[selected_floats] = self.raw_data[selected_floats].astype('float')
        self.raw_data[selected_ints] = self.raw_data[selected_ints].apply(pd.to_numeric, errors='coerce')
        self.raw_data['Date Accepted'] = pd.to_datetime(self.raw_data['Date Accepted'], format='%d/%m/%Y', errors='coerce')

        # Drop unnecessary columns
        self.raw_data.drop(labels=[
            'Flexible Connection (Yes/No)', 'Storage Capacity 1 (MWh)', 
            'Storage Capacity 2 (MWh)', 'Storage Capacity 3 (MWh)',
            'Storage Duration 1 (Hours)', 'Storage Duration 2 (Hours)', 
            'Storage Duration 3 (Hours)', 'Distribution Service Provider (Y/N)',
            'Transmission Service Provider (Y/N)', 'Reference',
            'In a Connection Queue (Y/N)', 'Distribution Reinforcement Reference',
            'Transmission Reinforcement Reference','Customer Name',
            'Customer Site', 'Address Line 1', 'Address Line 2',
            'Postcode', 'Country'], axis=1, inplace=True)

    def convert_to_geodataframe(self) -> gpd.GeoDataFrame:
        """Converts the cleaned DataFrame to a GeoDataFrame."""
        gdata = gpd.GeoDataFrame(self.raw_data)
        gdata.geometry = gpd.points_from_xy(x=gdata.Eastings, y=gdata.Northings)
        gdata.set_crs('EPSG:27700', inplace=True)
        return gdata

    def save_to_geojson(self, geo_data: gpd.GeoDataFrame, output_path: str) -> None:
        """Saves the GeoDataFrame to a GeoJSON file."""
        geo_data.to_file(output_path, driver='GeoJSON')




def run_preprocessor(name_as: str='processed_ecr'):
    print('fectching preprocessed data ...')
    url = 'https://www.nationalgrid.co.uk/ECRDownload/672543'
    file_path = './datastore/download.xlsx'
    
    downloader = DataDownloader(url, file_path)
    downloader.download_data()

    processor = DataProcessor(file_path)
    processor.load_data()
    
    geo_data = processor.convert_to_geodataframe()
    geo_data.to_file(f'datastore/{name_as}.geojson', driver='GeoJSON')
    # print(geo_data.head())

# run_preprocessor()

