class voidNum():
  def __init__(self,coefficient):
    
    self.coefficient = coefficient
  
  @staticmethod
  def validateCoefficient(coefficient):
    if not isinstance(coefficient,complex) or not isinstance(coefficient,float) or not isinstance(coefficient,int):
      raise TypeError("voidNum class only accepts complex, float, or integer coefficients")
