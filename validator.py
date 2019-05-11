import datetime
import re
class Validator:
    def __init__(self,data,rules,customAttributes = {}, customErrorMessage = {}):
      self.data = data
      self.rules = rules
      self.customAttributes = customAttributes
      self.customErrorMessage = customErrorMessage
      self.wrong = []
      self.validate()
      
          
    def validate(self):
      types = {
        "string": self.isString,
        "number": self.isNumber,
        "email": self.isEmail,
        "date": self.isDate,
        "required":self.isRequired,
        "array": self.isArray,
        "phone": self.isPhone,
        "min": self.minValue,
        "max": self.maxValue,
        "in": self.isIn
      }

      errors = {
        "string": "The $x field must be a string",
        "number": "The $x field must be numeric",
        "email": "The $x field must be a valid e-mail",
        "date": "The $x field must be a valid date",
        "required": "The $x field is required",
        "array": "The $x must be an array",
        "phone": "The $x must be a vald phone number",
        "min": "The $x field must be atleast $y",
        "max": "The $x field must be at max $y",
        "in": "The $x field must be one of $y"
      }

      for key,values in self.rules.items():
        nested = False
        if "." in key:
          keytoks = key.split(".")
          nested = True
        if not nested:
          for value in values.split("|"):
            if value == "required":
              ans = types["required"](key)
            elif value in types and key in self.data.keys():
              ans = types[value](self.data[key])
            elif value.split(":")[0] in types and key in self.data.keys():
              toks = value.split(":")
              ans = types[toks[0]](self.data[key],toks[1])
            if not ans:
              temp = value.split(":")
              err = errors[temp[0]].replace("$x",key)
              if len(temp) > 1:
                err = err.replace("$y",temp[1])
              if not self.listFind(value):
                self.wrong.append([key,err])
              else:
                self.listAppend(key,err)
        else:
          for value in values.split("|"):
            if value == "required":
              ans = types["required"](self.data[keytoks[0]][keytoks[1]])
            elif value in types and keytoks[1] in self.data[keytoks[0]].keys():
              ans = types[value](self.data[keytoks[0]][keytoks[1]])
            elif value.split(":")[0] in types and keytoks[1] in self.data[keytoks[0]].keys():
              toks = value.split(":")
              ans = types[toks[0]](self.data[keytoks[0]][keytoks[1]],toks[1])
            if not ans:
              temp = value.split(":")
              err = errors[temp[0]].replace("$x",key)
              if len(temp) > 1:
                err = err.replace("$y",temp[1])
              if not self.listFind(value):
                self.wrong.append([key,err])
              else:
                self.listAppend(key,err)


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
      if x <= int(min):
        print(x,min)
        return False
      return True

    def maxValue(self,x,max):
      if x >= int(max):
        return False
      return True
    
    def isRequired(self,x):
      flag = True
      if x not in self.data.keys() or not self.data[x]:
        flag = False
      for key,value in self.data.items():
        if type(value) is dict:
            if x in self.data[key].values():
              flag = True
      return flag

    def isDate(self,x):
      try:
        datetime.datetime.strptime(x, "%d-%m-%Y")
      except Exception:
        try:
          datetime.datetime.strptime(x, "%d/%m/%Y")
        except Exception:
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
        failed = []
        for item in self.wrong:
          if item[0] in self.customAttributes:
            failed.append(self.customAttributes[item[0]])
          elif item[0]:
            failed.append(item[0])
        failed = set(failed)
        failed = list(failed)
        return failed

    def listFind(self,y):
      for i in self.wrong:
        if(i[0] == y):
            return True
      return False

    def listAppend(self,y,x):
      for i in self.wrong:
          if(i[0] == y):
              i.append(x)

    def getErrorMessages(self):
      if len(self.wrong) == 0:
        return None
      else:
        failed = []
        for item in self.wrong:
          if item[0] in self.customErrorMessage:
            failed.append(self.customErrorMessage[item[0]])
          else:
            failed.append(item[1])
        return failed

    def updateValidation(self,data,rules):
      self.data = data
      self.rules = rules
      self.wrong = []
      self.validate()
      
