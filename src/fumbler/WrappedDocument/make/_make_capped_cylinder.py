import FreeCAD, FreeCADGui, Part
import re
import math
from ...WrappedPart import WrappedPart

def make_capped_cylinder(
  self,
  r,
  h,
  angle = 60,
  name = "Cylinder",
):
  return self.make_loft([
    self.draw_capped_circle(r, angle),
    self.draw_capped_circle(r, angle).elevate(h),
  ])
