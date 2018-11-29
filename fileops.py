
try:
    f = open("/tmp/test2.txt", 'r')
    content = f.readlines()
    print(content)
except IOError as e:
    print(e)

#
# f = open("/tmp/test2.txt", 'r')
# content = f.readlines()
# print(content)

print("end program")