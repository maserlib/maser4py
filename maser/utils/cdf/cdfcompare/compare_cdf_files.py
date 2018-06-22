#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Maser4py - Compare 2 CDF files module"""

import os
import sys
import os.path
import numpy as np
from spacepy import pycdf
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Checking file
def checking_file_exist(cdf_file):
    if os.path.isfile(cdf_file) == False:
        logger.error("%s : does not exist !", cdf_file)
        exit()
    if os.access(cdf_file, os.R_OK) == False:
        logger.error("%s : is not readable !", cdf_file)
        exist()

# Listing the names of all data variables (zVars)
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
        #logger.debug("     %s", liste[i])
        i += 1

# Getting global attributes (gAttrs)
def get_global_attributes(cdf_file):
    cdf = pycdf.CDF(cdf_file)
    cdf_data = cdf.copy()
    global_attributes = cdf_data.attrs
    cdf.close()
    return global_attributes


# Deleting a dictionnary's key
def delete_key(dict, key_to_remove):
    if key_to_remove in dict:
        del dict[key_to_remove]
    return dict


# Getting a given vAttr's not matched keys
def get_not_matched_vAttrKey(field1, field2):
    vAttrsList1 = field1.attrs  # class 'spacepy.pycdf.zAttrList'
    listA1 = sorted([attr_key for attr_key in vAttrsList1])
    vAttrsList2 = field2.attrs
    listA2 = sorted([attr_key for attr_key in vAttrsList2])
    if listA1 != listA2:
        result = returnNotMatches(listA1, listA2)
    else:
        result = []

    return result

# Getting a given vAttr's matched keys
def get_matched_vAttrKey(field1, field2):
    vAttrsList1 = field1.attrs  # class 'spacepy.pycdf.zAttrList'
    listA1 = sorted([attr_key for attr_key in vAttrsList1])
    vAttrsList2 = field2.attrs
    listA2 = sorted([attr_key for attr_key in vAttrsList2])

    not_match = get_not_matched_vAttrKey(field1, field2)
    notmatch_list = not_match[0] + not_match[1]
    all_items = listA1 + listA2
    all_items_list = sorted(list(set(all_items)))
    uniq_items = [x for x in all_items_list if x not in notmatch_list]
    return uniq_items

