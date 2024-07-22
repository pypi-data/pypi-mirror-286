class t:
    def red(text):
        return f"\033[91m{text}\033[0m"
    def green(text):
        return f"\033[92m{text}\033[0m"
    def yellow(text):
        return f"\033[93m{text}\033[0m"
    def blue(text):
        return f"\033[94m{text}\033[0m"
    def purple(text):
        return f"\033[95m{text}\033[0m"
    def cyan(text):
        return f"\033[96m{text}\033[0m"
    def white(text):
        return f"\033[97m{text}\033[0m"
    def black(text):
        return f"\033[98m{text}\033[0m"
    def bg_red(text):
        return f"\033[101m{text}\033[0m"
    def bg_green(text):
        return f"\033[102m{text}\033[0m"
    def bg_yellow(text):
        return f"\033[103m{text}\033[0m"
    def bg_blue(text):
        return f"\033[104m{text}\033[0m"
    def bg_purple(text):
        return f"\033[105m{text}\033[0m"
    def bg_cyan(text):
        return f"\033[106m{text}\033[0m"
    def bg_white(text):
        return f"\033[107m{text}\033[0m"
    def bg_black(text):
        return f"\033[100m{text}\033[0m"


    @staticmethod
    def combined_color(text, fg_color, bg_color):
        return f"{bg_color}{fg_color}{text}\033[0m"
