import pandas as pd
import numpy as np
import os

def funfact(H2,HC,f,t):
    i = np.random.randint(0,5)
    CO2_saved = HC - H2 #kg
    fact = {
        0 : ["eat ",2.35," Big macs"], #Big mac
        1 : ["exhaling air in ",1," days"], #Exhale
        2 : ["producing ",68, " iphone 12"], #Iphone
        3 : ["drive a Toyota Corolla Sedan Petrol ",0.196974607," km"], #Driving a car
        4 : ["experiencing a ",55.79/60, " seconds voyage on Taylor Swift's private jet."], #taylor swift
    }
    eq = str(round(CO2_saved / fact[i][1] ,2))
    first_text = f"Choosing hydrogen flight from {f} to {t} saves the planet for {round(CO2_saved,2)} kg amount of CO2. That is equivalent to "
    return first_text + fact[i][0] + eq + fact[i][2]

def get_flight_distance(f, t):
    flight_data = {
        "OsloTrondheim": 364,  # km
        "TrondheimOslo": 364,  # km
        "TrondheimTromsø": 778, # km
        "TromsøTrondheim": 778, # km
        "OsloTromsø": 1119,     # km
        "TromsøOslo": 1119,     # km
    }#all data is extracted from www-airmilescalculator.com/distance
    # Return data if the key exists, else return None
    return flight_data.get(f + t)

def distance_H2_transport(f):
    transport_data = {
        "Oslo": 0.7155928,  # kg CO2 equivalent
        "Trondheim": 0.685224268,  # kg CO2 equivalent
        "Tromsø": 0.6778548, # kg CO2 equivalent
    }
    # Return data of kg CO2 equivalent for specific airport
    return transport_data.get(f)

def emmisson_conven(d):
    return 0.0296 * 3.16 *d * 100 #unit is KG of CO2 per passenger for common petrol flight

#Node is the call function with the hybird software with LCA
def node(f, t):
    distance = get_flight_distance(f, t)
    #file_path = os.path.join(os.getcwd(), "src", "Data.xlsx")
    file_path = "/Users/sigurdherland/Documents/eit/eit/src/Data.xlsx"
    if distance is None:
        return [0,0] #if the input does not have a valid travel desstiny
    
    # The A2 is the symetric tabel
    # The feauters in the tabel are from production to flight with units kg and kWh
    A2 = pd.read_excel(file_path, sheet_name='A-matrix', index_col=[0])
    
    # The CS2 tabel with climate change for a spec
    CS2 = pd.read_excel(file_path, sheet_name='C@S-matrix_TRD', index_col=[0])
    
    y2 = pd.read_excel(file_path, sheet_name='y-vector', index_col=[0])
    
    CS2.loc["Climate change (kg CO2-eq)", "H2 transportation (kg)"] = distance_H2_transport(f)


    I2 = np.identity(len(A2))
    L2 = pd.DataFrame(np.linalg.inv(I2 - A2), A2.index, A2.columns)
    x2 = L2 @ y2
    x2 = x2.rename(columns={"Final demand": "Output"})
    d2 = CS2 @ x2
    d2 = d2.rename(columns={"Output": "Total impact"})

    
    #H2 climate impact
    total_impact_modified = distance * d2["Total impact"] / 70
    H2_climate_change_impact = total_impact_modified.loc["Climate change (kg CO2-eq)"] 
    #HC hydrocarbons impact
    HC_climate_change_impact = emmisson_conven(distance) / 70
    #fun fact
    fun_fact = funfact(H2_climate_change_impact,HC_climate_change_impact,f,t)
    return  [H2_climate_change_impact, HC_climate_change_impact,fun_fact] #returns tons of CO2




