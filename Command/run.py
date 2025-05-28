import sys
from Main.Query import WhooshQuery  

def main():
    whoosh_query = WhooshQuery()
    while True:
        try:
            user_input = input("# ")
            if user_input.lower() == "exit":
                break
            whoosh_query.ProcQuery(user_input)
        except Exception as e:
            print(e)
    print("Program exited.")

if __name__ == "__main__":
    main()