


import numpy as np
from scipy.special import binom
from scipy.special import factorial
from tools_io import is_iterable



def target_filter(
    target_sequence: list,
    sample_rate: float = 44100 / 110,
    onset_state: float = None,
    sample_times: list = None,
    filter_order: int = 5,
    start_time: float = 0.0,
    end_time: float = None,
    ):
    #if isinstance( target_sequence, tam.TargetSequence ):
    #    target_sequence = target_sequence.targets
    trajectory = []
    start = start_time
    if end_time == None:
        end = sum( [ tg.duration for tg in target_sequence ] )
    else:
        end = end_time
    duration = end - start
    n_samples = duration * sample_rate
    if not is_iterable( sample_times ):
        sample_times = np.arange( start, end, duration / n_samples )
    #print( 'Len of sample times: {}'.format( len(sample_times) ) )
    #print( 'tam onset: {}'.format(onset_state) )
    if onset_state == None:
        onset_state = target_sequence[0].b
    current_state = [ onset_state ]
    for _ in range( 1, filter_order ):
        current_state.append( 0.0 )

    b_begin = start
    b_end = b_begin
    sample_index = 0
    for target in target_sequence:
        b_begin = b_end
        b_end = b_begin + target.duration
        c = _calculate_coefficients( target, current_state, filter_order )
        while( sample_times[ sample_index ] <= b_end +  0.000000000000001 ):
            #print( 'sample time: {}, b_end: {}'.format( sample_times[ sample_index ], b_end ) )
            constant = 0.0
            t = sample_times[ sample_index ] - b_begin
            for n in range( 0, filter_order ):
                constant += c[ n ] * ( t**n )
            time = sample_times[ sample_index ]
            value= constant * np.exp( - (1/target.tau) * t ) + target.m * t + target.b
            #print( 'time: {}, value: {}'.format( time, value ) )
            trajectory.append( np.array( [ time, value ] ) )
            sample_index += 1
            if sample_index >= len( sample_times ):
                return np.array( trajectory )
        current_state = _calculate_state( current_state, b_end, b_begin, target, filter_order );
    return np.array( trajectory )

def _calculate_coefficients(
    target,
    current_state,
    filter_order,
    ):
    coefficients = [ 0 for _ in current_state ]
    assert len( coefficients ) == filter_order, 'Size conflict'
    coefficients[ 0 ] = current_state[ 0 ] - target.b
    for n in range( 1, filter_order ):
        acc = 0
        for i in range( 0, n ):
            acc += ( coefficients[ i ] * ( (-1 / target.tau)**(n - i) ) * binom( n, i ) * factorial( i ) )
        if n == 1:
            acc += target.m # adaption for linear targets; minus changes in following term!
        coefficients[ n ] = ( current_state[ n ] - acc ) / factorial( n )
    return coefficients

def _calculate_state(
    state,
    time,
    start_time,
    target,
    filter_order,
    ):
    t = time - start_time
    state_update = [ 0 for _ in range( 0, filter_order ) ]
    c = _calculate_coefficients( target, state, filter_order)
    for n in range( 0, filter_order ):
        acc = 0
        for i in range( 0, filter_order ):
            q = 0
            for k in range( 0, np.min( [ filter_order - i, n + 1 ] ) ):
                q += ( ( (-1 / target.tau)**(n - k) ) * binom(n, k) * c[i + k] * factorial(k + i) / factorial(i) )
            acc += ( (t**i) * q )
        state_update[ n ] = acc * np.exp( -( 1 / target.tau) * t)
    # correction for linear targets
    if (filter_order > 1):
        state_update[ 0 ] += (target.b + target.m * t)
    if (filter_order > 2):
        state_update[ 1 ] += target.m
    return state_update