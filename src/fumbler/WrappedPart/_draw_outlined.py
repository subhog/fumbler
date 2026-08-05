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
    cap_edges = [
      edge
      for edge in boundary_edges
      if type(edge.Curve) in (Part.Line, Part.LineSegment)
      and all(
        (vertex.Point - endpoint).Length < radius * 1.1
        for vertex in edge.Vertexes
      )
    ]
    cap_points = [
      vertex.Point
      for edge in cap_edges
      for vertex in edge.Vertexes
    ]
    cap_start, cap_end = max(
      (
        (point_a, point_b)
        for i, point_a in enumerate(cap_points)
        for point_b in cap_points[i + 1:]
      ),
      key=lambda points: (points[0] - points[1]).Length,
    )
    for edge in cap_edges:
      boundary_edges.remove(edge)

    first_point = source_edge.valueAt(source_edge.FirstParameter)
    if (first_point - endpoint).Length < 0.000001:
      inward = source_edge.tangentAt(source_edge.FirstParameter)
    else:
      inward = -source_edge.tangentAt(source_edge.LastParameter)
    cap_midpoint = endpoint - inward * (radius / inward.Length)
    boundary_edges.append(Part.Arc(
      cap_start,
      cap_midpoint,
      cap_end,
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
