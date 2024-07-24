def print_colored(text, color, end='\n'):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    color_code = colors.get(color, colors["white"])
    reset_code = colors["reset"]
    print(f"{color_code}{text}{reset_code}", end=end)