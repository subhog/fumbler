import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart



def draw_rect(
  self,
  x,
  y,
  name = "Rect",
):
  x2 = x / 2
  y2 = y / 2
  lines = [
    self.plot_line(x2, y2, -x2, y2),
    self.plot_line(-x2, y2, -x2, -y2),
    self.plot_line(-x2, -y2, x2, -y2),
    self.plot_line(x2, -y2, x2, y2),
  ]

  wire = Part.Wire([line.part.Shape for line in lines])
  face = Part.show(Part.Face(wire), name)

  for line in lines:
    self.remove_and_clean(line.part)
  self.recompute()
  return WrappedPart(self, face)


def draw_rounded_rect(
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
    self.plot_arc(x2 - radius, y2 - radius, radius, 0, 90),
    self.plot_line(x2 - radius, y2, -x2 + radius, y2),
    self.plot_arc(-x2 + radius, y2 - radius, radius, 90, 180),
    self.plot_line(-x2, y2 - radius, -x2, -y2 + radius),
    self.plot_arc(-x2 + radius, -y2 + radius, radius, 180, 270),
    self.plot_line(-x2 + radius, -y2, x2 - radius, -y2),
    self.plot_arc(x2 - radius, -y2 + radius, radius, 270, 360),
    self.plot_line(x2, -y2 + radius, x2, y2 - radius),
  ]

  wire = Part.Wire([line.part.Shape for line in lines])
  face = Part.show(Part.Face(wire), name)

  for line in lines:
    self.remove_and_clean(line.part)
  self.recompute()
  return WrappedPart(self, face)


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

