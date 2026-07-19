"""
Options and configuration enums
"""


from enum import Enum


class Anchor(str, Enum):
  Corner = "Corner"
  Edge = "Edge"
  Face = "Face"
  Volume = "Volume"


TeethInset = Enum("TeethInset", ["Inset", "Outset"])
TeethSide = Enum("TeethSide", ["Bottom", "Top"])

CircleCap = Enum("CircleCap", ["None", "Flat", "Point", "RightPoint", "LeftPoint"])
