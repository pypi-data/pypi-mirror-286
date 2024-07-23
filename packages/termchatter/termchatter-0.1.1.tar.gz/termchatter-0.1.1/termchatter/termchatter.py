import sys
sys.dont_write_bytecode = True
from . import setup
from . import send_message
from . import receive_message
from . import credits

def main():
    if len(sys.argv) < 2:
        print("Type 'termchatter help' for guidance")
        return
    
    command = sys.argv[1]

    if(command == "setup"):
        setup.main(sys.argv[2:])
    elif(command == "send"):
        send_message.main(sys.argv[2:])
    elif(command == "receive"):
        receive_message.main()
    elif(command == "credits"):
        credits.main()
    elif(command == "help"):
        print("setup:")
        print("  termchatter setup [channel]")
        print("    Changes/sets the pusher channel you want to broadcast and receive messages to and from\n")
        print("  termchatter setup [channel] [username]")
        print("    Changes/sets both the pusher channel and username you want to use\n")
        print("  termchatter setup pusher [app id] [app key] [secret] [cluster]")
        print("    Sets up pusher\n")
        print("chat:")
        print("  termchatter send [message]")
        print("    Broadcasts a message to the pusher channel you've selected\n")
        print("  termchatter receive")
        print("    Run a listener to the pusher channel you've selected\n")
        print("Run 'termchatter receive' on a separate console")
    else:
        print("Type 'termchatter help' for guidance")

if __name__ == "__main__":
    main()