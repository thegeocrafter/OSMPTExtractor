#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'fernandinand'

import os, subprocess, time


class Osmosis:
    def __init__(self):
        """ Default region keys hold by Geofabrik files
        """
        self.keys = {
            'AZ': ['AZ', 'ACORES'],
            'PT': ['PT', 'CONTINENTE', 'MADEIRA']
        }

    def cutDistritos(self, filename, region, name):
        """ Performs district level osmosis bounding box
            clip via input poly file
            @param filename: The main level OSM filename
            @type filename: string
            @param region: The region key
            @type region: string
            @param name: The district name
            @type name: string
        """
        from osmpt.geofabrik import Geofabrik

        pStart = time.time()
        print 'Starting: ' + name.strip()
        try:
            subprocess.Popen(
                ['sh', 'scripts/osmosis_distritos.sh', filename, region, name.strip().replace(' ', '_')],
                stdout=open(os.devnull, 'wb'), stderr=open('logs/cut_distritos.log', 'wb')).communicate()
            print 'Finished ' + name.strip() + ' in ' + str((time.time() - pStart)) + ' seconds!'
        except:
            print 'Osmosis District generation error. District name: ' + name

        Geofabrik().renameFiles(name.strip().replace(' ', '_') + '.osm.pbf')

    def cutConcelhos(self, distrito, region, name):
        """ Performs municipality level osmosis bounding box
            clip via input poly file as well changeset generation
            @param distrito: The district name
            @type distrito: string
            @param region: The region key
            @type region: string
            @param name: The municipality name
            @type name: string
        """
        from osmpt.geofabrik import Geofabrik

        pStart = time.time()
        print 'Starting: ' + name.strip()
        Geofabrik().removeFiles(region, str.upper(name))
        try:
            subprocess.Popen(
                ['sh', 'scripts/osmosis_concelhos.sh', str.upper(distrito.strip().replace(' ', '_')),
                 region, str.upper(name.strip().replace(' ', '_'))],
                stdout=open(os.devnull, 'wb'), stderr=open('logs/cut_concelhos.log', 'wb')).communicate()

            print 'Finished ' + name.strip() + ' in ' + str((time.time() - pStart)) + ' seconds!'
        except:
            print 'Osmosis Concelhos generation error. Concelho name: ' + name