from . import passwordstate
import argparse
from ..common import prettyllog




def main():
    parser = argparse.ArgumentParser(description="Ignite password state", usage="ign8_passwordstate <action> \n\n \
               \
               version : 0.0.1\n                                              \
               actions:\n                                                      \
               status        status of passwordstate \n\
               sync          sync passwordstate \n\
               export        export of passwordstate \n\
               import        import of passwordstate \n\
               \
               2024 Jakob Holst\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='add, delete, list, sync, status')
    args = parser.parse_args()
    ready = False
    print("check if we are ready to go")


    if args.action[0] == "sync":
        passwordstate.sync()

    if args.action[0] == "export":
        passwordstate.exp()
        
    if args.action[0] == "import":
        passwordstate.imp()
        
    if args.action[0] == "status":
        passwordstate.status()
