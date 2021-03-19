#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Maser4py - Compare 2 CDF files module"""

import logging
import os
import os.path
import sys
from pprint import pformat

import numpy as np
from maser.utils.cdf import CDF

logger = logging.getLogger(__name__)


# Checking file
def checking_file_exist(cdf_file):
    if os.path.isfile(cdf_file) == False:
        raise FileNotFoundError('%s : does not exist !' % cdf_file)
    if os.access(cdf_file, os.R_OK) == False:
        raise IOError('%s : is not readable !' % cdf_file)


#
def get_keys_and_attributes(cdf_filepath):
    """
    Get the list data keys (zVars) and global attributes (gAttrs)

    :param cdf_filepath:
    :return:
    """
    with CDF(cdf_filepath) as cdf_file:
        return list(cdf_file.keys()), cdf_file.attrs.copy()


def list_differences(a, b):
    """
    Find list differences

    :param a: first list
    :param b: second list
    :return: a tuple containing the differences
    """
    return [x for x in a if x not in b], [x for x in b if x not in a]


# Listing all items
def list_elements(liste):
    n = len(liste)
    i = 0
    while i < n:
        # logger.debug("     %s", liste[i])
        i += 1


# Deleting a dictionnary's key
def delete_key(dict, key_to_remove):
    if key_to_remove in dict:
        del dict[key_to_remove]
    else:
        logger.debug("Key to remove '%s' does not exist !", key_to_remove)
    return dict


# Getting a given vAttr's not matched keys
def get_v_att_keys_diff(field1, field2):
    """
    get the differences between v_att keys of field 1 and field 2

    :param field1:
    :param field2:
    :return:
    """

    # convert v_att (class 'spacepy.cdf.zAttrList') of cdf files to sorted
    # lists

    list_a1 = sorted([attr_key for attr_key in field1.attrs])

    list_a2 = sorted([attr_key for attr_key in field2.attrs])
    if list_a1 != list_a2:
        result = list_differences(list_a1, list_a2)
    else:
        result = []

    return result


# Getting a given vAttr's matched keys
def get_matched_vAttrKey(field1, field2):
    set_a1 = set([attr_key for attr_key in field1.attrs])

    set_a2 = set([attr_key for attr_key in field2.attrs])

    return set_a1 & set_a2


def compare_global_attributes(global_att1, global_att2, list_ignore_gatt):
    """

    Compare global attributes

    :return: the global attribute differences
    """

    # initialize the Global Attributes dictionary
    gAttrs = {}

    list_global_att1 = sorted(list(global_att1.keys()))
    list_global_att2 = sorted(list(global_att2.keys()))

    if list_ignore_gatt != []:
        list_global_att1 = [
            n for n in list_global_att1 if n not in list_ignore_gatt]
        list_global_att2 = [
            n for n in list_global_att2 if n not in list_ignore_gatt]
    not_match_attribute = list_differences(list_global_att1, list_global_att2)

    l1 = len(not_match_attribute[0])
    l2 = len(not_match_attribute[1])

    if list_ignore_gatt != []:
        logger.debug('%s Global Attributes to be ignored for comparison : %s', len(list_ignore_gatt),
                     list_ignore_gatt)
    if l1 != 0 or l2 != 0:
        logger.debug('Global attributes: different')
        logger.debug('File 1 : %s%s', str(
            len(global_att1)), ' global attributes')
        logger.debug("File1's Global Attributes List : %s", list_global_att1)
        logger.debug('File 2 : %s%s', str(
            len(global_att2)), ' global attributes')
        logger.debug("File2's Global Attributes List : %s", list_global_att2)
        logger.debug('Not matched global attributes')
        logger.debug('   File1 : %s - %s',
                     len(not_match_attribute[0]), not_match_attribute[0])
        logger.debug('   File2 : %s - %s',
                     len(not_match_attribute[1]), not_match_attribute[1])

        gAttrs['NotMatched'] = not_match_attribute
        # Remove not matched keys from the 2 dictionaries
        not_match1 = not_match_attribute[0]
        not_match2 = not_match_attribute[1]

        for key_to_remove in not_match1:
            global_att1 = delete_key(global_att1, key_to_remove)

        for key_to_remove in not_match2:
            global_att2 = delete_key(global_att2, key_to_remove)

    # Compare Global Attributes's value
    nl1 = len(global_att1)
    nl2 = len(global_att2)
    if nl1 == nl2:  # The 2 dictionaries have the same keys
        # Compare 2 dictionaries
        checking = global_att1 == global_att2
        if checking == False:
            # Not equal !!
            logger.debug('Global attributes value: different')
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
                        logger.debug('   File1 : %s', val1)
                        logger.debug('   File2 : %s', val2)

                        DiffValueAttr[com_att] = [val1, val2]
            if DiffValueAttr:
                gAttrs['Value'] = DiffValueAttr
            logger.debug('gAttrs:  %s', pformat(DiffValueAttr, width=1000))

    return gAttrs


