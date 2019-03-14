#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Maser4py - Compare 2 CDF files module"""

import os
import sys
import os.path
import numpy as np
from maser.utils.cdf import CDF
import logging

logging.basicConfig(level=logging.WARNING, format='%(levelname)s : %(message)s')
logger = logging.getLogger(__name__)

# Checking file
def checking_file_exist(cdf_file):
    if os.path.isfile(cdf_file) == False:
        logger.error("%s : does not exist !", cdf_file)
        exit()
    if os.access(cdf_file, os.R_OK) == False:
        logger.error("%s : is not readable !", cdf_file)
        exit()

# Listing the names of all data variables (zVars)
def read_cdf_list_keys(cdf_file):
    cdf = CDF(cdf_file)
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
    cdf = CDF(cdf_file)
    cdf_data = cdf.copy()
    global_attributes = cdf_data.attrs
    cdf.close()
    return global_attributes


# Deleting a dictionnary's key
def delete_key(dict, key_to_remove):
    if key_to_remove in dict:
        del dict[key_to_remove]
    else:
        logger.warning("Key to remove '%s' does not exist !", key_to_remove)
    return dict


# Getting a given vAttr's not matched keys
def get_not_matched_vAttrKey(field1, field2):
    vAttrsList1 = field1.attrs  # class 'spacepy.cdf.zAttrList'
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
    vAttrsList1 = field1.attrs  # class 'spacepy.cdf.zAttrList'
    listA1 = sorted([attr_key for attr_key in vAttrsList1])
    vAttrsList2 = field2.attrs
    listA2 = sorted([attr_key for attr_key in vAttrsList2])

    not_match = get_not_matched_vAttrKey(field1, field2)
    if not_match != []:
        notmatch_list = not_match[0] + not_match[1]
    else:
        notmatch_list = []
    all_items = listA1 + listA2
    all_items_list = sorted(list(set(all_items)))
    uniq_items = [x for x in all_items_list if x not in notmatch_list]
    return uniq_items

