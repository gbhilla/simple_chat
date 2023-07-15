import subprocess

class ServerClientRunner:
    def __init__(self):
        self.server_process = None
        self.client_processes = []

    def run_server(self):
        self.server_process = subprocess.Popen(['python', 'Server.py'])

    def run_clients(self, num_clients):
        for _ in range(num_clients):
            client_process = subprocess.Popen(['python', 'Client.py'])
            self.client_processes.append(client_process)

    def stop_server(self):
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()

    def stop_clients(self):
        for client_process in self.client_processes:
            client_process.terminate()
            client_process.wait()

    def run(self, num_clients):
        self.run_server()
        self.run_clients(num_clients)

        # Wait for the server and clients to finish running
        self.server_process.wait()
        self.stop_clients()

        # Cleanup any remaining client processes
        for client_process in self.client_processes:
            client_process.wait()

        self.client_processes.clear()

# Usage example
runner = ServerClientRunner()
runner.run(num_clients=3)