def precision_dict_from_list(precision_list):
    precision_dict = {}
    for key_value in precision_list:
        key, value = key_value.split(':')
        precision_dict[key] = float(value)
    return precision_dict


def compare_z_var(field1, field2, key, dict_numerical_precision={}, shape_diff_dict={}, value_diff_dict={}):
    # check if fields have the same shape
    if field1.shape:
        data1 = field1[...]
    else:
        # Make sure to have numpy ndarray if data1 is a scalar
        data1 = np.atleast_1d(field1[...])
    if field2.shape:
        data2 = field2[...]
    else:
        # Make sure to have numpy ndarray if data2 is a scalar
        data2 = np.atleast_1d(field2[...])

    res = False

    if data1.shape != data2.shape:
        logger.debug('%s - array shape is different: %s | %s',
                     key, field1.shape, field2.shape)
        shape_diff_dict[key] = [data1.shape, data2.shape]

    else:
        differences_mask = data1 != data2
        fields_are_different = np.any(differences_mask)

        # zVariable's key : check for different values
        if fields_are_different:
            if key in dict_numerical_precision.keys():
                tab_diff = np.isclose(
                    data1, data2, atol=dict_numerical_precision[key])
                res = np.all(tab_diff)
                if not res:
                    logger.debug(
                        "Different values for zVariable '%s' : %s | %s", key, field1, field2)
                    value_diff_dict[key] = [
                        data1[differences_mask], data2[differences_mask]]

            else:
                logger.debug(
                    "Different values for zVariable '%s' : %s | %s", key, field1, field2)
                value_diff_dict[key] = [
                    data1[differences_mask], data2[differences_mask]]

    return shape_diff_dict, value_diff_dict


def compare_v_att(field1, field2, key, key_diff_dict={}, value_diff_dict={}, list_ignore_vatt=[]):
    v_att_keys_diff = list_differences(field1.attrs, field2.attrs)

    if list_ignore_vatt != []:
        logger.debug('%s Variable Attributes to be ignored for comparison : %s', len(list_ignore_vatt),
                     list_ignore_vatt)
        for item1 in list_ignore_vatt:
            if item1 in v_att_keys_diff[0]:
                (v_att_keys_diff[0]).remove(item1)
        for item2 in list_ignore_vatt:
            if item2 in v_att_keys_diff[1]:
                (v_att_keys_diff[1]).remove(item2)

    if len(v_att_keys_diff[0]) != 0 or len(v_att_keys_diff[1]) != 0:
        logger.debug(
            "Different Variable Attribute's keys of the zVariable '%s' : %s", key, v_att_keys_diff)
        key_diff_dict[key] = v_att_keys_diff

    common_v_att_keys = get_matched_vAttrKey(field1, field2)
    logger.debug("Identical Variable Attribute's key : %s", common_v_att_keys)

    vAttrsList1 = field1.attrs
    vAttrsList2 = field2.attrs

    DiffValue_vAttr = {}

    for check_item in common_v_att_keys:
        logger.debug('%s : %s  |  %s', check_item, vAttrsList1[
                     check_item], vAttrsList2[check_item])

        if vAttrsList1[check_item] == vAttrsList2[check_item]:
            logger.debug('%s : equal', check_item)
        else:
            logger.debug('%s : not equal', check_item)
            DiffValue_vAttr[check_item] = [
                vAttrsList1[check_item], vAttrsList2[check_item]]
            value_diff_dict[key] = DiffValue_vAttr
            logger.debug("vAttrs['Value'] : %s", value_diff_dict)

    return key_diff_dict, value_diff_dict


