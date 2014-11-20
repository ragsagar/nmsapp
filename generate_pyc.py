import os
from compileall import compile_dir

current_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.join(current_dir, 'nms')
print "Generating pyc in %s" % (app_dir)
compile_dir(app_dir)


