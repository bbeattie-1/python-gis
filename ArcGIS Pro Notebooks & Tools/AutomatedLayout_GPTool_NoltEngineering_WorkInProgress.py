    # -*- coding: utf-8 -*-

import arcpy

class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]

class Tool:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Nolt Engineering Location Map Generator"
        self.description = ""

    def getParameterInfo(self):
        """Define the tool parameters."""
        address_input = arcpy.Parameter(
            displayName="Address:",
            name="address",
            datatype="GPString",  # Changed to DEFeatureClass
            parameterType="Required",
            direction="Input")
        municipality_input = arcpy.Parameter(
            displayName="Municipality:",
            name="municipality",
            datatype="GPString",  # Changed to DEFeatureClass
            parameterType="Required",
            direction="Input")
        county_input = arcpy.Parameter(
            displayName="County:",
            name="county",
            datatype="GPString",  # Changed to DEFeatureClass
            parameterType="Required",
            direction="Input")

        return [address_input, municipality_input, county_input ]

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        address_inputs = parameters[0].valueAsText  # Address input parameter
        township_inputs = parameters[1].valueAsText  # Municipality input parameter
        county_inputs = parameters[2].valueAsText  # County input parameter

        def MakeRec_LL(llx, lly, w, h):
            xyRecList = [[llx, lly], [llx, lly+h], [llx+w,lly+h], [llx+w,lly], [llx,lly]]
            array = arcpy.Array([arcpy.Point(*coords) for coords in xyRecList])
            rec = arcpy.Polygon(array)
            return rec

        p = arcpy.mp.ArcGISProject('current')

        stylesheet = r'X:\GIS\ArcGIS Pro\ArcGIS Projects\Projects\NoltEngineering\NoltEngineering.stylx'

        m = p.createMap(f"z_LocationMap_{''.join(address_inputs.split(' '))}", 'MAP')
        m.addDataFromPath ('https://benjaminbeattie.maps.arcgis.com/sharing/rest/content/items/606d523213ef4836b65a8419c6a85c09/resources/styles/root.json', {'VECTOR_TILE'})

        #Create a new layout
        lyt = p.createLayout(8.5, 11, 'INCH', f"z_LocationLayout_{''.join(address_inputs.split(' '))}" )

        #Add Neatline
        neatlineStyle = p.listStyleItems(stylesheet, 'Polygon', 'Black Outline 2')[0]
        p.createPredefinedGraphicElement(lyt, MakeRec_LL(0.25,0.25,8,10.5), 'RECTANGLE',neatlineStyle, 'Neatline')

        #Add Dark Grey Footer Polygon Graphic
        backgroundFooterGeometry = [[0.24999999999999944,1.5948662612753246],[8.2500000000000142,1.5948662612753246],[8.2500000000000142,0.25],[0.24999999999999944,0.25],[0.24999999999999944,1.5948662612753246]]
        backgroundFooter = arcpy.Polygon(arcpy.Array([arcpy.Point(*coords) for coords in backgroundFooterGeometry]))
        backgroundFooterStyle = p.listStyleItems(stylesheet, 'Polygon', 'Dark Grey Fill')[0]
        backgroundFooterElement = p.createGraphicElement(lyt, backgroundFooter, backgroundFooterStyle, 'Background Footer Polygon')

        #Add Red Accent Footer Polygon Graphic
        accentFooterGeometry = [[1.9082157343129404,1.4797948882561867],[2.2055052079473496,1.4762298943334839],[3.2799453553860189,0.21624967035188047],[2.9419769547793644,0.22798398887084714],[1.9082157343129404,1.4797948882561867]]
        accentFooter = arcpy.Polygon(arcpy.Array([arcpy.Point(*coords) for coords in accentFooterGeometry]))
        accentFooterStyle = p.listStyleItems(stylesheet, 'Polygon', 'Brand Red Fill')[0]
        accentFooterElement = p.createGraphicElement(lyt, accentFooter, accentFooterStyle, 'Accent Footer Polygon')
        accentFooterElement.elementRotation = 2

        #Add Left Footer Polygon Graphic
        leftFooterGeometry = [[0.25000000000000089,1.594866261275325],[1.8598916157478025,1.594866261275325],[3.0603671131850287,0.25000000000000178],[0.25000000000000089,0.25000000000000178],[0.25000000000000089,1.594866261275325]]
        leftFooter = arcpy.Polygon(arcpy.Array([arcpy.Point(*coords) for coords in leftFooterGeometry]))
        leftFooterStyle = p.listStyleItems(stylesheet, 'Polygon', 'Black Outline 2')[0]
        p.createGraphicElement(lyt, leftFooter, leftFooterStyle, 'Left Footer Polygon')

        #Add Logo
        logoPath = r'X:\GIS\ArcGIS Pro\ArcGIS Projects\Projects\NoltEngineering\NoltEngineering_Logo_Clipped.jpeg'
        picture = p.createPictureElement (lyt, MakeRec_LL(0.3537,1.3194,1.6477,1.0694), logoPath, 'Nolt Engineering Logo')
        picture.elementPositionX = 0.3537
        picture.elementPositionY = 1.3194

        #Add Right Footer Polygon Graphic
        rightFooterGeometry = [[8.2500000000000142,2.9397325225506483],[10.2092812458326225,2.9397325225506483],[11.6702921022173722,1.5948662612753257],[8.2500000000000142,1.5948662612753257],[8.2500000000000142,2.9397325225506483]]
        rightFooter = arcpy.Polygon(arcpy.Array([arcpy.Point(*coords) for coords in rightFooterGeometry]))
        rightFooterStyle = p.listStyleItems(stylesheet, 'Polygon', 'Black Outline 2')[0]
        rightFooterElement = p.createGraphicElement(lyt, rightFooter, rightFooterStyle, 'Right Footer Polygon')
        rightFooterElement.elementRotation = 180

        #Add Project Map Text
        projectInfoGeometry = arcpy.Point(5.8875442346885523, 1.300414264177167)
        projectInfoText = p.createTextElement(lyt, projectInfoGeometry, 'POINT', "<FNT  wght='700'>Project Location Map:</FNT>", 16, 'Bahnschrift')
        projectInfoText.setAnchor('CENTER_POINT')

        #Add Date Created Text
        createdDateGeometry = arcpy.Point(6.63, 0.40)
        createdDateText = p.createTextElement(lyt, createdDateGeometry, 'POINT', '<FNT wght="600"><dyn type="date" format=""/></FNT>', 11, 'Bahnschrift')

        #Add Address Footer Text
        addressTextGeometry = arcpy.Point(6.9406, 1.1331)
        addressText = p.createTextElement(lyt, addressTextGeometry, 'POINT', f'<ALIGN horizontal = "center"><FNT size="13.5844">{address_inputs}</FNT></ALIGN>', 13.5, 'Bahnschrift')
        addressText.setAnchor('CENTER_POINT')
        addressText.elementPositionX = projectInfoText.elementPositionX

        #Add Municipality Footer Text
        municipalityTextGeometry = arcpy.Point(6.9406, 0.9225)
        municipalityText = p.createTextElement(lyt, municipalityTextGeometry, 'POINT', f'<ALIGN horizontal = "center"><FNT size="12.5844" wght="300" wdth="87" >{township_inputs}</FNT></ALIGN>' , 12.5, 'Bahnschrift')
        municipalityText.setAnchor('CENTER_POINT')
        municipalityText.elementPositionX = projectInfoText.elementPositionX

        #Add County Footer Text
        countyTextGeometry = arcpy.Point(6.9406, 0.7138)
        countyText = p.createTextElement(lyt, countyTextGeometry, 'POINT', f'<ALIGN horizontal = "center"><FNT size="12.5844" wght="300" wdth="87" >{county_inputs} County</FNT></ALIGN>' , 12.5, 'Bahnschrift')
        countyText.setAnchor('CENTER_POINT')
        countyText.elementPositionX = projectInfoText.elementPositionX

        #Add Items To Group
        parcelLocationGroupItems = [addressText, municipalityText, countyText]
        parcelLocationGroupElement = p.createGroupElement(lyt, parcelLocationGroupItems, 'Address Text Group')
        parcelLocationGroupElement.setAnchor('CENTER_POINT')
        parcelLocationGroupElement.elementPositionX = projectInfoText.elementPositionX
        parcelLocationGroupElement.elementPositionY = 0.93

        #Add Scale Container
        scaleContainerStyle = p.listStyleItems(stylesheet, 'Polygon', 'Black Outline 1')[0]
        p.createPredefinedGraphicElement(lyt, MakeRec_LL(7.8232,0.25,0.4268,0.3754), 'RECTANGLE',scaleContainerStyle, 'Scale Container')
        
        #Add Scale Initials/Date Text
        initialsGeometry = arcpy.Point(7.8662, 0.6469)
        initialsText = p.createTextElement(lyt, initialsGeometry, 'POINT', '<FNT wght="300"><dyn preSTR="BB " type="date" format="M/y"/></FNT>', 6.63, 'Bahnschrift')

        #Add Scale 1 Text
        scale1Geometry = arcpy.Point(7.9822, 0.459)
        scale1Text = p.createTextElement(lyt, scale1Geometry, 'POINT', '<FNT wght="300">1"</FNT>', 9, 'Bahnschrift')

        #Add Scale 2 Text
        scale2Geometry = arcpy.Point(7.8824, 0.272)
        scale2Text = p.createTextElement(lyt, scale2Geometry, 'POINT', "<FNT wght='300'>1000'</FNT>", 9, 'Bahnschrift')

        #Create a map frame
        mf = lyt.createMapFrame(MakeRec_LL(0.25,1.5949 ,8,9.1551), m, "Main Map Frame")

        #Create a north arrow
        northArrowStyle = p.listStyleItems(stylesheet, 'North_Arrow', 'North Arrow')[0]
        na = lyt.createMapSurroundElement(arcpy.Point(7.84,2.24), 'North_Arrow', mf, northArrowStyle, "North Arrow")
        na.elementWidth = 0.5  


        #Close all view and open and active the layout view
        lyt.openView()
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
