import FreeCAD, FreeCADGui, Part
import re
import math

def rotate_around(
  self,
  center,
  axis,
  angle,
):
  self.part.Placement.rotate(FreeCAD.Vector(center[0], center[1], center[2]), FreeCAD.Vector(axis[0], axis[1], axis[2]), angle, True)
  return self