def compare_data(cdf1, cdf2, cdf_keys1, cdf_keys2, list_ignore_zvar=[], list_ignore_vatt=[], list_numerical_precision=[]):
    zVars = {}  # store data differences
    vAttrs = {}  # store attribute differences

    # Ignored zVariables for comparison
    if list_ignore_zvar != []:
        logger.debug('%s zVariables to be ignored for comparison : %s', len(
            list_ignore_zvar), list_ignore_zvar)

    if len(cdf_keys1) != len(cdf_keys2):
        logger.debug('Zvariables: different')

    # ***** Not matched keys *****
    list_diff1, list_diff2 = list_differences(cdf_keys1, cdf_keys2)

    if cdf_keys1 == cdf_keys2:
        logger.debug('Zvariables keys: identical')
        same_keys = cdf_keys1
        ordered_common_keys = sorted(list(same_keys))
    else:
        if (list_diff1 != []) or (list_diff2 != []):

            zVars['Keys'] = [list_diff1, list_diff2]

            logger.debug('NOT MATCHED zVARIABLES :')
            for idx, diff_list in enumerate(zVars['Keys']):
                logger.debug('   File %d : %d - %s', idx +
                             1, len(diff_list), diff_list)
        # ***** Matched keys *****
        same_keys = set(cdf_keys1) & set(cdf_keys2)

        # ***** Alphabetical order *****
        ordered_common_keys = sorted(list(same_keys))

    logger.debug('MATCHED zVARIABLES : %d', len(ordered_common_keys))
    logger.debug('    %s', ordered_common_keys)

    # prepare the dicts to store z_var and v_att diff
    v_att_key_diff_dict = {}
    v_att_value_diff_dict = {}
    z_var_shape_diff_dict = {}
    z_var_value_diff_dict = {}

    for key in ordered_common_keys:
        if (key in list_ignore_zvar):
            continue

        # Raw values comparison : It's really necessary for time values like "Epoch"
        #   cdf1.raw_var(key) => 549441617029459008
        #   cdf1[key] => 2017-05-30 18:39:07.845459
        field1 = cdf1.raw_var(key)
        field2 = cdf2.raw_var(key)

        dict_numerical_precision = {}
        if len(list_numerical_precision) != 0:
            dict_numerical_precision = precision_dict_from_list(
                list_numerical_precision)

        compare_z_var(field1, field2, key, dict_numerical_precision=dict_numerical_precision,
                      shape_diff_dict=z_var_shape_diff_dict, value_diff_dict=z_var_value_diff_dict)

        compare_v_att(field1, field2, key,
                      list_ignore_vatt=list_ignore_vatt,
                      key_diff_dict=v_att_key_diff_dict,
                      value_diff_dict=v_att_value_diff_dict)

    if v_att_value_diff_dict:
        vAttrs['Value'] = v_att_value_diff_dict
        logger.debug("vAttrs['Value'] : %s", vAttrs['Value'])

    if z_var_shape_diff_dict:
        zVars['Shape'] = z_var_shape_diff_dict
    if z_var_value_diff_dict:
        zVars['Value'] = z_var_value_diff_dict

    if v_att_key_diff_dict:
        vAttrs['Keys'] = v_att_key_diff_dict
    if v_att_value_diff_dict:
        vAttrs['Value'] = v_att_value_diff_dict

    return zVars, vAttrs


