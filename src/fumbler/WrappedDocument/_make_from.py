import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

def make_from(
  self,
  raw,
):
  return WrappedPart(self, Part.show(raw))
