import FreeCAD, FreeCADGui, Part
import re
import math
from ...WrappedPart import WrappedPart
from ...utils import Anchor, assert_exclusive_non_zero, first_non_none


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
  anchor = Anchor.Face,
  round = None,
  fi = None,
  chamfer = None,
  ch = None,
  ftl = None,
  ftr = None,
  fbl = None,
  fbr = None,
  ctl = None,
  ctr = None,
  cbl = None,
  cbr = None,
):
  assert_exclusive_non_zero([
    ["round", "fi", "chamfer", "ch"],
    ["ftl", "ctl"],
    ["ftr", "ctr"],
    ["fbl", "cbl"],
    ["fbr", "cbr"],
  ], {
    "round": round,
    "fi": fi,
    "chamfer": chamfer,
    "ch": ch,
    "ftl": ftl,
    "ftr": ftr,
    "fbl": fbl,
    "fbr": fbr,
    "ctl": ctl,
    "ctr": ctr,
    "cbl": cbl,
    "cbr": cbr,
  })

  tl = first_non_none([ctl, ftl, chamfer, ch, round, fi])
  tr = first_non_none([ctr, ftr, chamfer, ch, round, fi])
  bl = first_non_none([cbl, fbl, chamfer, ch, round, fi])
  br = first_non_none([cbr, fbr, chamfer, ch, round, fi])
  tl_is_radius = first_non_none([ftl, round, fi]) > 0 and ctl == None
  tr_is_radius = first_non_none([ftr, round, fi]) > 0 and ctr == None
  bl_is_radius = first_non_none([fbl, round, fi]) > 0 and cbl == None
  br_is_radius = first_non_none([fbr, round, fi]) > 0 and cbr == None

  assert x > 0, "Width must be positive"
  assert y > 0, "Height must be positive"
  assert tl + bl < y, "Total corner radii are too large for the given height"
  assert tr + br < y, "Total corner radii are too large for the given height"
  assert tl + tr < x, "Total corner radii are too large for the given width"
  assert br + bl < x, "Total corner radii are too large for the given width"

  x2 = x / 2
  y2 = y / 2
  lines = [
    self.plot_line(x2, -y2 + br,   x2, y2 - tr),
    self.plot_arc(x2 - tr, y2 - tr, tr, 0, 90) if tr_is_radius
      else self.plot_line(x2, y2 - tr,   x2 - tr, y2) if tr > 0
      else None,

    self.plot_line(x2 - tr, y2,   -x2 + tl, y2),
    self.plot_arc(-x2 + tl, y2 - tl, tl, 90, 180) if tl_is_radius
      else self.plot_line(-x2 + tl, y2,   -x2, y2 - tl) if tl > 0
      else None,

    self.plot_line(-x2, y2 - tl,   -x2, -y2 + bl),
    self.plot_arc(-x2 + bl, -y2 + bl, bl, 180, 270) if bl_is_radius
      else self.plot_line(-x2, -y2 + bl,   -x2 + bl, -y2) if bl > 0
      else None,

    self.plot_line(-x2 + bl, -y2,   x2 - br, -y2),
    self.plot_arc(x2 - br, -y2 + br, br, 270, 360) if br_is_radius
      else self.plot_line(x2 - br, -y2,   x2, -y2 + br) if br > 0
      else None,
  ]
  lines = [x for x in lines if x is not None]

  wire = Part.Wire([line.part.Shape for line in lines])
  face = Part.show(Part.Face(wire), name)

  for line in lines:
    self.remove_and_clean(line.part)
  self.recompute()
  
  part = WrappedPart(self, face)
  if anchor == Anchor.Corner:
    part.move((x2, y2, 0))
  elif anchor == Anchor.Edge:
    part.move((0, y2, 0))

  return part
