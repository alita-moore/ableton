import warnings

class Warp():
    def __init__(self):
        self.beat_markers = {}    # beat line
        self.second_markers = {}  # seconds line
        self.end_tempo = None     # tempo of end section
        self.count_markers = 0    # number of defined markers
    
    def set_marker(self, beat_marker, seconds_marker):
        """Set a marker by its intercept with beat and second tracks, defines tempo

        :param beat_marker float: the positive beat to set the marker
        :param seconds_marker float: the positive second to set the marker
        """
        if self.count_markers > 0:
            for count, beat_marker_reference in self.beat_markers:                
                seconds_marker_reference = self.beat_markers[(count, beat_marker_reference)]  
                if beat_marker_reference == beat_marker or seconds_marker_reference == seconds_marker:
                    warnings.warn("this marker already exists")
                    return
                
                beat_marker_reference = beat_marker_reference < beat_marker
                seconds_marker_reference = seconds_marker_reference < seconds_marker
                if beat_marker_reference != seconds_marker_reference:
                    warnings.warn("This is an invalid marker because it intersects with at least marker %d" % count)
                    return
        
        self.count_markers += 1
        self.beat_markers[(self.count_markers, beat_marker)] = seconds_marker
        self.second_markers[(self.count_markers, seconds_marker)] = beat_marker

    def get_tempo(self, a, b, c,  d):
        r"""Get the tempo provided the edge points a, b, c, d

        beat line   ------*(a)-----*(point of interest)----------*(b)-------
                            |       area of interest               \ 
                            | tempo = (b-a)/(d-c) [beats / second]  \ 
        seconds line------*(c)---------------------------------------*(d)--- 

        :param a float: beat intercept left of the point of interest
        :param b float: beat intercept right of the point of interest
        :param c float: seconds intercept left of the point of interest
        :param d float: seconds intercept right of the point of interest
        :return float: tempo [beats per second]
        """
        return (d-c)/(b-a)

    def set_end_tempo(self, end_tempo):
        r"""Set the tempo of the final section
    
        beat line   ------*(a)-----------*(b)------->
                            |             \  (assume there're are no markers past this point)  
                            |              \ final section must have defined tempo = end_tempo
        seconds line------*(c)--------------*(d)---->

        :param end_tempo float: value of the final tempo [beats per second]
        """
        self.end_tempo = end_tempo

    def get_first_region(self, reference):
        """Get the first region by using the count_markers value"""
        a, b = (None, None), (None, None)
        for count, marker_intercept in reference:
            if a[1] == None or marker_intercept < a[1]:
                a = (count, marker_intercept)
        for count, marker_intercept in reference:
            if (b[1] == None or marker_intercept - a[1] < b[1]) and (marker_intercept != a[1]):
                b = (count, marker_intercept)
        
        c = reference[a]
        d = reference[b]
        return a[1], b[1], c, d
    
    def get_compliments(self, intercept, reference):
        r"""Get the relevant compliment features (compliment reference, tempo) (POI)

        reference  line   ------*(a)-----*(POI)----------*(b)------->
        (before first region)   |                         \   (after last region)
                                |                          \ 
        compliment line   ------*(c)------------------------*(d)---->
                                ^ this is the compliment
                                reference, and it's used
                                for later steps such as a
                                beats 2 seconds conversion

        :param intercept float: absolute intercept at POI on the reference line  
        :param reference dict: the reference directory for the given POI
        :return (c, tempo) (float, float): edges
        """
        left = (None, None)  # (count, intercept)
        right = (None, None)

        if len(reference) == 0:
            warnings.warn("There must be at least 1 marker, currently there are none")
            return None

        # collect nearby points if they exist
        for count, marker_intercept in reference:
            if marker_intercept < intercept:
                if left[1] == None or left[1] < marker_intercept:
                    left = (count, marker_intercept)
            elif marker_intercept > intercept:
                if right[1] == None or right[1] > marker_intercept:
                    right = (count, marker_intercept)
            elif marker_intercept == intercept:
                left = (count, marker_intercept)
                right = (count, marker_intercept)
                break
        
        # define special point locations
        before_first = False  # before the first marker
        after_last = False    # after the last marker
        on_point = False      # on a marker

        if left[0] == right[0]:
            on_point = True
        elif right[0] == None:
            after_last = True
        elif left[0] == None:
            before_first = True

        # filter the above cases
        if before_first:
            a, b, c, d = self.get_first_region(reference)
            tempo = self.get_tempo(a, b, c, d)
            return (c, a, tempo)
        elif after_last:
            if self.end_tempo == None:
                warnings.warn("You can't search the end region without defining an end tempo")
                return None
            else:
                return (reference[left], left[1], None)
        elif on_point:
            return (reference[left], left[1], 0)
        
        # calculate and return the relevant compliment features
        a, c = left[1], reference[left]
        b, d = right[1], reference[right]
        tempo = self.get_tempo(a, b, c, d)
        return (c, a, tempo)

    def b2s(self, input_beat):
        """Converts the input beat to its compliment time based on the defined warp object"""
        compliments = self.get_compliments(input_beat, self.beat_markers)
        if compliments == None:
            return None
        else:
            compliment_intercept = compliments[0]
            reference_intercept = compliments[1]
            compliment_tempo = compliments[2]
            if compliments[2] == None:
                compliment_tempo = 1/self.end_tempo
            else:
                compliment_tempo = compliments[2]
            # print('compliment intercept: %f, compliment tempo: %f' % (compliment_intercept, compliment_tempo))

            delta_reference = input_beat - reference_intercept
            delta_compliment = delta_reference * compliment_tempo

            return delta_compliment + compliment_intercept
    
    def s2b(self, input_seconds):
        """Converts the input time to its compliment beat based on the defined warp object"""
        compliments = self.get_compliments(input_seconds, self.second_markers)
        if compliments == None:
            return None
        else:
            compliment_intercept = compliments[0]
            reference_intercept = compliments[1]
            if compliments[2] == None:
                compliment_tempo = self.end_tempo
            else:
                compliment_tempo = compliments[2]
            # print('ref intercept: %f, compliment intercept: %f, compliment tempo: %f' % (reference_intercept, compliment_intercept, compliment_tempo))

            delta_reference = input_seconds - reference_intercept
            delta_compliment = delta_reference * compliment_tempo

            return delta_compliment + compliment_intercept



        