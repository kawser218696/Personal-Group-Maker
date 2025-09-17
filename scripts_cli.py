#!/usr/bin/env python3
"""
CLI for interacting with the HTTP API: list/add/delete sessions and bulk-create groups.
"""
import argparse
import os
import requests
import sys
import csv

DEFAULT_BASE = os.getenv("TG_API_BASE", "http://localhost:8000")
API_KEY = os.getenv("API_KEY")

def api_headers(key):
    return {"X-API-KEY": key, "Content-Type": "application/json"}

def list_sessions(base, key):
    r = requests.get(base + "/api/sessions", headers=api_headers(key))
    print(r.status_code, r.text)

def add_session(base, key, name, string_session):
    r = requests.post(base + "/api/sessions", headers=api_headers(key), json={"name": name, "string_session": string_session})
    print(r.status_code, r.text)

def delete_session(base, key, name):
    r = requests.delete(base + f"/api/sessions/{name}", headers=api_headers(key))
    print(r.status_code, r.text)

def create_group(base, key, session_name, title, about=None):
    payload = {"session_name": session_name, "title": title}
    if about is not None:
        payload["about"] = about
    r = requests.post(base + "/api/create_supergroup", headers=api_headers(key), json=payload)
    print(r.status_code, r.text)

def bulk_create_from_file(base, key, session_name, file_path):
    titles = []
    if file_path == "-":
        titles = [line.strip() for line in sys.stdin if line.strip()]
    else:
        with open(file_path, newline='') as f:
            for row in csv.reader(f):
                if len(row) == 0: continue
                titles.append(row[0].strip())
    for t in titles:
        print("Creating:", t)
        create_group(base, key, session_name, t)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default=DEFAULT_BASE, help="Base URL of server, e.g. http://localhost:8000")
    parser.add_argument("--api-key", default=API_KEY, help="API key (or set API_KEY env var)")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list-sessions")
    p = sub.add_parser("add-session")
    p.add_argument("name")
    p.add_argument("string_session")
    p = sub.add_parser("del-session")
    p.add_argument("name")
    p = sub.add_parser("create-group")
    p.add_argument("session_name")
    p.add_argument("title")
    p.add_argument("--about", default=None)
    p = sub.add_parser("bulk-create")
    p.add_argument("session_name")
    p.add_argument("file", help="Path to file with titles (first column) or - for stdin")

    args = parser.parse_args()
    if not args.api_key:
        print("API key required. Set --api-key or API_KEY env var.")
        sys.exit(2)

    if args.cmd == "list-sessions":
        list_sessions(args.base, args.api_key)
    elif args.cmd == "add-session":
        add_session(args.base, args.api_key, args.name, args.string_session)
    elif args.cmd == "del-session":
        delete_session(args.base, args.api_key, args.name)
    elif args.cmd == "create-group":
        create_group(args.base, args.api_key, args.session_name, args.title, args.about)
    elif args.cmd == "bulk-create":
        bulk_create_from_file(args.base, args.api_key, args.session_name, args.file)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()