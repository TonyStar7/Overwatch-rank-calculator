
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if project_root not in sys.path:
    sys.path.append(project_root)



from Src.app import MyWindow


if __name__ == "__main__":  
    window = MyWindow()
    window.mainloop()


