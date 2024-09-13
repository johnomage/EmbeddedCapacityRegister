# Data Fields

1. Export MPAN / MSID
2. Import MPAN / MSID
3. Customer Name
4. Customer Site
5. Address Line 1
6. Address Line 2
7. Town/City
8. County
9. Postcode
10. Country
11. Location (X-coordinate): Eastings (where data is held)
12. Location (Y-coordinate): Northings (where data is held)
13. Grid Supply Point
14. Bulk Supply Point
15. Primary
16. Point of Connection (POC) Voltage (kV)
17. Licence Area

## Energy Source 1
18. Energy Source 1
19. Energy Conversion Technology 1
20. CHP Cogeneration (Yes/No)
21. Storage Capacity 1 (MWh)
22. Storage Duration 1 (Hours)
23. Energy Source & Energy Conversion Technology 1 - Registered Capacity (MW)

## Energy Source 2
24. Energy Source 2
25. Energy Conversion Technology 2
26. CHP Cogeneration 2 (Yes/No)
27. Storage Capacity 2 (MWh)
28. Storage Duration 2 (Hours)
29. Energy Source & Energy Conversion Technology 2 - Registered Capacity (MW)

## Energy Source 3
30. Energy Source 3
31. Energy Conversion Technology 3
32. CHP Cogeneration 3 (Yes/No)
33. Storage Capacity 3 (MWh)
34. Storage Duration 3 (Hours)
35. Energy Source & Energy Conversion Technology 3 - Registered Capacity (MW)

## Connection Details
36. Flexible Connection (Yes/No)
37. Connection Status
38. Already connected Registered Capacity (MW)
39. Maximum Export Capacity (MW)
40. Maximum Export Capacity (MVA)
41. Maximum Import Capacity (MW)
42. Maximum Import Capacity (MVA)
43. Date Connected
44. Accepted to Connect Registered Capacity (MW)
45. Change to Maximum Export Capacity (MW)
46. Change to Maximum Export Capacity (MVA)
47. Change to Maximum Import Capacity (MW)
48. Change to Maximum Import Capacity (MVA)
49. Date Accepted
50. Target Energisation Date

## Service Provider Information
51. Distribution Service Provider (Y/N)
52. Transmission Service Provider (Y/N)

## Additional Information
53. Reference
54. In a Connection Queue (Y/N)
55. Distribution Reinforcement Reference
56. Transmission Reinforcement Reference
57. Last Updated
58. Location (X-coordinate): Eastings (where data is held)
59. Location (Y-coordinate): Northings (where data is held)

<br></br>


# Feature Descriptions

[Note]: Some of the features are removed from privacy


