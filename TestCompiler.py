import os
import glob

skip = ("examples\\test_15.u", "")

files = glob.glob("examples\\*.u")

for file in files:
    if file in skip:
        continue

    ret = os.system("python main.py" + " " + "\"" + file + "\"")

    if ret != 0:
        print("\nerror in file" + " " + file)
        exit(-1)

    ret = os.system(file.rsplit('.u', maxsplit=1)[0] + ".exe")

    if ret != 0:
        print("\nerror in program" + " " + file)
        exit(-1)

print("\nsuccess!")
