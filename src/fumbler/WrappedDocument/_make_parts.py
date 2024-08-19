import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

from ..utils import TeethInset, TeethSide

def make_teeth(
    self,
    length,
    tooth,
    height,
    depth,
    inset,
    side,
    tolerance = 0.1
  ):

  count = math.floor(length / tooth)
  step = (length - tolerance) / count
  width = step - tolerance

  parts = []

  if (inset == TeethInset.Outset) and (side == TeethSide.Bottom):
    for idx in range(count):
      if idx % 2 == 0:
        parts.append(
          self.make_loft([
            self.draw_rect(width, depth * 2).move((0, - tolerance / 2, 0)),
            self.draw_rect(width, depth * 2).move((0, - depth - tolerance / 2, height)),
          ])
          .move((width / 2, 0, 0))
          .move((idx * step + tolerance, 0, 0))
        )
  
  if (inset == TeethInset.Outset) and side == (TeethSide.Top):
    for idx in range(count):
      if idx % 2 == 1:
        parts.append(
          self.make_loft([
            self.draw_rect(width, depth * 2).move((0, + tolerance / 2, 0)),
            self.draw_rect(width, depth * 2).move((0, + depth + tolerance / 2, height)),
          ])
          .move((width / 2, 0, 0))
          .move((idx * step + tolerance, 0, 0))
        )

  if (inset == TeethInset.Inset) and (side == TeethSide.Bottom):
    for idx in range(count):
      if idx % 2 == 1:
        parts.append(
          self.make_loft([
            self.draw_rect(width + 2 * tolerance, depth * 2).move((0, - tolerance / 2, 0)),
            self.draw_rect(width + 2 * tolerance, depth * 2).move((0, depth - tolerance / 2, height)),
          ])
          .move((width / 2, 0, 0))
          .move((idx * step + tolerance, 0, 0))
        )

  if (inset == TeethInset.Inset) and (side == TeethSide.Top):
    for idx in range(count):
      if idx % 2 == 0:
        parts.append(
          self.make_loft([
            self.draw_rect(width + 2 * tolerance, depth * 2).move((0, + tolerance / 2, 0)),
            self.draw_rect(width + 2 * tolerance, depth * 2).move((0, - depth + tolerance / 2, height)),
          ])
          .move((width / 2, 0, 0))
          .move((idx * step + tolerance, 0, 0))
        )
      

  return self.make_fuse(parts)
