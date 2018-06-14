#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Maser4py - Compare 2 CDF files module"""

import os
import os.path
import numpy as np
from spacepy import pycdf
import cdflib


cdf_file1 = "/obs/qnnguyen/Data/data_input/ROC-SGSE_L1_RPW-TNR-SURV_V01.cdf"
cdf_file2 = "/obs/qnnguyen/Data/data_input/ROC-SGSE_L1_RPW-TNR-SURV_81297ce_CNE_V02.cdf"
##cdf_file2 = "/obs/qnnguyen/Data/data_input/ROC-SGSE_L1_RPW-TNR-SURV_V01.cdf"

list_cdf = [cdf_file1,cdf_file2]



# TEST BLOC
cdffile = cdflib.CDF(cdf_file1)
info_cdf = cdffile.cdf_info()
#print(info_cdf.get('zVariables'))  # Returns the dictionary for zVariable numbers and their corresponding names
#print(info_cdf.get('rVariables'))  # Returns the dictionary for rVariable numbers and their corresponding names
#print(info_cdf.get('Attributes'))   # Returns the dictionary for attribute numbers and their corresponding names and scopes


# Variable's information dictionary
#dict = cdffile.varinq('CROSS_I')
#print(dict.get('Num_Dims'))
#print(dict.get('Dim_Vary'))


#global_attributes = cdffile.globalattsget(expand = False)
#print(lobal_attributes)

#data_var = cdffile.varget(VariableName)
cdffile.close()

# TEST BLOC : End


# Checking file
def checking_file_exist(cdf_file):
    result = False
    if os.path.isfile(cdf_file) and os.access(cdf_file, os.R_OK):
       result = True
    else:
      print("WARING : ")
      print ("   ", cdf_file, " : Either file is missing or is not readable")
      result = False

# Listing the names of all variables
def read_cdf_list_keys(cdf_file):
    cdf = pycdf.CDF(cdf_file)
    cdf_data = cdf.copy()
    listkeys = list(cdf_data.keys())
    cdf.close()
    return listkeys

# Finding not matched values
def returnNotMatches(a, b):
    return [[x for x in a if x not in b], [x for x in b if x not in a]]

# Listing all items
def list_elements(liste):
    n = len(liste)
    i = 0
    while i < n:
        print("     ", liste[i])
        i += 1

# Getting a variable's data
def get_variable(cdf_file, VariableName):
    cdffile = cdflib.CDF(cdf_file)
    cdffile.cdf_info()
    data_var = cdffile.varget(VariableName)
    cdffile.close()
    return data_var

# Getting global attributes
def get_global_attributes(cdf_file):
    cdffile = cdflib.CDF(cdf_file)
    global_attributes = cdffile.globalattsget(expand = False)
    cdffile.close()
    return global_attributes

# Deleting a dictionnary's key
def delete_key(dict, key_to_remove):
    if key_to_remove in dict:
        del dict[key_to_remove]
    return dict


