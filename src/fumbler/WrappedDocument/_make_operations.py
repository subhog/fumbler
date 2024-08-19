import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart


def make_fuse(
  self,
  list
):
  if len(list) < 1:
    nope = self.doc.addObject("Part::Feature", "Nope")
    return WrappedPart(self, nope)
  head, *tail = list
  return head.fuse(tail)
