import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

def draw_chamfered_rect(
  self,
  x,
  y,
  r = 0,
  name = "Rect",
):
  radius = min(x / 2, y / 2, r)
  x2 = x / 2
  y2 = y / 2
  lines = [
    self.plot_line(x2, y2 - radius, x2 - radius, y2), ###
    self.plot_line(x2 - radius, y2, -x2 + radius, y2),
    self.plot_line(-x2 + radius, y2, -x2, y2 - radius), ###
    self.plot_line(-x2, y2 - radius, -x2, -y2 + radius),
    self.plot_line(-x2, -y2 + radius, -x2 + radius, -y2,), ###
    self.plot_line(-x2 + radius, -y2, x2 - radius, -y2),
    self.plot_line(x2 - radius, -y2, x2, -y2 + radius), ###
    self.plot_line(x2, -y2 + radius, x2, y2 - radius),
  ]

  wire = Part.Wire([line.part.Shape for line in lines])
  face = Part.show(Part.Face(wire), name)

  for line in lines:
    self.remove_and_clean(line.part)
  self.recompute()
  return WrappedPart(self, face)
