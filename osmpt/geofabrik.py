#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'fernandinand'

import os


class Geofabrik:
    def __init__(self):
        """ Default region keys downloads
        """
        self.AZ = {
            'filename': 'azores-latest.osm.pbf',
            'url': 'http://download.geofabrik.de/europe/'
        }

        self.PT = {
            'filename': 'portugal-latest.osm.pbf',
            'url': 'http://download.geofabrik.de/europe/'
        }

    def downloadGeoFabrik(self, regionKey):
        """ We use GeoFabrik extracts to download Portuguese main files
            @param regionKey: The main region key to match GeoFabrik Downloads
            @type regionKey: string
        """
        import urllib2, shutil

        if regionKey == 'AZ':
            filename = self.AZ['filename']
            url = self.AZ['url'] + filename
            target = self.AZ['filename'] + '.tmp'
        else:
            filename = self.PT['filename']
            url = self.PT['url'] + filename
            target = self.PT['filename'] + '.tmp'
        try:
            req = urllib2.urlopen(url)
            block_sz = 1024
            with open('Data/Geofabrik/' + target, 'wb') as f:
                while True:
                    chunk = req.read(block_sz)
                    if not chunk:
                        break
                    f.write(chunk)
        except urllib2.URLError, e:
            print "Download error: " + e
            return False
        if regionKey == 'AZ':
            os.remove('Data/Geofabrik/' + target.replace('.tmp', ''))
            os.rename('Data/Geofabrik/' + target, 'Data/Geofabrik/' + target.replace('.tmp', ''))
            shutil.copy('Data/Geofabrik/' + target.replace('.tmp', ''), 'Data/Distritos/ACORES.osm.pbf')
        else:
            os.remove('Data/Geofabrik/' + target.replace('.tmp', ''))
            os.rename('Data/Geofabrik/' + target, 'Data/Geofabrik/' + target.replace('.tmp', ''))

        return True

    def renameFiles(self, filename):
        """ Performs the renaming and remove of OSM files
            for changesets generation
            @param filename: The filename to be renamed
            @type filename: string
        """
        try:
            # TODO: Get data folder from config
            if os.path.isfile('Data/Distritos/' + 'old_' + filename):
                os.remove('Data/Distritos/' + 'old_' + filename)
            if os.path.isfile('Data/Distritos/' + 'new_' + filename):
                os.rename('Data/Distritos/' + 'new_' + filename, 'Data/Distritos/' + 'old_' + filename)
            if os.path.isfile('Data/Distritos/' + filename):
                os.rename('Data/Distritos/' + filename, 'Data/Distritos/' + 'new_' + filename)
        except OSError, e:
            print 'Could not perform district files renaming. Reason: ' + e.strerror

    def removeFiles(self, regionName, concelho):
        """ Removes municipal level OSM PBF and GZ files
            @param regionName: The main region key
            @type regionName: string
            @param concelho: The municipality name
            @type regionName: string
        """
        try:
            # TODO: Get data folder from config
            os.remove('Data/Shared/' + regionName + '/' + concelho.strip().replace(' ', '_') +
                      '/' + concelho.strip().replace(' ', '_') + '.osm.pbf')
            os.remove('Data/Shared/' + regionName + '/' + concelho.strip().replace(' ', '_') +
                      '/' + concelho.strip().replace(' ', '_') + '.osm.gz')
        except OSError, e:
            print 'Error: ' + e.strerror + ' File: ' + e.filename
            return
