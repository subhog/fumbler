import FreeCAD, FreeCADGui, Part
import re
import math

def all_edges(
  self,
):
  return [i for i, e in enumerate(self.part.Shape.Edges)]
