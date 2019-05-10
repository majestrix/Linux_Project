import validator as vld
import re
data = {
"title": "Book",
"author": {
 "name": "Maher",
 "dob": "11-01-1996",
 "email": 20,
 "co_authors": ["Monica", "Ziad"]
},
"pages": 50,
"creation_date": "15/12/2015"
}


rules = {
"title": "string",
"author": "array",
"name": "string",
"dob": "date",
"email": "email",
"co_authoers": "array",
"pages": "number",
"creation_date": "date"
}

test = []
y = "in:10,12,14"
x = "12"
valid = vld.Validator(data,rules)
print(valid.isValidData())
# print(valid.getFailedAttributes())
print(valid.wrong)
