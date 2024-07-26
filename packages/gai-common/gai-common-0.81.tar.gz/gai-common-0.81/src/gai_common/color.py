class Color:
    def white(self,text,end="\n",flush=False):
        italic_start = "\033[3m"
        color_start = "\033[97m"  # Bright white color
        reset = "\033[0m"
        print(f"{italic_start}{color_start}{text}{reset}", end=end, flush=flush)

    def yellow(self,text,end="\n",flush=False):
        italic_start = "\033[3m"
        color_start = "\033[93m"  # Bright yellow color
        reset = "\033[0m"
        print(f"{italic_start}{color_start}{text}{reset}", end=end, flush=flush)

    def green(self,text,end="\n",flush=False):
        italic_start = "\033[3m"
        color_start = "\033[92m"
        reset = "\033[0m"
        print(f"{italic_start}{color_start}{text}{reset}", end=end, flush=flush)

    def red(self,text,end="\n",flush=False):
        italic_start = "\033[3m"
        color_start = "\033[91m"
        reset = "\033[0m"
        print(f"{italic_start}{color_start}{text}{reset}", end=end, flush=flush)

    def purple(self,text,end="\n",flush=False):
        italic_start = "\033[3m"
        color_start = "\033[95m"
        reset = "\033[0m"
        print(f"{italic_start}{color_start}{text}{reset}", end=end, flush=flush)

    def cyan(self,text,end="\n",flush=False):
        italic_start = "\033[3m"
        color_start = "\033[96m"
        reset = "\033[0m"
        print(f"{italic_start}{color_start}{text}{reset}", end=end, flush=flush)

