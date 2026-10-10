#!/usr/bin/env python3
"""Serve the self-contained static page on localhost, without dependencies."""
import argparse
import os
import re
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class VideoRequestHandler(SimpleHTTPRequestHandler):
    """Support byte ranges so the local video can seek without a full download."""

    def send_head(self):
        self.bytes_remaining = None
        path = Path(self.translate_path(self.path))
        if path.suffix.lower() != ".mp4" or not path.is_file():
            return super().send_head()
        try:
            stream = path.open("rb")
        except OSError:
            self.send_error(404, "File not found")
            return None
        info = os.fstat(stream.fileno())
        start, end = 0, info.st_size - 1
        requested_range = self.headers.get("Range", "") if self.command == "GET" else ""
        match = re.fullmatch(r"bytes=(\d*)-(\d*)", requested_range.strip())
        if match:
            first, last = match.groups()
            if first:
                start = int(first)
                end = min(int(last), end) if last else end
            elif last and int(last) > 0:
                start = max(0, info.st_size - int(last))
            else:
                start = info.st_size
            if start > end or start >= info.st_size:
                stream.close()
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{info.st_size}")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return None
            stream.seek(start)
            self.bytes_remaining = end - start + 1
        self.send_response(206 if match else 200)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Last-Modified", self.date_time_string(info.st_mtime))
        if match:
            self.send_header("Content-Range", f"bytes {start}-{end}/{info.st_size}")
        self.end_headers()
        return stream

    def copyfile(self, source, outputfile):
        try:
            if self.bytes_remaining is None:
                return super().copyfile(source, outputfile)
            remaining = self.bytes_remaining
            while remaining > 0:
                chunk = source.read(min(64 * 1024, remaining))
                if not chunk:
                    break
                outputfile.write(chunk)
                remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            # Browsers may close a preload request after reading the metadata.
            pass


def main():
    parser = argparse.ArgumentParser(description="PanoHK360 local homepage")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent / "dist"
    handler = partial(VideoRequestHandler, directory=str(directory))
    server = None
    for port in range(args.port, args.port + 11):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), handler)
            break
        except OSError:
            continue
    if server is None:
        raise SystemExit("No available port. Run with --port 8080.")
    print(f"PanoHK360 homepage: http://localhost:{server.server_port}/", flush=True)
    print("Press Ctrl+C to stop.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
