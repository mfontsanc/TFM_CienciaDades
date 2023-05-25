from rdflib import Graph, URIRef, Literal

from config import constants


class TransformationCommunity2RDF:
    clinical_trials_relationship: list
    triples_relationship: list

    def __init__(self, clinical_trials_relationship: list):
        self.clinical_trials_relationship = clinical_trials_relationship
        self.triples_relationship = []

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
