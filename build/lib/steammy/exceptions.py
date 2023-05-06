
def exception(error: str, object: any, reference: any, message: str):
  if error == 'type':
    if not isinstance(object, reference):
      raise TypeError(message)
    else:
      pass

  elif error == 'contain':
    if object not in reference:
      raise ValueError(message)
    else:
      pass

  elif error == 'network':
    if object == reference:
      raise ConnectionError(message)
    else:
      pass
  
  if error == 'exceed':
    if object > reference:
      raise Exception(message)
    else:
      pass