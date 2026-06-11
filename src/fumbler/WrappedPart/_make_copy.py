import FreeCAD, FreeCADGui, Part
import re
import math


def make_copy(self):
  return WrappedPart(self.doc, Part.show(self.part.Shape))
