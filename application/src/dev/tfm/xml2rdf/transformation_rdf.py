import os

from config import constants, messages
from tfm.data_type.clinical_trial_structure import ClinicalTrialStructure
from rdflib import Graph, URIRef, RDF, Literal, XSD

from tfm.data_type.ct_phases import PhasesType
from tfm.data_type.ct_recruiting_status import RecruitingStatus
from tfm.data_type.ct_study_type import StudyType
from tfm.validate.file_manager import FileManager
from tfm.xml2rdf import logger
from utils.utils import Utils


class TransformationRDF:
    ocre_namespace = constants.OCRE_NAMESPACE
    ocre_protocol_ns = constants.OCRE_PROTOCOL_NAMESPACE
    ocre_design_ns = constants.OCRE_DESIGN_NAMESPACE

    @staticmethod
    def process_to_rdf(clinical_trial: ClinicalTrialStructure, result_path: str):
        """
            Method to execute the transformation process to RDF and manage the possible errors and outputs.

            Parameters:
                clinical_trial (ClinicalTrialStructure): ClinicalTrialStructure object.
                result_path (str): Path to save the RDF file with the output result.

            Returns:
                bool: Whether the process has ended successfully or not.
                str: Message with the status of the process.
        """
        try:
            result_path = result_path + constants.RDF_FOLDER
            FileManager.create_folder(result_path)
            TransformationRDF.transformation_rdf(clinical_trial, result_path)
        except Exception as ex:
            message = clinical_trial.identifier + ": " + messages.MESSAGE_TRANSFORMATION_KO + ": " + ex.__str__()
            logger.error(message)
            return False, message

        if clinical_trial.filename:
            return True, messages.MESSAGE_TRANSFORMATION_OK
        else:
            return False, messages.MESSAGE_TRANSFORMATION_KO

    @staticmethod
    def transformation_rdf(clinical_trial: ClinicalTrialStructure, result_path: str):
        """
            Method to generate the RDF using the OCRe structure

            Parameters:
                clinical_trial (ClinicalTrialStructure): ClinicalTrialStructure object.
                result_path (str): Path to save the RDF file with the output result.

            Returns:
                None
        """
        # Namespaces
        ocre = TransformationRDF.ocre_namespace
        ocre_protocol = TransformationRDF.ocre_protocol_ns
        ocre_design = TransformationRDF.ocre_design_ns

        graph = Graph()
        graph.bind("ocre", ocre)
        graph.bind("study_protocol", ocre_protocol)
        graph.bind("study_design", ocre_design)

        # STUDY
        study = URIRef(ocre + clinical_trial.identifier)
        TransformationRDF.rdf_study_data_properties(clinical_trial, graph, study)

        # Identifier
        identifier = URIRef(ocre + "id_" + clinical_trial.identifier)
        graph.add((study, URIRef(ocre+"OCRE901005"), identifier))               # Study :hasIdentifier Identifier
        graph.add((identifier, RDF.type, URIRef(ocre+"OCRE400001")))            # Identifier a Identifier
        graph.add((identifier, URIRef(ocre+"OCRE900242"), Literal(clinical_trial.identifier)))  # ID :instanceID Literal

        # Recruitment status
        TransformationRDF.rdf_recruitment_status(clinical_trial, graph, study)

        # Results
        TransformationRDF.rdf_outcome(clinical_trial, graph, study)

        # Contact person
        TransformationRDF.rdf_contact_person(clinical_trial, graph, study)

        # Location
        TransformationRDF.rdf_location(clinical_trial, graph, study)

        # Sponsoring
        TransformationRDF.xml_sponsoring(clinical_trial, graph, study)

        # STUDY PROTOCOL
        study_protocol = URIRef(ocre_protocol + clinical_trial.identifier)
        graph.add((study, URIRef(ocre+"OCRE900089"), study_protocol))
        # Intervention
        TransformationRDF.rdf_intervention(clinical_trial, graph, study_protocol)
        # Eligibility criteria
        TransformationRDF.rdf_eligibility_criteria(clinical_trial, graph, study_protocol)

        # STUDY DESIGN
        study_design = URIRef(ocre_design + clinical_trial.identifier)
        graph.add((study, URIRef(ocre+"OCRE820850"), study_design))
        TransformationRDF.xml_study_design(clinical_trial, graph, study_design)
        # Phase
        TransformationRDF.xml_phase(clinical_trial, graph, study_design)

        # Save into RDF file
        filename = os.path.join(result_path, clinical_trial.identifier + ".ttl")
        graph.serialize(destination=filename)
        clinical_trial.filename = filename

    @staticmethod
    def rdf_study_data_properties(clinical_trial: ClinicalTrialStructure, graph: Graph, study: URIRef):
        """
            Method to generate the RDF using the OCRe structure related to Study data properties.

            Parameters:
                clinical_trial (ClinicalTrialStructure): ClinicalTrialStructure object.
                graph (Graph): Graph object to save the data.
                study (URIRef): URI of the subject.

            Returns:
                None
        """
        ocre = TransformationRDF.ocre_namespace

        # Study data properties
        graph.add((study, RDF.type, URIRef(ocre+"OCRE400029")))                 # rdf:type
        graph.add((study, URIRef(ocre+"OCRE900213"), Literal(clinical_trial.official_title))) \
            if clinical_trial.official_title is not None else None              # hasScientificTitle
        graph.add((study, URIRef(ocre+"OCRE900212"), Literal(clinical_trial.brief_title))) \
            if clinical_trial.brief_title is not None else None                 # hasPublicTitle
        graph.add((study, URIRef(ocre + "OCRE413000"), Literal(clinical_trial.summary))) \
            if clinical_trial.summary is not None else None                     # hasScientificDescription
        graph.add((study, URIRef(ocre + "OCRE189000"), Literal(clinical_trial.brief_summary))) \
            if clinical_trial.brief_summary is not None else None               # hasPublicDescription
        for keyword in clinical_trial.keywords:                                 # hasName (keywords)
            graph.add((study, URIRef(ocre + "OCRE900224"), Literal(keyword)))
        for keyword in clinical_trial.keywords_low:                             # hasName (keywords)
            graph.add((study, URIRef(ocre + "OCRE900224"), Literal(keyword)))
        for keyword in clinical_trial.keywords_intervention:                    # hasName (keywords)
            graph.add((study, URIRef(ocre + "OCRE900224"), Literal(keyword)))
        for keyword in clinical_trial.keywords_intervention_low:                # hasName (keywords)
            graph.add((study, URIRef(ocre + "OCRE900224"), Literal(keyword)))

        for obj in clinical_trial.objective:
            graph.add((study, URIRef(ocre + "OCRE058000"), Literal(obj)))       # hasStudyObjective

        graph.add((study, URIRef(ocre + "OCRE900210"), Literal(clinical_trial.start_date, datatype=XSD.date))) \
            if clinical_trial.start_date is not None else None                  # hasDateOfFirstEnrollment
        graph.add((study, URIRef(ocre + "OCRE900211"), Literal(clinical_trial.end_date, datatype=XSD.date))) \
            if clinical_trial.end_date is not None else None                    # hasDateOfLastEnrollment
        graph.add((study, URIRef(ocre + "OCRE900214"), Literal(clinical_trial.primary_end_date, datatype=XSD.date))) \
            if clinical_trial.primary_end_date is not None else None            # hasDescriptionDate
        graph.add((study, URIRef(ocre + "OCRE900237"), Literal(clinical_trial.number_participants, datatype=XSD.int))) \
            if clinical_trial.number_participants is not None else None         # hasStudyPopulationNumber

    @staticmethod
    def rdf_recruitment_status(clinical_trial: ClinicalTrialStructure, graph: Graph, study: URIRef):
        """
            Method to generate the RDF using the OCRe structure related to Recruitment status.

            Parameters:
                clinical_trial (ClinicalTrialStructure): ClinicalTrialStructure object.
                graph (Graph): Graph object to save the data.
                study (URIRef): URI of the subject.

            Returns:
                None
        """
        ocre = TransformationRDF.ocre_namespace

        # Recruitment status
        if clinical_trial.recruiting_status:
            recruitment = URIRef(ocre + "rs_" + clinical_trial.identifier)
            graph.add((study, URIRef(ocre+"OCRE901007"), recruitment))               # Study :hasRecruitmentStatus
            graph.add((recruitment, RDF.type, URIRef(ocre+"OCRE400003")))            # RecruitmentStatus

            if clinical_trial.recruiting_status in (RecruitingStatus.RECRUITING,
                                                    RecruitingStatus.ENROLLING_BY_INVITATION):
                graph.add((recruitment, RDF.type, URIRef(ocre+"OCRE400016")))
            if clinical_trial.recruiting_status is RecruitingStatus.NOT_YET_RECRUITING:
                graph.add((recruitment, RDF.type, URIRef(ocre+"OCRE400073")))
            if clinical_trial.recruiting_status in (RecruitingStatus.COMPLETED, RecruitingStatus.ACTIVE_NOT_RECRUITING):
                graph.add((recruitment, RDF.type, URIRef(ocre+"OCRE400030")))
            if clinical_trial.recruiting_status is RecruitingStatus.SUSPENDED:
                graph.add((recruitment, RDF.type, URIRef(ocre+"OCRE400075")))
            if clinical_trial.recruiting_status is RecruitingStatus.TERMINATED:
                graph.add((recruitment, RDF.type, URIRef(ocre+"OCRE400068")))
            if clinical_trial.recruiting_status is RecruitingStatus.WITHDRAWN:
                graph.add((recruitment, RDF.type, URIRef(ocre+"OCRE261000")))

            graph.add((recruitment, URIRef(ocre + "OCRE900224"),
                       Literal(RecruitingStatus(clinical_trial.recruiting_status).name)))

    @staticmethod
    def rdf_outcome(clinical_trial: ClinicalTrialStructure, graph: Graph, study: URIRef):
        """
            Method to generate the RDF using the OCRe structure related to Recruitment status.

            Parameters:
                clinical_trial (ClinicalTrialStructure): ClinicalTrialStructure object.
                graph (Graph): Graph object to save the data.
                study (URIRef): URI of the subject.

            Returns:
                None
        """
        ocre = TransformationRDF.ocre_namespace
        ocre_design = TransformationRDF.ocre_design_ns

        # Outcomes
        out_len = 1
        for outcome in clinical_trial.outcomes:
            outcome_uri = URIRef(ocre_design + str(out_len) + "out_" + clinical_trial.identifier)
            graph.add((study, URIRef(ocre+"OCRE738000"), outcome_uri))
            graph.add((outcome_uri, URIRef(ocre+"OCRE900224"), Literal(outcome.name))) \
                if outcome.name is not None else None                                         # hasName
            graph.add((outcome_uri, URIRef(ocre+"OCRE900214"), Literal(outcome.description))) \
                if outcome.description is not None else None                                  # hasDescription
            graph.add((outcome_uri, URIRef(ocre+"OCRE000021"), Literal(outcome.time))) \
                if outcome.time is not None else None                                         # hasTimePointExtractor
            out_len += 1

    @staticmethod
    def rdf_contact_person(clinical_trial: ClinicalTrialStructure, graph: Graph, study: URIRef):
        """
            Method to generate the RDF using the OCRe structure related to Contact person

            Parameters:
                clinical_trial (ClinicalTrialStructure): ClinicalTrialStructure object.
                graph (Graph): Graph object to save the data.
                study (URIRef): URI of the subject.

            Returns:
                None
        """
        ocre = TransformationRDF.ocre_namespace

        # Contact person
        cp_len = 1
        for cp in clinical_trial.contact_persons:
            cp_uri = URIRef(ocre + str(cp_len) + "cp_" + clinical_trial.identifier)
            graph.add((study, URIRef(ocre+"OCRE400076"), cp_uri))
            graph.add((cp_uri, URIRef(ocre+"OCRE900224"), Literal(cp.name))) \
                if cp.name is not None else None                                              # hasName
            cp_len += 1

    @staticmethod
    def rdf_location(clinical_trial: ClinicalTrialStructure, graph: Graph, study: URIRef):
        """
            Method to generate the RDF using the OCRe structure related to Locations

            Parameters:
                clinical_trial (ClinicalTrialStructure): ClinicalTrialStructure object.
                graph (Graph): Graph object to save the data.
                study (URIRef): URI of the subject.

            Returns:
                None
        """
        ocre = TransformationRDF.ocre_namespace

        pi_len = 1
        relation_org_inv = {}
        for org in clinical_trial.locations:
            org_uri = URIRef(ocre + str(pi_len) + "org_" + clinical_trial.identifier)
            pi_len += 1

            graph.add((study, URIRef(ocre+"OCRE400076"), org_uri))
            graph.add((org_uri, URIRef(ocre+"OCRE744000"), Literal(org.country)))           # hasCountry
            graph.add((org_uri, URIRef(ocre+"OCRE885000"), Literal(org.postcode)))          # hasZip
            graph.add((org_uri, URIRef(ocre+"OCRE400040"), Literal(org.city)))              # hasAddress
            graph.add((org_uri, URIRef(ocre+"OCRE900224"), Literal(org.facility))) \
                if org.facility is not None else None

            cp_len = 1
            for member in org.collaborators:
                cp_uri = URIRef(ocre + str(cp_len) + "col_" + clinical_trial.identifier)
                graph.add((org_uri, URIRef(ocre+"OCRE900057"), cp_uri))                     # hasMember
                graph.add((cp_uri, URIRef(ocre+"OCRE900064"), org_uri))                     # isMemberOf
                graph.add((cp_uri, URIRef(ocre+"OCRE900224"), Literal(member.name))) \
                    if member.name is not None else None                                    # hasName
                graph.add((cp_uri, URIRef(ocre+"OCRE900212"), Literal(member.role))) \
                    if member.role is not None else None                                    # hasPublicTitle
                cp_len += 1

            if not relation_org_inv.get(org.facility):
                relation_org_inv[org.facility] = []
            relation_org_inv[org.facility].append(org_uri)

        pi_len = 1
        relation_loc_inv = {}
        for pi in clinical_trial.principal_investigator:
            pi_uri = URIRef(ocre + str(pi_len) + "cp_" + clinical_trial.identifier)
            graph.add((study, URIRef(ocre+"OCRE901006"), pi_uri))                            # hasPrincipalInvestigator
            graph.add((pi_uri, URIRef(ocre+"OCRE900224"), Literal(pi.name))) \
                if pi.name is not None else None
            graph.add((pi_uri, URIRef(ocre+"OCRE900212"), Literal(pi.role))) \
                if pi.role is not None else None                                            # hasPublicTitle

            if relation_org_inv.get(pi.affiliation):
                for org_uri in relation_org_inv[pi.affiliation]:
                    graph.add((org_uri, URIRef(ocre+"OCRE900057"), pi_uri))                # hasMember
                graph.add((pi_uri, URIRef(ocre+"OCRE900064"), org_uri))                    # isMemberOf
            else:
                if not relation_loc_inv.get(pi.affiliation):
                    relation_loc_inv[pi.affiliation] = []
                relation_loc_inv[pi.affiliation].append(pi_uri)

            pi_len += 1

        locn = 0
        for loc in relation_loc_inv.keys():
            loc_uri = URIRef(ocre + str(locn) + "loc_" + clinical_trial.identifier)

            graph.add((loc_uri, URIRef(ocre+"OCRE900224"), Literal(loc)))              # hasName
            pi_uris = relation_loc_inv[loc]

            for pi_uri in pi_uris:
                graph.add((loc_uri, URIRef(ocre+"OCRE900057"), pi_uri))                # hasMember
                graph.add((pi_uri, URIRef(ocre+"OCRE900064"), loc_uri))                # isMemberOf
            locn += 1

    @staticmethod
    def rdf_intervention(clinical_trial: ClinicalTrialStructure, graph: Graph, study_protocol: URIRef):
        """
            Method to generate the RDF using the OCRe structure related to interventions

            Parameters:
                clinical_trial (ClinicalTrialStructure): ClinicalTrialStructure object.
                graph (Graph): Graph object to save the data.
                study_protocol (URIRef): URI of the subject.

            Returns:
                None
        """
        ocre = TransformationRDF.ocre_namespace
        ocre_protocol = TransformationRDF.ocre_protocol_ns

        # Study protocol / Intervention study protocol
        graph.add((study_protocol, RDF.type, URIRef(ocre_protocol+"OCRE300012")))
        graph.add((study_protocol, RDF.type, URIRef(ocre_protocol+"OCRE892807")))

        for condition in clinical_trial.conditions:                             # hasHealthConditionStudied
            graph.add((study_protocol, URIRef(ocre + "OCRE900086"), Literal(condition)))

        # Epoch
        ep_len = 1
        for epoch in clinical_trial.interventions:
            epoch_uri = URIRef(ocre_protocol + str(ep_len) + "ep_" + clinical_trial.identifier)
            graph.add((study_protocol, URIRef(ocre_protocol+"OCRE885707"), epoch_uri))
            graph.add((epoch_uri, RDF.type, URIRef(ocre_protocol+"OCRE300000")))

            for names in epoch.name:
                graph.add((epoch_uri, URIRef(ocre+"OCRE900224"), Literal(names)))           # hasName

            graph.add((epoch_uri, URIRef(ocre+"OCRE900214"), Literal(epoch.description))) \
                if epoch.description is not None else None                                  # hasDescription
            graph.add((epoch_uri, URIRef(ocre+"OCRE900218"), Literal(epoch.type.name))) \
                if epoch.type is not None else None                                         # conceptDescriptorProperty
            ep_len += 1

    @staticmethod
    def rdf_eligibility_criteria(clinical_trial: ClinicalTrialStructure, graph: Graph, study_protocol: URIRef):
        """
            Method to generate the RDF using the OCRe structure related to eligibility criteria

            Parameters:
                clinical_trial (ClinicalTrialStructure): ClinicalTrialStructure object.
                graph (Graph): Graph object to save the data.
                study_protocol (URIRef): URI of the subject.

            Returns:
                None
        """
        ocre = TransformationRDF.ocre_namespace

        # Eligibility criteria
        if clinical_trial.eligibility_criteria and clinical_trial.eligibility_criteria is not None:
            value_uri = URIRef(ocre + "ec_d_" + clinical_trial.identifier)
            graph.add((study_protocol, URIRef(ocre+"OCRE693433"), value_uri))
            graph.add((value_uri, URIRef(ocre+"OCRE900214"),
                       Literal(clinical_trial.eligibility_criteria)))                       # hasDescription
        if clinical_trial.gender and clinical_trial.gender is not None:
            value_uri = URIRef(ocre + "ec_g_" + clinical_trial.identifier)
            graph.add((study_protocol, URIRef(ocre+"OCRE693433"), value_uri))
            graph.add((value_uri, URIRef(ocre+"OCRE900214"), Literal(clinical_trial.gender.name)))   # hasDescription
        if clinical_trial.minimum_age and clinical_trial.minimum_age is not None:
            value_uri = URIRef(ocre + "ec_mi_" + clinical_trial.identifier)
            graph.add((study_protocol, URIRef(ocre+"OCRE693433"), value_uri))
            graph.add((value_uri, URIRef(ocre+"OCRE900224"), Literal("Minimum age")))   # hasName
            graph.add((value_uri, URIRef(ocre+"OCRE900214"),
                       Literal(clinical_trial.minimum_age)))   # hasDescription
        if clinical_trial.maximum_age and clinical_trial.maximum_age is not None:
            value_uri = URIRef(ocre + "ec_ma_" + clinical_trial.identifier)
            graph.add((study_protocol, URIRef(ocre+"OCRE693433"), value_uri))
            graph.add((value_uri, URIRef(ocre+"OCRE900224"), Literal("Maximum age")))   # hasName
            graph.add((value_uri, URIRef(ocre+"OCRE900214"),
                       Literal(clinical_trial.maximum_age)))                            # hasDescription

    @staticmethod
    def xml_study_design(clinical_trial: ClinicalTrialStructure, graph: Graph, study_design: URIRef):
        """
            Method to generate the RDF using the OCRe structure related to study design

            Parameters:
                clinical_trial (ClinicalTrialStructure): ClinicalTrialStructure object.
                graph (Graph): Graph object to save the data.
                study_design (URIRef): URI of the subject.

            Returns:
                None
        """
        ocre_design = TransformationRDF.ocre_design_ns

        graph.add((study_design, RDF.type, URIRef(ocre_design+"OCRE100056")))

        if clinical_trial.study_type is StudyType.INTERVENTIONAL:
            graph.add((study_design, RDF.type, URIRef(ocre_design+"OCRE100007")))
        if clinical_trial.study_type is StudyType.OBSERVATIONAL:
            graph.add((study_design, RDF.type, URIRef(ocre_design+"OCRE100055")))

    @staticmethod
    def xml_phase(clinical_trial: ClinicalTrialStructure, graph: Graph, study_design: URIRef):
        """
            Method to generate the RDF using the OCRe structure related to Phase

            Parameters:
                clinical_trial (ClinicalTrialStructure): ClinicalTrialStructure object.
                graph (Graph): Graph object to save the data.
                study_design (URIRef): URI of the subject.

            Returns:
                None
        """
        ocre = TransformationRDF.ocre_namespace
        ocre_design = TransformationRDF.ocre_design_ns

        # Study design - Phase
        if len(clinical_trial.phases) > 0:
            phase = URIRef(ocre_design + "phase_" + clinical_trial.identifier)
            graph.add((study_design, URIRef(ocre+"OCRE741000"), phase))
            graph.add((phase, RDF.type, URIRef(ocre_design+"OCRE100038")))

            for phase_name in clinical_trial.phases:
                if phase_name is PhasesType.NOT_APPLICABLE:
                    graph.add((phase, RDF.type, URIRef(ocre_design+"OCRE100016")))
                else:
                    if phase_name is PhasesType.EARLY_PHASE_1:
                        graph.add((phase, RDF.type, URIRef(ocre_design+"OCRE100068")))
                    if phase_name is PhasesType.PHASE_1:
                        graph.add((phase, RDF.type, URIRef(ocre_design+"OCRE100067")))
                    if phase_name is PhasesType.PHASE_2:
                        graph.add((phase, RDF.type, URIRef(ocre_design+"OCRE100070")))
                    if phase_name is PhasesType.PHASE_3:
                        graph.add((phase, RDF.type, URIRef(ocre_design+"OCRE100069")))
                    if phase_name is PhasesType.PHASE_4:
                        graph.add((phase, RDF.type, URIRef(ocre_design+"OCRE100066")))

                graph.add((phase, URIRef(ocre + "OCRE900224"),
                           Literal(PhasesType(phase_name).name)))

    @staticmethod
    def xml_sponsoring(clinical_trial: ClinicalTrialStructure, graph: Graph, study: URIRef):
        """
            Method to generate the RDF using the OCRe structure related to Sponsoring data

            Parameters:
                clinical_trial (ClinicalTrialStructure): ClinicalTrialStructure object.
                graph (Graph): Graph object to save the data.
                study (URIRef): URI of the subject.

            Returns:
                None
        """
        ocre = TransformationRDF.ocre_namespace

        # Sponsoring
        sponsor = URIRef(ocre + "sp_" + clinical_trial.identifier)
        graph.add((study, URIRef(ocre+"OCRE535519"), sponsor))                  # Study hasSponsoringRelation
        graph.add((sponsor, URIRef(ocre+"OCRE547004"), study))                  # Sponsor isSponsoringRelationOf
        graph.add((sponsor, RDF.type, URIRef(ocre+"OCRE581634")))               # Sponsoring class
        graph.add((sponsor, URIRef(ocre+"OCRE900224"), Literal(clinical_trial.sponsor_name)))       # hasName
