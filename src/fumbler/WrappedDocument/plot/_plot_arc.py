import FreeCAD, FreeCADGui, Part
import re
import math
from ...WrappedPart import WrappedPart

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
