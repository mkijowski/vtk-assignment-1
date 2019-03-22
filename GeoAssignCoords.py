#!/usr/bin/python

import vtk
import pandas as pd

def main():
    colors = vtk.vtkNamedColors()

    g = vtk.vtkMutableDirectedGraph()
    latitude = vtk.vtkDoubleArray()
    latitude.SetName("latitude")
    longitude = vtk.vtkDoubleArray()
    longitude.SetName("longitude")

    latlong = pd.read_csv('data/unique-sorted-lat-long.dat', delimiter = ' ')

    for i in range(0, len(latlong)):
            g.AddVertex()
            latitude.InsertNextValue(latlong.Latitude[i])
            longitude.InsertNextValue(latlong.Longitude[i])

    g.GetVertexData().AddArray(latitude)
    g.GetVertexData().AddArray(longitude)

    assign = vtk.vtkGeoAssignCoordinates()
    assign.SetInputData(g)

    assign.SetLatitudeArrayName("latitude")
    assign.SetLongitudeArrayName("longitude")
    assign.SetGlobeRadius(1.0)
    assign.Update()

    globeobjPath = "/home/mkijowski/git/vtk-assignment-1/data/globe.obj"

    globe = vtk.vtkOBJReader()
    globe.SetFileName(globeobjPath)
    globe.Update()

    globeMapper = vtk.vtkPolyDataMapper()
    globeMapper.SetInputConnection(globe.GetOutputPort())
    globeActor = vtk.vtkActor()
    globeActor.SetMapper(globeMapper)

    glyph = vtk.vtkGlyph3D()
    glyph.SetInputConnection(globe.GetOutputPort())
    glyph.SetSourceConnection(assign.GetOutputPort())
    glyph.SetVectorModeToUseNormal()
    glyph.SetScaleModeToScaleByVector()
    glyph.SetScaleFactor(0.25)



    pingMapper = vtk.vtkGraphMapper()
    pingMapper.SetInputConnection(glyph.GetOutputPort())
    pingActor = vtk.vtkActor()
    pingActor.SetMapper(pingMapper)

    ren = vtk.vtkRenderer()
    ren.AddActor(pingActor)
    ren.AddActor(globeActor)

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
