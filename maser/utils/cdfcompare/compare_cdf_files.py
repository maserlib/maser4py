#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Maser4py - Compare 2 CDF files module"""

import os
import os.path
import sys
import logging
import operator
import numpy
from spacepy import pycdf



cdf_file1 = "/obs/qnnguyen/Data/data_input/ROC-SGSE_L1_RPW-TNR-SURV_V01.cdf"
cdf_file2 = "/obs/qnnguyen/Data/data_input/ROC-SGSE_L1_RPW-TNR-SURV_81297ce_CNE_V02.cdf"
#cdf_file2 = "/obs/qnnguyen/Data/data_input/ROC-SGSE_L1_RPW-TNR-SURV_V01.cdf"


list_cdf = [cdf_file1,cdf_file2]

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
    n_keys = len(cdf)
    #print(cdf)
    cdf_data = cdf.copy()
    listkeys = list(cdf_data.keys())
    #print(listkeys)
    #print(cdf)
    #print(len(listkeys))
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


# Comparing 2 CDF files data
def compare_cdf_files(cdf_file1, cdf_file2):
    cdf1 = pycdf.CDF(cdf_file1)
    cdf2 = pycdf.CDF(cdf_file2)

    #print()
    #print(cdf1)
    #print()
    #print(cdf2)

    list1 = list(cdf1.keys())
    list2 = list(cdf2.keys())
    # print()
    # print(list1)
    # print(len(list1))
    # print()
    # print(list2)
    # print(len(list2))

    i = 0
    while i < 2:
        cdf_file = list_cdf[i]
        checking_file_exist(cdf_file)
        list_keys = read_cdf_list_keys(cdf_file)

        if i == 0:
            d1 = list_keys
        if i == 1:
            d2 = list_keys
        i += 1

    print()
    if len(d1) != len(d2):
        print("******************************")
        print("WARING : Files different !!!")
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
    print("******************************")

    # ***** Matched keys *****
    print()
    same_keys = set(d1) & set(d2)
    print("MATCHED KEYS : ", len(same_keys))
    # print(same_keys)
    print("******************************")


    # ***** Alphabetical order *****
    order_same_keys = sorted(list(same_keys))
    n_same_keys = len(order_same_keys)
    #print(n_same_keys)

    i = 1
    j = 1
    while i < n_same_keys+1:
        find_str = order_same_keys[i-1]
        field1 = cdf1[find_str]
        field2 = cdf2[find_str]

        if len(field1) != len(field2):
            print()
            print(str(j), "/", str(n_same_keys), ". WARNING : sizes different !!!")
            print("  ", find_str, " :     ", field1.shape, "     ", field2.shape)
            j += 1

        else:
            arraycheck = numpy.array_equal(field1, field2)
            if arraycheck == False:
                print()
                print(str(j), "/", str(n_same_keys), ". WARNING : values different !!!")
                print("  ", find_str, " :     ", field1.shape, "     ", field2.shape)
                j += 1
            else:
                print()
                print(str(j), "/", str(n_same_keys), ": OK")
                print("  ", find_str, " :     ", field1.shape, "     ", field2.shape)
                j += 1

        i += 1

    cdf1.close()
    cdf2.close()
    return cdf1, cdf2



# *°*°*°*°*°*°*°*°
#  Main program
# *°*°*°*°*°*°*°*°


data = compare_cdf_files(cdf_file1, cdf_file2)





print()
print("End !")