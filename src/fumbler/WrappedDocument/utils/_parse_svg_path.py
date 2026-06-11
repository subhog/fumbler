import FreeCAD, FreeCADGui, Part
import re
import math
from ...WrappedPart import WrappedPart

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
