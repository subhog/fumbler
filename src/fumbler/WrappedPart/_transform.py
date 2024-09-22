import FreeCAD, FreeCADGui, Part
import re
import math


def move(self, delta):
  x = 0 if len(delta) < 1 else delta[0]
  y = 0 if len(delta) < 2 else delta[1]
  z = 0 if len(delta) < 3 else delta[2]
  self.part.Placement.Base = (
    self.part.Placement.Base[0] + x,
    self.part.Placement.Base[1] + y,
    self.part.Placement.Base[2] + z,
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