# Comparing 2 CDF files data
def cdf_compare(cdf_file1, cdf_file2, ignore_gatt=[], ignore_zvar=[], ignore_vatt=[]):
    logger.warning(' CDF file 1 : %s', cdf_file1)
    logger.warning(' CDF file 2 : %s', cdf_file2)
    checking_file_exist(cdf_file1)
    checking_file_exist(cdf_file2)
    cdf1 = CDF(cdf_file1)
    cdf2 = CDF(cdf_file2)
    list_cdf = [cdf_file1, cdf_file2]

    list_argv = sys.argv
    list_ignore_gatt = []
    list_ignore_zvar = []
    list_ignore_vatt = []

    if list_argv == ['']: # Execution under Python
        if ignore_gatt != []:
            list_ignore_gatt = ignore_gatt
            logger.warning("Ignored global attributes list : %s", list_ignore_gatt)
        else:
            logger.info("No global attributes to be ignored")

        if ignore_zvar != []:
            list_ignore_zvar = ignore_zvar
            logger.warning("Ignored zVariables list : %s", list_ignore_zvar)
        else:
            logger.info("No zVariables to be ignored")

        if ignore_vatt != []:
            list_ignore_vatt = ignore_vatt
            logger.warning("Ignored variable attributes list : %s", list_ignore_vatt)
        else:
            logger.info("No variable attributes to be ignored")

    else: # Execution under command lines
        if "--ignore_gatt" in (list_argv):
            ind_ignore_gatt = (list_argv).index("--ignore_gatt")
            list_ignore_gatt = []
            for item in list_argv[ind_ignore_gatt + 1 :]:
                if item.startswith("--ignore_") == False: list_ignore_gatt.append(item)
                else: break
            logger.warning("Ignored global attributes list : %s", list_ignore_gatt)
        else:
            logger.info("No global attributes to be ignored")

        if "--ignore_zvar" in (list_argv):
            ind_ignore_zvar = (list_argv).index("--ignore_zvar")
            list_ignore_zvar = []
            for item in list_argv[ind_ignore_zvar + 1 :]:
                if item.startswith("--ignore_") == False: list_ignore_zvar.append(item)
                else: break
            logger.warning("Ignored zVariables list : %s", list_ignore_zvar)
        else:
            logger.info("No zVariables to be ignored")

        if "--ignore_vatt" in (list_argv):
            ind_ignore_vatt = (list_argv).index("--ignore_vatt")
            list_ignore_vatt = []
            for item in list_argv[ind_ignore_vatt + 1:]:
                if item.startswith("--ignore_") == False: list_ignore_vatt.append(item)
                else:
                    break
            logger.warning("Ignored variable attributes list : %s", list_ignore_vatt)
        else:
            logger.info("No variable attributes to be ignored")

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
    # *°*°*  COMPARE GLOBAL ATTRIBUTES  *°*°*
    # *°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*

    # Initialize the Global Attributes dictionary
    gAttrs = {}

    list_global_att1 = sorted(list(global_att1.keys()))
    list_global_att2 = sorted(list(global_att2.keys()))

    if list_ignore_gatt != []:
        list_global_att1 = [n for n in list_global_att1 if n not in list_ignore_gatt]
        list_global_att2 = [n for n in list_global_att2 if n not in list_ignore_gatt]
    notmathattribute = returnNotMatches(list_global_att1, list_global_att2)

    l1 = len(notmathattribute[0])
    l2 = len(notmathattribute[1])

    if list_ignore_gatt != []:
        logger.warning("%s Global Attributes to be ignored for comparison : %s", len(list_ignore_gatt), list_ignore_gatt)
    if l1 != 0 or l2 != 0:
        logger.warning("****************************************")
        logger.warning("WARNING : GLOBAL ATTRIBUTES DIFFERENT !!!")
        logger.warning("****************************************")
        logger.warning('File 1 : %s%s', str(len(global_att1)), ' global attributes')
        logger.debug("File1's Global Attributes List : %s", list_global_att1)
        logger.warning('File 2 : %s%s', str(len(global_att2)), ' global attributes')
        logger.debug("File2's Global Attributes List : %s", list_global_att2)
        logger.warning("NOT MATCHED GLOBAL ATTRIBUTES :")
        logger.warning("   File1 : %s - %s", len(notmathattribute[0]), notmathattribute[0])
        logger.warning("   File2 : %s - %s", len(notmathattribute[1]) ,notmathattribute[1])

        gAttrs['NotMatched'] = notmathattribute
        # Remove not matched keys from the 2 dictionaries
        notmatch1 = notmathattribute[0]
        notmatch2 = notmathattribute[1]

        for key_to_remove in notmatch1:
            global_att1 = delete_key(global_att1, key_to_remove)

        for key_to_remove in notmatch2:
            global_att2 = delete_key(global_att2, key_to_remove)

    # Compare Global Attributes's value
    nl1 = len(global_att1)
    nl2 = len(global_att2)
    if nl1 == nl2:  # The 2 dictionaries have the same keys
        # Compare 2 dictionaries
        checking = global_att1 == global_att2
        if checking == False:
            # Not equal !!
            logger.warning("************************************************")
            logger.warning("WARNING : GLOBAL ATTRIBUTES' VALUE DIFFERENT !!!")
            logger.warning("************************************************")
            common_att = sorted(list(global_att1.keys()))

            DiffValueAttr = {}
            for com_att in common_att:
                if com_att not in list_ignore_gatt:
                    dd1 = global_att1.get(com_att)
                    dd2 = global_att2.get(com_att)
                    if dd1 != dd2:
                        val1 = dd1[0]
                        val2 = dd2[0]
                        logger.debug('** %s', com_att)
                        logger.debug("   File1 : %s", val1)
                        logger.debug("   File2 : %s", val2)

                        DiffValueAttr[com_att] = [val1, val2]

            gAttrs['Value'] = DiffValueAttr
            logger.warning("*°*°* gAttrs *°*°*")
            logger.warning(gAttrs["Value"])
    dict_result = {'gAttrs': gAttrs}


    # *°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*
    # *°*°*  COMPARE zVARIABLES  *°*°*
    # *°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*

    zVars = {}  # Data

    # Ignored zVariables for comparison
    if list_ignore_zvar != []:
        logger.warning("%s zVariables to be ignored for comparison : %s", len(list_ignore_zvar), list_ignore_zvar)

    if len(d1) != len(d2):
        logger.warning("**********************************")
        logger.warning("WARNING : zVARIABLES DIFFERENT !!!")
        logger.warning("**********************************")

    # ***** Not matched keys *****
    notmathkeys = returnNotMatches(d1, d2)

    if d1 == d2:
        logger.info("****************************************")
        logger.info("       zVARIABLES : IDENTICAL !!!")
        logger.info("****************************************")
    else:
        if (notmathkeys[0] != []) or (notmathkeys[1] != []):
            logger.warning("NOT MATCHED zVARIABLES :")
            i = 0
            while i < 2:
                logger.warning("   File %d : %d - %s", i + 1, len(notmathkeys[i]), notmathkeys[i])
                i += 1

            zVars['NotMatched'] = [notmathkeys[0], notmathkeys[1]]
            dict_result['zVars'] = zVars

        # ***** Matched keys *****
        same_keys = set(d1) & set(d2)
        logger.info("MATCHED zVARIABLES : %d", len(same_keys))
        logger.info("    %s", same_keys)

        # ***** Alphabetical order *****
        order_same_keys = sorted(list(same_keys))
        n_same_keys = len(order_same_keys)

        j = 1

        diff_array = {}  # For different dimensions
        diff_data = [] # For different data

        diff_zvar_values = [] # For zVariable key which has different values

        NotMatch_vAttr = {}
        vAttrs = {}
        Value_vAttr = {}

        # forced_ignored_zvar = []

        for key in order_same_keys:
            if (key in list_ignore_zvar):
                continue

            # Raw values comparison : It's really necessary for time values like "Epoch"
            #   cdf1.raw_var(key) => 549441617029459008
            #   cdf1[key] => 2017-05-30 18:39:07.845459
            field1 = cdf1.raw_var(key)
            field2 = cdf2.raw_var(key)

            # *°*°*°*°*°*°*°*°*°*°*°*°*
            # *°* Compare zVariables *°*
            # *°*°*°*°*°*°*°*°*°*°*°*°*

            if len(field1) != len(field2):
                logger.warning("%s:     %s      %s", key, np.array(field1.shape), np.array(field2.shape))
                diff_array[key] = [field1.shape,field2.shape]
                j += 1

            else:
                arraycheck2 = field1[...] == field2[...]
                uniq_val = np.unique(arraycheck2)  # [], [False  True], [ True], [ False]

                # zVariable's key : Different values
                if False in uniq_val:
                    logger.warning("Different values for zVariable '%s' : %s | %s", key, field1, field2)
                    diff_zvar_values.append(key)

            # *°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*
            # *°* Compare Variable Attributes *°*
            # *°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*°*

            # Ignored zVariables for comparison
            if list_ignore_vatt != []:
                logger.warning("%s Variable Attributes to be ignored for comparison : %s", len(list_ignore_vatt), list_ignore_vatt)

            tab_diff = get_not_matched_vAttrKey(field1, field2)
            
            # Case of ACQUISITION_TIME_LABEL ACQUISITION_TIME_UNITS BAND_LABEL CHANNEL_LABEL FRONT_END_LABEL RPW_STATUS_LABEL
            #         TEMPERATURE_LABEL ...
            # if tab_diff == []:
            #     forced_ignored_zvar.append(key)
            #     continue

            if list_ignore_vatt !=[]:
                for item1 in list_ignore_vatt:
                    if item1 in tab_diff[0]:
                        (tab_diff[0]).remove(item1)
                for item2 in list_ignore_vatt:
                    if item2 in tab_diff[1]:
                        (tab_diff[1]).remove(item2)

            if len(tab_diff) != 0:
                if tab_diff[0] != [] or tab_diff[1] != []:
                    logger.warning("Different Variable Attribute's keys of the zVariable '%s' : %s", key, tab_diff)
                    NotMatch_vAttr[key] = tab_diff

            uniq_items_vAtt = get_matched_vAttrKey(field1, field2)
            logger.info("Identical Variable Attribute's key : %s", uniq_items_vAtt)

            vAttrsList1 = field1.attrs
            vAttrsList2 = field2.attrs

            DiffValue_vAttr = {}

            for check_item in uniq_items_vAtt:
                logger.debug("%s : %s  |  %s", check_item, vAttrsList1[check_item], vAttrsList2[check_item])

                if vAttrsList1[check_item] == vAttrsList2[check_item]:
                     logger.info("%s : equal", check_item)
                else:
                    logger.warning("%s : not equal", check_item)
                    DiffValue_vAttr[check_item] = [vAttrsList1[check_item], vAttrsList2[check_item]]
                    Value_vAttr[key] = DiffValue_vAttr
                    vAttrs['Value'] = Value_vAttr
                    logger.debug("vAttrs['Value'] : %s", vAttrs['Value'])

        if len(diff_array) != 0:
            zVars['Size'] = diff_array
        if len(diff_data) != 0:
            zVars['Value'] = diff_data
        if len(diff_zvar_values) != 0:
            zVars['Diff_Val'] = diff_zvar_values

        dict_result = {'gAttrs' : gAttrs, 'zVars' : zVars}

        if len(NotMatch_vAttr) != 0:
            vAttrs['NotMatched'] = NotMatch_vAttr
            dict_result['vAttrs'] = vAttrs
            logger.debug("Not Matched Variable Attributes : %s", NotMatch_vAttr.keys())
        if len(Value_vAttr) !=0:
            vAttrs['Value'] = Value_vAttr
            dict_result['vAttrs'] = vAttrs
            logger.debug("Variable Attribute's value different : %s", NotMatch_vAttr)

        cdf1.close()
        cdf2.close()

        for key, value in dict_result.items():
            logger.warning("*°*°* %s *°*°*", key)
            for key1, value1 in dict_result[key].items():
                logger.warning("     *°* %s : %s", key1, value1)

        # Case of we need to force to ignore some zVariables 
        # if forced_ignored_zvar != []:
        #     logger.warning("Forced ignored zVariables (Particular case) : %s", forced_ignored_zvar)

    if dict_result != {}:
        logger.warning("*°*°* FINAL RESULT *°*°*")
        logger.warning(dict_result)


    return dict_result

# *°*°*°*°*°*°*°*°
#  Main program
# *°*°*°*°*°*°*°*°

if __name__ == '__main__':
    if len(sys.argv)>=3:
        result=cdf_compare(sys.argv[1], sys.argv[2])
        logger.debug("")
        logger.debug("Result : %s", result)



