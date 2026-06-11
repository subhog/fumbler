"""
Options and configuration enums
"""


from enum import Enum


Anchor = Enum("Anchor", ["Corner", "Edge", "Face", "Volume"])


TeethInset = Enum("TeethInset", ["Inset", "Outset"])
TeethSide = Enum("TeethSide", ["Bottom", "Top"])

CircleCap = Enum("CircleCap", ["None", "Flat", "Point", "RightPoint", "LeftPoint"])
