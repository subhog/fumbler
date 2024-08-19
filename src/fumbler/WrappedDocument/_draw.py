import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart



def draw_polygon(
  self,
  points,
  name = "Polygon"
):
  lines = []
  for idx in range(0, len(points)):
    a = points[idx]
    b = points[(idx + 1) % len(points)]
    lines.append(self.plot_line(a[0], a[1], b[0], b[1]))

  wire = Part.Wire([line.part.Shape for line in lines])
  face = Part.show(Part.Face(wire), name)

  for line in lines:
    self.remove_and_clean(line.part)
  self.recompute()
  return WrappedPart(self, face)

