from Tkinter import Tk

__root = Tk()
__root.withdraw()

def get():
    return __root.clipboard_get()
    
def set(data):
    __root.clipboard_clear()
    __root.clipboard_append(data)
    
def append(data):
    __root.clipboard_append(data)
    
    
if __name__ == "__main__":
    set("Clipboard test")
    print get()