#!/usr/bin/python

import vtk
import pandas as pd

def main():
    colors = vtk.vtkNamedColors()

    ## Latitude and Lognitude setup
    g = vtk.vtkMutableDirectedGraph()
    latitude = vtk.vtkDoubleArray()
    latitude.SetName("latitude")
    longitude = vtk.vtkDoubleArray()
    longitude.SetName("longitude")

    ## Use Pandas to import lat/long from data
    latlong = pd.read_csv('data/unique-sorted-lat-long.dat', delimiter = ' ')
    for i in range(0, len(latlong)):
            g.AddVertex()
            latitude.InsertNextValue(latlong.Latitude[i])
            longitude.InsertNextValue(latlong.Longitude[i])

    ## Create assign from latlong
    g.GetVertexData().AddArray(latitude)
    g.GetVertexData().AddArray(longitude)
    assign = vtk.vtkGeoAssignCoordinates()
    assign.SetInputData(g)
    assign.SetLatitudeArrayName("latitude")
    assign.SetLongitudeArrayName("longitude")
    assign.SetGlobeRadius(60.0)
    assign.Update()
    assignMapper = vtk.vtkGraphMapper()
    assignMapper.SetInputConnection(assign.GetOutputPort())
    assignActor = vtk.vtkActor()
    assignActor.SetMapper(assignMapper)


    ## Graph to poly
    graphtopoly = vtk.vtkGraphToPolyData()
    graphtopoly.SetInputData(assign.GetOutput())
    graphtopoly.Update()



    ## Import Tom's globe.obj
    globeobjPath = "/home/mkijowski/git/vtk-assignment-1/data/globe.obj"

    globe = vtk.vtkOBJReader()
    globe.SetFileName(globeobjPath)
    globe.Update()

    globeMapper = vtk.vtkPolyDataMapper()
    globeMapper.SetInputConnection(globe.GetOutputPort())
    globeActor = vtk.vtkActor()
    globeActor.SetMapper(globeMapper)

    ## Import Earth.source
    earthSource = vtk.vtkEarthSource()
    earthSource.OutlineOn()
    earthSource.Update()
    earthMapper = vtk.vtkPolyDataMapper()
    earthMapper.SetInputConnection(earthSource.GetOutputPort())
    earthActor = vtk.vtkActor()
    earthActor.SetMapper(earthMapper)

    ## Sphere markers for location data
    sphere = vtk.vtkSphereSource()
    sphere.SetThetaResolution(7)
    sphere.SetPhiResolution(7)

    ## Create glyph
    glyph = vtk.vtkGlyph3D()
    #glyph.SetInputConnection(earthSource.GetOutputPort())
    glyph.SetInputConnection(graphtopoly.GetOutputPort())
    #glyph.SetSourceConnection(graphtopoly.GetOutputPort())
    glyph.SetSourceConnection(sphere.GetOutputPort())
    glyph.SetVectorModeToUseNormal()
    glyph.SetScaleModeToScaleByVector()
    # Size for globe
    glyph.SetScaleFactor(2)

    #size for earth
    #glyph.SetScaleFactor(.01)

    ## 
    pingMapper = vtk.vtkPolyDataMapper()
    pingMapper.SetInputConnection(glyph.GetOutputPort())
    pingActor = vtk.vtkActor()
    pingActor.SetMapper(pingMapper)
    pingActor.GetProperty().SetColor(.5,0,0)

    ren = vtk.vtkRenderer()
    ren.AddActor(pingActor)
#    ren.AddActor(assignActor)
    ren.AddActor(globeActor)
#    ren.AddActor(earthActor)

    iren = vtk.vtkRenderWindowInteractor()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetInteractor(iren)
    ren.SetBackground(colors.GetColor3d('MidnightBlue'))
    ren.ResetCamera()
    ren.GetActiveCamera().SetPosition(-1.02, -4.6, 3.45)
    ren.GetActiveCamera().SetViewUp(0.12, 0.78, 0.61)
    ren.GetActiveCamera().SetDistance(4.53)

    iren.Initialize()
    renWin.Render()
    iren.Start()


if __name__ == '__main__':
    main()
