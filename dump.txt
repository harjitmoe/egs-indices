#!/usr/bin/env python3
import os, io, hashlib, shutil
for i in os.listdir("."):
     shutil.move(i, hashlib.md5(io.open(i, "rb").read()).hexdigest() + os.path.splitext(i)[1])

