import FreeCAD, FreeCADGui, Part
import re
import math

def face_edges(
  self,
  face_idx,
):
  print(self.part.Shape.Faces[face_idx])
