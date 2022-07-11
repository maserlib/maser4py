#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module providing das2stream output capability for MASER datasets
"""

# import sys
# sys.path.append('/usr/local/das2srv/lib/python2.7')
# sys.path.append('/usr/local/das2srv/lib/debian8/python2.7')
# import das2

import datetime
from dateutil import parser


class MaserDas2StreamReader:

    def __init__(self, dataset, start_time, end_time, variables):

        self.time = dict()
        self.time['query'] = dict()
        if isinstance(start_time, datetime.datetime):
            self.time['query']['start'] = start_time
        else:
            self.time['query']['start'] = parser.parse(start_time)

        if isinstance(end_time, datetime.datetime):
            self.time['query']['end'] = end_time
        else:
            self.time['query']['end'] = parser.parse(end_time)

        self.time['valid'] = dict()
        self.time['valid']['min'] = datetime.datetime(1970, 1, 1)
        self.time['valid']['max'] = datetime.datetime(2030, 12, 31, 23, 59, 59)

        self.vars = variables.append['time']
        self.data = {}
        self.meta = {}

    def header(self):
        header = "<stream version 2.2>\n" \
                 "    <properties double:zFill=\"-1.0e+31\" DatumRange:xRange=\"{} to {} UTC\"/>\n" \
                 "</stream>"\
            .format(self.time['query']['start'].isoformat(),
                    self.time['query']['end'].isoformat())
        return "[01]{:06d}{}".format(len(header), header)

    def packet(self):
        packet = "<packet>\n" \
               "    <x type=\"time27\" units=\"us2000\"></x>\n"
        for var in self.vars:
            packet = packet + \
                     "    <y type=\"ascii{}\" name=\"{}\" units=\"{}\">\n" \
                     "        <properties String:yLabel=\"{}\" />\n" \
                     "    </y>"\
                         .format(self.meta[var]['slen'], var,
                                 self.meta[var]['unit'],
                                 self.meta[var]['label'])

        packet = packet + "</packet>"
        return "[02]{:06d}{}".format(len(packet), packet)

    def d2s_line(self, index):
        line = ":01:{}".format(self.data['time'][index].isoformat())
        for i in self.vars:
            for j in self.meta[i]['dlen']:
                line += " {}"

    def d2s(self):
        stream = self.header()+self.packet()
        return stream


