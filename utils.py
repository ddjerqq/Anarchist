import os
import time

VERBOSE = True

END = "\33[0m"
#\033[38;2;<r>;<g>;<b>m

os.system("")

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
            print(
                red
                + f"[*] <{func.__name__}> Took: { round(time_end - time_start, precision) }"
                + "\a"
                + end
            )

            return return_val
        return wrap
    return real_stat

def warn(message="Warning!") -> None:
    """
        [^] use this to print warnings.\n
        yellow
    """
    rgb(f"[^] {str(message)}" + "\a" + END, 0xffff00)

def ok(message="Success") -> None:
    """
        [*] use this to print sucess messages.\n
        green
    """
    rgb(f"[*] {str(message)}" + END, 0x00ff00)

def rgb(text: str, /, color: str | tuple | int, *, newline: bool = True) -> None:
    """
        print rgb color 🎊 with this
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        \n
        ~~~~~~~~~~~~~~
        Args:
            text  (str): the text you want to print, str() method is automatically called on it
            color (str): #000000 hex representation of color, prefixed with # or not
            color (tuple): (red, green, blue) color tuple
            color (int): 0xff0000 integer representation of hex color.
            newline (bool default False): whether or now you want to print a new line \n
            after you are done printing rgb, you can insert colored text if you set this to false
        \n
        ~~~~~~~~~~~~~~
        Retrurns:
            None
        \n
        ~~~~~~~~~~~~~~
        Example:
            >>> rgb("lorem ipsum", "#ff0000")
            >>> rgb("lorem ipsum", (255, 0, 0))
            >>> rgb("lorem ipsum", 0xff0000)
            >>> rgb("lorem", "#ff0000", newline=False)
            >>> rgb("ipsum", "#00ff00", newline=False)
    """
    if type(color) == str:
        color = tuple(int(color.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    
    elif type(color) == tuple: pass

    elif type(color) == int:
        blue  = color % 256
        green = ( (color - blue) // 256 ) % 256
        red   = ( (color - blue) // 256 ** 2 ) - green // 256
        color = ( (red, green, blue) )
    
    else: raise Exception(f"invalid color {color}")

    if sum(color) > 765: return

    end = "\n" if newline else ""
    _color = f"\033[38;2;{color[0]};{color[1]};{color[2]}m"
    _end_char = "\033[0m"

    print( _color + str(text) + _end_char, end=end )