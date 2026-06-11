import FreeCAD, FreeCADGui, Part
import re
import math
from ...WrappedPart import WrappedPart

def make_plot(self, xrange, yrange, fun):
  NX = round((xrange[1] - xrange[0]) / xrange[2] + 1)
  NY = round((yrange[1] - yrange[0]) / yrange[2] + 1)
  NN = NX * NY

  points = [
    (x, y, fun(x, y))
    for x in [xrange[0] + i * xrange[2] for i in range(NX)]
    for y in [yrange[0] + i * yrange[2] for i in range(NY)]
  ] + [
    (xrange[0], yrange[0], 0),
    (xrange[0], yrange[1], 0),
    (xrange[1], yrange[0], 0),
    (xrange[1], yrange[1], 0),
  ]

  faces = [
    [x * NY + y, (x + 1) * NY + y, (x + 1) * NY + y + 1]
    for x in range(NX - 1)
    for y in range(NY - 1)
  ] + [
    [x * NY + y, x * NY + y + 1, (x + 1) * NY + y + 1]
    for x in range(NX - 1)
    for y in range(NY - 1)
  ] + [
    [x * NY for x in range(NX)] + [NN + 2, NN],
    [y for y in range(NY)] + [NN + 1, NN],
    [(x + 1) * NY - 1 for x in range(NX)] + [NN + 3, NN + 1],
    [(NN - NY) + y for y in range(NY)] + [NN + 3, NN + 2],
    [NN, NN + 1, NN + 3, NN + 2],
  ]

  return self.make_polyhedron(points, faces)
