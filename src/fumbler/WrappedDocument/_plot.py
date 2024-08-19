import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart




def plot_line(
  self,
  x0, y0,
  x1, y1,
):
  line = self.doc.addObject("Part::Feature")
  line.Shape = Part.makeLine(FreeCAD.Vector(x0, y0, 0), FreeCAD.Vector(x1, y1, 0))
  return WrappedPart(self, line)


def plot_arc(
  self,
  cx, cy,
  r,
  startAngleDeg,
  endAngleDeg,
):
  arc = self.doc.addObject("Part::Circle")
  arc.Radius = r
  arc.Angle1 = startAngleDeg
  arc.Angle2 = endAngleDeg
  arc.Placement = FreeCAD.Placement(FreeCAD.Vector(cx, cy, 0), FreeCAD.Rotation(0, 0, 0))
  return WrappedPart(self, arc)
