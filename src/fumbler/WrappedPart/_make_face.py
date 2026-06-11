import FreeCAD, FreeCADGui, Part
import re
import math


def make_face(self, idx):
  part = self.doc.doc.addObject("Part::Feature", "Face")
  part.Shape = self.part.Shape.Faces[idx]
  self.doc.recompute()
  return WrappedPart(self.doc, part)
