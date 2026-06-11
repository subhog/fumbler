import FreeCAD, FreeCADGui, Part
import re
import math

def remove_and_clean(self):
  self.doc.remove_and_clean(self.part)
