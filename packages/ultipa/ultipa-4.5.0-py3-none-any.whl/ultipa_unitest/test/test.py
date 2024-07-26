# from ultipa.types.types_request import CreateUser,GraphPrivilege
#
# ret= CreateUser('test','123',[GraphPrivilege('defaut',['rest']),GraphPrivilege('defaut',['rest'])],[],[])
# print(ret.toDict())
# from ultipa.utils.ufilter import ufilter
#
# ret = ufilter.EqFilter(name='id',value=[1,2,3])
# print(ret.builder())
#
# ret = ufilter.OrFilter(name='id',value=[ ufilter.EqFilter(name='id',value=[1,2,3]),ufilter.GtFilter(name='id',value=[1,2,3])])
# print(ret.builder())


# from ultipa import ULTIPA_REQUEST,ULTIPA
# ret = ULTIPA_REQUEST.Header(name='name',type=ULTIPA.PropertyType.PROPERTY_STRING)
# print(ret.toDict())


# import random
# ret = random.random()
# name_list = ['Like', 'Help', 'Love', 'test']
# ret = random.choice(name_list)
# print(ret)
import types
from typing import Dict


class Test:
	def __init__(self,name):
		self.name=name

	def __str__(self):
		print("Test")

class Test1(Test):
	def __init__(self, name):
		super().__init__(name)

	def __str__(self):
		print("Test1")

# def test_cadfg():
# 	for i in range(10):
# 		yield i

# a : Dict[str,Test]= {}
# a.update({"a":Test(1)})

class My:
	name=None
	age=None
	city=None



from typing import Dict

class DictToObject:
	def __init__(self, dictionary: Dict[str, any]):
		for key, value in dictionary.items():
			setattr(self, key, value)

def cover(my_dict)->My:
	ret = DictToObject(my_dict)
	return ret
# Example dictionary
my_dict = {'name': 'John', 'age': 30, 'city': 'New York'}

# Convert dictionary to object
my_object = cover(my_dict)

# Access attributes
print(my_object.name)  # Output: John
print(my_object.age)   # Output: 30
print(my_object.city)  # Output: New York



if __name__ == '__main__':
	...
	# print(a.get("a").name)
	# ret = Test()
	# print(ret)
	# re = Test1(name="test")
	# print(re.__dict__)
	# print(type(re).__name__)
	# print(isinstance(re,Test1))
	# print(isinstance(re,Test))
	# print(isinstance(test_cadfg(), types.GeneratorType))
