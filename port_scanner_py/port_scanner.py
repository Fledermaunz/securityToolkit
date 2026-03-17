"""
Port Scanner - Step-by-Step Exercise Blueprint
=====================================================

This is a learning guide for building a port scanner in Python.
Each section contains TODO comments with exercises you need to complete.
Follow the steps in order and implement the functionality yourself.

Topics covered:
- Socket programming basics
- Threading for concurrent operations
- Error handling
- Command-line argument parsing
"""

import socket
import threading
import argparse
import sys
from datetime import datetime
from typing import List, Optional


# ============================================================================
# EXERCISE 1: Create the PortScanner Class
# ============================================================================
# TODO 1.1: Define a class called 'PortScanner' with proper docstring
# The class should store:
#   - target: the host to scan
#   - ports: list of ports to scan
#   - timeout: socket timeout value
#   - open_ports: list to store discovered open ports
#   - lock: threading lock for thread safety
#
# HINT: Use __init__() method to initialize all attributes
# HINT: You'll need: threading.Lock() for the lock
# HINT: Default ports range could be 1-1024 if none specified

class PortScanner:
    def __init__(
            self,
            target: str,
            ports: Optional[List[int]] = None,
            timeout: float = 1.0,
            threads_count: int = 100
    ):
        self.target = target
        self.ports = ports if ports else list(range(1, 1025))
        self.timeout = timeout
        self.open_ports: List[int] = []
        self.threads_count = threading.Lock()



# ============================================================================
# EXERCISE 2: Resolve Hostname to IP Address
# ============================================================================
# TODO 2.1: Create a method called 'resolve_hostname()'
# This method should:
#   - Take no parameters (besides self)
#   - Use socket.gethostbyname() to convert hostname/IP to IP
#   - Return the resolved IP address
#   - Handle socket.gaierror exception if hostname can't be resolved
#   - Print error message and exit if resolution fails
#
# HINT: Use try-except block for error handling
# HINT: Use sys.exit(1) to exit on error
# HINT: Return the IP address on success

def resolve_hostname(self) -> str:
    """TODO: Add docstring explaining what this method does"""
    try:
        ip = socket.gethostbyname(self.target)
        return ip
    except socket.gaierror as e:
        print(f"[-] Error resolving hostname '{self.target}': {e}")
        sys.exit(1)


# ============================================================================
# EXERCISE 3: Scan a Single Port
# ============================================================================
# TODO 3.1: Create a method called 'scan_port(port)'
# This method should:
#   - Accept an integer port number as parameter
#   - Create a socket object (AF_INET for IPv4, SOCK_STREAM for TCP)
#   - Set socket timeout using self.timeout
#   - Attempt to connect using connect_ex() which returns:
#     * 0 if connection successful (port is open)
#     * non-zero if connection fails (port is closed)
#   - Close the socket after attempt
#   - Return True if port is open, False otherwise
#   - Handle socket.timeout and socket.error exceptions
#
# HINT: socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# HINT: sock.connect_ex((self.target, port))
# HINT: sock.close() to free resources
# HINT: Catch exceptions and return False on error

