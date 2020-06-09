# 1. Introduction
## 1.1. Purpose
As a technical interview, I was instructed to develop a solution to the following (abreviated) problem:


## 1.2. Requirements
This module was designed for use with python 3

# 2. Usage
## 2.1. Main Function
Change the command console's directory to this directory

```Bash
$ cd <this directory>
```

Call the [Main.py](main.py) function
```Bash
$ python main.py
```

Once called, you will get a python-esk console to interact with the 'Warp' object directly
```Bash
>>> 
```

The following commands are supported and further explained in the documentation of the [console](src/utils.py)
```Bash
>>> marker a b   # a and b are floats, a is the beat, b is the seconds on the time-line
>>> end_tempo c  # c is a float greater than 0, and is the tempo after all markers
>>> s2b d        # d is a float, this function prints the beat at which d (sec.) occurs
>>> b2s e        # e is a float, this function prints the time (sec.) which beat e occurs
```

If an input is invalid then there will be no output and no change to the Warp object. More details about the handling of exceptions, design, and optimizations can be found in the documentation of the [Warp object](src/warp.py).

## 2.2. Testing
Tests were defined throughout the development of this module. They verify the baseline functionality of the Warp object and console, the handling of exceptions, and verifies that the optimal solution is being employeed -- O(logn). More information on the tests can be seen in the documentation of the [warp_tests file](src/warp_test.py). To run these tests, simply cd into the src folder and run the file as a script directly.

```Bash
$ cd src
$ python warp_test.py
```

# 3. Summary of Skills Demonstrated
Here, I demonstrate my knowledge in object oriented and functional programming, comprehensive documentation, unit test designs, optimizations / algorithms, and readable code. To explain a bit on where each of these are demonstrated...

## 3.1. Object Oriented and Functional Programming
The [Main](main.py) function employees the two main parts of the warp module; i.e. the functionalities are the Warp function are contained in the Warp class, and the interaction with that class is through the console function. This allows for the easy to understand flow of the [Main](main.py) loop, and it also will help theoretical future programmers to debug the code because each change is isolated to its specific functionality.

To demonstrate the cleanliness of the functional programming in this project, here is the entirety of the Main function.

```Python
from src.utils import console
from src.warp import Warp

warp = Warp()
while True:
    output = console(warp)
    if output != None:
        print(output)
```

This hierarchical based methodology was emphasized for two reasons...

### 3.1.1. for one it was done for __readibility__.
 the concise format of [Main](main.py) allows any outside developer that is trying to understand my code a high level understanding of functionalitality. If you skim over the above code, think to yourself (in pseudocode) what's happening. For me, I'd think 

    1) the warp object is initialized
    2) the console prompts the user for an input
    3) the console does something to the warp object
    4) if the output from the console is not None then it prints that output
    5) back to 2 and repeat

At a high level, this is exactly correct. At each decreasing level the complexity increases, but the functionality and purpose also narrows. This allows for easy to read code because it flows as a piece of the greater whole. This is an intuitive behavior, and therefore easy to read. The documentation follows a similar pattern, or at least that was my goal :);

### 3.1.2. second, it was done for __scalability__.


## 3.2. Comprehensive Documentation
See the documentation of [console](src/utils.py) or the [warp object](src/warp.py) to see the extensive explanation of usages, dependency, and optimizations. This extensive documentation is present so that future theoretical developers will have an easier time to make changes without breaking things. This documentation is also produced with an online demonstration in mind: because of the example code.

For example, here's the documentation for the ```__binomial_search__``` [Warp object](src/warp.py) method:
```Python
    def __binomial_search__(self, input_ref, beat_or_time):
        """
        ## explanation
        Improves the efficiency of finding the relevant region
        for a given input; specifically designed for use with
        the s2b and b2s functionalities.

        For purposes of demonstration of understanding (this is
        for a technical interview), this method only uses two ints 
        that actually change; it also avoids using recursion. This 
        is done in the interest of maximizing performance. If any other 
        method (to my knowledge) is used here, either the method is
        greatly bottlenecked by that (recursion) or it does
        not scale as expected. The average performance decrease of 
        calling the s2b function:
        """ ...
```

$$
\begin{aligned}
\frac{p_{t + 1}}{p_{t}} &~= \left(\frac{n_{t+1}}{n_{t}}\right)^{0.1}\\
&\text{and}\\
p_{t+1} &~= 360 \left(\frac{n_{t+1}}{n_{t}}\right)^{0.1} [khz]\\
\text{Note: the exact} & \text{  frequency is device specific}
\end{aligned}
$$ 


``` Python
        ... """
        where p_(t+1) is the maximum frequency of calling s2b or b2s
        at time + 1, and n represents the number of markers in a given 
        system.
        
        ## parameters
        :param input_ref float: the input reference value to
                                isolate region w.r.t the regions
        :param beat_or_time int: either 0 (beat) or 1 (time)
        :return int: the relevant region of the input
        """
```

## 3.3. Unit Test Designs
See the definition of the [tests](src/warp_test.py) to see the specifics of which functionalities, exceptions, and performance are tested. But as a summary, the tests were developed alongside the code, and therefore they properly include any and all potential bugs that were reasonably encountered. Comprehensive tests are important because a program is only as good as its bugs, so a comprehensive list of bugs aids future development.

## 3.4. Optimizations / Algorithms
The [warp object](src/warp.py) is built with performance in mind. The main functionality is that of conversion between beat and time (beat -> seconds, seconds -> beat). This call-back is optimized by front-loading calculations: progressively sorted list of markers and updating dynamic tempos as markers as set. Because the markers are inherently sorted, binary search is employeed; specifically, it's used to find which 'region' a given input is.

## 3.5. Readable Code
All the functions and variables are written with readability in mind. For example, from the [warp object](src/warp.py),

```python
def __update_regions__(self):
        """updates the region dictionary with the new edges and tempo"""
        # step through each available region
        self.regions = []
        for count in range(len(self.markers)-1):
            left = self.markers[count]
            right = self.markers[count+1]
            a, b, c, d = left[0], right[0], left[1], right[1]
            tempo = self.get_tempo(a, b, c, d)
            self.regions.append((a, c, tempo))
        
        # append end region
        last_marker = self.markers[-1]
        self.regions.append((last_marker[0], last_marker[1], self.end_tempo))
```

This similarly can be read as 

    for each convolution of length 2:
        collect the marker to the left
        collect the marker to the right
        use these markers to calculate the tempo
        save the required values in the regions variable

    now do the same for the end region