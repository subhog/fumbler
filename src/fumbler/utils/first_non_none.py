# def first_non_zero(values):
#   for value in values:
#     if value != 0 and value is not None and value is not False:
#       return value
#   return 0

def first_non_none(values):
  for value in values:
    if value is not None:
      return value
  return 0
