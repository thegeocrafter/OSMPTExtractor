#!/usr/bin/python
# -*- coding: UTF-8 -*-
# OSMPT - OSM extracts for Portuguese municipalities

__author__ = "The Geocrafter aka Fernando Ribeiro"
__copyright__ = "Copyright (C) 2013-2015 Fernando Ribeiro"
__license__ = "GPL"
__version__ = "2.0"

if __name__ == "__main__":
    # Connect DB
    from db.pg import DB
    from time import time

    start = time()

    db = DB('config.json')

    # Step 1 - Perform Geofabrik downloads
    from osmpt.geofabrik import Geofabrik
    print '-> STEP 1 -Starting Geofabrik downloads'
    Geofabrik().downloadGeoFabrik('AZ')
    Geofabrik().downloadGeoFabrik('PT')
    print '-> End Geofabrik downloads'

    ### 	OSMOSIS 	###
    from osmpt.osmosis import Osmosis
    #Get default keys
    o = Osmosis()
    # Step 2 - Split main areas to district level
    print '-> STEP 2 - Init distritos generation'
    # Cut Azores
    print '-> Starting Açores'
    Geofabrik().renameFiles(o.keys['AZ'][1] + '.osm.pbf')
    print '-> Done Açores'
    # Cut Madeira
    print '-> Starting Madeira'
    o.cutDistritos(Geofabrik().PT['filename'], o.keys['PT'][2], o.keys['PT'][2])
    print '-> Done Madeira'

    #Cut Continente
    d = db.getDistritos()
    print '-> Starting Continente'
    for n in d:
        o.cutDistritos(Geofabrik().PT['filename'], o.keys['PT'][1], n[0])

    print '-> Done Continente'

    print '-> Done distritos generation'

    # Step 3 - Derive municipal level files
    print '-> STEP 3 - Derive concelhos files and changes'

    print '-> Starting Acores'
    # Azores
    c = db.getConcelhos(o.keys['AZ'][1], str.lower(o.keys['AZ'][1]))
    for i in c:
       o.cutConcelhos(o.keys['AZ'][1], o.keys['AZ'][1], i[0])
    print '-> End Acores'

    # Madeira
    print '-> Starting Madeira'
    c = db.getConcelhos(o.keys['PT'][2], o.keys['PT'][2])
    for i in c:
        o.cutConcelhos(o.keys['PT'][2], o.keys['PT'][2], i[0])
    print '-> End Madeira'

    # Continente
    print '-> Starting Continente'
    for n in d:
        print '-> Starting Distrito ' + n[0]
        c = db.getConcelhos(o.keys['PT'][1], n[0])
        for i in c:
            o.cutConcelhos(n[0], o.keys['PT'][1], i[0])
        print '-> Finish Distrito ' + n[0]
    print '-> End Continente'

    # Close db connection
    db.closeConn()

    print "Overall time: " + str((time() - start)) + ' seconds!'


