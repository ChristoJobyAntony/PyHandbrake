from typing import Callable, List, Tuple


class Menu : 

    def __init__(self, name:str, menu:List[Tuple[str, Callable[[None], None]]] = [], runUntilExit:bool =True) -> None:
        self.name = name
        self.menu : List[Tuple[str, Callable[[any], None], List[any]]] = menu[0:]
        self.runUntilExit = runUntilExit

    def addMenu (self, name : str, run : Callable[[None], None], args:List[any]=[]) :
        self.menu.append((name, run, args))

    def _printHeader (self) : 
        l = len(self.name)
        print("="*(l+2))
        print("|", self.name, "|", sep="")
        print("="*(l+2))

    def run (self) : 
        menu = self.menu + [( "Return", lambda : print("Returning ..."), []) ]
        while True : 
            self._printHeader()
            print()
            # Print the complete Menu
            for index, (name, _, _)in enumerate(menu) :
                print(f"{index+1}. {name}")
            print()
            # Get the input from user
            while True :
                try :
                    n = int(input("Enter menu item index : "))
                    if n >= 1 and n <= len(self.menu) : 
                        item = self.menu[n-1]
                        try :
                            item[1](*item[2])
                        except Exception as e:
                            print("Failed to excute function due to,", e) 
                            raise e
                        if self.runUntilExit : break
                        else : return
                    elif n == len(self.menu)+1 : 
                        return None
                    else :
                        print("Enter a number within a valid range")
                except ValueError as e:
                    print("Please enter a valid input !", e)
        


