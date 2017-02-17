#!usr/bin/sh
pyxbgen \
    --schema-location=./CGML2_0/CityGML.xsd --module=base \
    --schema-location=./CGML2_0/CityGML/appearance.xsd --module=appearance \
    --schema-location=./CGML2_0/CityGML/bridge.xsd --module=bridge \
    --schema-location=./CGML2_0/CityGML/building.xsd --module=building \
    --schema-location=./CGML2_0/CityGML/cityFurniture.xsd --module=cityFurniture \
    --schema-location=./CGML2_0/CityGML/cityGMLBase.xsd --module=cityGMLBase \
    --schema-location=./CGML2_0/CityGML/cityObjectGroup.xsd --module=cityObjectGroup \
    --schema-location=./CGML2_0/CityGML/generics.xsd --module=generics \
    --schema-location=./CGML2_0/CityGML/landUse.xsd --module=landUse \
    --schema-location=./CGML2_0/CityGML/relief.xsd --module=relief \
    --schema-location=./CGML2_0/CityGML/texturedSurface.xsd --module=texturedSurface \
    --schema-location=./CGML2_0/CityGML/transportation.xsd --module=transportation \
    --schema-location=./CGML2_0/CityGML/tunnel.xsd --module=tunnel \
    --schema-location=./CGML2_0/CityGML/vegetation.xsd --module=vegetation \
    --schema-location=./CGML2_0/CityGML/waterBody.xsd --module=waterBody \
    --binding-root ./citygml
