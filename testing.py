import validator as vld
import unittest as ut

class TestBench(ut.TestCase):
    def test_basic(self):
        data = {
            "username": "linuxmaster123",
            "password": "preencryption",
            "email": "lm123@outlook.com",
            "creditcard": {
                "id": 82325,
                "name": "mr. maher",
                "age": 21,
            },
            "creation": "10/12/2009",
            "dob": "12-12-1996",
            "phone": "+970200200200"
        }
        rules = {
            "username": "required|string",
            "password": "required|string",
            "email": "required|email",
            "credicard": "array",
            "creditcard.id": "number",
            "creditcard.name": "string",
            "creditcard.age": "number|min:18",
            "creation": "required|date",
            "dob":"date",
            "phone":"phone"
        }
        valid = vld.Validator(data,rules)
        print(valid.wrong)
        self.assertEqual(valid.getFailedAttributes(),None)
        data["username"] = 123
        valid.updateValidation(data,rules)
        self.assertEqual(valid.getFailedAttributes(),["username"])
        del data["password"]
        valid.updateValidation(data,rules)
        for asserts in ["username","password"]:
            self.assertIn(asserts,valid.getFailedAttributes())
        

    def test_nested(self):
        data = {
        "title": "Master Linux with Maher",
        "author": {
        "name": "Maher",
        "dob": "11-01-1996",
        "email": "maher@birzeit.edu",
        "co_authors": ["Monica", "Ziad"]
        },
        "pages": 120,
        "creation_date": "15/12/2015"
        }

        rules = {
        "title": "string",
        "author": "array",
        "author.name": "string",
        "author.dob": "date",
        "author.email": "email",
        "author.co_authoers": "array",
        "pages": "number",
        "creation_date": "date"
        }
        valid = vld.Validator(data,rules)
        self.assertEqual(valid.getFailedAttributes(),None)

    def test_cascade(self):
        rules = {
        "dob" : "required|date",
        "pages": "required|number|min:5|max:20",
        "author.name" : "required|string",
        }
        data = {
            "dob": "11-9-1996",
            "pages": 15,
            "author": {
                "name": "asd"
            }
        }
        valid = vld.Validator(data,rules)
        self.assertEqual(valid.getFailedAttributes(),None)

    def test_custom(self):
        attr = {
            "dob": "Date of Birth",
            "author.name": "Name of Author"
        }
        errs = {
            "dob": "Some custom date err",
            "author.name": "Another custom err"
        }
        data = {
            "dob": 20,
            "author": {
                "name": 21
            }
        }
        rules = {
            "dob": "date",
            "author": "array",
            "author.name": "string"
        }
        valid = vld.Validator(data,rules,customAttributes = attr,customErrorMessage = errs)
        for attr in list(attr.values()):
            self.assertIn(attr, valid.getFailedAttributes())
        for err in list(errs.values()):
            self.assertIn(err,valid.getErrorMessages())
if __name__ == "__main__":
    ut.main()