from src.utils import console
from src.warp import Warp

sample = Warp()
while True:
    output = console(sample)
    if output != None:
        print(output)