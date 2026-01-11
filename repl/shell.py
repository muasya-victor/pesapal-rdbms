class MiniDBShell:
    def __init__(self):
        self.running = True
    
    def run(self):
        print("Muasya RDBMS - Type 'EXIT;' to quit")
        while self.running:
            try:
                command = input("mini-db> ").strip()
                if not command:
                    continue
                self.handle_command(command)
            except KeyboardInterrupt:
                print("\nUse EXIT; to quit")
            except EOFError:
                break

    def handle_command(self, command):
    # Normalize: remove trailing semicolon, uppercase
        cmd = command.rstrip(';').upper()
        
        if cmd in ['EXIT', 'QUIT']:
            print("Goodbye!")
            self.running = False
            return
        
        # Special demo command
        if cmd == "SELECT 1":
            print("[1]")
            return
        
        # Echo everything else
        print(f"Command received: {command}")

    def get_full_command(self):
        """Collect lines until semicolon"""
        lines = []
        while True:
            line = input("... " if lines else "mini-db> ")
            lines.append(line)
            if ';' in line:
                break
        return ' '.join(lines)