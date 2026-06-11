import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

def make_polyhedron(
  self,
  points,
  faces,
  name = "Polyhedron"
):
  vectors = [FreeCAD.Vector(p) for p in points]
  face_parts = []
  for face in faces:
    vertices = [vectors[idx] for idx in face]
    wire = Part.makePolygon(vertices + [vertices[0]])  # Close the polygon
    face_parts.append(Part.Face(wire))

  polyhedron = self.doc.addObject("Part::Feature", name)
  polyhedron.Shape = Part.makeSolid(Part.makeShell(face_parts))

  self.recompute()
  return WrappedPart(self, polyhedron)