| **Heading**                             | **Explanation** |
|-----------------------------------------|-----------------|
| **General Data**                        |                 |
| **Export MPAN / MSID**                  | The core meter point administration number, a 13-digit reference used in MPAS to identify the relevant Metering Point. For generation and storage sites, the "Export" MPAN (or MSID for CVA registered sites) should be included. For "Accepted to Connect" generation or storage entries, please indicate "data not available". |
| **Import MPAN / MSID**                  | The core meter point administration number, a 13-digit reference used in MPAS to identify the relevant Metering Point. For sites subject to a DSR contract and for storage sites, the "Import" MPAN (or MSID for CVA registered sites) should be included. For generation sites, including generators taking on-site supplies, please indicate "not applicable". For "Accepted to Connect" storage sites, please indicate "data not available". |
| **Customer Name**                      | Name of party that is connected or contracted to connect. |
| **Customer Site**                      | Name of Customer Site/project name. |
| **Address Line 1**                     | Address line 1 of the Customer Site. |
| **Address Line 2**                     | Address line 2 of the Customer Site. |
| **Town/ City**                         | Town / City of the Customer Site. |
| **County**                             | County of the Customer Site. |
| **Postcode**                           | Postcode of the Customer Site. |
| **Country**                            | GB country of the Customer Site. |
| **Location (X-coordinate): Eastings (where data is held)** | Six-digit British National Grid X coordinate of the Customer Site. Generally this is the same as the Point of Connection / Metering Point. In exceptional cases where the Point of Connection or Metering Point is not located at the Customer Site, the coordinates of the Customer Site are included. |
| **Location (Y-coordinate): Northings (where data is held)** | Six or seven-digit British National Grid Y coordinate of the Customer Site. (In Northern Scotland, these will be seven-digit coordinates.) Generally this is the same as the Point of Connection / Metering Point. In exceptional cases where the Point of Connection or Metering Point is not located at the Customer Site, the coordinates of the Customer Site are included. |
| **Grid Supply Point**                  | The point of connection between the transmission system and the distribution system that is linked with the Customer Site. |
| **Bulk Supply Point**                  | The supply point on the distribution system (representing an EHV/EHV transformation level) that is linked with the Customer Site. |
| **Primary**                            | The primary substation on the distribution system that is linked with the Customer Site. |
| **Point of Connection (POC) Voltage (kV)** | The voltage at the Point of Connection to the distribution system. |
| **Licence Area**                       | Licence area Customer Site is connected within. |
| **Energy Source 1**                    | Meaning any of the below energy source types used in the production of electricity: Advanced Fuel (produced via gasification or pyrolysis of biofuel or waste), Biofuel - Biogas from anaerobic digestion (excluding landfill & sewage), Biofuel - Landfill gas, Biofuel - Sewage gas, Biofuel - Other, Biomass, Fossil - Brown coal/lignite, Fossil - Coal gas, Fossil - Gas, Fossil - Hard coal, Fossil - Oil, Fossil - Oil shale, Fossil - Peat, Fossil - Other, Geothermal, Hydrogen, Nuclear, Solar, Stored Energy (all stored energy irrespective of the original energy source), Waste, Water (flowing water or head of water), Wind, Other, Data not available. |
| **Energy Conversion Technology 1**     | Meaning any of the below technology types that export electricity onto a distribution system: Engine (combustion / reciprocating), Steam turbine (thermal power plant), Gas turbine (OCGT), Steam-gas turbine (CCGT), Fuel Cell, Hydro - Run of river, Hydro - Reservoir (not pumped), Hydro - Other, Tidal lagoons, Tidal stream devices, Wave devices, Photovoltaic, Offshore wind turbines, Onshore wind turbines, Geothermal power plant, Storage - Chemical, Storage - Electrical, Storage - Mechanical - Compressed Air (Adiabatic & Diabatic), Storage - Mechanical - Liquid Air, Storage - Mechanical - Pumped Hydro, Storage - Mechanical - Flywheel, Storage - Thermal, Storage - Electrochemical (Batteries), Storage - Other, Interconnector, Other, Data not available. |
| **CHP Cogeneration (Yes/No)**           | Indicates whether the generation in the Customer Site forms part of a CHP scheme. |
| **Storage Capacity 1 (MWh)**            | This is the energy capacity of the storage facility (MWh). |
| **Storage Duration 1 (Hours)**          | Divide the storage capacity (MWh) by the Registered Capacity (MW) and round it down to the nearest 0.5 (half-hour). If the value is less than 0.5 before rounding, it could be rounded to 0.5 hours so that it is not zero. |
| **Energy Source & Energy Conversion Technology 1 - Registered Capacity (MW)** | This is the Registered Capacity of the "Energy Source 1" expressed in MW. |
| **Energy Source 2**                    | Where there is more than one plant type at a site, the "Energy Source 2" and "Energy Source 3" fields would be used to show the energy source types additional to the "Energy Source 1". Meaning any of the energy source types stated above for the "Energy Source 1". |
| **Energy Conversion Technology 2**     | Defined as above for “Energy Conversion Technology 1”. |
| **CHP Cogeneration 2 (Yes/No)**         | Indicates whether the generation in the Customer Site forms part of a CHP scheme. |
| **Storage Capacity 2 (MWh)**            | This is the energy capacity of the storage facility (MWh). |
| **Storage Duration 2 (Hours)**          | Divide the storage capacity (MWh) by the Registered Capacity (MW) and round it down to the nearest 0.5 (half-hour). If the value is less than 0.5 before rounding, it could be rounded to 0.5 hours so that it is not zero. |
| **Energy Source & Energy Conversion Technology 2 - Registered Capacity (MW)** | This is the Registered Capacity of the "Energy Source 2" expressed in MW. |
| **Energy Source 3**                    | Defined as above for “Energy Source 2”. |
| **Energy Conversion Technology 3**     | Defined as above for “Energy Conversion Technology 2”. |
| **CHP Cogeneration 3 (Yes/No)**         | Indicates whether the generation in the Customer Site forms part of a CHP scheme. |
| **Storage Capacity 3 (MWh)**            | This is the energy capacity of the storage facility (MWh). |
| **Storage Duration 3 (Hours)**          | Divide the storage capacity (MWh) by the Registered Capacity (MW) and round it down to the nearest 0.5 (half-hour). If the value is less than 0.5 before rounding, it could be rounded to 0.5 hours so that it is not zero. |
| **Energy Source & Energy Conversion Technology 3 - Registered Capacity (MW)** | This is the Registered Capacity of the "Energy Source 3" expressed in MW. |
| **Flexible Connection (Yes/No)**        | Indicates whether the connection is subject to a flexible connection arrangement e.g. Active Network Management (ANM) during system normal conditions. |
| **Connection Status**                  | “Connected" or "Accepted to Connect"? |
| **Already Connected**                  |                 |
| **Already connected Registered Capacity (MW)** | This is the total Registered Capacity of generation already connected at the site expressed in MW. |
| **Maximum Export Capacity (MW)**       | This is the total MW export capacity permitted as per the connection agreement. |
| **Maximum Export Capacity (MVA)**      | This is the total MVA export capacity permitted as per the connection agreement. |
| **Maximum Import Capacity (MW)**       | This is the total MW import capacity permitted as per the connection agreement. |
| **Maximum Import Capacity (MVA)**      | This is the total MVA import capacity permitted as per the connection agreement. |
| **Date Connected**                     | Date the connection was provided in the case of a new connection. In cases where there was an existing connection, this is the date the new equipment was connected. |
| **Accepted to Connect**                |                 |
| **Accepted to Connect Registered Capacity (MW)** | This is the Registered Capacity of generation that is not already connected but has been Accepted to Connect, expressed in MW. |
| **Change to Maximum Export Capacity (MW)** | This is the new/additional MW export capacity (i.e., not yet connected) that has been accepted to connect as per the connection agreement. |
| **Change to Maximum Export Capacity (MVA)** | This is the new/additional MVA export capacity (i.e., not yet connected) that has been accepted to connect as per the connection agreement. |
| **Change to Maximum Import Capacity (MW)** | This is the new/additional MW import capacity (i.e., not yet connected) that has been accepted to connect as per the connection agreement. |
| **Change to Maximum Import Capacity (MVA)** | This is the new/additional MVA import capacity (i.e., not yet connected) that has been accepted to connect as per the connection agreement. |
| **Date Accepted**                      | Date the Customer accepted the connection offer from the DNO or IDNO. |
| **Target Energisation Date**           | Estimated date of energisation. This date is likely to change to reflect the latest date notified by customers. |
| **Services Provided**                  |                 |
| **Distribution Service Provider (Y/N)** | Indicates whether a service is provided to the DNO. |
| **Transmission Service Provider (Y/N)** | Indicates whether a service is provided to the ESO or a TO. |
| **Reference**                          | Unique reference to the service(s) being provided. |
| **Reinforcement Works**                |                 |
| **In a Connection Queue (Y/N)**        | Indicates whether the connection to the Customer Site is in a connection queue. |
| **Distribution Reinforcement Reference** | Unique reference to relevant distribution reinforcement required for connection. |
| **Transmission Reinforcement Reference** | Unique reference to relevant transmission reinforcement required for connection. |
| **Last Update**            | Date on which entry was last updated. |
