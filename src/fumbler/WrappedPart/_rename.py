import FreeCAD, FreeCADGui, Part
import re
import math

def rename(self, name):
  self.part.Label = name
  return self
