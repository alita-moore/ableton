def console(warp, *input_str):
    """
    The console is designed as a user friendly way of interacting with
    the warp object. It allows for the following commands:

    >>> marker a b
    where a and b are floats and define the beat and time point (in
    seconds) where to set a marker. Markers are only valid if:
        - they don't intersect with other markers (0,5) and (1,3)
            intersect
        - no ends match for any two markers (0,0) and (0, 1) have
            matching ends
    if a marker is invalid, then nothing will happend except that the
    markers known by the warp object will not change. It's assumed that
    there will always be at least 1 marker.

    >>> end_tempo a
    where a is a float value that defines the tempo (beats per second)
    in the final region. This is necessary because all tempos are
    defined by their surrounding markers. At the end, this cannot
    be determined, so it must be specified. The end_tempo >= 0 or
    nothing will change.

    >>> s2b a
    where a is a float value that represents the time a in seconds
    the output is the relatively mapped note; i.e. if the tempo is
    10 beats / s, then at time = 1s, beat 10 will be occuring. This
    method automatically adjusts the tempo, and interpolates the
    relevant value based on the predefined markers.

    >>> b2s a
    where a is a float value that represents the reference beat;
    the output is the relatively mapped time (s); i.e. if the tempo is
    10 beats / s, then beat = 10 will occur at time = 1s. This
    method automatically adjusts the tempo, and interpolates the
    relevant value based on the predefined markers.

    The console allows for predefined inputs as an optional input.
    they will follow the same format as demonstrated above. e.g. 
    >>> console(warp_object, "b2s 10")
    1.0
    
    :param warp Warp: the current instance of the warp class
    :param input_str str: optional input string for automatic commands
    """

    if len(input_str) != 0:
        user_input = input_str[0]
    else:
        user_input = input(">>> ")
    
    user_input = user_input.split(' ')

    if user_input[0] == "b2s":
        beat = float(user_input[1])
        return(warp.b2s(beat))

    elif user_input[0] == "s2b":
        seconds = float(user_input[1])
        return(warp.s2b(seconds))

    elif user_input[0] == "marker":
        beat_marker = float(user_input[1])
        seconds_marker = float(user_input[2])
        warp.set_marker(beat_marker, seconds_marker)
        return None

    elif user_input[0] == "end_tempo":        
        end_tempo = float(user_input[1])
        warp.set_end_tempo(end_tempo)
        return None

    elif user_input[0] == "show":
        print('Your warp object: ')
        print('end tempo: %a' % warp.end_tempo)
        print('beat markers: %a' % warp.beat_markers)
        print('second markers: %a' % warp.second_markers)
