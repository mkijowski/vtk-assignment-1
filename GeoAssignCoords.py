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

    mapper = vtk.vtkGraphMapper()
    mapper.SetInputConnection(assign.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
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
