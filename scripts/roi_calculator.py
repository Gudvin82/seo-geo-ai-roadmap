#!/usr/bin/env python3
"""Estimate SEO / GEO / AI acquisition ROI from simple business inputs."""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate visits, leads, sales, revenue, margin, and ROI."
    )
    parser.add_argument("--traffic", type=float, required=True, help="Visits in the period.")
    parser.add_argument(
        "--conversion-rate",
        type=float,
        required=True,
        help="Visit-to-lead conversion rate as a decimal, for example 0.03.",
    )
    parser.add_argument(
        "--lead-to-sale-rate",
        type=float,
        required=True,
        help="Lead-to-sale rate as a decimal, for example 0.2.",
    )
    parser.add_argument(
        "--average-check",
        type=float,
        required=True,
        help="Average revenue per sale.",
    )
    parser.add_argument(
        "--margin-rate",
        type=float,
        required=True,
        help="Gross margin rate as a decimal, for example 0.4.",
    )
    parser.add_argument("--seo-cost", type=float, required=True, help="Channel cost for the period.")
    parser.add_argument(
        "--ai-referred-share",
        type=float,
        default=0.0,
        help="Optional share of traffic attributed to AI-referrals as a decimal.",
    )
    parser.add_argument(
        "--period",
        choices=["monthly", "quarterly"],
        default="monthly",
        help="Reporting period label.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    visits = args.traffic
    leads = visits * args.conversion_rate
    sales = leads * args.lead_to_sale_rate
    revenue = sales * args.average_check
    gross_margin = revenue * args.margin_rate
    cost = args.seo_cost
    roi = ((gross_margin - cost) / cost) if cost else 0.0
    ai_referred_visits = visits * args.ai_referred_share

    print(f"Period: {args.period}")
    print(f"Visits: {visits:.2f}")
    print(f"AI-referred visits: {ai_referred_visits:.2f}")
    print(f"Leads: {leads:.2f}")
    print(f"Sales: {sales:.2f}")
    print(f"Revenue: {revenue:.2f}")
    print(f"Gross margin: {gross_margin:.2f}")
    print(f"Cost: {cost:.2f}")
    print(f"Estimated ROI / ROMI: {roi:.2%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
