#!/usr/bin/env python
import os, io, md5, shutil
for i in os.listdir("."):
     shutil.move(i, md5.md5(io.open(i,"rb").read()).hexdigest() + os.path.splitext(i)[1])

