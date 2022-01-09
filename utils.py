import os
import time

VERBOSE = True

END     = "\33[0m"
#RGB \033[38;2;<r>;<g>;<b>m

def stat(precision: int = 6) -> callable:
    """
        decorator to measure the time a function takes
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        precision (int, optional): floating point numbers of the precision. Defaults to 4.
    """
    def real_stat(func) -> callable:
        def wrap(*args, **kwargs):

            time_start = time.time()
            
            return_val = func(*args, **kwargs)
            
            time_end = time.time()
            
            os.system("")
            red = "\033[91m"
            end = "\033[0m"
            print(red + f"[*] <{func.__name__}> Took: { round(time_end - time_start, precision) }" + "\a" + end)
            
            return return_val
        return wrap
    return real_stat

def log(message = "Log") -> None:
    """
        [*] use this to log things to the console\n
        blue
    """
    os.system("")
    if VERBOSE:
        print("\033[38;2;0;0;255m" + "[*] " + str(message).strip() + END)

def warn(message = "Warning!") -> None:
    """
        [^] use this to print warnings.\n
        yellow
    """
    os.system("")
    print("\033[38;2;0;255;255m" + f"[^] {str(message).strip()}" + "\a" + END)

def ok(message = "Success") -> None:
    """
        [*] use this to print sucess messages.\n
        green
    """
    os.system("")
    print("\033[38;2;0;255;0m" + f"[*] {str(message).strip()}" + "\a" + END)

def rgb(text: str, /, r: int, g: int, b: int, *, newline: bool = True) -> None:
    """
        print rgb color 🎊 with this
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        \n
        ~~~~~~~~~~~~~~
        Args:
            text (str): the text you want to print
            r (int): 0-255 value of Red
            g (int): 0-255 value of Green
            b (int): 0-255 value of Blue
            newline (bool default False): whether or now you want to print a new line \n
            after you are done printing rgb, you can insert colored text if you set this to false
        \n
        ~~~~~~~~~~~~~~
        Retrurns:
            None
        \n
        ~~~~~~~~~~~~~~
        Example:
            >>> rgb("foo bar candy", 255, 0, 255)
            "foo bar candy" but printed in red
            >>> rgb("red", 255, 0, 0, newline=False)
            >>> rgb("green", 0, 255, 0, newline=False)
            >>> rgb("blue", 0, 0, 255, newline=False)
            "red green blue" #but they will be colored respectively
    """
    end = "\n" if newline else ""
    print(f"\033[38;2;{r};{g};{b}m" + str(text) + "\033[0m", end=end)
