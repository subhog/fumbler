from time import sleep
import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart



def draw_rounded_shape(
  self,
  centers,
  r,
  name = "RoundedShape"
):
    # dist_r = r * math.sin(math.pi / n)

  # for i in range(n):
  #   pr = here[(i - 1 + n) % n]
  #   he = here[i]
  #   ne = here[(i + 1) % n]
  #   prev.append(he.add(pr.sub(he).normalize().multiply(dist_r)))
  #   next.append(he.add(ne.sub(he).normalize().multiply(dist_r)))

  # # REGULAR FACE
  # for i in range(n):
  #   a = here[i]
  #   b = here[(i + 1) % n]
  #   segments.append(self.plot_line(a.x, a.y, b.x, b.y))

  # self.recompute()
  
  # wire = Part.Wire([segment.part.Shape for segment in segments])
  # face = Part.show(Part.Face(wire), name)

  # for segment in segments:
  #   self.remove_and_clean(segment.part)

  cent = [FreeCAD.Vector(c[0], c[1], 0) for c in centers]


  # ROUNDED FACE
  segments = []
  first = None
  previous = None
  n = len(centers)

  for i in range(n):
    
    b = cent[(i) % n]
    c = cent[(i + 1) % n]
    d = cent[(i + 2) % n]
    
    # // CALCULATE THESE ANGLES PROPERLY
    alpha = math.degrees(math.atan2(b.x - c.x, - b.y + c.y))
    beta = math.degrees(math.atan2(- d.x + c.x, d.y - c.y))

    alpha = (alpha + 360) % 360
    beta = (beta + 360) % 360
    # alpha = 0
    # beta = 40
    # (360 / n * i + 180 / n) % 360
    # beta = (360 / n * (i + 1) + 180 / n) % 360
    # print(i, "~->", alpha, beta)
    current = self.plot_arc(c.x, c.y, r, alpha, beta)
    if previous:
      segments.append(self.plot_line(
        previous.part.Shape.lastVertex().X,
        previous.part.Shape.lastVertex().Y,
        current.part.Shape.firstVertex().X,
        current.part.Shape.firstVertex().Y,
      ))
    else:
      first = current
    segments.append(current)
    previous = current
    # print("~->", alpha, beta)
    # segments.append(self.plot_line(b.x, b.y, d.x, d.y))

  segments.append(self.plot_line(
    previous.part.Shape.lastVertex().X,
    previous.part.Shape.lastVertex().Y,
    first.part.Shape.firstVertex().X,
    first.part.Shape.firstVertex().Y,
  ))


  # self.recompute()
  # sleep(1)
  
  wire = Part.Wire([segment.part.Shape for segment in segments])
  face = Part.show(Part.Face(wire), name)



  for segment in segments:
    self.remove_and_clean(segment.part)

  self.recompute()
  return WrappedPart(self, face)

