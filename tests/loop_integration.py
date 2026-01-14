#!/usr/bin/env python3
"""
Simple integration script that exercises the manager API:

- POST /links/         -> create a new link
- POST /start-loop     -> start the continuous loop
- GET  /links/{id}/status -> poll until content+tags exist
- POST /stop-loop      -> stop the loop
- DELETE /links/{id}   -> remove the link (and related content/tags)

Usage:
  MANAGER_URL=http://localhost:8001 python3 manager/integration_script.py

Environment:
  MANAGER_URL - base URL of the manager service (default: http://localhost:8001)
"""
import os
import sys
import time
import uuid
import requests


MANAGER_URL = os.environ.get("MANAGER_URL", "http://localhost:8001").rstrip("/")
POLL_INTERVAL = 1.0
TIMEOUT = 60.0


def create_link(url: str):
    r = requests.post(f"{MANAGER_URL}/links/", json={"url": url})
    if r.status_code not in (200, 201):
        raise SystemExit(f"Failed to create link: {r.status_code} {r.text}")
    return r.json()


def start_loop():
    r = requests.post(f"{MANAGER_URL}/start-loop")
    if r.status_code != 200:
        raise SystemExit(f"Failed to start loop: {r.status_code} {r.text}")


def stop_loop():
    r = requests.post(f"{MANAGER_URL}/stop-loop")
    if r.status_code != 200:
        raise SystemExit(f"Failed to stop loop: {r.status_code} {r.text}")


def get_status(link_id: int):
    r = requests.get(f"{MANAGER_URL}/links/{link_id}/status")
    if r.status_code == 404:
        raise SystemExit("Link not found when checking status")
    if r.status_code != 200:
        raise SystemExit(f"Failed status check: {r.status_code} {r.text}")
    return r.json()


def delete_link(link_id: int):
    r = requests.delete(f"{MANAGER_URL}/links/{link_id}")
    if r.status_code not in (200, 204):
        raise SystemExit(f"Failed to delete link: {r.status_code} {r.text}")


def search_query(query: str):
    r = requests.post(f"{MANAGER_URL}/search", json={"query": query})
    if r.status_code != 200:
        raise SystemExit(f"Search failed: {r.status_code} {r.text}")
    return r.json()


def main():
    test_url = f"http://c5xoy22aadb2rqgw3jh2m2irmu563evukqqddu5zjandunaimzaye5id.onion"

    print(f"Creating link: {test_url}")
    link = create_link(test_url)
    link_id = link.get("id")
    if not link_id:
        raise SystemExit(f"Create response missing id: {link}")
    print(f"Created link id={link_id}")

    print("Starting loop...")
    start_loop()

    print(f"Polling status for link id={link_id} up to {TIMEOUT}s...")
    deadline = time.time() + TIMEOUT
    succeeded = False
    try:
        while time.time() < deadline:
            status = get_status(link_id)
            has_content = status.get("has_content", False)
            tags = status.get("tags", []) or []
            print(f"  status: has_content={has_content}, tags={tags}")
            if has_content and tags:
                # verify search returns our link for the first tag
                first_tag = tags[0]
                print(f"Found tags; searching for first tag: {first_tag}")
                results = search_query(first_tag)
                urls = [r.get("url") for r in results]
                if test_url in urls:
                    print("Search returned the crawled URL for tag '", first_tag, "'.")
                    succeeded = True
                    break
                else:
                    print("Search did not return the crawled URL yet; continuing to poll...")
            time.sleep(POLL_INTERVAL)
        if not succeeded:
            raise SystemExit("Timed out waiting for content/tags to appear")

    finally:
        print("Stopping loop...")
        stop_loop()

    print("Deleting link...")
    delete_link(link_id)

    print("Integration script completed: content and tags observed, link deleted successfully.")


if __name__ == "__main__":
    main()
