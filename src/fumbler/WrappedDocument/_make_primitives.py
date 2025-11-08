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


def make_from(
  self,
  raw,
):
  return WrappedPart(self, Part.show(raw))

def make_extruded(
  self,
  shape,
  height,
  name = "Extruded",
):
  v = self.doc.addObject("Part::Loft", name)
  v.Sections = [shape.part, shape.make_copy().elevate(height).part]
  v.Solid = True    # Make sure it's a solid
  v.Ruled = True    # Set to True if you want straight sections
  v.Closed = False  # Closed loft makes a solid (if shapes are closed and profiles are compatible)

  shape.part.Visibility = False

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
  path.hide()
  shape.hide()
  return WrappedPart(self, v)


def make_plot(self, xrange, yrange, fun):
  NX = round((xrange[1] - xrange[0]) / xrange[2] + 1)
  NY = round((yrange[1] - yrange[0]) / yrange[2] + 1)
  NN = NX * NY

  points = [
    (x, y, fun(x, y))
    for x in [xrange[0] + i * xrange[2] for i in range(NX)]
    for y in [yrange[0] + i * yrange[2] for i in range(NY)]
  ] + [
    (xrange[0], yrange[0], 0),
    (xrange[0], yrange[1], 0),
    (xrange[1], yrange[0], 0),
    (xrange[1], yrange[1], 0),
  ]

  faces = [
    [x * NY + y, (x + 1) * NY + y, (x + 1) * NY + y + 1]
    for x in range(NX - 1)
    for y in range(NY - 1)
  ] + [
    [x * NY + y, x * NY + y + 1, (x + 1) * NY + y + 1]
    for x in range(NX - 1)
    for y in range(NY - 1)
  ] + [
    [x * NY for x in range(NX)] + [NN + 2, NN],
    [y for y in range(NY)] + [NN + 1, NN],
    [(x + 1) * NY - 1 for x in range(NX)] + [NN + 3, NN + 1],
    [(NN - NY) + y for y in range(NY)] + [NN + 3, NN + 2],
    [NN, NN + 1, NN + 3, NN + 2],
  ]

  return self.make_polyhedron(points, faces)