def scan_port(port):
    """TODO: Add docstring"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        result = sock.connect_ex((self.target, port))
        sock.close()
        return result == 0
    
    except socket.timeout:
        return False
    except socket.error as e:
        print(f"Error scanning port {port}: {e}")
        return False


# ============================================================================
# EXERCISE 4: Scan Ports Concurrently with Threading
# ============================================================================
# TODO 4.1: Create a method called 'scan_ports_threaded()'
# This method should:
#   - Print start message with target and timestamp
#   - Calculate chunk size (divide total ports by thread count)
#   - Loop through ports in chunks
#   - For each chunk, create a threading.Thread
#   - Thread should call a helper method '_scan_chunk()' with the port chunk
#   - Set thread as daemon (daemon=True)
#   - Start each thread
#   - Wait for all threads to complete using thread.join()
#   - Finally print completion message
#
# HINT: len(self.ports) // self.threads_count for chunk size
# HINT: Use range(0, len(self.ports), chunk_size) for chunking
# HINT: threading.Thread(target=method, args=(params,), daemon=True)
# HINT: Store threads in a list and join() them all

def scan_ports_threaded():
    """TODO: Add docstring"""
    print(f"\n[*] Starting port scan on {self.target}")
    print(f"[*] Scanning {len(self.ports)} ports with {self.threads_count} threads")
    print(f"[*] Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    threads = []

    chunk_size = max(1, len(self.ports) // self.threads_count)

    for i in range(0, len(self.ports), chunk_size):
        port_chunk = self.ports[i:i + chunk_size]
        thread = threading.Thread(
            target=self._scan_chunk,
            args=(port_chunk,),
            daemon=True 
        )
        threads.start()
        threads.append(thread
        )


    for thread in threads:
        thread.join()


# ============================================================================
# EXERCISE 5: Helper Method for Scanning Port Chunks
# ============================================================================
# TODO 5.1: Create a method called '_scan_chunk(ports)'
# This method is called by each thread and should:
#   - Accept a list of ports as parameter
#   - Loop through each port in the list
#   - Call self.scan_port(port) for each port
#   - If port is open (returns True):
#     * Acquire the lock with: with self.lock:
#     * Add port to self.open_ports list
#     * Print message that port is open (e.g., "[+] Port 22 is OPEN")
#
# HINT: Use for loop to iterate through ports
# HINT: Use 'with self.lock:' for thread-safe list access
# HINT: Print with [+] prefix to indicate success

def _scan_chunk(ports):
    """TODO: Add docstring"""
    pass  # TODO: Implement this method


# ============================================================================
# EXERCISE 6: Display Results
# ============================================================================
# TODO 6.1: Create a method called 'display_results()'
# This method should:
#   - Print completion timestamp
#   - Check if self.open_ports has any entries
#   - If ports found:
#     * Sort the list
#     * Print the count of open ports
#     * For each port, try to get service name using socket.getservbyport()
#     * Print port number and service name
#     * If service not found, print "Unknown service"
#   - If no ports found: print "[−] No open ports found"
#
# HINT: self.open_ports.sort()
# HINT: socket.getservbyport(port) returns service name
# HINT: Wrap socket.getservbyport() in try-except for OSError
# HINT: Use datetime.now().strftime() for timestamp formatting

def display_results():
    """TODO: Add docstring"""
    pass  # TODO: Implement this method


# ============================================================================
# EXERCISE 7: Main Run Method
# ============================================================================
# TODO 7.1: Create a method called 'run()'
# This method should orchestrate the entire scanning process:
#   - Resolve the target hostname to IP (call resolve_hostname())
#   - Update self.target with the resolved IP
#   - Call scan_ports_threaded() to scan all ports
#   - Call display_results() to show findings
#
# HINT: Call methods in logical order
# HINT: This is the main entry point for the scanner

def run():
    """TODO: Add docstring"""
    pass  # TODO: Implement this method


# ============================================================================
# EXERCISE 8: Command-Line Argument Parser
# ============================================================================
# TODO 8.1: Create a function called 'main()'
# This function should:
#   - Create an argparse.ArgumentParser
#   - Add a positional argument "target" (required)
#   - Add optional argument "-p" or "--ports" for specific ports (comma-separated)
#   - Add optional argument "-r" or "--range" for port range (format: start-end)
#   - Add optional argument "-t" or "--timeout" (float, default 1.0)
#   - Add optional argument "-T" or "--threads" (int, default 100)
#   - Parse the arguments
#
# TODO 8.2: Parse the port arguments:
#   - If --ports provided: split by comma and convert to integers
#   - If --range provided: split by hyphen and create range from start to end
#   - If neither provided: ports should be None (will use default 1-1024)
#   - Handle ValueError for invalid input
#
# TODO 8.3: Create PortScanner instance with:
#   - target from args
#   - ports (or None if not specified)
#   - timeout from args
#   - threads_count from args
#
# TODO 8.4: Call scanner.run() in try-except block:
#   - Catch KeyboardInterrupt for Ctrl+C
#   - Catch generic Exception for other errors
#   - Print appropriate messages before exiting
#
# HINT: argparse.ArgumentParser(description="...")
# HINT: parser.add_argument("target", help="...")
# HINT: parser.add_argument("-p", "--ports", ...)
# HINT: args = parser.parse_args()
# HINT: [int(p.strip()) for p in args.ports.split(",")] for port parsing
# HINT: list(range(start, end + 1)) for range creation

def main():
    """TODO: Add docstring"""
    pass  # TODO: Implement this function


# ============================================================================
# EXERCISE 9: Entry Point
# ============================================================================
# TODO 9.1: Add the standard Python entry point:
# if __name__ == "__main__":
#     main()
#
# This ensures main() only runs when script is executed directly,
# not when imported as a module

# TODO: Add entry point here


# ============================================================================
# CHALLENGE EXERCISES (Optional - After completing basics)
# ============================================================================
#
# CHALLENGE 1: Service Detection
# Modify display_results() to also show common service names for known ports
# (e.g., 22=SSH, 80=HTTP, 443=HTTPS, 3306=MySQL)
#
# CHALLENGE 2: Port Range Validation
# Add validation in main() to ensure port numbers are 1-65535
#
# CHALLENGE 3: Improve Threading
# Implement a queue-based approach instead of chunking for more flexibility
#
# CHALLENGE 4: Export Results
# Add an option to export results to a file (JSON or CSV format)
#
# CHALLENGE 5: Keyboard Interrupt Handler
# Add a signal handler to gracefully stop scanning and display partial results
#   HINT: import signal
#   HINT: signal.signal(signal.SIGINT, handler_function)
#
# ============================================================================