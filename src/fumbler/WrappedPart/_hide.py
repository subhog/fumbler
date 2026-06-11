import FreeCAD, FreeCADGui, Part
import re
import math

def hide(self):
  self.part.ViewObject.Visibility = False
  return self