def draw_rounded_n_gon(
  self,
  n,
  R,
  r,
  name = "NGon"    
):
  """
    Draws a regular n-gon with radius R and rounded corners with radius r.
    
    Parameters:
    n (int): Number of sides
    R (float): Radius of the circumscribed circle
    r (float): Radius of the corner circles
    name (string): Name of the drawing
    
    Returns:
    WrappedPart<Part.Face>: The rounded n-gon face
  """
  # Calculate angles
  # angle_step = 2 * math.pi / n
  # corner_angle = math.asin(r / (R - r))  # Angle from vertex to where corner circle touches edge
  
  # Calculate the distance from center to where corner circles touch the edges
  # edge_radius = R - r
  
  
  # here = []
  # prev = []
  # next = []
  cent = []

  corner_r = r / math.cos(math.pi / n)

  for i in range(n):
    # here.append(FreeCAD.Vector(
    #   R * math.cos(i * 2 * math.pi / n),
    #   R * math.sin(i * 2 * math.pi / n),
    #   0
    # ))
    cent.append(FreeCAD.Vector(
      (R - corner_r) * math.cos(i * 2 * math.pi / n),
      (R - corner_r) * math.sin(i * 2 * math.pi / n),
      0
    ))

  return self.draw_rounded_shape(cent, r, name)

  # lines = []
  
  # for i in range(n):
  #   # Calculate vertex position
  #   vertex_angle = i * angle_step
  #   vertex_x = R * math.cos(vertex_angle)
  #   vertex_y = R * math.sin(vertex_angle)
    
  #   # Calculate where corner circle touches the edge
  #   edge_angle = vertex_angle + angle_step / 2
  #   edge_x = edge_radius * math.cos(edge_angle)
  #   edge_y = edge_radius * math.sin(edge_angle)
    
  #   # Calculate corner circle center
  #   corner_center_x = vertex_x + r * math.cos(vertex_angle)
  #   corner_center_y = vertex_y + r * math.sin(vertex_angle)
    
  #   # Create corner circle arc
  #   arc = self.doc.addObject("Part::Circle", f"___CORNER_{i}")
  #   arc.Radius = r
    
  #   # Calculate start and end angles for the corner arc
  #   start_angle = math.degrees(vertex_angle + math.pi/2)
  #   end_angle = math.degrees(vertex_angle + math.pi/2 + angle_step)
    
  #   arc.Angle1 = start_angle
  #   arc.Angle2 = end_angle
  #   arc.Placement = FreeCAD.Placement(
  #     FreeCAD.Vector(corner_center_x, corner_center_y, 0),
  #     FreeCAD.Rotation(0, 0, 0)
  #   )
  #   arcs.append(arc)
    
  #   # Create line connecting to next corner (if not the last one)
  #   if i < n - 1:
  #     next_edge_angle = edge_angle + angle_step
  #     next_edge_x = edge_radius * math.cos(next_edge_angle)
  #     next_edge_y = edge_radius * math.sin(next_edge_angle)
      
  #     line = Part.makeLine(
  #       FreeCAD.Vector(edge_x, edge_y, 0),
  #       FreeCAD.Vector(next_edge_x, next_edge_y, 0)
  #     )
  #     line_obj = self.doc.addObject("Part::Feature", f"___LINE_{i}")
  #     line_obj.Shape = line
  #     lines.append(line_obj)
  #   else:
  #     # Connect last edge to first edge
  #     first_edge_angle = angle_step / 2
  #     first_edge_x = edge_radius * math.cos(first_edge_angle)
  #     first_edge_y = edge_radius * math.sin(first_edge_angle)
      
  #     line = Part.makeLine(
  #       FreeCAD.Vector(edge_x, edge_y, 0),
  #       FreeCAD.Vector(first_edge_x, first_edge_y, 0)
  #     )
  #     line_obj = self.doc.addObject("Part::Feature", f"___LINE_{i}")
  #     line_obj.Shape = line
  #     lines.append(line_obj)
  
  # self.recompute()
  
  # # Create wire from arcs and lines
  # shapes = [arc.Shape for arc in arcs] + [line.Shape for line in lines]
  # wire = Part.Wire(shapes)
  # face = Part.show(Part.Face(wire), name)
  
  # # Clean up temporary objects
  # for part in arcs + lines:
  #   self.remove_and_clean(part)
  
  # self.recompute()
  # return WrappedPart(self, face)


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


