import FreeCAD, FreeCADGui, Part
import re
import math

def rotate(
  self,
  axis,
  angle,
):
  self.part.Placement.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(axis[0], axis[1], axis[2]), angle, True)
  return self
