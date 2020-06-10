# 1. Introduction
## 1.1. Purpose
As a technical interview, I was instructed to develop a solution to the following (paraphrased) problem:

>

> In Live, audio samples can be stretched and squeezed to change their timing. This is known as warping. Pins called warp markers lock a specific point in the sample (in sample time) to a specific place in a measure (in beat time).  
> 
> Write a program that, given a set of warp markers, can map time values between the two value spaces: beat time and sample time.
> 
> Assume the following behavior,  
> 
>    1)  An Audio sample always has at least one marker
> 2) betwen two warp markers, the tempo is constant
> 3) the tempo before the first warp marker is the same as the tempo after the first warp marker
> 4) the tempo after the last warp marker is specified seperately in the input
> 5) beat time is measure in beats, sample time is measured in seconds, and the tempo is measured in beats per second

In addition to the above problem statement, it's expected that all inputs to the program be via the stdin; similarly, all outputs should be via stdout. This should be such that the following is shown in bash.

```Bash
# inputs
marker 0.0 0.0  
marker 1.0 5.0  
end_tempo 10.0  
b2s 0.5         
s2b 6           

# outputs
2.5             
11.0            
```

## 1.2. Requirements
This module was designed for use with python 3; this README is meant to be viewed in markdown; there's an html copy for simplicity.

# 2. Usage
## 2.1. Main Function
Change the bash directory to this directory

```Bash
$ cd <this directory>
```

Call the [Main.py](main.py) function
```Bash
$ python main.py
```

Once called, all inputs are via stdin and outputs via stdout. Commands directly manipulate the [Warp instance](src/warp.py) of your call; e.g. by just copy and pasting the commands into stdin, the following output is given.
```Bash
# input
marker 0.0 0.0  
marker 1.0 5.0  
end_tempo 10.0  
b2s 0.5         
s2b 6           

# output
2.5             
11.0            
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

# 3. Verbose Explanation of Code (To Make 'Grading' Easier)
What do I consider quality production-level code? Well, to be concise, code is quality if it answers these questions with a definitive 'yes'.

1) Does it accomplish the assigned goal / task?
2) Could you (a developer) confidently make edits to or use this code?

A bit more verbosely, this section explains what I believe to be the 5 fundamental characteristics of quality code and how I accomplished them in this project 

3.1) Object Oriented and Functional Programming  
3.2) Comprehensive Documentation  
3.3) Unit Test Design  
3.4) Optimization   
3.5) Readible Code

## 3.1. Object Oriented and Functional Programming (OOFP)
The [Main](main.py) script employees OOFP. [Main's](main.py) simplicity allows theoretical future developers to easily debug and edit my code. To demonstrate, here's the entirety of [Main](main.py):

```Python
from src.utils import console
from src.warp import Warp

warp = Warp()
while True:
    output = console(warp)
    if output != None:
        print(output)
```

OOFP (in the scope of this project) offers two main advantages: readibility and scalability / modularity.

### 3.1.1. __readibility__
 The concise format of [Main](main.py) allows an outside developer to quickly understand its high level functionalitality. As an exercise, skim over the above code, and write out what the code is doing (in pseudocode) For me, I'd say 

    1) the warp object is initialized
    2) the console prompts the user for an input
    3) the console does something to the warp object with that input
    4) if the output from the console is not None then it prints that output
    5) back to 2 and repeat indefinitely

In the context of the problem statement, this parallels its high-level purpose. If the code did not parallel the problem statement, then it would be clear that something wrong. In addition to high-level readability, Other methods of explanation are allowed by OOFP; which, are discussed in section 3.5.

### 3.1.2. __Scalability / Modularity__
This method was designed with Ableton's software in mind. I have worked with music software occasionally in the past, and I know that they often come with a host of modules. As I see it, the main value proposition of music software is the quality and quantity of these modules. e.g. If an artist wants to interface their tap-deck with the software, is there an efficient and easy to use controller? 

In the case of the warp object, it could be used in a situation where someone wants to build a unique sound. Finally, due to its simple methods of interfacing, it can be used in an emergent way and developed into something significantly more complex.

## 3.2. Comprehensive Documentation
The documentation of the [console function](src/utils.py) and [warp class](src/warp.py) have extensive explanations in terms of usage, theory, and optimization. This is done to simplify editing and for use in the scope of a larger documentation API.

For example, here's the documentation for the ```__binary_search__``` [Warp object](src/warp.py) method:
```Python
    def __binary_search__(self, input_ref, beat_or_time):
        """
        # Purpose
        Improves the efficiency of finding the relevant region
        for a given input; specifically designed for use with
        the s2b and b2s functionalities.

        # Theory
        For the purpose of demonstration of understanding (this is
        for a technical interview), this method only uses two ints 
        that actually change; it also avoids using recursion. This 
        is done in the interest of maximizing performance. If any other 
        method (to my knowledge) is used here, either the method is
        greatly bottlenecked by it (recursion) or the method does
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
        at the step (t + 1), and n represents the number of markers in a given 
        system.
        
        ## parameters
        :param input_ref float: the input reference value to
                                isolate region w.r.t all regions
        :param beat_or_time int: either 0 (beat) or 1 (time)
        :return int: the relevant region of the input
        """
