#! /usr/bin/env python
# -*-coding:Utf-8 -*

"""
This is a python client to query the Heliophysics Feature Catalogue.

@author: Xavier Bonnin for LESIA 11-03-2013
"""
__version__ = "1.0"
__license__ = "GPL"
__author__ = "Xavier BONNIN"
__credit__ = ["Xavier BONNIN"]
__maintainer__ = "Xavier BONNIN"
__email__ = "xavier.bonnin@obspm.fr"

__project__ = "HELIO"

import os
from datetime import datetime
from PIL import Image
import suds
import logging
from urllib.request import urlopen
import io

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.INFO)
logging.getLogger('suds.transport').setLevel(logging.INFO)
logging.getLogger('suds.xsd.schema').setLevel(logging.INFO)
logging.getLogger('suds.wsdl').setLevel(logging.INFO)

#### Set Global variables ####
TODAY = datetime.today()

SQL_TFORMAT = "%Y-%m-%d %H:%M:%S"
HFC_TFORMAT = "%Y-%m-%dT%H:%M:%S"

# TAVERNA WSDL
TAVERNA_WSDL = "http://voparis-helio.obspm.fr/hfc-hqi/HelioTavernaService?wsdl"
SQL_METHOD = "SQLSelect"

# default url of the hfc web service wsdl file
HFC_WSDL = "http://voparis-helio.obspm.fr/hfc-hqi/HelioService?wsdl"
QUERY_METHOD = "Query"

# List of HFC tables
FRC_TABLE="FRC_INFO"
OBS_TABLE="VIEW_OBS_HQI"
AR_TABLE="VIEW_AR_HQI"
CH_TABLE="VIEW_CH_HQI"
SS_TABLE="VIEW_SP_HQI"
FI_TABLE="VIEW_FIL_HQI"
RS_TABLE="VIEW_RS_HQI"
T3_TABLE="VIEW_T3_HQI"
T2_TABLE="VIEW_T2_HQI"


def get_table(feature):

    """
    Method that return the name of the HFC table
    providing a feature name
    """

    feature = feature.lower().strip()
    if (feature == "ar") or ("activeregion" in feature):
        return AR_TABLE
    elif (feature == "ch") or ("coronalhole" in feature):
        return CH_TABLE
    elif (feature == "rs") or ("radiosource" in feature):
        return RS_TABLE
    elif (feature == "ss") or (feature == "sp") or ("sunspot" in feature):
        return SS_TABLE
    elif (feature == "fi") or (feature.startswith("fil")):
        return FI_TABLE
    elif ((feature == "t3") or (feature == "type3") or
          (feature == "typeiii") or (feature == "type_iii")):
          return T3_TABLE
    elif ((feature == "t2") or (feature == "type2") or
          (feature == "typeii") or (feature == "type_ii")):
          return T2_TABLE
    else:
          print("No table for the feature %s" % (feature))
          return None

def nearest_date(date,only_date=True,
                 **kwargs):

    """
    Method to get meta-data of the nearest
    date of observation available in a given table
    """

    date_obs = date.strftime(SQL_TFORMAT)
    LIMIT=1
    ORDER = "ABS(UNIX_TIMESTAMP(DATE_OBS)-UNIX_TIMESTAMP(\"%s\"))" % (date_obs)

    votable = query(method=SQL_METHOD,
                    wsdl=TAVERNA_WSDL,
                    ORDER_BY=ORDER,
                    LIMIT=LIMIT,
        **kwargs)

    if (only_date):
        if (len(votable.tabledata) > 0):
            if (votable.tabledata[0].has_key('DATE_OBS')):
                return datetime.strptime(votable.tabledata[0]['DATE_OBS'],HFC_TFORMAT)
            else:
                return None
        else:
            return None
    else:
        return votable


