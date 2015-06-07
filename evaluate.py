#usr/bin/env python
import math
import sys

from usefulfunctions import *
import clip

args = sys.argv[1:]

if not args:
    #print("Call with what you want to eval as an argument")
    pass
else:
    
    setClip = False
    if "-setclip" in args:
        args.remove("-setclip")
        setClip = True
    
    command = " ".join(args)
    _ = ans = eval(command)
    
    if setClip:
        clip.set(str(ans))
    else:
        print(ans)