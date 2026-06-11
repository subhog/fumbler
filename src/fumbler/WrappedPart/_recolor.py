import FreeCAD, FreeCADGui, Part
import re
import math

def recolor(self, color, transparency):
  self.part.ViewObject.ShapeColor = color
  self.part.ViewObject.Transparency = int(100 * (1 - transparency))
  return self