def previous_date(date,only_date=False,
                 **kwargs):

    """
    Method to get meta-data of the nearest previous date of observation
    available in a given table
    """

    date_obs = date.strftime(SQL_TFORMAT)
    LIMIT=1
    if "WHERE" in kwargs:
        kwargs["WHERE"]+=" AND (DATE_OBS < \"%s\")" % (date_obs)
    else:
        kwargs["WHERE"]="(DATE_OBS < \"%s\")" % (date_obs)
    ORDER = "DATE_OBS DESC"

    votable = query(method=SQL_METHOD,
                    wsdl=TAVERNA_WSDL,
                    ORDER_BY=ORDER,
                    LIMIT=LIMIT,
        **kwargs)

    if (only_date):
        if (len(votable.tabledata) > 0):
            if (votable.tabledata[0].has_key('DATE_OBS')):
                return datetime.strptime(votable.tabledata[0]['DATE_OBS'],HFC_TFORMAT)
            else:
                return None
        else:
            return None
    else:
        return votable

def next_date(date,only_date=False,
                 **kwargs):

    """
    Method to get meta-data of the nearest next date of observation
    available in a given table
    """

    date_obs = date.strftime(SQL_TFORMAT)
    LIMIT=1
    if "WHERE" in kwargs:
        kwargs["WHERE"]+=" AND (DATE_OBS > \"%s\")" % (date_obs)
    else:
        kwargs["WHERE"]="(DATE_OBS > \"%s\")" % (date_obs)
    ORDER = "DATE_OBS ASC"

    votable = query(method=SQL_METHOD,
                    wsdl=TAVERNA_WSDL,
                    ORDER_BY=ORDER,
                    LIMIT=LIMIT,
        **kwargs)

    if (only_date):
        if (len(votable.tabledata) > 0):
            if (votable.tabledata[0].has_key('DATE_OBS')):
                return datetime.strptime(votable.tabledata[0]['DATE_OBS'],HFC_TFORMAT)
            else:
                return None
        else:
            return None
    else:
        return votable

# Method to get active region data
def get_ar(**kwargs):
    votable=query(FROM=AR_TABLE,**kwargs)
    return votable

# Method to get coronal hole data
def get_ch(**kwargs):
    return query(FROM=CH_TABLE,**kwargs)

# Method to get filament data
def get_fi(**kwargs):
    return query(FROM=FI_TABLE,**kwargs)

# Method to get sunspot data
def get_ss(**kwargs):
    return query(FROM=SS_TABLE,**kwargs)

# Method to get nancay radio source data
def get_rs(**kwargs):
    return query(FROM=RS_TABLE,**kwargs)

# Method to get type 3 burst data
def get_t3(**kwargs):
    return query(FROM=T3_TABLE,**kwargs)

# Method to get type 2 burst data
def get_t2(**kwargs):
    return query(FROM=T2_TABLE,**kwargs)

# Method to get observatory data
def get_obs(**kwargs):
    return query(FROM=OBS_TABLE,**kwargs)

# Method to get FRC data
def get_frc(**kwargs):
    return query(FROM=FRC_TABLE,**kwargs)

# Method to get the list of the HFC web service methods
def get_methods(wsdl=HFC_WSDL):
    client = suds.client.Client(wsdl)
    return str(client)

def query(**kwargs):
    """
    Method to query the HFC using the Helio Query Interface

    :param kwargs: input keywords containing query fields
    :return: votable stream
    """

    if "FROM" not in kwargs:
        print("You must provide at least the FROM input keyword!")
        return None

    wsdl = kwargs.pop("wsdl",HFC_WSDL)
    method = kwargs.pop("method","Query")
    quiet = kwargs.pop("quiet",False)

    if not quiet:
        print("Reaching %s ..." % (wsdl))
    client = suds.client.Client(wsdl)
    if not (hasattr(client.service,method)):
        print("Web service %s has no method %s!" % (wsdl,method))
        return None

    try:
        response = client.service.__getattr__(method)(**kwargs)
    except suds.WebFault as e:
        print("Can not reach %s!" % (wsdl))
        print(e)
        return None
    else:
        votable = queryResponse(response)
        if not (quiet) and (votable.tabledata is not None):
            print("%i row(s) returned." % (len(votable.tabledata)))
        return votable

