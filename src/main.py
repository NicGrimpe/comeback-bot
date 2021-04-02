from comebackMachine import ComebackMachine

BOT_TOKEN = "YOUR_BOTH_KEY"
COMEBACK_JSON_PATH = 'basicComebacks.json'

def main():
    myComeBackMachine = ComebackMachine(COMEBACK_JSON_PATH, BOT_TOKEN)
    myComeBackMachine.run()

if __name__ == "__main__":
    main()