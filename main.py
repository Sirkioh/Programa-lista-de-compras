from gui import interfaz
from services import excel,webscrapping

def main():
    xl = excel.xl()
    ws = webscrapping.ws(xl)
    gui = interfaz.gui(xl, ws)
    
    gui.main()
    
if __name__ == "__main__":
    main()