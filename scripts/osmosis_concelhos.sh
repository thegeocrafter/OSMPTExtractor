#!/bin/bash

# OSMembrane auto-generated pipeline for osmosis
# Name: 
# Date: Tue Dec 12 20:26 GMT 2013
# Comment:
# Args:
# - The target distrito name
# - The main area name (Continente, Madeira or Acores)
# - The concelho name (corrected as dict)

# Set output directories
if [ ! -d "Data\/Shared\/$2\/$3" ]; then
  mkdir -p Data\/Shared\/$2\/$3
fi

now=$(date +"%d%m%Y")

osmosis \
--read-pbf-fast workers=2 file=Data\/Distritos\/old_$1.osm.pbf outPipe.0=1 \
--read-pbf-fast workers=2 file=Data\/Distritos\/new_$1.osm.pbf outPipe.0=2 \
--tee 2 inPipe.0=2 outPipe.0=3 outPipe.1=4 \
--buffer bufferCapacity=500 inPipe.0=1 outPipe.0=5 \
--buffer bufferCapacity=500 inPipe.0=3 outPipe.0=6 \
--bounding-polygon file=Data\/Poly\/Concelhos\/$2\/$3.poly completeWays=true completeRelations=false inPipe.0=6 outPipe.0=7 \
--buffer bufferCapacity=250 inPipe.0=4 outPipe.0=8 \
--bounding-polygon file=Data\/Poly\/Concelhos\/$2\/$3.poly completeWays=true completeRelations=false inPipe.0=8 outPipe.0=9 \
--tee 2 inPipe.0=9 outPipe.0=10 outPipe.1=11 \
--buffer bufferCapacity=500 inPipe.0=10 outPipe.0=12 \
--buffer bufferCapacity=500 inPipe.0=11 outPipe.0=13 \
--bounding-polygon file=Data\/Poly\/Concelhos\/$2\/$3.poly completeWays=true completeRelations=false inPipe.0=5 outPipe.0=14 \
--derive-change inPipe.0=14 inPipe.1=7 outPipe.0=15 \
--write-xml file=Data\/Shared\/$2\/$3\/$3.osm.gz compressionMethod=gzip inPipe.0=12 \
--write-pbf file=Data\/Shared\/$2\/$3\/$3.osm.pbf inPipe.0=13 \
--buffer-change bufferCapacity=300 inPipe.0=15 outPipe.0=16 \
--write-xml-change file=Data\/Shared\/$2\/$3\/$3_$now.osc compressionMethod=gzip inPipe.0=16