#!/usr/bin/env python3
"""Collect recently released UK structures for the "New UK structures" feed.

Sources
  PDB     entries funded by a UK organisation (pdbx_audit_support.country) or
          with data collected at Diamond (diffrn_source.pdbx_synchrotron_site).
          Cryo-EM entries carry their EMDB map IDs.
  SASBDB  entries measured on an instrument in the United Kingdom.

Writes data/uk_structures.json (read by Hugo). Standard library only, so it
runs on a plain GitHub Actions runner.

Usage
  python3 scripts/uk_structures.py                  # update the feed
  python3 scripts/uk_structures.py --images DIR     # download PDB images for the feed
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEED = ROOT / "data" / "uk_structures.json"
SASBDB_SEEN = ROOT / "data" / "sasbdb_seen.json"

RCSB_SEARCH = "https://search.rcsb.org/rcsbsearch/v2/query"
RCSB_GRAPHQL = "https://data.rcsb.org/graphql"
RCSB_IMAGE = "https://cdn.rcsb.org/images/structures/{id}_assembly-1.jpeg"
SASBDB_CODES = "https://www.sasbdb.org/rest-api/entry/codes/all/"
SASBDB_SUMMARY = "https://www.sasbdb.org/rest-api/entry/summary/{code}/"

UK_COUNTRIES = {"United Kingdom", "UK", "Great Britain", "England", "Scotland", "Wales", "Northern Ireland"}
UK_SYNCHROTRONS = {"Diamond"}

METHODS = {
    "X-RAY DIFFRACTION": ("X-ray crystallography", "crystallography"),
    "ELECTRON MICROSCOPY": ("Cryo-EM", "cryo-em"),
    "ELECTRON CRYSTALLOGRAPHY": ("Electron crystallography", "cryo-em"),
    "SOLUTION NMR": ("NMR", "nmr"),
    "SOLID-STATE NMR": ("NMR", "nmr"),
    "NEUTRON DIFFRACTION": ("Neutron crystallography", "crystallography"),
}

GRAPHQL_QUERY = """
query($ids: [String!]!) {
  entries(entry_ids: $ids) {
    rcsb_id
    struct { title }
    exptl { method }
    rcsb_entry_info { resolution_combined }
    rcsb_accession_info { initial_release_date }
    rcsb_primary_citation { title journal_abbrev year pdbx_database_id_DOI rcsb_authors }
    pdbx_audit_support { country }
    rcsb_entry_container_identifiers { emdb_ids }
    diffrn_source { pdbx_synchrotron_site }
  }
}
"""


def http_json(url: str, payload: dict | None = None, retries: int = 3):
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Content-Type": "application/json", "User-Agent": "bsg-website-feed (https://biostructures.org.uk)"}
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
                return json.loads(body) if body else None
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt == retries - 1:
                raise
            print(f"  retrying {url}: {e}", file=sys.stderr)
            time.sleep(5 * (attempt + 1))


def short_authors(names: list[str]) -> str:
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    return f"{names[0]} … {names[-1]}"


# ------------------------------------------------------------------ PDB

def pdb_search(since: dt.date) -> list[str]:
    date_node = {"type": "terminal", "service": "text", "parameters": {
        "attribute": "rcsb_accession_info.initial_release_date", "operator": "greater_or_equal",
        "value": since.isoformat()}}
    uk_nodes = [
        {"type": "terminal", "service": "text", "parameters": {
            "attribute": "pdbx_audit_support.country", "operator": "exact_match", "value": "United Kingdom"}},
    ] + [
        {"type": "terminal", "service": "text", "parameters": {
            "attribute": "diffrn_source.pdbx_synchrotron_site", "operator": "exact_match", "value": site}}
        for site in sorted(UK_SYNCHROTRONS)
    ]
    query = {
        "query": {"type": "group", "logical_operator": "and", "nodes": [
            date_node, {"type": "group", "logical_operator": "or", "nodes": uk_nodes}]},
        "return_type": "entry",
        "request_options": {"return_all_hits": True},
    }
    result = http_json(RCSB_SEARCH, query)
    return [r["identifier"] for r in (result or {}).get("result_set", [])]


def pdb_details(ids: list[str]) -> list[dict]:
    out = []
    for i in range(0, len(ids), 50):
        batch = ids[i:i + 50]
        res = http_json(RCSB_GRAPHQL, {"query": GRAPHQL_QUERY, "variables": {"ids": batch}})
        for e in (res or {}).get("data", {}).get("entries", []) or []:
            out.append(pdb_entry(e))
    return out


def pdb_entry(e: dict) -> dict:
    methods = [m.get("method", "") for m in (e.get("exptl") or [])]
    label, tech = METHODS.get(methods[0] if methods else "", (methods[0].title() if methods else "", "other"))
    res = ((e.get("rcsb_entry_info") or {}).get("resolution_combined") or [None])[0]
    cit = e.get("rcsb_primary_citation") or {}
    countries = {s.get("country") for s in (e.get("pdbx_audit_support") or [])}
    sites = {s.get("pdbx_synchrotron_site") for s in (e.get("diffrn_source") or [])}
    reasons = []
    if countries & UK_COUNTRIES:
        reasons.append("UK-funded")
    for site in sorted(sites & UK_SYNCHROTRONS):
        reasons.append(f"Data collected at {site}")
    pid = e["rcsb_id"]
    entry = {
        "id": pid,
        "db": "PDB",
        "title": (e.get("struct") or {}).get("title", "").strip(),
        "method": label,
        "techniques": [tech],
        "released": (e.get("rcsb_accession_info") or {}).get("initial_release_date", "")[:10],
        "reasons": reasons,
        "url": f"https://www.ebi.ac.uk/pdbe/entry/pdb/{pid.lower()}",
        "image": f"images/latest/{pid.lower()}.jpeg",
    }
    if res:
        entry["resolution"] = round(float(res), 2)
    emdb = (e.get("rcsb_entry_container_identifiers") or {}).get("emdb_ids") or []
    if emdb:
        entry["emdb"] = emdb
    if cit.get("title"):
        entry["paper"] = {
            "title": cit.get("title", "").rstrip("."),
            "journal": cit.get("journal_abbrev") or "",
            "year": cit.get("year"),
            "doi": cit.get("pdbx_database_id_DOI") or "",
            "authors": short_authors(cit.get("rcsb_authors") or []),
        }
    return entry


# --------------------------------------------------------------- SASBDB

def sasbdb_new(since: dt.date, max_fetch: int) -> list[dict]:
    """Entries not seen before, measured in the UK and released since `since`.

    On the first run the list of existing codes is only recorded, so later
    runs report genuinely new entries without fetching thousands of records.
    """
    codes = [c["code"] for c in http_json(SASBDB_CODES) or [] if c.get("status") == "Published"]
    first_run = not SASBDB_SEEN.exists()
    seen = set(json.loads(SASBDB_SEEN.read_text())) if not first_run else set()
    new = [c for c in codes if c not in seen]
    out = []
    if not first_run:
        for code in new[:max_fetch]:
            try:
                d = http_json(SASBDB_SUMMARY.format(code=code))
            except Exception as e:  # one bad record should not stop the feed
                print(f"  SASBDB {code}: {e}", file=sys.stderr)
                continue
            inst = (d.get("experiment") or {}).get("instrument") or {}
            if (inst.get("country") or "") not in UK_COUNTRIES:
                continue
            project = d.get("project") or {}
            released = (project.get("released_date") or "")[:10]
            if released and released < since.isoformat():
                continue
            pub = project.get("publication") or {}
            molecules = [m.get("long_name") for m in (d.get("experiment") or {}).get("sample", {}).get("molecule", []) if m.get("long_name")]
            where = " ".join(x for x in [inst.get("name"), inst.get("beamline_name")] if x)
            entry = {
                "id": code,
                "db": "SASBDB",
                "title": "; ".join(molecules) or project.get("title", ""),
                "method": "Bio-SAXS",
                "techniques": ["saxs"],
                "released": released,
                "reasons": [f"Measured at {where}"] if where else ["Measured in the UK"],
                "url": f"https://www.sasbdb.org/data/{code}/",
            }
            if pub.get("title"):
                entry["paper"] = {"title": pub.get("title", "").rstrip("."), "journal": pub.get("journal") or "",
                                  "year": (pub.get("published_date") or "")[:4], "doi": pub.get("doi") or "",
                                  "authors": short_authors([a.strip() for a in (pub.get("author_list") or "").split(",") if a.strip()])}
            out.append(entry)
            time.sleep(0.2)  # be gentle with a small academic server
    SASBDB_SEEN.write_text(json.dumps(sorted(set(codes)), indent=0) + "\n")
    if first_run:
        print(f"SASBDB: first run, recorded {len(codes)} existing codes")
    return out


# ----------------------------------------------------------------- main

def update(days: int, keep_days: int, max_items: int) -> None:
    today = dt.date.today()
    since = today - dt.timedelta(days=days)
    feed = json.loads(FEED.read_text()) if FEED.exists() else {"entries": []}
    items = {e["id"]: e for e in feed.get("entries", [])}

    ids = pdb_search(since)
    print(f"PDB: {len(ids)} UK-linked entries released since {since}")
    for e in pdb_details(ids):
        items[e["id"]] = e

    try:
        for e in sasbdb_new(since, max_fetch=300):
            items[e["id"]] = e
    except Exception as e:  # keep the PDB part even if SASBDB is down
        print(f"SASBDB skipped: {e}", file=sys.stderr)

    cutoff = (today - dt.timedelta(days=keep_days)).isoformat()
    entries = sorted((e for e in items.values() if e.get("released", "") >= cutoff),
                     key=lambda e: (e.get("released", ""), e["id"]), reverse=True)[:max_items]
    FEED.write_text(json.dumps({"updated": today.isoformat(), "entries": entries}, indent=1, ensure_ascii=False) + "\n")
    print(f"Feed: {len(entries)} entries written to {FEED.relative_to(ROOT)}")


def download_images(dest: Path) -> None:
    """Fetch the RCSB image for each PDB entry in the feed (build time only, not committed)."""
    dest.mkdir(parents=True, exist_ok=True)
    feed = json.loads(FEED.read_text()) if FEED.exists() else {"entries": []}
    for e in feed["entries"]:
        if e.get("db") != "PDB":
            continue
        target = dest / f"{e['id'].lower()}.jpeg"
        if target.exists():
            continue
        try:
            req = urllib.request.Request(RCSB_IMAGE.format(id=e["id"].lower()), headers={"User-Agent": "bsg-website-feed"})
            with urllib.request.urlopen(req, timeout=60) as r:
                target.write_bytes(r.read())
        except Exception as err:
            print(f"  no image for {e['id']}: {err}", file=sys.stderr)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=8, help="look back this many days for new releases (default 8)")
    ap.add_argument("--keep-days", type=int, default=35, help="keep entries released within this many days (default 35)")
    ap.add_argument("--max", type=int, default=60, help="maximum entries in the feed (default 60)")
    ap.add_argument("--images", type=Path, help="download PDB images for the current feed into this folder and exit")
    args = ap.parse_args()
    if args.images:
        download_images(args.images)
    else:
        update(args.days, args.keep_days, args.max)
