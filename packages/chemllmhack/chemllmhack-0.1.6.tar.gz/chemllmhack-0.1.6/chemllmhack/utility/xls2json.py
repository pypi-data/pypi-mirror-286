# -*- coding: utf-8 -*-
"""
File name: xls2json.py
Author: Bowen
Date created: 23/7/2024
Description: This Python file transfer xls BTK dataset into json format.

Copyright information: © 2024 QDX
"""

import pandas as pd
import json

def handle_BTK_wT_101():
    data = pd.read_excel('./BTKbindingData.xlsx', sheet_name='BTK_wT_101')

    data = data[['Ligand SMILES', 'Ki (nM)']]

    data = data.drop_duplicates(subset=['Ligand SMILES'])

    json_data = data.set_index('Ligand SMILES').to_json(orient='index')

    with open('./benchmark_affinity_wT.json', 'w') as f:
        json.dump(json.loads(json_data), f, indent=4)

    print("JSON data has been saved to file.")

def handle_BTK_M_343():
    data = pd.read_excel('./BTKbindingData.xlsx', sheet_name='BTK_M_343')

    data = data[['Ligand SMILES', 'IC50 (nM)']]

    data = data.drop_duplicates(subset=['Ligand SMILES'])

    json_data = data.set_index('Ligand SMILES').to_json(orient='index')

    with open('./benchmark_affinity_M.json', 'w') as f:
        json.dump(json.loads(json_data), f, indent=4)

    print("JSON data has been saved to file.")


if __name__ == "__main__":
    handle_BTK_wT_101()
    handle_BTK_M_343()