# Comparing 2 CDF files data
def compare_cdf_files(cdf_file1, cdf_file2):
    cdf1 = pycdf.CDF(cdf_file1)
    cdf2 = pycdf.CDF(cdf_file2)

    i = 0
    while i < 2:
        cdf_file = list_cdf[i]
        checking_file_exist(cdf_file)
        list_keys = read_cdf_list_keys(cdf_file)
        global_att = get_global_attributes(cdf_file)

        if i == 0:
            d1 = list_keys
            global_att1 = global_att    # Dictionnary
        if i == 1:
            d2 = list_keys
            global_att2 = global_att    # Dictionnary
        i += 1


    #*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*
    # *°*°*  COMPARE GLOBAL ATTRUBUTES  *°*°*
    # *°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*

    list_global_att1 = sorted(list(global_att1.keys()))
    list_global_att2 = sorted(list(global_att2.keys()))
    notmathattribute = returnNotMatches(list_global_att1, list_global_att2)

    l1 = len(notmathattribute[0])
    l2 = len(notmathattribute[1])

    if l1 != 0 or l2 != 0:
        print
        print("****************************************")
        print("WARING : GLOBAL ATTRIBUTES DIFFERENT !!!")
        print("****************************************")
        print
        print('File 1 : ', len(global_att1), ' global attributes')
        print('File 2 : ', len(global_att2), ' global attributes')
        print('   ', notmathattribute)
        print

        # Remove not atched keys from the 2 dictionaries
        notmatch1 = notmathattribute[0]
        notmatch2 = notmathattribute[1]

        for c in range(len(notmatch1)):
            key_to_remove = notmatch1[c]
            global_att1 = delete_key(global_att1, key_to_remove)

        for c in range(len(notmatch2)):
            key_to_remove = notmatch2[c]
            global_att2 = delete_key(global_att2, key_to_remove)

        nl1 = len(global_att1)
        nl2 = len(global_att2)
        if nl1 == nl2: # The 2 dictionaries have the same keys
            # Compare 2 dictionaries

    common_att = sorted(list(set(list_global_att1).intersection(list_global_att1)))
    #print(common_att)


    #for k, v in global_att1.items():
        #print(k, ':', v)



        #print(global_att1.keys())
        #print(global_att1.values())



    # *°*°*°*°*°*°*°*°*°*°*°*°*°*
    # *°*°*  COMPARE DATA  *°*°*
    # *°*°*°*°*°*°*°*°*°*°*°*°*°*
    if len(d1) != len(d2):
        print()
        print("******************************")
        print("WARING : DATA DIFFERENT !!!")
        print("******************************")

    # ***** Not matched keys *****
    print()
    notmathkeys = returnNotMatches(d1, d2)
    print("NOT MATCHED KEYS:")

    i = 0
    while i < 2:
        print("   List", i + 1, ':', len(notmathkeys[i]))
        list_elements(notmathkeys[i])
        i += 1
    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")

    # ***** Matched keys *****
    print()
    same_keys = set(d1) & set(d2)
    print("MATCHED KEYS : ", len(same_keys))
    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")


    # ***** Alphabetical order *****
    order_same_keys = sorted(list(same_keys))
    n_same_keys = len(order_same_keys)


    i = 0
    j = 1
    skip_list = []

    for i in range(n_same_keys):
        i += 1
        find_str = order_same_keys[i-1]
        # Skip list
        if ('_LABEL' in find_str) or ('_UNITS' in find_str) or ('_FREQ' in find_str):
            skip_list.extend([find_str])
            i = i - 1
            continue
        field1 = cdf1[find_str]
        field2 = cdf2[find_str]

        if len(field1) != len(field2):
            print()
            print(str(j), "/", str(n_same_keys), ". WARNING : sizes different !!!")
            print("  ", find_str, " :     ", field1.shape, "     ", field2.shape)
            j += 1

        else:
            arraycheck2 = np.array(field1.shape) == np.array(field1.shape)
            uniq_val = np.unique(np.array(arraycheck2))
            if len(uniq_val) == 1 and (uniq_val[0]) == True:
                # print()
                # print(str(j), "/", str(n_same_keys), ": OK")
                # print("  ", find_str, " :     ", field1.shape, "     ", field2.shape)
                j += 1
            else:
                print()
                print(str(j), "/", str(n_same_keys), ". WARNING : values different !!!")
                print("  ", find_str, " :     ", field1.shape, "     ", field2.shape)
                print(np.array(field1[:, :]) == np.array(field1[:, :]))
                j += 1

    print()
    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    print('SKIP LIST :', len(skip_list))
    print('     ', skip_list)

    cdf1.close()
    cdf2.close()


# *°*°*°*°*°*°*°*°
#  Main program
# *°*°*°*°*°*°*°*°

compare_cdf_files(cdf_file1, cdf_file2)

print()
print("End !")