#coding=utf8
import pymongo
from mongoengine import *
import json
import datetime
import traceback
coll = connect("first",host="127.0.0.1",port=27017)

register_connection('second','second',host='127.0.0.1',is_slave=False)
class Student(Document):
	name = StringField(max_length=50,required=True)
	age = IntField(default=20,choices=[18,20,30,25])
	parents = ListField(StringField(max_length=50),default=[])
	datas = ListField(IntField() ,default=[1,2,3,4,5,6,7,8])
	favor = DictField(default={})
	created = StringField(max_length=50)

	meta = {'db_alias':'second'}

std,create = Student.objects.get_or_create(name="wanglong")
print(std)
# s1 = Student(name="wanglong",age=30,id='5a27a77fb15ca92e0cd4bc5f')
# std["parents"]=["wyx","ply"]
# std.name='wanglong'
# std.save()

# conn = Student.objects(Q(name="wanglong")&Q(age=15))
# conn.update_one(inc__age=5)
# conn.reload()

# conn = Student.objects.only("name")
# print(conn.count(),len(conn),conn.average("age"))

# conn = Student.objects.filter(name="wanglong").order_by("-age").limit(1)

# Student.objects.get_or_create(name="wangzong",created=datetime.datetime.now().strftime("%Y-%m-%d"))
# conn=Student.objects(__raw__={"age":{"$gt":0}})
# Student.objects(name="wangzong").delete()
# Student.objects(name="wanghai").update_one(push__parents="sdsds")
# Student
# conn = Student.objects(parents__size=2)[:1]

# Student.objects.filter(name='wanghai').update(set__parenrts__0='pp')
# Student.objects.get_or_create(age=20)
# Student.objects(name='wanghai').update(set__datas=[1,2,3,4,5,6,7,8])
# print(Student.objects().average('age'))
# m = Student()
# m.update(set__name= u'洪亚光')
# m.save()
# all = Student.objects()
# for i in all:
# 	i.reload()

# for st in conn:
# 	print(st.name)
# 	print(st.age)
# 	print(st.parents)
# 	try:
# 		print(st.created)
# 	except Exception as e:
# 		print(e)


# def printdebug(func):
#     def __decorator(user):    
#         print('enter the login')
#         result = func(user)  #recevie the native function call result
#         print('exit the login')
#         return result        #return to caller
#     return __decorator  
 
# @printdebug 
# def login(user):
#     print('in login:' + user)
#     msg = "success" if user == "jatsz" else "fail"
#     return msg  #login with a return value
 
# result1 = login('jatsz');
# print result1  #print login result
 
# result2 = login('candy');
# print result2