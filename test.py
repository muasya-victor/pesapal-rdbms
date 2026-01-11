class VictorTest:
    def __init__(self):
        self.running = True

    def run(self):
        print("running victor test")
        while self.running:
            input_command = input("Enter command: ").strip()
            print(f"You entered: {input_command}")

            if input_command:
                self.command_handler(input_command)


    def command_handler(self, command):
        # turn to uppercase and remove trailing semicolon
        cmd = command.upper().rstrip(';')
        if cmd in ['EXIT', 'QUIT']:
            print("Exiting victor test")
            self.running = False
        else:
            print(f"Victor received command: {command}")

vic = VictorTest()
vic.run()