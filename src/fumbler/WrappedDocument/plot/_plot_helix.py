import FreeCAD, FreeCADGui, Part
import re
import math
from ...WrappedPart import WrappedPart

def plot_helix(
  self,
  step_height,
  total_height,
  radius,
):
  helix = self.doc.addObject("Part::Feature", "PATH")
  helix.Shape = Part.makeHelix(step_height, total_height, radius)
  return WrappedPart(self, helix)
