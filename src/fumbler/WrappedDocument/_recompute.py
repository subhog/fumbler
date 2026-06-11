import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

def recompute(self):
  self.doc.recompute()
  return self
