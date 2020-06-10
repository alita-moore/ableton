class Warp():
    """
    # Description
    The Warp class organizes this program's priamry functionality. 
    Specifically, this is defined as the ability to automatically
    adjust tempo (beats / s) as a function of markers. A marker
    is defined as given beat and its complimentary seconds marker.
    Notably, the warp class is a dynamic system, and it will 
    accurately convey the complimentary beats and time depending 
    on the known markers at that moment. These dynamic methods (b2s 
    and s2b) run in time complexity O(log(n)) where n is the number 
    of markers; details about optimization can be found in the 
    README.

    # Usage
    Set two markers at 
        (beat = 0, seconds = 0) 
    and
        (beat = 1, seconds = 5)
    >>> test_warp = Warp()
    >>> test_warp.set_marker(0, 0)
    >>> test_warp.set_marker(1, 5)

    Lets make sure these were set properly
    >>> test_warp.markers
    [(0, 0), (1, 5)]
    # This list is automatically sorted

    If an invalid marker was provided, nothing happens
    >>> test_warp.set_marker(0,4)  # beat = 0 is already set
    >>> test_warp.set_marker(2,3)  # intersecting markers are invalid
    # checking that nothing happened...
    >>> test_warp.markers
    [(0, 0), (1, 5)]

    An end_tempo can be provided at any time, but we'll do it now
    >>> test_warp.set_end_tempo(10)

    The primary use of the warp functionality is in converting an arbitary
    input of either time (s) or beat and getting the complimentary time or 
    beat output. That is, what time does beat 11 occur? Or what beat is 
    occuring at 2.5s?
    >>> test_warp.s2b(2.5)
    0.5
    >>> test_warp.b2s(0.5)
    2.5
    >>> test_warp.b2s(11)
    6.0
    >>> test_warp.s2b(6.0)
    11.0

    There are a few edge cases to consider..
    
    **Before**

    the beat or sample time given is before the first marker, therefore
    the tempo of this 'before' region is the same as the tempo after
    the first marker
    >>> test_warp.b2s(-0.5)
    -2.5
    >>> test_warp.s2b(-2.5)
    -0.5

    **On a point**

    if an input is on a marker, its output is pre-defined
    >>> test_warp.b2s(1)
    5
    >>> test_warp.s2b(5)
    1

    **After the last marker**
    the tempo in the region after the last marker is defined
    as the end_tempo, the end_tempo is assumed to be defined
    but if it's not then nothing is outputted
    >>> test_warp.set_end_tempo(None)
    >>> test_warp.b2s(2)
    >>> test_warp.s2b(6)
    """

    def __init__(self):
        self.end_tempo = None
        self.markers = []
        self.regions = []
    
    def __binary_search__(self, input_ref, beat_or_time):
        """
        Improves the efficiency of finding the relevant region
        for a given input; specifically designed for use with
        the s2b and b2s functionalities.

        For purposes of demonstration of understanding (this is
        for a technical interview), this method only uses two value 
        that actually change; it also avoids using recursion. This 
        is done in the interest of maximizing performance. If any other 
        method (to my knowledge) is used here, either the method is
        greatly bottlenecked by that (recursion) or it does
        not scale as expected. The average performance decrease of 
        calling the s2b function:
            
            $
            \frac{p_{t + 1}}{p_{t}} ~= \frac{n_{t+1}}{n_{t}}^{0.1}.
            and,
            p_{t+1} ~= 360 * \frac{n_{t+1}}{n_{t}}^{0.1} [khz]
            $

        where p_(t+1) is the maximum frequency of calling s2b or b2s
        at time + 1 (i.e. the next one); similarly, n representts the
        number of markers in a given system.

        :param input_ref float: the input reference value to
                                isolate region w.r.t the regions
        :param beat_or_time int: either 0 (beat) or 1 (time)
        :return int: the relevant region of the input
        """
        # perform binary search
        left, right = 0, len(self.markers)  # purposes of optimization
        while (right-left) > 1:
            median = left + (right-left) // 2
            median_value = self.markers[median][beat_or_time]
            if input_ref < median_value:
                right = median
            elif input_ref > median_value:
                left = median
            else:
                left, right = median, median

        # finalize binary search and return
        if self.markers[left][beat_or_time] == input_ref:
            return left
        else:
            if input_ref < self.markers[left][beat_or_time]:
                if left == 0:
                    return 0
                else:
                    return left - 1
            else:
                return left

    def __get_tempo__(self, a, b, c,  d):
        r"""Get the tempo provided the edge points a, b, c, d

        beat line   ------*(a)-----*(point of interest)----------*(b)-------
                            |       region of interest             \ 
                            | tempo = (b-a)/(d-c) [beats / second]  \ 
        seconds line------*(c)---------------------------------------*(d)--- 

        :param a float: beat intercept left of the point of interest
        :param b float: beat intercept right of the point of interest
        :param c float: seconds intercept left of the point of interest
        :param d float: seconds intercept right of the point of interest
        :return float: tempo [beats per second]
        """
        return (b-a)/(d-c)

    def __get_insert_index__(self, beat_marker, seconds_marker):
        """
        This method is meant to be an inbetween so that the 
        __binaray_search__ method can be used when setting the
        marker and also when updating the regions. In effect,
        this optimization makes adding markers and updating
        the regions have a complexity of O(nlog(n))
        """
        insert_index_beat = self.__binary_search__(beat_marker, 0)
        insert_index_samp = self.__binary_search__(seconds_marker, 1)

        # filter invalid inputs
        if insert_index_beat != insert_index_samp:  # if intersection
            return None
        elif self.markers[insert_index_beat][0] == beat_marker:
            return None
        elif self.markers[insert_index_samp][1] == seconds_marker:
            return None
        
        # adjust the index so it's inserted properly
        insert_index = insert_index_beat  # either one works
        if self.markers[insert_index][0] < beat_marker:
            insert_index += 1
        
        return insert_index
    
    def __update_regions__(self, insert_index, left, right):
        """
        Front-loads the s2b and b2s calculations.
        Specifically, this is done via an O(n) loop
        calcualtions on the sorted 'markers' list.
        It finds the necessary values for proper
        linear interpolation.

        note that in practice this will have complexity
        O(n**2) because it's called at each step.
        """
        # front-load calculations for all regions
        # self.regions = []
        # for count in range(len(self.markers)-1):
        #     left = self.markers[count]  # earlier marker
        #     right = self.markers[count + 1]  # next marker
        #     a, b, c, d = left[0], right[0], left[1], right[1]  # the 'edges'
        #     tempo = self.__get_tempo__(a, b, c, d)
        #     self.regions.append((a, c, tempo))


        if insert_index != None:
            if insert_index == len(self.markers):  # i.e. change made to end
                left = self.makers[-2]
                right = self.markers[-1]
                tempo = self.__get_tempo__(left[0], right[0], left[1], right[1])
                self.regions.append((left[0], left[1], tempo))
        
        # append end region
        last_marker = self.markers[-1]
        self.regions[-1] = (last_marker[0], last_marker[1], self.end_tempo)
        
    def set_marker(self, beat_marker, seconds_marker):
        """
        Set a marker by its intercept with beat and time lines.
                
        :param beat_marker float: the positive beat to set the marker
        :param seconds_marker float: the positive second to set the marker
        """
        if len(self.markers) == 0:
            self.markers.append([beat_marker, seconds_marker])
            return None
        
        insert_index = self.__get_insert_index__(beat_marker, seconds_marker)
        if insert_index == None:
            return None
        else:
            self.markers.insert(insert_index, [beat_marker, seconds_marker])

        # front load the region and tempo calculations
        self.__update_regions__()

    def set_end_tempo(self, end_tempo):
        r"""
        Set the tempo of the final section
    
        beat line   ------*(a)-----------*(b)------->
                            |             \  (assume there're are no markers past this point)  
                            |              \ final section must have defined tempo = end_tempo
        seconds line------*(c)--------------*(d)---->

        :param end_tempo float: value of the final tempo [beats per second]
        """
        if end_tempo != None and end_tempo < 0:  # end_tempo can only be positive float
            return None

        self.end_tempo = end_tempo
        if len(self.markers) > 0:  # allows end_tempo to be set before markers
            self.__update_regions__()  # front loading calculations

    def b2s(self, input_beat):
        """
        Converts the input beat to its compliment 
        time based on the defined warp object
        """  
        # get required properties of the input
        region = self.__binary_search__(input_beat, 0)
        compliments = self.regions[region]  

        # linear interpolation: got (x, x0, slope) in above step
        if compliments[-1] == None:
            return None
        else:
            compliment_intercept = compliments[1]
            reference_intercept = compliments[0]
            compliment_tempo = 1 / compliments[2]  # seconds per beat

            delta_reference = input_beat - reference_intercept
            delta_compliment = delta_reference * compliment_tempo

            return delta_compliment + compliment_intercept
    
    def s2b(self, input_seconds):
        """
        Converts the input time to its compliment
        beat based on the defined warp object
        """
        # get requred properties of the input
        region = self.__binary_search__(input_seconds, 1)
        compliments = self.regions[region]

        # linear interpolation: got (x0, x, slope) in above step
        if compliments[-1] == None:
            return None
        else:
            compliment_intercept = compliments[0]
            reference_intercept = compliments[1]
            compliment_tempo = compliments[2]  # beats per second

            delta_reference = input_seconds - reference_intercept
            delta_compliment = delta_reference * compliment_tempo

            return delta_compliment + compliment_intercept
