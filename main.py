import validator as vld
import re
data = {
"name": "Maher",
"age": 15
}

rules = {
"name": "required|string",
"age": "required|number|min:15",
"date": "date",
}
test = []
y = "in:10,12,14"
x = "12"
valid = vld.Validator(data,rules)
print(valid.isValidData())
print(valid.getFailedAttributes())

#For Ameer Paraskiva c:
