### CEG-7560 Assignment 1

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
