import datetime
import re
class Validator:
    def __init__(self,data,rules,customAttributes = {}, customErrorMessage = {}):
      self.data = data
      self.rules = rules
      self.wrong = []
      self.validate()
      
          
    def validate(self):
      types = {
        "string": self.isString,
        "number": self.isNumber,
        "email": self.isEmail,
        "date": self.isDate,
        "required":self.isRequired,
        "min": self.minValue,
        "max": self.maxValue,
        "in": self.isIn
      }

      for key,values in self.rules.items():
        for value in values.split("|"):
          if value == "required":
            ans = types["required"](key)
          elif value in types and key in self.data.keys():
            ans = types[value](self.data[key])
          elif value.split(":")[0] in types and key in self.data.keys():
            toks = value.split(":")
            ans = types[toks[0]](self.data[key],toks[1])
          if not ans:
            if not key in self.wrong:
              self.wrong.append(key)

    def isString(self,x):
      if type(x) is str:
        return True
      else:
        return False

    def isNumber(self,x):
      if type(x) in [type(1),type(1.0)]:
        return True
      else:
        return False 

    def isEmail(self,x):
      if "@" not in x:
        return False
      if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', x) == None:
        return False
      return True
    
    def isPhone(self,x):
      if re.match("^\+[0-9]{12}$",x) == None:
        return False
      return True

    def minValue(self,x,min):
      if x < int(min):
        print(x,min)
        return False
      return True

    def maxValue(self,x,max):
      if x > int(max):
        return False
      return True
    
    def isRequired(self,x):
      if x not in self.data.keys() or not self.data[x]:
        return False
      return True

    def isDate(self,x):
      try:
        datetime.datetime.strptime(x, "%d-%m-%Y")
      except ValueError:
        try:
          datetime.datetime.strptime(x, "%d/%m/%Y")
        except ValueError:
          return False
      return True
    
    def isArray(self,x):
      return type(x) is list

    def isIn(self,x,opts):
      opts = opts.split(",")
      if type(x) is not str:
        str(x)
      if x not in opts:
        return False
      return True

    def isValidData(self):
      if len(self.wrong) == 0:
        return True
      else:
        return False

    def getFailedAttributes(self):
      if len(self.wrong) == 0:
        return None
      else:
        return self.wrong

    # def getErrorMessages(self):
    #   if wrong
