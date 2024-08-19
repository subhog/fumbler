import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart


def make_fuse(
  self,
  list
):
  head, *tail = list
  return head.fuse(tail)
