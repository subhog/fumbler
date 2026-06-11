import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

def parse_svg_path(svg_path, scale=1):
  """Parse an SVG path string and extract commands and points."""
  commands = []

  path = svg_path.replace(",", " ")
  path = re.sub(r'(?<=[A-Za-z])(?=\d)', ' ', path)
  tokens = path.split()

  last_command = tokens[0]
  last_point = (0, 0)
  # print("TOKENS", tokens)
  idx = 0

  def POS(t):
    # print("T", )
    return float(int(float(t) * scale * 256)) / 256.0


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
      last_point = (POS(tokens[idx+1]), POS(tokens[idx+2]))
      commands.append((command, last_point))
      idx += 3
      continue
    
    if command == "m" or command == "l":
      last_point = (last_point[0] + POS(tokens[idx+1]), last_point[1] + POS(tokens[idx+2]))
      commands.append((command.upper(), last_point))
      idx += 3
      continue

    if command == "h":
      last_point = (last_point[0] + POS(tokens[idx+1]), last_point[1])
      commands.append(("L", last_point))
      idx += 2
      continue

    if command == "H":
      last_point = (POS(tokens[idx+1]), last_point[1])
      commands.append(("L", last_point))
      idx += 2
      continue
    
    if command == "v":
      last_point = (last_point[0], last_point[1] + POS(tokens[idx+1]))
      commands.append(("L", last_point))
      idx += 2
      continue
    
    if command == "V":
      last_point = (last_point[0], POS(tokens[idx+1]))
      commands.append(("L", last_point))
      idx += 2
      continue
    
    if command == "C":
      commands.append((
        "C",
        (POS(tokens[idx+1]), POS(tokens[idx+2])),
        (POS(tokens[idx+3]), POS(tokens[idx+4])),
        (POS(tokens[idx+5]), POS(tokens[idx+6])),
      ))
      last_point = (POS(tokens[idx+5]), POS(tokens[idx+6]))
      idx += 7
      continue
    
    if command == "c":
      pt_1 = (last_point[0] + POS(tokens[idx+1]), last_point[1] + POS(tokens[idx+2]))
      pt_2 = (last_point[0] + POS(tokens[idx+3]), last_point[1] + POS(tokens[idx+4]))
      pt_3 = (last_point[0] + POS(tokens[idx+5]), last_point[1] + POS(tokens[idx+6]))
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


def draw_svg(self, svg_path, scale=1, name="SVGPath"):
  """Draw a shape from an SVG path using Bezier curves."""
  commands = parse_svg_path(svg_path, scale)

  beziers = []
  current_point = None
  first_point = None

  for i, command in enumerate(commands):
    # print(command)
    self.recompute()
    if first_point is None:
      first_point = vector(command[1])

    if command[0] == 'M':  # Move to
      current_point = vector(command[1])
    elif command[0] == 'L':  # Line to
      next_point = vector(command[1])
      # bezier = Part.BezierCurve()
      # bezier.setPoles([current_point, current_point, next_point, next_point])
      # beziers.append(bezier.toShape())
      # line = self.doc.addObject("Part::Feature")
      beziers.append(Part.makeLine(current_point, next_point))
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
        # bezier = Part.BezierCurve()
        # bezier.setPoles([current_point, current_point, beziers[0].Vertexes[0], beziers[0].Vertexes[0]])  # Close with line
        # beziers.append(bezier.toShape())
        beziers.append(Part.makeLine(current_point, first_point))
      break

  # for bezier in beziers:
  #   Part.show(bezier)

  wire = Part.Wire(beziers)
  face = Part.show(Part.Face(wire), name)

  self.recompute()
  return WrappedPart(self, face)
