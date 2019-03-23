### CEG-7560 Assignment 1

This README would be better read online @
https://github.com/mkijowski/vtk-assignment-1

Feel free to clone this with the following command:
```
git clone https://github.com/mkijowski/vtk-assignment-1.git
```
Note: cloning from this might get you a later version of this code than was
submitted to pilot.  Please check the commit history to see if any major changes
occured after submission (or just use the submitted code).

Attempting to build a python vtk container with
[vtk.build](../blob/master/vtk.build)

Assuming that my singularity is not so out of date that the build process hasnt
changed you can build the container with:

```
sudo singularity build ~/vtk.simg ~/git/vtk-assignment-1/vtk.build
```

Be sure to check your path to the build file.

You can then run vtk python files with the following:
```
singularity exec ~/vtk.simg ~/git/vtk-assignment/code.py
```

### First pass of locations.dat
The following changes were made to the dataset:
* remove all line swith string characters
* remove the third "row" of numbers
* remove all whitespace lines
* remove all duplicate lines

The first three changes removed about 3-4k lines (of over 50k), the last change
brought the total of unique lines to under 500.

Example code obtained from:
* [lorensen.github.io](https://lorensen.github.io/VTKExamples/site/Python/)
* [python vtk .obj input](https://stackoverflow.com/questions/52910944/how-to-show-an-obj-file-in-python-vtk)
* [vtk files linked from avida](http://avida.cs.wright.edu/courses/CEG7560/assignment.html)
* Dr. Thomas Wischgoll's office hours (thanks!)

### Usage
Assuming you have built the vtk container above you can run this program with
the following:
```
singularity exec vtk.simg python GeoAssignCoords.py
```
By default this will render the globe.obj provided in the assignment.  If you
would rather use vtkEarthSource() simply change line 19 to 
```
globj = 0
```

Also by default this will use the pared down (429 lines)
`data/unique-sorted-lat-long.dat`.  If you would rather run it on a different
dataset, make sure the first line of the dataset specifies whether that column
is `Latitude` or `Longitude`, similar to the layout of the default
`data/unique-sorted-lat-long.dat`.

You can load other data into this rendering by passing a absolute or relative
path to your data as the first argument to this python program.  Example:
```
singularity exec vtk.simg python GeoAssignCoords.py data/orientation.dat
```
`Orientation.dat` is a data file with lat/long coordinates starting in dayton
and moving north.  This was used to orient the glyphs over the rendered
globe.obj.

After playing with rotations of globe.obj, it appears there are some unique
quirks that the rendered earth model inherits, starting with being off center.
This is was easy enough to fix by finding the center of the obj in XYZ
cordinates and creating a filter to transform the globe, shifting its center to
*almost* by in line with the lat/long glyphed spheres.