# Method to parse the input votable
def parse_votable(votable):

    resource = votable.RESOURCE
    nres = len(resource)
    if (nres == 1):
        DESCRIPTION=resource[0].DESCRIPTION
        INFO = resource[0].INFO
        TABLE = resource[0].TABLE[0]
    elif (nres == 2):
        DESCRIPTION=resource[0]
        INFO=resource[1]
        TABLE=None
    elif (nres == 3):
        DESCRIPTION = resource[0]
        INFO=resource[1]
        TABLE=resource[2]

    # Add service's description to the header
    header = {'DESCRIPTION':DESCRIPTION}

    # Add query's info to the header
    info = []
    for current_row in INFO:
        current_info = {}
        if (hasattr(current_row, "_value")):
            current_info['VALUE'] = current_row._value
        if (hasattr(current_row, "value")):
            current_info['VALUE'] = current_row.value
        if (hasattr(current_row, "_name")):
            current_info['NAME'] = current_row._name
        if (hasattr(current_row, "name")):
            current_info['NAME'] = current_row.name
        info.append(current_info)
    header['INFO'] = info

    if (TABLE is None):
        return header, []

    # Add fields' info to the header
    field = [] ; current_field = {}
    if (hasattr(TABLE,"FIELD")):
        for current_row in TABLE.FIELD:
            if (type(current_row) is tuple):
                if (current_row[0] == "_datatype"):
                    current_field['DATATYPE'] = current_row[1]
                elif (current_row[0] == "_arraysize"):
                    current_field['ARRAYSIZE'] = current_row[1]
                elif (current_row[0] == "_name"):
                    current_field['NAME'] = current_row[1]
                if (field.count(current_field) == 0): field.append(current_field)
            else:
                current_field = {}
                if (hasattr(current_row, "_name")):
                    current_field['NAME'] = current_row._name
                if (hasattr(current_row, "name")):
                    current_field['NAME'] = current_row.name
                if (hasattr(current_row, "_datatype")):
                    current_field['DATATYPE'] = current_row._datatype
                if (hasattr(current_row,"_ucd")):
                    current_field['UCD'] = current_row._ucd
                if (hasattr(current_row,"_utype")):
                    current_field['UTYPE'] = current_row._utype
                if (hasattr(current_row,"_arraysize")):
                    current_field['ARRAYSIZE'] = current_row._arraysize
                field.append(current_field)
        header['FIELD'] = field


    # Add data to the tabledata list
    tabledata = []
    if (hasattr(TABLE.DATA[0],"TR")):
        for current_row in TABLE.DATA[0].TR:
            current_tabledata = {}
            if (hasattr(current_row,"TD")):
                current_row_td = current_row.TD
            else:
                current_row_td = current_row[1]

            if (type(current_row_td) is not list):
                current_tabledata[header['FIELD'][0]['NAME']]=current_row_td
            else:
                for i,current_td in enumerate(current_row_td):
                    current_tabledata[header['FIELD'][i]['NAME']]=current_td
            tabledata.append(current_tabledata)

    return header, tabledata

# Method to get the quicklook image for a given instrument and date
#def get_quicklook(instrument="AIA", observatory="SDO",


# Method to load an image file
def load_image(file):

    if (file.startswith("http:")) or \
        (file.startswith("ftp:")):
        try:
            buff = urlopen(file).read()
            file = io.StringIO(buff)
        except:
            print("Can not load %s!" % file)
            return None
    else:
        if not (os.path.isfile(file)):
            print(file+" does not exists!")
            return None
    image = Image.open(file)
    return image

# Method to overplot feature(s) on an image
#def plot_feat(features=["AR","CH"],
#              instrument="AIA", observatory="SDO",
#              date_obs=TODAY,no_image=False):


class queryResponse:

    def __init__(self,votable):
        self.votable=votable
        self.header, self.tabledata = parse_votable(self.votable)
