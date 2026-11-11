#!/usr/bin/env python3
"""Capture raw NOVA20 UART bytes for later protocol verification.

This intentionally does not parse frames or make any hardware claims.
"""

import argparse
from pathlib import Path
import sys
import time


def positive_seconds(value: str) -> float:
    try:
        seconds = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("seconds must be a positive number") from exc
    if not 0 < seconds <= 3600:
        raise argparse.ArgumentTypeError("seconds must be between 0 and 3600")
    return seconds


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True, help="Serial port (for example, /dev/ttyUSB0)")
    parser.add_argument("--output", required=True, type=Path, help="New .bin file; existing files are never overwritten")
    parser.add_argument("--seconds", type=positive_seconds, default=10.0, help="Capture duration (default: 10)")
    parser.add_argument("--baudrate", type=int, default=921600, help="UART baud rate (default: 921600)")
    args = parser.parse_args(argv)
    if args.baudrate <= 0:
        parser.error("baudrate must be positive")
    if args.output.exists():
        parser.error(f"output already exists: {args.output}")

    try:
        import serial
    except ImportError:
        print("pyserial is required: python3 -m pip install pyserial", file=sys.stderr)
        return 2

    count = 0
    try:
        with serial.Serial(args.port, args.baudrate, bytesize=8, parity="N", stopbits=1, timeout=0.2) as stream:
            with args.output.open("xb") as target:
                deadline = time.monotonic() + args.seconds
                while time.monotonic() < deadline:
                    chunk = stream.read(4096)
                    target.write(chunk)
                    count += len(chunk)
    except (OSError, serial.SerialException) as exc:
        print(f"Capture stopped: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Capture interrupted; any partial output was retained.", file=sys.stderr)
        return 130

    print(f"Saved {count} raw bytes to {args.output}")
    if count == 0:
        print("No bytes received. Check the actual port, wiring, power and baud rate.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
