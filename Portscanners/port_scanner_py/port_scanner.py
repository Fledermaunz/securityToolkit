import socket
import threading
import argparse
import sys
from datetime import datetime
from typing import List, Optional


class PortScanner:
    """
    A simple multi-threaded port scanner.
    """

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
        self.threads_count = threads_count
        self.lock = threading.Lock()

    def resolve_hostname(self) -> str:
        """Resolve hostname to IP address."""
        try:
            ip = socket.gethostbyname(self.target)
            return ip
        except socket.gaierror as e:
            print(f"[-] Error resolving hostname '{self.target}': {e}")
            sys.exit(1)

    def scan_port(self, port: int) -> bool:
        """Scan a single port."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            sock.close()
            return result == 0
        except socket.timeout:
            return False
        except socket.error:
            return False

    def _scan_chunk(self, ports: List[int]):
        """Scan a chunk of ports (used by threads)."""
        for port in ports:
            if self.scan_port(port):
                with self.lock:
                    self.open_ports.append(port)
                print(f"[+] Port {port} is OPEN")

    def scan_ports_threaded(self):
        """Scan ports using multiple threads."""
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

            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def display_results(self):
        """Display scan results."""
        print(f"\n[*] Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n[*] === Results ===")

        if self.open_ports:
            self.open_ports.sort()
            print(f"[*] Found: {len(self.open_ports)} open port(s):")

            for port in self.open_ports:
                try:
                    service = socket.getservbyport(port)
                except OSError:
                    service = "Unknown service"

                print(f"   Port {port}: {service}")
        else:
            print("[−] No open ports found")

    def run(self):
        """Run the scanner."""
        self.target = self.resolve_hostname()
        self.scan_ports_threaded()
        self.display_results()


def main():
    parser = argparse.ArgumentParser(
        description="Simple Port Scanner in Python",
        epilog="Example: python scanner.py 127.0.0.1 -p 22,80,443"
    )

    parser.add_argument(
        "target",
        help="Target hostname or IP address"
    )

    parser.add_argument(
        "-p", "--ports",
        help="Specific ports (e.g. 22,80,443)",
        type=str,
        default=None
    )

    parser.add_argument(
        "-r", "--range",
        help="Port range (e.g. 1-1000)",
        type=str,
        default=None
    )

    parser.add_argument(
        "-t", "--timeout",
        help="Timeout (default: 1.0)",
        type=float,
        default=1.0
    )

    parser.add_argument(
        "-T", "--threads",
        help="Number of threads (default: 100)",
        type=int,
        default=100
    )

    args = parser.parse_args()

    ports = None

    if args.ports:
        try:
            ports = [int(p.strip()) for p in args.ports.split(",")]
        except ValueError:
            print("Error: Ports must be comma-separated integers")
            sys.exit(1)

    elif args.range:
        try:
            start, end = map(int, args.range.split("-"))
            ports = list(range(start, end + 1))
        except ValueError:
            print("Error: Range must be format start-end")
            sys.exit(1)

    if args.threads < 1:
        print("Error: Threads must be >= 1")
        sys.exit(1)

    scanner = PortScanner(
        target=args.target,
        ports=ports,
        timeout=args.timeout,
        threads_count=args.threads
    )

    try:
        scanner.run()
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()