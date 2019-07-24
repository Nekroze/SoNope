#!/usr/bin/env python
"""Sonope

Bringing sanity to the workplace sonos.
Given a CSV of Artist, Album, and Title headings any matches for non empty fields to the currently playing song is instantly skipped.

Usage: sonope [-hv] [-z SPEAKER_NAME | -i IP] [-b FILE]

Options:
  -h --help       Show this screen.
  -v --version    Show version.
  -b FILE         Path to a blacklist csv [default: ./blacklist.csv]
  -z NAME         Specify the sonos zone to use to when multiple are discovered
  -i IP           IP Address of sonos zone to control, disables discovery
"""

import sys
import time
import csv
from soco import SoCo, discovery
from docopt import docopt


def Main():
    arguments = docopt(__doc__, version='Sonope 0.1.0')

    target = get_target(arguments['-i'], arguments['-z'])
    if target is None:
        print("Did not connect to a Sonos Zone!")
        print("Try specifying the IP address with -i")
        sys.exit(1)

    blacklist = load_blacklist(arguments['-b'])

    lastTrack = {'title':''} # Seed the last track with something that never matches
    startTime = time.time()
    while True:
        track = target.get_current_track_info()
        if track['title'] != lastTrack['title']:
            print("Now playing: {},{},{}".format(track['artist'], track['album'], track['title']))
            maybe_skip_track(target, blacklist, track)
            lastTrack = track
        time.sleep(1 - ((time.time() - startTime) % 1.0))

def maybe_skip_track(target, blacklist, track):
    if track_is_blacklisted(blacklist, track):
        print("Skipping {}!".format(track['title']))
        if target.group is not None:
            target.group.coordinator.next()
        else:
            target.next()

def get_target(ip = None, zone = None):
    if ip is not None:
        return SoCo(ip)
    elif zone is not None:
        return discovery.by_name(arguments['-z'])
    else:
        return discovery.any_soco()

def load_blacklist(path):
    blacklist = []
    with open(path, 'r') as f:
        for row in csv.DictReader(f):
            blacklist.append(row)
    return blacklist

def track_is_blacklisted(blacklist, track):
    for item in blacklist:
        if blacklistItemMatchesTrack(item, track):
            return True
    return False

def blacklistItemMatchesTrack(item, track):
    mismatched = False
    if item['Title']:
        if track['title'].lower() != item['Title'].lower():
            mismatched = True
    if item['Album']:
        if track['album'].lower() != item['Album'].lower():
            mismatched = True
    if item['Artist']:
        if track['artist'].lower() != item['Artist'].lower():
            mismatched = True
    return not mismatched


if __name__ == '__main__':
    Main()
