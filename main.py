from src.utils import console
from src.warp import Warp

warp = Warp()
while True:
    output = console(warp)
    if output != None:
        print(output)