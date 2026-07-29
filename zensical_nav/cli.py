import argparse
import os
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Sequence

from .config import NavConfigError
from .yaml_config import dump_config, expanded_config, expand_config_file, load_config


def main(argv: Sequence[str] | None = None) -> int:
    _install_sigterm_handler()
    parser = _parser()
    arguments, forwarded = parser.parse_known_args(argv)
    config_path = arguments.config_file.resolve()

    try:
        if arguments.command == "expand":
            rendered = dump_config(expanded_config(config_path), arguments.output)
            if rendered:
                sys.stdout.write(rendered)
            return 0
        if arguments.command == "build":
            return _build(config_path, forwarded)
        return _serve(config_path, forwarded, arguments.watch_interval)
    except (NavConfigError, OSError, ValueError) as error:
        parser.error(str(error))
    return 2


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="zensical-nav",
        description="Expand mixed manual and automatic navigation before running Zensical.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    expand = subparsers.add_parser("expand", help="print or write the expanded configuration")
    _config_option(expand)
    expand.add_argument("-o", "--output", type=Path, help="write expanded YAML to this path")

    build = subparsers.add_parser("build", help="expand navigation and run zensical build")
    _config_option(build)

    serve = subparsers.add_parser("serve", help="expand navigation and run zensical serve")
    _config_option(serve)
    serve.add_argument("--watch-interval", type=float, default=0.5, help=argparse.SUPPRESS)
    return parser


def _config_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-f", "--config-file", type=Path, default=Path("mkdocs.yml"))


def _build(config_path: Path, forwarded: list[str]) -> int:
    generated = _temporary_config_path(config_path)
    try:
        expand_config_file(config_path, generated)
        return subprocess.run(
            _zensical_command("build", generated, forwarded),
            check=False,
        ).returncode
    finally:
        generated.unlink(missing_ok=True)


def _serve(config_path: Path, forwarded: list[str], interval: float) -> int:
    if interval <= 0:
        raise ValueError("--watch-interval must be greater than zero")
    generated = _temporary_config_path(config_path)
    expand_config_file(config_path, generated)
    stop = threading.Event()
    watcher = threading.Thread(
        target=_watch_and_expand,
        args=(config_path, generated, interval, stop),
        daemon=True,
    )
    watcher.start()
    process: subprocess.Popen | None = None
    try:
        process = subprocess.Popen(_zensical_command("serve", generated, forwarded))
        return process.wait()
    except KeyboardInterrupt:
        return 130
    finally:
        stop.set()
        watcher.join(timeout=max(1.0, interval * 2))
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        generated.unlink(missing_ok=True)


def _zensical_command(command: str, config_path: Path, forwarded: list[str]) -> list[str]:
    return [sys.executable, "-m", "zensical", command, "-f", str(config_path), *forwarded]


def _watch_and_expand(source: Path, destination: Path, interval: float, stop: threading.Event) -> None:
    previous: tuple[tuple[str, int, int], ...] = ()
    while not stop.is_set():
        current = _source_snapshot(source)
        if current != previous:
            try:
                config = expanded_config(source)
                temporary = destination.with_suffix(destination.suffix + ".tmp")
                dump_config(config, temporary)
                os.replace(temporary, destination)
                previous = current
            except (NavConfigError, OSError, ValueError) as error:
                print(f"zensical-nav: cannot update navigation: {error}", file=sys.stderr)
        if stop.wait(interval):
            break


def _source_snapshot(config_path: Path) -> tuple[tuple[str, int, int], ...]:
    config = load_config(config_path)
    docs_setting = config.get("docs_dir", "docs") if isinstance(config, dict) else "docs"
    docs_dir = (config_path.parent / docs_setting).resolve()
    paths = [config_path]
    if docs_dir.is_dir():
        paths.extend(path for path in docs_dir.rglob("*") if path.is_file() and path.suffix.casefold() == ".md")
    snapshot = []
    for path in paths:
        try:
            stat = path.stat()
        except FileNotFoundError:
            continue
        snapshot.append((str(path), stat.st_mtime_ns, stat.st_size))
    return tuple(sorted(snapshot))


def _install_sigterm_handler() -> None:
    if threading.current_thread() is not threading.main_thread():
        return

    def interrupt(_signum, _frame):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, interrupt)


def _temporary_config_path(config_path: Path) -> Path:
    descriptor, name = tempfile.mkstemp(
        prefix=f".{config_path.stem}.zensical-nav-",
        suffix=config_path.suffix,
        dir=config_path.parent,
    )
    os.close(descriptor)
    return Path(name)


if __name__ == "__main__":
    raise SystemExit(main())
