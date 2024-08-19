import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart




class WrappedDocument:


  def __init__(self, name):
    self.doc = FreeCAD.newDocument()

    doc_names = [d.Label for (_, d) in FreeCAD.listDocuments().items()]
    doc_number_pattern = re.compile(r'v(\d+)$')
    doc_numbers = [int(match.group(1)) for s in doc_names if (match := doc_number_pattern.search(s))]
    self.doc.Label = name + " v" + str(1 + (max(doc_numbers) if doc_numbers else 0))
  
  from ._maintenance import flush, recompute, remove_and_clean
  from ._plot import plot_line, plot_arc
  from ._draw import draw_polygon, draw_cubic, draw_flat_cubic
  from ._draw_rectangle import draw_rect, draw_rounded_rect, draw_chamfered_rect
  from ._draw_circle import draw_circle, draw_capped_circle, draw_pointy_circle, draw_right_pointy_circle, draw_left_pointy_circle

  from ._make_primitives import make_cube, make_cylinder, make_capped_cylinder, make_loft




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


  def make_screw_thread(self, radius, step_height, total_height, thread_depth):

    helix = self.doc.addObject("Part::Feature", "PATH")
    helix.Shape = Part.makeHelix(step_height, total_height, radius)

    tooth_a_wire = Part.Wire([
      Part.makeLine(FreeCAD.Vector(0, 0, -thread_depth), FreeCAD.Vector(thread_depth, 0, 0)),
      Part.makeLine(FreeCAD.Vector(thread_depth, 0, 0,), FreeCAD.Vector(0, 0, thread_depth)),
      Part.makeLine(FreeCAD.Vector(0, 0, thread_depth,), FreeCAD.Vector(0, 0, -thread_depth)),
    ])
    tooth_b_wire = Part.Wire([
      Part.makeLine(FreeCAD.Vector(0, 0, -thread_depth), FreeCAD.Vector(thread_depth, 0, 0)),
      Part.makeLine(FreeCAD.Vector(thread_depth, 0, 0,), FreeCAD.Vector(0, 0, thread_depth)),
      Part.makeLine(FreeCAD.Vector(0, 0, thread_depth,), FreeCAD.Vector(0, 0, -thread_depth)),
    ])
    tooth_a_wire.translate(FreeCAD.Vector(radius, 0, 0))
    tooth_b_wire.translate(FreeCAD.Vector(radius, 0, total_height))
    tooth_b_wire.Placement.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 360 * ((total_height / step_height) % 1), True)

    tooth_a = Part.show(Part.Face(tooth_a_wire), "TOOTH")
    tooth_b = Part.show(Part.Face(tooth_b_wire), "TOOTH")

    v = self.doc.addObject("Part::Sweep", "Screw")
    v.Sections = [tooth_a, tooth_b]
    v.Spine = helix
    v.Solid = True
    v.Frenet = True

    helix.Visibility = False
    tooth_a.Visibility = False
    tooth_b.Visibility = False

    self.recompute()

    return WrappedPart(self, v)
  
  def make_square_spiral(self, radius, step_height, total_height, thread_depth, thread_width):

    helix = self.doc.addObject("Part::Feature", "PATH")
    helix.Shape = Part.makeHelix(step_height, total_height, radius)

    tooth_a_wire = Part.Wire([
      Part.makeLine(FreeCAD.Vector(0, -thread_width, 0), FreeCAD.Vector(thread_depth, -thread_width, 0)),
      Part.makeLine(FreeCAD.Vector(thread_depth, -thread_width, 0), FreeCAD.Vector(thread_depth, thread_width, 0)),
      Part.makeLine(FreeCAD.Vector(thread_depth, thread_width, 0), FreeCAD.Vector(0, thread_width, 0)),
      Part.makeLine(FreeCAD.Vector(0, thread_width, 0), FreeCAD.Vector(0, -thread_width, 0)),
    ])
    tooth_b_wire = Part.Wire([
      Part.makeLine(FreeCAD.Vector(0, -thread_width, 0), FreeCAD.Vector(thread_depth, -thread_width, 0)),
      Part.makeLine(FreeCAD.Vector(thread_depth, -thread_width, 0), FreeCAD.Vector(thread_depth, thread_width, 0)),
      Part.makeLine(FreeCAD.Vector(thread_depth, thread_width, 0), FreeCAD.Vector(0, thread_width, 0)),
      Part.makeLine(FreeCAD.Vector(0, thread_width, 0), FreeCAD.Vector(0, -thread_width, 0)),
    ])
    tooth_a_wire.translate(FreeCAD.Vector(radius, 0, 0))
    tooth_b_wire.translate(FreeCAD.Vector(radius, 0, total_height))
    tooth_b_wire.Placement.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 360 * ((total_height / step_height) % 1), True)

    tooth_a = Part.show(Part.Face(tooth_a_wire), "TOOTH")
    tooth_b = Part.show(Part.Face(tooth_b_wire), "TOOTH")

    v = self.doc.addObject("Part::Sweep", "Screw")
    v.Sections = [tooth_a, tooth_b]
    v.Spine = helix
    v.Solid = True
    v.Frenet = True

    helix.Visibility = False
    tooth_a.Visibility = False
    tooth_b.Visibility = False

    self.recompute()

    return WrappedPart(self, v)

