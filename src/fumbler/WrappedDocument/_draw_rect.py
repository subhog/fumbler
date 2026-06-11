import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart
from ..errors import FumblerConfigurationError


"""
Draws a rectangle on the z=0 plane,
with center in (0, 0, 0) and given width and height.

Parameters:
x (float): Width of the rectangle
y (float): Height of the rectangle

Keyword arguments:
name (string): Name of the element
anchor (Anchor): Anchor point for the rectangle. Default is `Anchor.Corner`.
round (float): Rounding radius
fi (float): Rounding radius (shorthand)
chamfer (float): Chamfer radius
ch (float): Chamfer radius (shorthand)
ftl (float): Top left corner rounding (fillet) radius
ftr (float): Top right corner rounding (fillet) radius
fbl (float): Bottom left corner rounding (fillet) radius
fbr (float): Bottom right corner rounding (fillet) radius
ctl (float): Top left corner chamfer radius
ctr (float): Top right corner chamfer radius
cbl (float): Bottom left corner chamfer radius
cbr (float): Bottom right corner chamfer radius


Returns:
WrappedPart<Part.Face>: 


"""
def draw_rect(
  self,
  x,
  y,
  name = "Rect",
  anchor = Anchor.Corner,
  round = 0,
  fi = 0,
  chamfer = 0,
  ch = 0,
  ftl = 0,
  ftr = 0,
  fbl = 0,
  fbr = 0,
  ctl = 0,
  ctr = 0,
  cbl = 0,
  cbr = 0,
):
  global_corner_params = ["round", "fi", "chamfer", "ch"]
  global_corner_set = [p for p in global_corner_params if p in kwargs]
  if len(global_corner_set) > 1:
    raise FumblerConfigurationError(
      f"Only one of {', '.join(global_corner_params)} may be set, "
      f"got {', '.join(global_corner_set)}"
    )

  corner_pairs = [
    ("ftl", "ctl"),
    ("ftr", "ctr"),
    ("fbl", "cbl"),
    ("fbr", "cbr"),
  ]
  for fillet_param, chamfer_param in corner_pairs:
    if fillet_param in kwargs and chamfer_param in kwargs:
      raise FumblerConfigurationError(
        f"Only one of {fillet_param} and {chamfer_param} may be set for a single corner"
      )

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
