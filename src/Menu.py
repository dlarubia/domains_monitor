from time import sleep
import os
from src.Menu_options import Menu_Options

SIZE = 45
options = Menu_Options().options

def show_div():
    print("-" * SIZE)

def show_header():
    show_div()
    print(return_centered("DOMAINS MONITOR"))
    show_div()

def return_centered(text):
    return (int((SIZE-len(text))/2)*" " + text)

def show_options(options):
    for i in range(1, len(options)+1):
        print(f'\033[33m{i}\033[m  - \033[34m{options[i-1]}\033[m')
    show_div()

def read_option():
    while True:
        try:
            option = int(input("\033[32mSelect the option: \033[m"))
        except (ValueError, TypeError):
            show_main_menu()
            print("\033[31mERROR: please, type a valid integer\033[m")
        else:
            return option

def clear_screen():
    os.system('cls||clear')

def execute_option(n):
    try:
        print("Executando opção:" + str(options[n-1]))
    except:
        show_main_menu()
        print("\033[31mERROR: " + str(n) + " is not a valid option. Try again\033[m")
        return
    else:
        new_options = ["Yes", "No"]
        while True:
            show_div()
            print("Want to go back to the main menu?")
            show_options(new_options)
            option = read_option()
            if option == 1:
                show_main_menu()
                return
            if option == 2:
                print("Leaving...")
                exit() 
            else: 
                print("\033[31mERROR: " + str(n) + " is not a valid option. Try again\033[m")


def show_main_menu():
    clear_screen()
    show_header()
    show_options(options)

def menu():
    show_header()
    # options = Menu_Options().options
    show_options(options)
    option = read_option()
    while option != len(options):
        execute_option(option)
        option = read_option()

menu()