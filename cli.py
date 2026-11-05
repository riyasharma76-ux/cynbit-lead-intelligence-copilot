"""CLI entry point for the proof of concept."""
import argparse
import json
import sys
from pathlib import Path

from src.scorer import Lead, score_lead


def main() -> None:
    # Windows terminals may default to cp1252; JSON output contains the INR sign.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Explainable inbound-lead triage")
    parser.add_argument("--input", help="JSON file containing one lead object or a list of lead objects")
    parser.add_argument("--name"); parser.add_argument("--email", default="")
    parser.add_argument("--service", default=""); parser.add_argument("--company-size", type=int, default=0)
    parser.add_argument("--budget", type=int, default=0); parser.add_argument("--timeline", default="")
    parser.add_argument("--message", default=""); parser.add_argument("--source", default="website")
    args = parser.parse_args()
    if args.input:
        raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
        leads = raw if isinstance(raw, list) else [raw]
    else:
        if not args.name:
            parser.error("provide --input or at least --name")
        leads = [{"name": args.name, "email": args.email, "service": args.service,
                  "company_size": args.company_size, "budget": args.budget, "timeline": args.timeline,
                  "message": args.message, "source": args.source}]
    print(json.dumps([score_lead(Lead(**lead)) for lead in leads], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
