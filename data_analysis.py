#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 15:36:58 2024
@author: arwan
"""

import pandas as pd
import numpy as np
import ahpy as ahpy

df = pd.read_csv('data.csv')
np_bni = df.to_numpy()

    
criteria = ['HC',
            'FC',
            'GCG',
            'RM',
            'BP',
            'IDN',
            'GC',
            'IT',
            'DBM',
            'OA']

weights = np.zeros((np_bni.shape[0], len(criteria)))

for data_index in range(0, np_bni.shape[0]):
    print(f'Data number {data_index}')
    
    data_sample = np_bni[data_index][:46]
    
    np_weight = np.zeros((len(criteria), len(criteria)))
    
    idx = 1
    leng = len(criteria) - 1  
    
    for i in range(0, len(criteria)):
        if i < len(criteria):
            data = data_sample[idx: idx + leng]
            np_weight[i, (i+1):] = data
            idx = idx + leng
            leng = leng - 1
        for j in range(0, len(criteria)):
            if i == j:
                np_weight[i][j] = 1
            if i > j:
                np_weight[i][j] = 1 / np_weight[j][i]
                
    # Convert the numpy matrix into a dictionary of comparisons for ahpy
    comparison_dict = {}
    for i in range(len(criteria)):
        for j in range(i+1, len(criteria)):
            comparison_dict[(criteria[i], criteria[j])] = np_weight[i][j]
    
    # Initialize the ahpy Compare object
    ahp_compare = ahpy.Compare(name='AHP_Model', comparisons=comparison_dict, precision=3)
    
    # Print the priority vector (weights)
    
    target_weights = ahp_compare.target_weights
    print("Criteria Weights:")
    print(target_weights)
    
    # Print the consistency ratio
    print("Consistency Ratio:")
    print(ahp_compare.consistency_ratio)
    
    temp = np.zeros((1, len(criteria)))
    
    for j in range(0, len(criteria)):
        crit = target_weights[criteria[j]]
        temp[0, j] = crit
    weights[data_index] = temp