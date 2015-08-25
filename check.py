#!/usr/bin/env python

import argparse
import csv
import json
import re
import requests


class Checker(object):
    def __init__(self):
        self.sess = requests.Session()
        self.sess.headers.update({
            'origin': 'https://ashley.cynic.al',
            'accept-encoding': 'gzip, deflate',
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://ashley.cynic.al/',
            'accept-language': 'en-US,en;q=0.8',
        })

        for result in self.check_emails(self.get_emails(self.get_args().file)):
           print result

    def get_emails(self, path):
        regex = re.compile("[^@]+@[^@]+\.[^@]+")
        emails = []
        with open(path, 'rb') as csvfile:
            reader = csv.reader((x.replace('\0', '') for x in csvfile), delimiter=',', quotechar='|', quoting=csv.QUOTE_ALL)
            return [m.group(0).strip('"') for m in [regex.match(addr) for addr in [email for row in reader for email in row]] if m]

    def check_emails(self, emails):
        results = []
        for email in emails:
            try:
                if json.loads(self.sess.post('https://ashley.cynic.al/check', data={'email': email}).text)['found']:
                    results.append(email)
            except:
                pass
        return results

    def get_args(self):
        ap = argparse.ArgumentParser(description='Checks .csv files containing email addresses against https://ashley.cynic.al.')
        ap.add_argument('file', type=str, help='Path to the .csv file to check.')
        return ap.parse_args()


if __name__ == "__main__":
    ch = Checker()