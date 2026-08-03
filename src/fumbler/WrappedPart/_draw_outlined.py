import FreeCAD, FreeCADGui, Part
import re
import math


def _outline_straight_edge(edge, radius):
  start = edge.Vertexes[0].Point
  end = edge.Vertexes[-1].Point
  direction = end - start
  if direction.Length == 0:
    raise ValueError("draw_outlined requires a non-zero-length wire")

  normal = FreeCAD.Vector(-direction.y, direction.x, 0)
  normal = normal * (radius / normal.Length)
  tangent = direction * (radius / direction.Length)
  boundary = Part.Wire([
    Part.makeLine(start + normal, end + normal),
    Part.Arc(end + normal, end + tangent, end - normal).toShape(),
    Part.makeLine(end - normal, start - normal),
    Part.Arc(start - normal, start - tangent, start + normal).toShape(),
  ])
  return Part.Face(boundary)


def _round_open_ends(outline, wire, radius):
  boundary_edges = list(outline.OuterWire.Edges)
  endpoints = (
    (wire.Vertexes[0].Point, wire.Edges[0]),
    (wire.Vertexes[-1].Point, wire.Edges[-1]),
  )

  for endpoint, source_edge in endpoints:
    candidates = [
      edge
      for edge in boundary_edges
      if type(edge.Curve) in (Part.Line, Part.LineSegment)
      and all(
        (vertex.Point - endpoint).Length < radius * 1.1
        for vertex in edge.Vertexes
      )
    ]
    cap_edge = min(candidates, key=lambda edge: abs(edge.Length - 2 * radius))
    boundary_edges.remove(cap_edge)

    inward_point = max(
      (vertex.Point for vertex in source_edge.Vertexes),
      key=lambda point: (point - endpoint).Length,
    )
    inward = inward_point - endpoint
    cap_midpoint = endpoint - inward * (radius / inward.Length)
    boundary_edges.append(Part.Arc(
      cap_edge.Vertexes[0].Point,
      cap_midpoint,
      cap_edge.Vertexes[-1].Point,
    ).toShape())

  sorted_edges = Part.sortEdges(boundary_edges)
  if len(sorted_edges) != 1:
    raise ValueError("could not build a continuous outline boundary")
  return Part.Face(Part.Wire(sorted_edges[0]))


def draw_outlined(self, thickness):
  if thickness <= 0:
    raise ValueError("thickness must be greater than zero")

  wire = self.part.Shape
  half_thickness = thickness / 2

  if wire.isClosed():
    outside = wire.makeOffset2D(half_thickness, 0, True, False, False)
    inside = wire.makeOffset2D(-half_thickness, 0, True, False, False)
    outline = outside.fuse(inside).removeSplitter()
  elif (
    len(wire.Edges) == 1
    and type(wire.Edges[0].Curve) in (Part.Line, Part.LineSegment)
  ):
    outline = _outline_straight_edge(wire.Edges[0], half_thickness)
  else:
    side_a = wire.makeOffset2D(
      half_thickness,
      0,
      True,
      True,
      False,
    )
    side_b = wire.makeOffset2D(
      -half_thickness,
      0,
      True,
      True,
      False,
    )
    outline = side_a.fuse(side_b).removeSplitter()
    if outline.ShapeType != "Face" and len(outline.Faces) == 1:
      outline = outline.Faces[0]
    outline = _round_open_ends(outline, wire, half_thickness)

  if outline.ShapeType != "Face" and len(outline.Faces) == 1:
    outline = outline.Faces[0]
  part = Part.show(outline, self.part.Label + " Outline")

  self.doc.recompute()
  return type(self)(self.doc, part)
