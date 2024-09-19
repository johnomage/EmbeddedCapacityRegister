geojson_data.groupby(energy_source)[['Accepted to Connect Registered Capacity (MW)',
                                                                    'Already connected Registered Capacity (MW)',
                                                                    'Maximum Export Capacity (MW)',
                                                                    'Maximum Import Capacity (MW)',
                                                                    'Change to Maximum Export Capacity (MW)',
                                                                    'Change to Maximum Import Capacity (MW)',]]
                                                                    .sum()
                                                                    .sort_values(by='Accepted to Connect Registered Capacity (MW)')
                                                                    .reset_index()








Latest Embedded Capacity Regiister: [Embedded Capacity Regiister](https://www.nationalgrid.co.uk/our-network/embedded-capacity-register)