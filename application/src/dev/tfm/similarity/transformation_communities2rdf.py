import os

import pandas as pd
from rdflib import Graph, URIRef, Literal

from config import constants


class TransformationCommunity2RDF:
    clinical_trials_relationship: list
    triples_relationship: list
    clinical_trials_data: pd.DataFrame

    def __init__(self, clinical_trials_relationship: list):
        self.clinical_trials_relationship = clinical_trials_relationship
        self.triples_relationship = []
        path = os.path.join("../../../results", constants.TSV_FILE)
        print(os.path.abspath(path))
        self.clinical_trials_data = pd.read_csv(path, sep='\t', header=0)

    def generate_triples(self):
        """ Method to generate the triples with the community relationships.

            Parameters:

            Returns:
                list: List with all triples to be inserted in the database.
        """
        community_id = 1
        for community in self.clinical_trials_relationship:
            self.__generate_triples_by_community__(community, community_id)

            community_id += 1

        return self.triples_relationship

    def __get_community_name__(self, community: list, community_id: int):
        """
            Method to get the community name.

            Parameters:
                community (list): List of clinical trials identifier of a specific community.
                community_id (int): Identifier of the community.

            Returns:
                str: Name of the community
        """
        community_name = ""
        for ct in community:
            ct = "ClinicalTrial::" + ct
            data = self.clinical_trials_data[self.clinical_trials_data['target'] == ct]

            sources_times = {}
            sources_weight = {}
            total = len(community)

            for source in data['source']:
                if not sources_times.get(source):
                    sources_times[source] = 0
                    sources_weight[source] = 0

                sources_times[source] += 1
                if len(data[data['source'] == source]) > 1:
                    sources_weight[source] += float(data[data['source'] == source][:1]['weight'])
                else:
                    sources_weight[source] += float(data[data['source'] == source]['weight'])

        list_sources_times = sorted(sources_times.items(), key=lambda x: x[1], reverse=True)
        list_sources_weight = sorted(sources_weight.items(), key=lambda x: x[1], reverse=True)

        i = 0
        name = ""

        max_weight = list_sources_times[0][1]
        name_done = False
        for sw in list_sources_weight:
            if sources_times[sw[0]] / max_weight >= 0.6:
                name = sw[0] if i == 0 else name + " - " + sw[0]

                i += 1

            if i == 3:
                community_name = str(community_id) + ": " + name
                name_done = True
                break

        i = 0
        if not name_done:
            for sw in list_sources_weight[0:3]:
                name = sw[0] if i == 0 else name + " - " + sw[0]
                i += 1

            if i == 3 or i == len(list_sources_weight[0:3]):
                community_name = str(community_id) + ": " + name

        return community_name

    def __generate_triples_by_community__(self, community: list, community_id: int):
        """ Method to generate the triples of a specific community

            Parameters:
                community (list): List of clinical trials identifier of a specific community.
                community_id (int): Identifier of the community.

            Returns:
                list: List with all triples to be inserted in the database.
        """
        # Namespaces
        tfm_namespace = constants.TFM_NAMESPACE
        ocre = constants.OCRE_NAMESPACE

        for clinical_trial_id in community:
            graph = Graph()
            graph.bind("tfm", tfm_namespace)

            study = URIRef(ocre + clinical_trial_id)
            graph.add((study, URIRef(tfm_namespace+"community_id"), Literal(community_id)))

            for clinical_trial_id_relationship in community:
                if clinical_trial_id != clinical_trial_id_relationship:
                    study_relationship = URIRef(ocre + clinical_trial_id_relationship)
                    graph.add((study, URIRef(tfm_namespace+"community_relationship"), study_relationship))

            serialized_triples = graph.serialize()
            serialized_triples = serialized_triples.replace('@prefix tfm: <http://purl.org/net/TFM/communities#> .\n',
                                                            '')
            serialized_triples = serialized_triples.replace('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n',
                                                            '')

            self.triples_relationship.append(serialized_triples)

        community_name = self.__get_community_name__(community, community_id)
        graph = Graph()
        graph.bind("tfm", tfm_namespace)

        comm = URIRef(tfm_namespace + str(community_id))
        graph.add((comm, URIRef(tfm_namespace+"community_name"), Literal(community_name)))

        serialized_triples = graph.serialize()
        serialized_triples = serialized_triples.replace('@prefix tfm: <http://purl.org/net/TFM/communities#> .\n',
                                                        '')
        serialized_triples = serialized_triples.replace('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n',
                                                        '')
        self.triples_relationship.append(serialized_triples)
