#!/bin/bash

# OSMembrane auto-generated pipeline for osmosis
# Name: 
# Date: Sun May 10 05:49:52 GMT 2015
# Comment:
# Args:
# - The target osm pbf file
# - The main area name (Continente, Madeira or Acores)
# - The distrito name

#Set output directories
if [ ! -d "Data\/Distritos" ]; then
  mkdir -p Data\/Distritos
fi

osmosis \
--read-pbf-fast workers=2 file=Data\/Geofabrik\/$1 \
--buffer bufferCapacity=1000 \
--bounding-polygon file=Data\/Poly\/Distritos\/$2\/$3.poly completeWays=true completeRelations=false \
--buffer bufferCapacity=1000 \
--write-pbf file=Data\/Distritos\/$3.osm.pbf