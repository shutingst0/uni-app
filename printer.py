class Printer:
    BLUE   = "\033[94m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    RESET  = "\033[0m"

    @staticmethod
    def info(text):
        print(f"{Printer.BLUE}{text}{Printer.RESET}")

    @staticmethod
    def success(text):
        print(f"{Printer.GREEN}{text}{Printer.RESET}")

    @staticmethod
    def warning(text):
        print(f"{Printer.YELLOW}{text}{Printer.RESET}")

    @staticmethod
    def error(text):
        print(f"{Printer.RED}{text}{Printer.RESET}")
