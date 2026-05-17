import argparse
import asyncio
import ipaddress
import socket
import sys


def main():
    parser = argparse.ArgumentParser(description="This is a basic network scanner.")

    parser.add_argument(
        "targets",
        type=str,
        help="The target IP address, hostname, or range (e.g. google.com or 8.8.8.8/24)",
    )
    parser.add_argument(
        "ports", type=str, help="The port(s) to scan (e.g., 80 or 80,443 or 21-660)"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="The number of seconds to wait for a response (default: 1.0)",
    )
    parser.add_argument(
        "--concurrent",
        type=int,
        default=25,
        help="The number of concurrent connections to make/attempt (default 25)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output (i.e. if ports are closed)",
    )

    args = parser.parse_args()

    targets = resolve_targets(args.targets)
    ports = listify_int_ports(args.ports)
    asyncio.run(run(targets, ports, args.timeout, args.concurrent, args.verbose))


def resolve_targets(target_str: str) -> ipaddress.IPv4Network | ipaddress.IPv6Network:
    # Check if its a ip range
    if "/" in target_str:
        return ipaddress.ip_network(target_str, strict=False)
    # Check if its a single ip
    try:
        ipaddress.ip_address(target_str)
        return ipaddress.ip_network(f"{target_str}/32")
    except ValueError:
        pass
    # Must be a hostname...
    try:
        ip = socket.gethostbyname(target_str)
    except socket.gaierror:
        print(f"Error: could not resolve hostname {target_str}")
        sys.exit(1)
    return ipaddress.ip_network(f"{ip}/32")


def listify_int_ports(ports_str: str) -> list[int]:
    ports: list[int] = []
    for part in ports_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    return ports


async def scan_port(
    target: str, port: int, timeout: float, sema: asyncio.Semaphore
) -> bool:
    """The non-async version:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((target, port))
    sock.close()
    """
    async with sema:
        try:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(target, port), timeout=timeout
            )
            writer.close()
            await writer.wait_closed()
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            return False


async def run(
    targets, ports: list[int], timeout: float, concurrent: int, verbose: bool
):
    sema = asyncio.Semaphore(concurrent)

    if targets.num_addresses == 1:
        ip = str(targets.network_address)
        tasks = [scan_port(ip, port, timeout, sema) for port in ports]
        results = await asyncio.gather(*tasks)
        for port, is_open in zip(ports, results):
            if is_open and not verbose:
                print(f"{ip}:{port} == open")
            elif verbose:
                print(f"{ip}:{port} == {'open' if is_open else 'closed'}")
    else:
        hosts = list(targets.hosts())
        for ip in hosts:
            tasks = [scan_port(str(ip), port, timeout, sema) for port in ports]
            results = await asyncio.gather(*tasks)

            for port, is_open in zip(ports, results):
                if is_open and not verbose:
                    print(f"{ip}:{port} == open")
                elif verbose:
                    print(f"{ip}:{port} == {'open' if is_open else 'closed'}")


if __name__ == "__main__":
    main()
