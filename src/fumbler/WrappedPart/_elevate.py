import FreeCAD, FreeCADGui, Part
import re
import math

def elevate(self, dz):
  return self.move((0, 0, dz))
