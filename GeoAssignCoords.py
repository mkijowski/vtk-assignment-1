#!/usr/bin/python
# CEG 7560 
# Visual & Image Process
# Assignment 1
# Mar 22, 2019
# 
# Matthew Kijowski
# matthewkijowski@gmail.com
# w114mek
#
############

import vtk
import pandas as pd
import sys

def main():
    ## Render globe.obj (=1) or earthsource (=0)
    globj = 1

    ## Figure out if we're trying to pass in a different data file
    if len(sys.argv) > 1:
        LatLongDataFile = sys.argv[1]
    else:
        LatLongDataFile = 'data/unique-sorted-lat-long.dat'

    colors = vtk.vtkNamedColors()

    ## Latitude and Lognitude setup (mostly from source in README.md)
    g = vtk.vtkMutableDirectedGraph()
    latitude = vtk.vtkDoubleArray()
    latitude.SetName("latitude")
    longitude = vtk.vtkDoubleArray()
    longitude.SetName("longitude")

    ## Use Pandas to import lat/long from data
    latlong = pd.read_csv( LatLongDataFile, delimiter = ' ')
    for i in range(0, len(latlong)):
            g.AddVertex()
            latitude.InsertNextValue(latlong.Latitude[i])
            longitude.InsertNextValue(latlong.Longitude[i])
    g.GetVertexData().AddArray(latitude)
    g.GetVertexData().AddArray(longitude)

    ## Render blobe.obj per above, this allows for quickly switching between
    ## earthSource() and blobe.obj.
    ## Thanks for the centering info Tom!
    if globj == 1:
        ## Import Tom's globe.obj
        globeobjPath = "/home/mkijowski/git/vtk-assignment-1/data/globe.obj"
        globeSource = vtk.vtkOBJReader()
        globeSource.SetFileName(globeobjPath)
        globeSource.Update()
        center = globeSource.GetOutput().GetCenter()
        TranslateToOrigin = vtk.vtkTransform()
        TranslateToOrigin.Translate( -center[0], -center[1], -center[2])
        globe = vtk.vtkTransformPolyDataFilter()
        globe.SetInputConnection(globeSource.GetOutputPort())
        globe.SetTransform(TranslateToOrigin)
        glyphsize = 2
        radius = 62
        distance = 4.53
    else:
        ## Import Earth.source
        globe = vtk.vtkEarthSource()
        globe.OutlineOn()
        glyphsize = .02
        radius = 1
        distance = 4.53

    globe.Update()
    globeMapper = vtk.vtkPolyDataMapper()
    globeMapper.SetInputConnection(globe.GetOutputPort())
    globeActor = vtk.vtkActor()
    globeActor.SetMapper(globeMapper)


    ## Create assign (GeoAssignCoordinates) from latitudes and longitudes
    assign = vtk.vtkGeoAssignCoordinates()
    assign.SetInputData(g)
    assign.SetLatitudeArrayName("latitude")
    assign.SetLongitudeArrayName("longitude")
    assign.SetGlobeRadius(radius)
    assign.Update()
    assignMapper = vtk.vtkGraphMapper()
    assignMapper.SetInputConnection(assign.GetOutputPort())
    assignActor = vtk.vtkActor()
    assignActor.SetMapper(assignMapper)

    ## Convert assign DirectedGraph to PolyData
    graphtopoly = vtk.vtkGraphToPolyData()
    graphtopoly.SetInputData(assign.GetOutput())
    graphtopoly.Update()
    ## Sphere marker for glyph
    sphere = vtk.vtkSphereSource()
    sphere.SetThetaResolution(7)
    sphere.SetPhiResolution(7)

    ## Create glyph
    glyph = vtk.vtkGlyph3D()
    glyph.SetInputConnection(graphtopoly.GetOutputPort())
    glyph.SetSourceConnection(sphere.GetOutputPort())
    glyph.SetVectorModeToUseNormal()
    glyph.SetScaleModeToScaleByVector()
    glyph.SetScaleFactor(glyphsize)
    glyph.Update()

    ## Create filter to rotate both the IP locations
    ## Kayleigh Duncan provided the rotation numbers through trial and error
    rotateping = vtk.vtkTransform()
    if globj == 1:
        rotateping.RotateX(-95)
        rotateping.RotateY(-5)
        rotateping.RotateZ(125)
    else:
        rotateping.RotateX(0)
        rotateping.RotateY(0)
        rotateping.RotateZ(0)

    pingshift = vtk.vtkTransformPolyDataFilter()
    pingshift.SetInputConnection(glyph.GetOutputPort())
    pingshift.SetTransform(rotateping)
    pingshift.Update()

    pingMapper = vtk.vtkPolyDataMapper()
    pingMapper.SetInputConnection(pingshift.GetOutputPort())
    pingActor = vtk.vtkActor()
    pingActor.SetMapper(pingMapper)
    pingActor.GetProperty().SetColor(.5,0,0)

    ren = vtk.vtkRenderer()
    ren.AddActor(pingActor)
    #ren.AddActor(assignActor)
    ren.AddActor(globeActor)

    iren = vtk.vtkRenderWindowInteractor()
    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(1280,1024)
    renWin.AddRenderer(ren)
    renWin.SetInteractor(iren)
    ren.SetBackground(colors.GetColor3d('SlateGray'))
    ren.ResetCamera()
    ren.GetActiveCamera().SetPosition(-1.02, -4.6, 3.45)
    ren.GetActiveCamera().SetViewUp(0.12, 0.78, 0.61)
    ren.GetActiveCamera().SetDistance(distance)

    iren.Initialize()
    renWin.Render()
    iren.Start()


if __name__ == '__main__':
    main()
