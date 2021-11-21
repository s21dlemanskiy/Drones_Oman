import os


a = input("num")
os.system(f"pyuic5 -x ./source/untitled{a}.ui -o ./source/output.py")