```

## 3.3. Unit Test Design
See the definition of the [tests](src/warp_test.py) to see the specifics of which functionalities, exceptions, and performances are tested. To summarize, the tests were developed alongside the code; they properly include any bugs that were encountered during development. Comprehensive tests are important because they allow further development, while also making sure that old bug fixes and functionality are reliably maintained.

## 3.4. Optimization
Optimization is important.

I assume the warp module is used in frequency modulation; i.e. digital sound is a series of signal frequencies -- converted into real audio via speakers. According to Google, the typical bit rate is about 44.1khz; which, if the warp module were used in real-time, would require the s2b functionality to access solutions at 44.1khz.

As outlined in section 3.2, front-loading computation and binary search were used. The sorted reference lists is built using binary search in O(nlog(n)), and the s2b and b2s methods access solutions in O(log(n)). The optimal solution easily achieves the 44.1khz requirements. For example, my program is able to access solutions at a theoretical frequency of 160khz while there are 260 thousand markers.

## 3.5. Readable Code
All of the functions and variables are named with readability in mind. For example, from the [warp object](src/warp.py),

```python
def __update_regions__(self):
        """
        **ignoring docstring**
        """
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

---
Note: this method was reworked for purposes of optimization; because of this, the ```__update_regions__``` method has a significantly more difficult to undersatnd structure. But I maintained readibility via comments and variable names.

---
In addition to high-level readability, I attempt to maintain a constant learning curve for each set of code. I do this by implementing a complementary hierarchical structure of complexity and focus...

That is, see the 'levels' of [Main](main.py) -> [console](src/utils.py) -> [Warp](src/warp.py) -- where [Main](main.py) is high-level, and [Warp](src/warp.py) is low-level. The complexity of the code / documentation increases as the level decreases. However, the scope narrows in a complementary way. This creates a hierarchy of sorts; with each step, the actual problem becomes easier to understand, but the solution less so. A proper balance of these two properties of readability allows for a (ideally) constant learning curve for each subsequent step.

To demonstrate this kind of hierarchical complexity in action, let's take a look at the [warp object's](src/warp.py) class method ```__get_tempo__```:
```Python
 def __get_tempo__(self, a, b, c, d):
        r"""
        Get the tempo provided the edge points a, b, c, d

        beat line    ------*(a)-----*(point of interest)----------*(b)-------
                            |       region of interest             \ 
                            | tempo = (b-a)/(d-c) [beats / second]  \ 
        seconds line ------*(c)--------------------------------------*(d)---- 

        :param a float: beat intercept left of the point of interest
        :param b float: beat intercept right of the point of interest
        :param c float: seconds intercept left of the point of interest
        :param d float: seconds intercept right of the point of interest
        :return float: tempo [beats per second]
        """
        return (b-a)/(d-c)
```
You might be thinking to yourself,   

> Well, Alita; this seems like a waste of valuable memory. It's just doing a simple algebraic expression! Which, could very easily have just been done inline.

```__get_tempo__``` was obfuscated because the solution is non-obvious. Understanding the solution would require that you'd realize the purposes of a, b, c, and d; and that you know what 'tempo' means in this context. A reader might say, 

> well what does this tempo define? As in the tempo of the whole piece? Or just any part of the piece?

The docstring shows how the tempo is the beats per second of a region defined by its left and right markers. i.e. delta beats divided by delta time [beats per second]. Devoid of context, however, this simple equation is confusing. So I split it off from the main function and explained it clearly.

This allows for other developers to double-check my work. e.g. let's say that I had made the simple error of ```return (d-c) / (b-a)```, instead. My coworker would probably notice that the calculated tempo is the inverse of what it should be and then just make a simple fix in its obvious place which is ```__get_tempo__```.

However, if it were placed inline, my coworker would first have to find where tempo is being defined (which might be in mulitple places), what and why it's being calculated, and then make a fix. They may even assume the code is just fundamentally flawed and instead opt to start from scratch; which, wastes time and money just because the equation was inverted.