import FreeCAD, FreeCADGui, Part
import re
import math

from .WrappedDocument import WrappedDocument

from .utils import TeethInset, TeethSide

epsilon = 0.0001



def create_wrapped_document(name):
  return WrappedDocument(name)


def close_all():
  [FreeCAD.closeDocument(d) for d in FreeCAD.listDocuments()]
