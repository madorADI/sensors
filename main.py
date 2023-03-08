from classifier import *
from ID_MODULES import *
from license_palte_verifier import *
from server import *
from utils import *
def main():
    print("Starting the server...")
    server = Server()
    server.start()
if __name__ == '__main__':
    main()