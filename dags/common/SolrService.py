from enum import Enum
import json
import os
import sys
import requests

class Solr():

    def __init__(self, solr_url, user, password):
        self.solr_url = solr_url
        self.auth_user = user
        self.auth_passwd = password
        self.session = requests.Session()
        # self.session.auth = (self.auth_user, self.auth_passwd)
        # self.auth = self.session.post(self.solr_url)

        # if not self.auth_user or not len(self.auth_user) > 0:
        #     sys.exit("SOLR_USER not found in configuration. Exiting")

    def get(self, query):
        try:
            url = "{}?{}".format(self.solr_url, query)
            # print(url)
            # resp = self.session.get(url)
            resp = requests.get(url = url)
            # print("resp")
            # print(resp)
            return resp.json()
        except requests.exceptions.HTTPError as httpErr:
            print("Http Error:", httpErr)
        except requests.exceptions.ConnectionError as connErr:
            print("Error Connecting:", connErr)
        except requests.exceptions.Timeout as timeOutErr:
            print("Timeout Error:", timeOutErr)
        except requests.exceptions.RequestException as reqErr:
            print("Something Else:", reqErr)

    def post(self, query_params):
        try:
            resp = self.session.post(self.solr_url, data=query_params)
            return resp.json()
        except requests.exceptions.HTTPError as httpErr:
            print("Http Error:", httpErr)
        except requests.exceptions.ConnectionError as connErr:
            print("Error Connecting:", connErr)
        except requests.exceptions.Timeout as timeOutErr:
            print("Timeout Error:", timeOutErr)
        except requests.exceptions.RequestException as reqErr:
            print("Something Else:", reqErr)


if __name__ == '__main__':
    s = Solr('http://localhost:8983/solr/#/~java-properties', 'solr', 'SolrRocks')
    data = s.get('')
    print(data['response'])
    # data = s.post({'q': 'oil', 'rows': 0})
    # print(data['response'])
