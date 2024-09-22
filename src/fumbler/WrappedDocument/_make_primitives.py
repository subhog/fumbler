import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart




def make_cube(
  self,
  x,
  y,
  z,
  name = "Cube",
):
  cube = self.doc.addObject("Part::Box", name)
  cube.Length = x
  cube.Width = y
  cube.Height = z
  return WrappedPart(self, cube)


def make_cylinder(
  self,
  r,
  h,
  name = "Cylinder",
):
  v = self.doc.addObject("Part::Cylinder", name)
  v.Radius = r
  v.Height = h
  return WrappedPart(self, v)

def make_loft(
  self,
  sections,
  name = "Loft",
):
  v = self.doc.addObject("Part::Loft", name)
  v.Sections = [section.part for section in sections]
  v.Solid = True    # Make sure it's a solid
  v.Ruled = True    # Set to True if you want straight sections
  v.Closed = False  # Closed loft makes a solid (if shapes are closed and profiles are compatible)

  for section in sections:
    section.part.Visibility = False

  self.recompute()
  return WrappedPart(self, v)

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
  # v = self.doc.addObject("Part::Cylinder", name)
  # v.Radius = r
  # v.Height = h
  # return WrappedPart(self, v)

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

def make_sweep(
  self,
  shape,
  path,
):
  
  v = self.doc.addObject("Part::Sweep", "Screw")
  v.Sections = [shape.part]
  v.Spine = path.part
  v.Solid = True
  v.Frenet = True

  # helix.Visibility = False
  # tooth_a.Visibility = False
  # tooth_b.Visibility = False

  self.recompute()
  return WrappedPart(self, v)

  