import pickle
mylist = []

mylist.append('This is a string')
mylist.append(5)
mylist.append(('localhost', 5000))

print mylist

p = pickle.dumps(mylist)
print type

u = pickle.loads(p)
print u