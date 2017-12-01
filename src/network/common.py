import sys

debug = False


def exceptionHandler(exception_type, exception, traceback, debug_hook=sys.excepthook):
    '''Print user friendly error messages normally, full traceback if DEBUG on.
       Adapted from http://stackoverflow.com/questions/27674602/hide-traceback-unless-a-debug-flag-is-set
    '''
    if debug:
        print('\n*** Error:')
        # raise
        debug_hook(exception_type, exception, traceback)
    else:
        print(f"\t{exception_type.__name__}: {exception}")
sys.excepthook = exceptionHandler
