"""This module provides the main functionality of cfbackup
"""
from __future__ import print_function
import sys
import argparse
import json

import CloudFlare

# https://api.cloudflare.com/#dns-records-for-a-zone-list-dns-records
class CF_DNS_Records(object):
    """
    commands for zones manipulation
    """
    def __init__(self, ctx):
        self._ctx = ctx

    def run(self):
        """
            run - entry point for DNS records manipulations
        """
        cmd = self._ctx.command
        if cmd == "show":
            self.show()
        else:
            sys.exit("Command " + cmd + " not implemened for zones")

    def show(self):
        """Show CF zones"""
        # print("Show DSN records")
        try:
            records = self._all_records()
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/zones %d %s - api call failed' % (e, e))
        if not self._ctx.pretty:
            print(json.dumps(records, indent=4))
            return

        records_by_type = {}
        types = {}
        for rec in records:
            if not records_by_type.get(rec["type"]):
                types[rec["type"]] = 0
                records_by_type[rec["type"]] = []
            types[rec["type"]] += 1
            records_by_type[rec["type"]].append(rec)

        for t in sorted(list(types)):
            for rec in records_by_type[t]:
                # print(json.dumps(rec, indent=4))
                print("Type:    {}".format(rec["type"]))
                print("Name:    {}".format(rec["name"]))
                print("Content: {}".format(rec["content"]))
                print("TTL:     {}{}".format(
                    rec["ttl"],
                    " (auto)" if str(rec["ttl"]) == "1" else "",
                    ))
                print("Proxied: {}".format(rec["proxied"]))
                print("Auto:    {}".format(rec["meta"]["auto_added"]))
                print("")

        print("")
        print("-------------------")
        print("Records stat:")
        print("-------------------")
        print("{0: <11} {1: >4}".format("<type>", "<count>"))
        for t in sorted(list(types)):
            print("{0: <11} {1: >4}".format(t, types[t]))
        print("-------------------")
        print("{0: <11} {1: >4}".format("Total:", len(records)))

    def _all_records(self):
        cf = CloudFlare.CloudFlare()
        zones = cf.zones.get(params={'name': self._ctx.zone_name, 'per_page': 1})
        if len(zones) == 0:
            exit('No zones found')

        zone_id = zones[0]['id']
        cf_raw = CloudFlare.CloudFlare(raw=True)
        page = 1
        records = []
        while True:
            raw_results = cf_raw.zones.dns_records.get(
                zone_id,
                params={'per_page':100, 'page':page},
            )
            total_pages = raw_results['result_info']['total_pages']
            result = raw_results['result']
            for rec in result:
                records.append(rec)

            if page == total_pages:
                break
            page += 1
        return records

# https://api.cloudflare.com/#zone-list-zones
class CF_Zones(object):
    """
    commands for zones manipulation
    """
    def __init__(self, ctx):
        self._ctx = ctx

    def run(self):
        """
            run - entry point for zones manipulations
        """
        cmd = self._ctx.command
        if cmd == "show":
            self.show()
        else:
            sys.exit("Command " + cmd + " not implemened for zones")

    def show(self):
        """Show CF zones"""
        # print("Show cf zones")
        try:
            zones = self._all_zones()
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/zones %d %s - api call failed' % (e, e))

        if not self._ctx.pretty:
            print(json.dumps(zones, indent=4))
            return

        for z in zones:
            print("Zone: {0: <16} NS: {1}".format(
                z["name"],
                z["name_servers"][0],
            ))
            for ns in z["name_servers"][1:]:
                print("      {0: <16}     {1}".format("", ns))

    def _all_zones(self):
        cf = CloudFlare.CloudFlare(raw=True)
        if self._ctx.zone_name:
            raw_results = cf.zones.get(params={
                'name': self._ctx.zone_name,
                'per_page': 1,
                'page': 1,
            })
            return raw_results['result']

        page = 1
        domains = []
        while True:
            raw_results = cf.zones.get(params={'per_page':5, 'page':page})
            total_pages = raw_results['result_info']['total_pages']
            zones = raw_results['result']

            for z in zones:
                domains.append(z)

            if page == total_pages:
                break
            page += 1
        return domains

COMMANDS = [
    "show",
    # "restore"
]
OBJECT_ENTRYPOINT = {
    "zones": CF_Zones,
    "dns": CF_DNS_Records,
}

def main():
    """Main entry"""
    parser = argparse.ArgumentParser(
        prog="cfbackup",
        description='Simple Cloudflare backup tool.',
    )
    parser.add_argument(
        "command",
        choices=[x for x in COMMANDS],
        help="command",
    )
    subparsers = parser.add_subparsers(
        help='Object of command',
        dest="object"
    )

    parser_zones = subparsers.add_parser("zones")
    parser_zones.add_argument(
        "--pretty",
        action='store_true',
        help="show user friendly output",
    )
    parser_zones.add_argument(
        "-z", "--zone-name",
        help="optional zone name",
    )

    parser_dns = subparsers.add_parser("dns")
    parser_dns.add_argument(
        "-z", "--zone-name",
        required=True,
        help="required zone name",
    )
    parser_dns.add_argument(
        "--pretty",
        action='store_true',
        help="show user friendly output",
    )
    args = parser.parse_args()
    OBJECT_ENTRYPOINT[args.object](args).run()
