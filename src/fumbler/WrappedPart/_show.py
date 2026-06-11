import FreeCAD, FreeCADGui, Part
import re
import math

def show(self):
  self.part.ViewObject.Visibility = True
  return self