# Comparing 2 CDF files data
def cdf_compare(cdf_file1, cdf_file2, list_ignore_gatt=[], list_ignore_zvar=[], list_ignore_vatt=[], list_numerical_precision=[]):
    logger.debug(' CDF file 1 : %s', cdf_file1)
    logger.debug(' CDF file 2 : %s', cdf_file2)
    checking_file_exist(cdf_file1)
    checking_file_exist(cdf_file2)

    cdf_keys1, global_att1 = get_keys_and_attributes(cdf_file1)
    cdf_keys2, global_att2 = get_keys_and_attributes(cdf_file2)

    cdf1 = CDF(cdf_file1)
    cdf2 = CDF(cdf_file2)

    dict_result = {}

    gAttrs = compare_global_attributes(
        global_att1, global_att2, list_ignore_gatt)

    if gAttrs:
        dict_result['gAttrs'] = gAttrs

    zVars, vAttrs = compare_data(cdf1, cdf2, cdf_keys1, cdf_keys2,
                                 list_ignore_zvar=list_ignore_zvar, list_ignore_vatt=list_ignore_vatt,
                                 list_numerical_precision=list_numerical_precision)

    if zVars:
        dict_result['zVars'] = zVars

    if vAttrs:
        dict_result['vAttrs'] = vAttrs

    cdf1.close()
    cdf2.close()

    for key, value in dict_result.items():
        logger.debug('*°*°* %s *°*°*', key)
        for key1, value1 in dict_result[key].items():
            logger.debug('     *°* %s : %s', key1, value1)

    # Case of we need to force to ignore some zVariables
    # if forced_ignored_zvar != []:
    #     logger.debug("Forced ignored zVariables (Particular case) : %s", forced_ignored_zvar)

    logger.debug('Return value: %s', pformat(dict_result, width=1000))
    return dict_result


def main(cdf_file1, cdf_file2):
    if len(sys.argv) >= 3:

        list_argv = sys.argv
        list_ignore_gatt = []
        list_ignore_zvar = []
        list_ignore_vatt = []
        list_numerical_precision = []

        if '--ignore_gatt' in (list_argv):
            ind_ignore_gatt = (list_argv).index('--ignore_gatt')
            list_ignore_gatt = []
            for item in list_argv[ind_ignore_gatt + 1:]:
                if (item.startswith('--ignore_') == False and item.startswith('--precision') == False):
                    list_ignore_gatt.append(item)
                else:
                    break
            logger.warning(
                'Ignored global attributes list : %s', list_ignore_gatt)
        else:
            logger.debug('No global attributes to be ignored')

        if '--ignore_zvar' in (list_argv):
            ind_ignore_zvar = (list_argv).index('--ignore_zvar')
            list_ignore_zvar = []
            for item in list_argv[ind_ignore_zvar + 1:]:
                if (item.startswith('--ignore_') == False and item.startswith('--precision') == False):
                    list_ignore_zvar.append(item)
                else:
                    break
            logger.warning('Ignored zVariables list : %s', list_ignore_zvar)
        else:
            logger.debug('No zVariables to be ignored')

        if '--ignore_vatt' in (list_argv):
            ind_ignore_vatt = (list_argv).index('--ignore_vatt')
            list_ignore_vatt = []
            for item in list_argv[ind_ignore_vatt + 1:]:
                if (item.startswith('--ignore_') == False and item.startswith('--precision') == False):
                    list_ignore_vatt.append(item)
                else:
                    break
            logger.warning(
                'Ignored variable attributes list : %s', list_ignore_vatt)
        else:
            logger.debug('No variable attributes to be ignored')

        if '--precision' in (list_argv):
            ind_precision_zvar = (list_argv).index('--precision')
            list_numerical_precision = []
            for item in list_argv[ind_precision_zvar + 1:]:
                if (item.startswith('--ignore_') == False and item.startswith('--precision') == False):
                    list_numerical_precision.append(item)
                else:
                    break
            logger.warning('Numerical precision list : %s',
                           list_numerical_precision)
        else:
            logger.debug('No zVariable precision set')

        if '--precision' in (list_argv):
            ind_precision_zvar = (list_argv).index('--precision')
            list_numerical_precision = []
            for item in list_argv[ind_precision_zvar + 1:]:
                if (item.startswith('--ignore_') == False and item.startswith('--precision') == False):
                    list_numerical_precision.append(item)
                else:
                    break
            logger.warning('Numerical precision list : %s',
                           list_numerical_precision)
        else:
            logger.debug('No zVariable precision set')

        result = cdf_compare(cdf_file1, cdf_file2,
                             list_ignore_gatt=list_ignore_gatt,
                             list_ignore_zvar=list_ignore_zvar,
                             list_ignore_vatt=list_ignore_vatt,
                             list_numerical_precision=list_numerical_precision)
        logger.info('Final result : %s', pformat(result, width=1000))


# *°*°*°*°*°*°*°*°
#  Main program
# *°*°*°*°*°*°*°*°

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
