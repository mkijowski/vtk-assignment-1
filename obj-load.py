#!/usr/bin/env python

import vtk

ColorBackground = [0.0, 0.0, 0.0]

FirstobjPath = "/home/mkijowski/git/vtk-assignment-1/globe.obj"

reader = vtk.vtkOBJReader()
reader.SetFileName(FirstobjPath)
reader.Update()


mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Create a rendering window and renderer

ren = vtk.vtkRenderer()
ren.SetBackground(ColorBackground)
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

# Create a renderwindowinteractor

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Assign actor to the renderer

ren.AddActor(actor)

# Enable user interface interactor

iren.Initialize()
renWin.Render()
iren.Start()

