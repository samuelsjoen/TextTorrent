# Written by Samuel Sjøen
# Based on skeleton code provided by Daniel Hernandez Escobar

from collections import defaultdict
from os import environ
from random import choice
from selectors import EVENT_READ, DefaultSelector
from socket import create_server, socket

TRACKER = environ.get("TRACKER", "localhost")

tracker: defaultdict[bytes, set[str]] = defaultdict(set)
selector = DefaultSelector()


def serve(peer: str, data: bytes) -> bytes:
    """Serves the peer depending on request"""

    match data.split(b" ", 1):
        case [b"ADD", file]:
            tracker[file].add(peer)
            reply = b"OK "
            print(f"{file} has new peer: {peer}")
        case [b"REMOVE", file]:
            try:
                tracker[file].remove(peer)
            except ValueError:
                reply = b"BAD File does not exist"
            else:
                reply = b"OK "
                print(f"{file} removed peer: {peer}")
        case [b"GET_PEER", file]:
            if peer_set := tracker.get(file):
                peer = choice(tuple(peer_set))
                reply = b"OK " + str(peer[0]).encode()
            else:
                reply = b"BAD File does not exist"
        case [b"LIST_FILES"]:
            reply = b"OK " + b"; ".join(tracker)
        case _:
            reply = b"BAD Method not supported"
    return reply


def read(conn: socket) -> None:
    """Function where the decison is made to either serve or unregister the peer"""

    data = conn.recv(1024)
    if data:
        peer = conn.getpeername()
        reply = serve(peer, data.strip())
        conn.sendall(reply)
    else:
        selector.unregister(conn)
        print(f"{conn.getpeername()} disconnected")
        conn.close()


def accept(sock: socket) -> None:
    """Function for accepting connections from peers"""

    conn, addr = sock.accept()
    print(f"{addr} connected")
    conn.setblocking(False)
    selector.register(conn, EVENT_READ, read)


def main() -> None:
    sock = create_server((TRACKER, 12000))
    print("Tracker is online")
    sock.setblocking(False)
    selector.register(sock, EVENT_READ, accept)

    while True:
        events = selector.select()
        for key, _ in events:
            key.data(key.fileobj)


if __name__ == "__main__":
    main()
# Written by Samuel Sjøen
# Based on skeleton code provided by Daniel Hernandez Escobar

from collections import defaultdict
from os import environ
from random import choice
from selectors import EVENT_READ, DefaultSelector
from socket import create_server, socket

TRACKER = environ.get("TRACKER", "localhost")

tracker: defaultdict[bytes, set[str]] = defaultdict(set)
selector = DefaultSelector()


def serve(peer: str, data: bytes) -> bytes:
    """Serves the peer depending on request"""

    match data.split(b" ", 1):
        case [b"ADD", file]:
            tracker[file].add(peer)
            reply = b"OK "
            print(f"{file} has new peer: {peer}")
        case [b"REMOVE", file]:
            try:
                tracker[file].remove(peer)
            except ValueError:
                reply = b"BAD File does not exist"
            else:
                reply = b"OK "
                print(f"{file} removed peer: {peer}")
        case [b"GET_PEER", file]:
            if peer_set := tracker.get(file):
                peer = choice(tuple(peer_set))
                reply = b"OK " + str(peer[0]).encode()
            else:
                reply = b"BAD File does not exist"
        case [b"LIST_FILES"]:
            reply = b"OK " + b"; ".join(tracker)
        case _:
            reply = b"BAD Method not supported"
    return reply


def read(conn: socket) -> None:
    """Function where the decison is made to either serve or unregister the peer"""

    data = conn.recv(1024)
    if data:
        peer = conn.getpeername()
        reply = serve(peer, data.strip())
        conn.sendall(reply)
    else:
        selector.unregister(conn)
        print(f"{conn.getpeername()} disconnected")
        conn.close()


def accept(sock: socket) -> None:
    """Function for accepting connections from peers"""

    conn, addr = sock.accept()
    print(f"{addr} connected")
    conn.setblocking(False)
    selector.register(conn, EVENT_READ, read)


def main() -> None:
    sock = create_server((TRACKER, 12000))
    print("Tracker is online")
    sock.setblocking(False)
    selector.register(sock, EVENT_READ, accept)

    while True:
        events = selector.select()
        for key, _ in events:
            key.data(key.fileobj)


if __name__ == "__main__":
    main()