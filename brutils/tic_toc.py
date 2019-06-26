## <tic_toc>
import time
import datetime

def tic() :
    """
        | tic-toc used to measure elapsed time (usage similar to matlab tic-toc)

        | basic tic, returns current time
        | when results of tic are given to a later toc, toc returns the elapsed time

    """
    return time.time()

def toc(start_time) :
    """
        | tic-toc used to measure elapsed time (usage similar to matlab tic-toc)

        | *returns* time in seconds since given ``tic``

        | start_time -> ``tic``
    """
    end_time = time.time()
    return (end_time-start_time)

## ptoc -> print_toc
def ptoc(start_time, descrip=None) :
    """
        *prints* time in seconds since given ``tic``

        | start_time -> ``tic``
    """
    elapsed_time = toc(start_time)
    if descrip == None :
        print('time elapsed {} seconds'.format(elapsed_time))
    else :
        #print('{} seconds'.format(descrip, elapsed_time))
        dtoc([start_time])

## dtic -> described_tic
def dtic(descrip) :
    """
        | like tic but takes a description of what is being timed
        | ``dtoc`` prints given description with the elapsed time

        | useful to identify what different times represent in output
    """
    return [time.time(),descrip]

## dtoc -> described_toc
def dtoc(descrip_n_time) :
    """
        prints elapsed time since given ``dtic``

        | descrip_n_time -> ``dtoc`` -> [start_time, descrip]
    """
    elapsed_time = time.time() - descrip_n_time[0]
    time_str = str(datetime.timedelta(seconds=elapsed_time))
    print('{} : {}'.format(descrip_n_time[1], int(elapsed_time)))

    # print('{} : {:.2f} seconds'.format(descrip_n_time[1], elapsed_time))
## </tic_toc>


def loc_print() :
    # print(locals().keys())
    # print(globals().keys())
    import inspect
    # print(inspect.getframeinfo(inspect.currentframe().f_back).function)
    cur_frame = inspect.currentframe()
    prev_frame = cur_frame.f_back
    prev_frame_info = inspect.getframeinfo(prev_frame).function
    print(inspect.getframeinfo(cur_frame).function)
    print(prev_frame_info)
    print(__name__)
    print(__package__)