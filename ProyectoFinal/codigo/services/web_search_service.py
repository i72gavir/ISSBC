# -*- coding: utf-8 -*-

from ddgs import DDGS


class WebSearchService:

    def search(self, query, max_results=5):

        results = []

        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                if r.get("href"):
                    results.append(r["href"])

        return results
