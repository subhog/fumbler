import FreeCAD, FreeCADGui, Part
import re
import math

def opacity(self, transparency):
  self.part.ViewObject.Transparency = int(100 * (1 - transparency))
  return self
