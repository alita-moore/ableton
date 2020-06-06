def console(warp, *input_str):
    """Console for interacting directly with the warp class
    
    :param warp Warp: the current instance of the warp class
    :param input_str str: optional input string for automatic commands
    """

    if len(input_str) != 0:
        user_input = input_str[0]
    else:
        user_input = input(">> ")
    
    user_input = user_input.split(' ')

    if user_input[0] == 'b2s':
        beat = float(user_input[1])
        return(warp.b2s(beat))
    elif user_input[0] == 's2b':
        seconds = float(user_input[1])
        return(warp.s2b(seconds))
    elif user_input[0] == 'marker':
        beat_marker = float(user_input[1])
        seconds_marker = float(user_input[2])
        warp.set_marker(beat_marker, seconds_marker)
        return None
    elif user_input[0] == 'end_tempo':
        end_tempo = float(user_input[1])
        warp.set_end_tempo(end_tempo)
        return None
    elif user_input[0] == 'show':
        print('Your warp object: ')
        print('end tempo: %a' % warp.end_tempo)
        print('beat markers: %a' % warp.beat_markers)
        print('second markers: %a' % warp.second_markers)
