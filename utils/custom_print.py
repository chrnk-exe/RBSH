from colorama import init, Fore, Back, Style
# init already called


def client_print(*args, **kwargs):
    print(Fore.LIGHTGREEN_EX + '[CLIENT] ', end='')
    print(*args, **kwargs)


def server_print(*args, **kwargs):
    print(Fore.LIGHTBLUE_EX + '[SERVER] ', end='')
    print(*args, **kwargs)

