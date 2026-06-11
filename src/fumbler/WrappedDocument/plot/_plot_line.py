import FreeCAD, FreeCADGui, Part
import re
import math
from ...WrappedPart import WrappedPart

def plot_line(
  self,
  x0, y0,
  x1, y1,
):
  print("plot_line", x0, y0, x1, y1)
  line = self.doc.addObject("Part::Feature")
  line.Shape = Part.makeLine(FreeCAD.Vector(x0, y0, 0), FreeCAD.Vector(x1, y1, 0))
  return WrappedPart(self, line)