def draw_pillow(
  self,
  r,
  scale = 0.75,
  name = "Pillow"
):
  s = r * scale

  a = Part.BezierCurve()
  b = Part.BezierCurve()
  c = Part.BezierCurve()
  d = Part.BezierCurve()


  a.setPoles([
    FreeCAD.Vector(r, 0, 0),
    FreeCAD.Vector(r, s, 0),
    FreeCAD.Vector(s, r, 0),
    FreeCAD.Vector(0, r, 0),
  ])

  b.setPoles([
    FreeCAD.Vector(0, r, 0),
    FreeCAD.Vector(-s, r, 0),
    FreeCAD.Vector(-r, s, 0),
    FreeCAD.Vector(-r, 0, 0),
  ])

  c.setPoles([
    FreeCAD.Vector(-r, 0, 0),
    FreeCAD.Vector(-r, -s, 0),
    FreeCAD.Vector(-s, -r, 0),
    FreeCAD.Vector(0, -r, 0),
  ])

  d.setPoles([
    FreeCAD.Vector(0, -r, 0),
    FreeCAD.Vector(s, -r, 0),
    FreeCAD.Vector(r, -s, 0),
    FreeCAD.Vector(r, 0, 0),
  ])
  
  beziers = [
    a.toShape(),
    b.toShape(),
    c.toShape(),
    d.toShape(),
  ]

  wire = Part.Wire(beziers)
  face = Part.show(Part.Face(wire), name)

  # for b in beziers:
    # self.remove_and_clean(b)
  self.recompute()
  return WrappedPart(self, face)


def draw_pillow_2(
  self,
  r,
  xshift = 0.75,
  yshift = 0.25,
  # rshift = 0.5,
  rshift = 0.0625,
  name = "Pillow"
):
  s = r * xshift
  t = r * (1 + yshift)

  rp = r * (1 + rshift)
  rm = r * (1 - rshift)

  a0 = Part.BezierCurve()
  a1 = Part.BezierCurve()
  b0 = Part.BezierCurve()
  b1 = Part.BezierCurve()
  c0 = Part.BezierCurve()
  c1 = Part.BezierCurve()
  d0 = Part.BezierCurve()
  d1 = Part.BezierCurve()

  a0.setPoles([
    FreeCAD.Vector(-r, -r, 0),
    FreeCAD.Vector(-rm, -rp, 0),
    FreeCAD.Vector(-s, -t, 0),
    FreeCAD.Vector(0, -t, 0),
  ])
  a1.setPoles([
    FreeCAD.Vector(0, -t, 0),
    FreeCAD.Vector(s, -t, 0),
    FreeCAD.Vector(rm, -rp, 0),
    FreeCAD.Vector(r, -r, 0),
  ])

  b0.setPoles([
    FreeCAD.Vector(r, -r, 0),
    FreeCAD.Vector(rp, -rm, 0),
    FreeCAD.Vector(t, -s, 0),
    FreeCAD.Vector(t, 0, 0),
  ])
  b1.setPoles([
    FreeCAD.Vector(t, 0, 0),
    FreeCAD.Vector(t, s, 0),
    FreeCAD.Vector(rp, rm, 0),
    FreeCAD.Vector(r, r, 0),
  ])

  c0.setPoles([
    FreeCAD.Vector(r, r, 0),
    FreeCAD.Vector(rm, rp, 0),
    FreeCAD.Vector(s, t, 0),
    FreeCAD.Vector(0, t, 0),
  ])
  c1.setPoles([
    FreeCAD.Vector(0, t, 0),
    FreeCAD.Vector(-s, t, 0),
    FreeCAD.Vector(-rm, rp, 0),
    FreeCAD.Vector(-r, r, 0),
  ])

  d0.setPoles([
    FreeCAD.Vector(-r, r, 0),
    FreeCAD.Vector(-rp, rm, 0),
    FreeCAD.Vector(-t, s, 0),
    FreeCAD.Vector(-t, 0, 0),
  ])
  d1.setPoles([
    FreeCAD.Vector(-t, 0, 0),
    FreeCAD.Vector(-t, -s, 0),
    FreeCAD.Vector(-rp, -rm, 0),
    FreeCAD.Vector(-r, -r, 0),
  ])
  
  beziers = [
    a0.toShape(),
    a1.toShape(),
    b0.toShape(),
    b1.toShape(),
    c0.toShape(),
    c1.toShape(),
    d0.toShape(),
    d1.toShape(),
  ]

  wire = Part.Wire(beziers)
  face = Part.show(Part.Face(wire), name)

  # for b in beziers:
    # self.remove_and_clean(b)
  self.recompute()
  return WrappedPart(self, face)

