#!/usr/bin/env python

import aur.exceptions
import aur.package
import json
import sys

try:
    from http.client import HTTPSConnection
    from urllib.parse import urlencode
except ImportError:
    from httplib import HTTPSConnection
    from urllib import urlencode


class AURClient(object):
    """Handles client requests to AUR."""
    def __init__(self, host="aur.archlinux.org", apiPath="/rpc.php"):
        self.host = host
        self.apiPath = apiPath
        self.c = self._connect()

    def _connect(self):
        """Initialise connection to AUR."""
        return HTTPSConnection(self.host)

    def _generic_search(self, query, query_type, multi=False):
        results = self.query(query, query_type, multi)
        return self.parse_search(results, query_type)

    def search(self, package):
        """Perform a search on the live AUR API."""
        return self._generic_search(package, "search")

    def msearch(self, user):
        """Perform a maintainer package search on the live AUR API."""
        return self._generic_search(user, "msearch")

    def info(self, package):
        results = self.query(package, "info")
        return self.parse_info(results)

    def multiinfo(self, packages):
        return self._generic_search(packages, "multiinfo", multi=True)

    def query(self, query, query_type, multi=False):
        """Perform a single query on the API."""
        query_key = "arg"
        if multi:
            query_key += "[]"

        self.c.request(
            "GET",
            self.apiPath + "?" + urlencode({
                "type": query_type,
                query_key: query
            }, doseq=True)
        )
        res = self.c.getresponse()
        return json.loads(res.read().decode("utf8"))

    def parse_search(self, res, query_type):
        """Parse the results of a package search."""
        if res["type"] == "error":
            if res["results"] == "Query arg too small":
                raise aur.exceptions.QueryTooShortError
            else:
                raise aur.exceptions.UnknownAURError(res["results"])
        elif res["type"] != query_type:
            raise aur.exceptions.UnexpectedResponseTypeError(res["type"])

        for result in res["results"]:
            yield aur.package.Package(**result)

    def parse_info(self, res):
        """Parse the results of a package search."""
        if res["type"] == "error":
            raise aur.exceptions.UnknownAURError(res["results"])
        elif res["type"] != "info":
            raise aur.exceptions.UnexpectedResponseTypeError(res["type"])

        if not res["results"]:
            raise aur.exceptions.UnknownPackageError

        return aur.package.Package(**res["results"])
