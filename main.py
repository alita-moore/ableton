from src.utils import console
from src.warp import Warp

warp = Warp()

console(warp, 'marker 1.0 5.0')
console(warp, 'end_tempo 10.0')
while True:
    output = console(warp)
    if output != None:
        print(output)