# Comparing 2 CDF files data
def compare_cdf_files(cdf_file1, cdf_file2):
    checking_file_exist(cdf_file1)
    checking_file_exist(cdf_file2)
    cdf1 = pycdf.CDF(cdf_file1)
    cdf2 = pycdf.CDF(cdf_file2)
    list_cdf = [cdf_file1, cdf_file2]

    dict_result = {}

    i = 0
    while i < 2:
        cdf_file = list_cdf[i]
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
        logger.warning("****************************************")
        logger.warning("WARNING : GLOBAL ATTRIBUTES DIFFERENT !!!")
        logger.warning("****************************************")
        logger.warning('File 1 : %s%s', str(len(global_att1)), ' global attributes')
        logger.warning('File 2 : %s%s', str(len(global_att2)), ' global attributes')
        logger.warning('   %s', notmathattribute)

        # Add not matched attributes list to the returned dictionary
        gAttrs = {}
        gAttrs['NotMatched'] = notmathattribute

        # Remove not matched keys from the 2 dictionaries
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
            checking = global_att1 == global_att2
            if checking == False:
                # Not equal !!
                common_att = sorted(list(global_att1.keys()))

                DiffValueAttr = {}

                for ind in range(len(common_att)):
                    com_att = common_att[ind]
                    dd1 = global_att1.get(com_att)
                    dd2 = global_att2.get(com_att)
                    if dd1 != dd2:
                        val1 = dd1[0]
                        val2 = dd2[0]
                        logger.debug('** %s', com_att)
                        logger.debug('     File1 : %s', val1)
                        logger.debug('     File2 : %s', val2)

                        DiffValueAttr[com_att] = [val1, val2]

                gAttrs['Value'] = DiffValueAttr
        dict_result = {'gAttrs': gAttrs}

    else:
        logger.info("****************************************")
        logger.info("    GLOBAL ATTRIBUTES : IDENTICAL !!!")
        logger.info("****************************************")


    # *°*°*°*°*°*°*°*°*°*°*°*°*°*
    # *°*°*  COMPARE DATA  *°*°*
    # *°*°*°*°*°*°*°*°*°*°*°*°*°*

    if len(d1) != len(d2):
        logger.warning("******************************")
        logger.warning("WARNING : DATA DIFFERENT !!!")
        logger.warning("******************************")

        zVars = {} # Data

    # ***** Not matched keys *****
    notmathkeys = returnNotMatches(d1, d2)

    if d1 == d2:
        logger.info("****************************************")
        logger.info("       DATA : IDENTICAL !!!")
        logger.info("****************************************")
    else:

        logger.warning("NOT MATCHED KEYS:")

        i = 0
        while i < 2:
            logger.warning("   File %d : %d - %s", i + 1, len(notmathkeys[i]), notmathkeys[i])
            i += 1

        zVars['NotMatched'] = [notmathkeys[0], notmathkeys[1]]

        dict_result['zVars'] = zVars

        # ***** Matched keys *****
        same_keys = set(d1) & set(d2)
        logger.info("MATCHED KEYS : %d", len(same_keys))


        # ***** Alphabetical order *****
        order_same_keys = sorted(list(same_keys))
        n_same_keys = len(order_same_keys)


        i = 0
        j = 1
        skip_list = []

        diff_array = {}  # For different dimensions
        diff_data = [] # For different data

        NotMatch_vAttr = {}
        vAttrs = {}
        Value_vAttr = {}

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


            # *°*°*°*°*°*°*°*°*°*°*°*°*
            # *°* Compare zVariables *°*
            # *°*°*°*°*°*°*°*°*°*°*°*°*

            if len(field1) != len(field2):
                logger.warning("%d/%d. Sizes different !!!", j, n_same_keys)
                logger.warning("   %s:     %s      %s", find_str, field1.shape, field2.shape)
                diff_array[find_str] = [field1.shape,field2.shape]
                j += 1

            else:
                arraycheck2 = np.array(field1.shape) == np.array(field1.shape)
                uniq_val = np.unique(np.array(arraycheck2))

                if len(uniq_val) == 1 and (uniq_val[0]) == False:
                    logger.warning("%d/%d. Values different !!!", j, n_same_keys)
                    logger.warning("  ", find_str, " :     ", field1.shape, "     ", field2.shape)
                    logger.warning(np.array(field1[:, :]) == np.array(field1[:, :]))
                    diff_data = [diff_data, find_str]
                if len(diff_data) != 0:
                    diff_data = diff_data[1:]

            # *°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*
            # *°* Compare Variable Attributes *°*
            # *°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*

            tab_diff = get_not_matched_vAttrKey(field1, field2)
            NotMatch_vAttr[find_str] = tab_diff

            uniq_items_vAtt = get_matched_vAttrKey(field1, field2)

            vAttrsList1 = field1.attrs
            vAttrsList2 = field2.attrs

            count = len(uniq_items_vAtt)
            DiffValue_vAttr = {}

            for k in range(count):
                check_item = uniq_items_vAtt[k]
                logger.info("%s : %s  |  %s", check_item, vAttrsList1[check_item], vAttrsList2[check_item])

                if vAttrsList1[check_item] == vAttrsList2[check_item]:
                     logger.info("%s : equal", check_item)
                else:
                    logger.info("%s : not equal", check_item)
                    DiffValue_vAttr[check_item] = [vAttrsList1[check_item], vAttrsList2[check_item]]
                    Value_vAttr[find_str] = DiffValue_vAttr
                    vAttrs['Value'] = Value_vAttr
                    logger.debug("vAttrs['Value'] : %s", vAttrs['Value'])

        if len(diff_array) != 0:
            zVars['Size'] = diff_array
        if len(diff_data) != 0:
            zVars['Value'] = diff_array

        dict_result = {'gAttrs' : gAttrs, 'zVars' : zVars}

        if len(NotMatch_vAttr) != 0:
            vAttrs['NotMatched'] = NotMatch_vAttr
            dict_result['vAttrs'] = vAttrs
        if len(Value_vAttr) !=0:
            vAttrs['Value'] = Value_vAttr
            dict_result['vAttrs'] = vAttrs

        logger.info('SKIP LIST : %d', len(skip_list))
        logger.info('     %s', skip_list)

        cdf1.close()
        cdf2.close()

    return dict_result

# *°*°*°*°*°*°*°*°
#  Main program
# *°*°*°*°*°*°*°*°

def cdf_compare(cdf_file1, cdf_file2):
    logger.info(' CDF file 1 : %s', cdf_file1)
    logger.info(' CDF file 2 : %s', cdf_file2)
    dict_result = compare_cdf_files(cdf_file1, cdf_file2)
    return dict_result


# _________________ Main _________________

if __name__ == '__main__':
    if len(sys.argv)==3:
        logging.basicConfig(level=logging.DEBUG, \
            format='%(levelname)s : %(message)s')

        result=cdf_compare(sys.argv[1], sys.argv[2])
        logger.debug("")
        logger.debug("Result : %s", result)
