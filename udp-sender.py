import socket
IP = "127.0.0.1"
PORT = 5005
running = True

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while running:
    scenario = input("Enter destination 1-4\nor 0 to exit:")
    try:
        scenario_int = int(scenario)
        if scenario_int > 4:
            print("Enter valid value (0-4)\n\n")
        elif int(scenario) == 0:
            running = False
            break
        else:
            sock.sendto(scenario.encode('utf-8'), (IP, PORT))
            print(f'Scenario {scenario}, sent to {IP}:{PORT}\n\n')
    except:
        print("Enter valid value (0-4)\n\n")

