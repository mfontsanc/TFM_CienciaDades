import os
from urllib.error import URLError

import requests
from SPARQLWrapper import SPARQLWrapper, JSON

from config import constants, sparql


class DatabaseManager:
    endpoint_url: str
    statements_url: str
    ontology_named_graph_url: str
    ontology_folder: str
    headers_ttl: dict
    headers_owl: dict

    def __init__(self):
        self.endpoint_url = constants.GRAPHDB_ENDPOINT
        self.statements_url = constants.GRAPHDB_STATEMENTS
        self.ontology_named_graph_url = constants.GRAPHDB_ONTOLOGY_NG
        self.ontology_folder = constants.ONTOLOGY_TTL_FOLDER
        self.headers_ttl = {
            'Content-Type': 'application/x-turtle',
            'Accept': 'application/json'
        }
        self.headers_owl = {
            'Content-Type': 'application/rdf+xml',
            'Accept': 'application/json'
        }

    def ping(self):
        """
            Method to execute a ping test to the database

            Parameters:

            Returns:
                bool: Whether the database is up and working or not.
        """
        sparql = SPARQLWrapper(self.endpoint_url)
        sparql.setQuery("""
            ASK  { ?s ?p ?o }
        """)
        sparql.method = 'GET'
        sparql.setReturnFormat(JSON)

        try:
            results = sparql.query().convert()

            return results["boolean"]
        except URLError:
            return False

    def insert_ontology_rdf(self):
        """
            Method to insert the ontology into the database

            Parameters:

            Returns:
                bool: Whether the RDF has been inserted correctly or not.
        """
        dir_list = os.listdir(self.ontology_folder)

        for file in dir_list:
            file_path = self.ontology_folder + "/" + file
            try:
                with open(file_path, 'r') as r_file:
                    r = requests.post(self.ontology_named_graph_url,
                                      data=r_file,
                                      headers=self.headers_owl)
            except Exception:
                return False
        return True

    def run_insert_rdf(self, filename):
        """
            Method to insert into GraphDB the RDF file.

            Parameters:
                filename (str): RDF file to be inserted.

            Returns:
                bool: Whether the RDF has been inserted correctly or not.
        """

        try:
            with open(filename, 'r', encoding="utf-8") as file:
                r = requests.post(self.statements_url,
                                  data=file,
                                  headers=self.headers_ttl)
            return r.ok
        except Exception as ex:
            return False

    def run_insert_triples(self, triples: list):
        """
            Method to insert into GraphDB the list of triples.

            Parameters:
                triples (list): List of triples

            Returns:
                bool: Whether the RDF has been inserted correctly or not.
                int: Number of processed triples.
        """
        sparqlwrapper = SPARQLWrapper(self.statements_url)
        processed = 0
        for triple in triples:
            insert_sparql = sparql.INSERT_DATA % triple

            sparqlwrapper.setQuery(insert_sparql)
            sparqlwrapper.method = 'POST'
            res = sparqlwrapper.query()
            if res.response.status == 204:
                processed += 1

        if processed == len(triples):
            return True, processed
        else:
            return False, processed

    def run_select_data(self, query: str):
        """
            Method to execute the select query to GraphDB.

            Parameters:
                query (str): SPARQL query to execute

            Returns:
                list: result of the executed query
        """
        sparqlwrapper = SPARQLWrapper(self.endpoint_url)
        sparqlwrapper.setQuery(query)
        sparqlwrapper.setReturnFormat(JSON)
        sparqlwrapper.method = 'GET'
        results = sparqlwrapper.query().convert()
        output_result = []

        return results["results"]["bindings"]
