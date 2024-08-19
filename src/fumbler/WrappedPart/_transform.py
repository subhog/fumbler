import FreeCAD, FreeCADGui, Part
import re
import math


def move(self, delta):
  self.part.Placement.Base = (
    self.part.Placement.Base[0] + delta[0],
    self.part.Placement.Base[1] + delta[1],
    self.part.Placement.Base[2] + delta[2],
  )
  return self

def elevate(self, dz):
  return self.move((0, 0, dz))

def rotate(
  self,
  axis,
  angle,
):
  self.part.Placement.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(axis[0], axis[1], axis[2]), angle, True)
  return self

