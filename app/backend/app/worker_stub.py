"""Durable scan worker entry point for self-hosted deployments."""

from __future__ import annotations

import argparse

from . import database
from .config import load_settings
from .services.scan_jobs import run_durable_scan_worker


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the durable scan worker.")
    parser.add_argument("--once", action="store_true", help="Process at most one job.")
    args = parser.parse_args()
    settings = load_settings()
    database.init_database(settings)
    if settings.auto_create_schema:
        database.Base.metadata.create_all(bind=database.engine)
    run_durable_scan_worker(settings, once=args.once)


if __name__ == "__main__":
    main()
