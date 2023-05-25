# -*- coding: utf-8 -*-
import unittest
from config import constants_test, messages
from tfm.data_type.ct_study_type import StudyType
from tfm.xml2rdf.transformation_rdf import TransformationRDF
from tfm.xml2rdf.transformation_xml2rdf import TransformationXML2RDF
from utils.utils import Utils
from utils.database_manager import DatabaseManager


class TestXML2RDF(unittest.TestCase):

    def test_transform_xml(self):
        """
        Given a XML,

        """
        transf = TransformationXML2RDF(folder_path=constants_test.CURRENT_PATH)
        status, message = transf.start_process()

        self.assertTrue(status)
        self.assertEqual(len(transf.clinical_trials), 1)

        TransformationRDF.transformation_rdf(transf.clinical_trials[0])

    def test_insert_database(self):
        vm = DatabaseManager()
        result = vm.run_insert_rdf(constants_test.TTL_PATH)

        self.assertTrue(result)

    def test_ping_database(self):
        vm = DatabaseManager()
        result = vm.ping()

    def test_ontology_insert(self):
        vm = DatabaseManager()
        vm.insert_ontology_rdf()


