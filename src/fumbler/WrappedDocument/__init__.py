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
  
  @staticmethod
  def close_all():
    [FreeCAD.closeDocument(d) for d in FreeCAD.listDocuments()]

  from ._maintenance import flush, recompute, remove_and_clean
  from ._plot import plot_line, plot_arc
  from ._draw import draw_rect, draw_rounded_rect, draw_chamfered_rect, draw_polygon
  from ._draw_circle import draw_circle, draw_capped_circle, draw_pointy_circle, draw_right_pointy_circle, draw_left_pointy_circle



  def draw_cubic(
    self,
    points,
    name = "Cubic"
  ):
    beziers = []
    for i in range(len(points)):
      j = (i + 1) % len(points)
      p0 = points[i][0]
      p1 = points[i][1]
      p2 = points[i][2]
      p3 = points[j][0]

      bezier = Part.BezierCurve()
      # bezier.increaseDegree(3)
      bezier.setPoles([
        FreeCAD.Vector(p0[0], p0[1], p0[2]),
        FreeCAD.Vector(p1[0], p1[1], p1[2]),
        FreeCAD.Vector(p2[0], p2[1], p2[2]),
        FreeCAD.Vector(p3[0], p3[1], p3[2]),
      ])
      beziers.append(bezier.toShape())

    wire = Part.Wire(beziers)
    face = Part.show(Part.Face(wire), name)

    # for b in beziers:
      # self.remove_and_clean(b)
    self.recompute()
    return WrappedPart(self, face)
  
  def draw_flat_cubic(
    self,
    points,
    name = "Cubic"
  ):
    beziers = []
    for i in range(len(points)):
      j = (i + 1) % len(points)
      p0 = points[i][0]
      p1 = points[i][1]
      p2 = points[i][2]
      p3 = points[j][0]

      bezier = Part.BezierCurve()
      # bezier.increaseDegree(3)
      bezier.setPoles([
        FreeCAD.Vector(p0[0], p0[1], 0),
        FreeCAD.Vector(p1[0], p1[1], 0),
        FreeCAD.Vector(p2[0], p2[1], 0),
        FreeCAD.Vector(p3[0], p3[1], 0),
      ])
      beziers.append(bezier.toShape())

    wire = Part.Wire(beziers)
    face = Part.show(Part.Face(wire), name)

    # for b in beziers:
      # self.remove_and_clean(b)
    self.recompute()
    return WrappedPart(self, face)


  def draw_roller(
    self,
    n,
    long_arc,
    short_arc,
    name = "Roller"
  ):
    VERTICES_X_DIFFERENCE = math.sin(math.pi / n)
    VERTICES_Y_DIFFERENCE = 1 + math.cos(math.pi / n)
    VERTICES_DIAGONAL = math.sqrt(VERTICES_X_DIFFERENCE * VERTICES_X_DIFFERENCE + VERTICES_Y_DIFFERENCE * VERTICES_Y_DIFFERENCE)
    EPICIRCLE_RADIUS = (long_arc - short_arc) / VERTICES_DIAGONAL
    ANGLE_DOUBLE_RAD = math.pi * 2 / n
    ANGLE_DOUBLE_DEG = 360 / n
    ANGLE_SINGLE_DEG = 180 / n
    ANGLE_HALF_DEG = 90 / n


    arcs = []
    for i in range(n):
      j = (i + math.ceil(n / 2)) % n
      center_i = FreeCAD.Vector(
        EPICIRCLE_RADIUS * math.cos(ANGLE_DOUBLE_RAD * i),
        EPICIRCLE_RADIUS * math.sin(ANGLE_DOUBLE_RAD * i),
        0
      )
      center_j = FreeCAD.Vector(
        EPICIRCLE_RADIUS * math.cos(ANGLE_DOUBLE_RAD * j),
        EPICIRCLE_RADIUS * math.sin(ANGLE_DOUBLE_RAD * j),
        0
      )

      arc = self.doc.addObject("Part::Circle", f"___LONG {i}")
      arc.Radius = long_arc
      arc.Angle1 = (180 + ANGLE_DOUBLE_DEG * i - ANGLE_HALF_DEG) % 360
      arc.Angle2 = (180 + ANGLE_DOUBLE_DEG * i + ANGLE_HALF_DEG) % 360
      arc.Placement = FreeCAD.Placement(center_i, FreeCAD.Rotation(0, 0, 0))
      arcs.append(arc)
      
      arc = self.doc.addObject("Part::Circle", f"___SHORT {i}")
      arc.Radius = short_arc
      arc.Angle1 = (ANGLE_DOUBLE_DEG * j - ANGLE_HALF_DEG) % 360
      arc.Angle2 = (ANGLE_DOUBLE_DEG * j + ANGLE_HALF_DEG) % 360
      arc.Placement = FreeCAD.Placement(center_j, FreeCAD.Rotation(0, 0, 0))
      arcs.append(arc)

    self.recompute()
    
    wire = Part.Wire([arc.Shape for arc in arcs])
    face = Part.show(Part.Face(wire), name)

    for part in arcs:
      self.remove_and_clean(part)

    self.recompute()
    return WrappedPart(self, face)





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

  def make_fuse(
    self,
    list
  ):
    head, *tail = list
    return head.fuse(tail)


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

