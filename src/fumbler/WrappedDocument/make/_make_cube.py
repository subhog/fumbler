import FreeCAD, FreeCADGui, Part
import re
import math
from ...WrappedPart import WrappedPart

def make_cube(
  self,
  x,
  y,
  z,
  name = "Cube",
):
  cube = self.doc.addObject("Part::Box", name)
  cube.Length = x
  cube.Width = y
  cube.Height = z
  return WrappedPart(self, cube)
