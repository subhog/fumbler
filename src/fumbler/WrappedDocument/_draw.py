import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart



def draw_polygon(
  self,
  points,
  name = "Polygon"
):
  lines = []
  for idx in range(0, len(points)):
    a = points[idx]
    b = points[(idx + 1) % len(points)]
    lines.append(self.plot_line(a[0], a[1], b[0], b[1]))

  wire = Part.Wire([line.part.Shape for line in lines])
  face = Part.show(Part.Face(wire), name)

  for line in lines:
    self.remove_and_clean(line.part)
  self.recompute()
  return WrappedPart(self, face)


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




def parse_svg_path(svg_path):
  """Parse an SVG path string and extract commands and points."""
  commands = []

  tokens = svg_path.replace(",", " ").split()
  last_command = tokens[0]
  last_point = (0, 0)
  # print("TOKENS", tokens)
  idx = 0
  while idx < len(tokens):
    command = tokens[idx]
    try:
      _ = float(command)
      command = last_command
      idx -= 1
    except ValueError:
      pass
    last_command = command

    if command == "M" or command == "L":
      last_point = (float(tokens[idx+1]), float(tokens[idx+2]))
      commands.append((command, last_point))
      idx += 3
      continue
    
    if command == "m" or command == "l":
      last_point = (last_point[0] + float(tokens[idx+1]), last_point[1] + float(tokens[idx+2]))
      commands.append((command.upper(), last_point))
      idx += 3
      continue

    if command == "h":
      last_point = (last_point[0] + float(tokens[idx+1]), last_point[1])
      commands.append(("L", last_point))
      idx += 2
      continue

    if command == "H":
      last_point = (float(tokens[idx+1]), last_point[1])
      commands.append(("L", last_point))
      idx += 2
      continue
    
    if command == "v":
      last_point = (last_point[0], last_point[1] + float(tokens[idx+1]))
      commands.append(("L", last_point))
      idx += 2
      continue
    
    if command == "V":
      last_point = (last_point[0], float(tokens[idx+1]))
      commands.append(("L", last_point))
      idx += 2
      continue
    
    if command == "C":
      commands.append((
        "C",
        (float(tokens[idx+1]), float(tokens[idx+2])),
        (float(tokens[idx+3]), float(tokens[idx+4])),
        (float(tokens[idx+5]), float(tokens[idx+6])),
      ))
      last_point = (float(tokens[idx+5]), float(tokens[idx+6]))
      idx += 7
      continue
    
    if command == "c":
      pt_1 = (last_point[0] + float(tokens[idx+1]), last_point[1] + float(tokens[idx+2]))
      pt_2 = (last_point[0] + float(tokens[idx+3]), last_point[1] + float(tokens[idx+4]))
      pt_3 = (last_point[0] + float(tokens[idx+5]), last_point[1] + float(tokens[idx+6]))
      commands.append((
        "C",
        pt_1,
        pt_2,
        pt_3,
      ))
      last_point = pt_3
      idx += 7
      continue
    
    if command == "Z" or command == "z":
      commands.append(("Z", last_point))
      idx += 1
      continue

    print(f"UNKNOWN SVG COMMAND: {command} AT: ${idx}")
    raise BaseException(f"UNKNOWN SVG COMMAND: {command} AT: ${idx}")
  return commands


def vector(point):
  return FreeCAD.Vector(point[0], point[1], 0)

def draw_svg(self, svg_path, name="SVGPath"):
  """Draw a shape from an SVG path using Bezier curves."""
  commands = parse_svg_path(svg_path)

  # print("COMMANDS", commands)

  beziers = []
  current_point = None

  for i, command in enumerate(commands):
    # print(command)
    self.recompute()
    if command[0] == 'M':  # Move to
      current_point = vector(command[1])
    elif command[0] == 'L':  # Line to
      next_point = vector(command[1])
      bezier = Part.BezierCurve()
      bezier.setPoles([current_point, current_point, next_point, next_point])
      beziers.append(bezier.toShape())
      current_point = next_point
    elif command[0] == 'C':  # Cubic Bezier curve
      p1 = vector(command[1])
      p2 = vector(command[2])
      next_point = vector(command[3])
      bezier = Part.BezierCurve()
      bezier.setPoles([current_point, p1, p2, next_point])
      beziers.append(bezier.toShape())
      current_point = next_point
    elif command == 'Z':  # Close path
      if beziers:  # If there are segments
        bezier = Part.BezierCurve()
        bezier.setPoles([current_point, current_point, beziers[0].Vertexes[0], beziers[0].Vertexes[0]])  # Close with line
        beziers.append(bezier.toShape())
      break

  # for bezier in beziers:
  #   Part.show(bezier)

  wire = Part.Wire(beziers)
  face = Part.show(Part.Face(wire), name)

  self.recompute()
  return WrappedPart(self, face)

