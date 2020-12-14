import time

def take_time(function):
        start = time.time()
        function_output = function()
        execution_time = time.time() - start
        return function_output, execution_time