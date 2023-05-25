


XML_ROOT = "./Struct[@Name='Study']/Struct[@Name='ProtocolSection']/"
XML_ROOT_MESH = "./Struct[@Name='Study']/Struct[@Name='DerivedSection']/"

# -------------------------------------------- IDENTIFICATION -------------------------------------------------
IDENTIFIER = XML_ROOT + "Struct[@Name='IdentificationModule']/Field[@Name='NCTId']"

# -------------------------------------------- DESCRIPTION ----------------------------------------------------
BRIEF_TITLE = XML_ROOT + "Struct[@Name='IdentificationModule']/Field[@Name='BriefTitle']"
OFFICIAL_TITLE = XML_ROOT + "Struct[@Name='IdentificationModule']/Field[@Name='OfficialTitle']"
BRIEF_SUMMARY = XML_ROOT + "Struct[@Name='DescriptionModule']/Field[@Name='BriefSummary']"
SUMMARY = XML_ROOT + "Struct[@Name='DescriptionModule']/Field[@Name='DetailedDescription']"

CONDITIONS = XML_ROOT + "Struct[@Name='ConditionsModule']/List[@Name='ConditionList']/Field[@Name='Condition']"
KEYWORDS = XML_ROOT_MESH + "Struct[@Name='ConditionBrowseModule']/List[@Name='ConditionBrowseLeafList']" \
                           "/Struct[@Name='ConditionBrowseLeaf']/Field[@Name='ConditionBrowseLeafName']"
KEYWORDS_RELEVANCE = XML_ROOT_MESH + "Struct[@Name='ConditionBrowseModule']/List[@Name='ConditionBrowseLeafList']" \
                                     "/Struct[@Name='ConditionBrowseLeaf']/Field[@Name='ConditionBrowseLeafRelevance']"
KEYWORDS_INTERVENTION = XML_ROOT_MESH + "Struct[@Name='InterventionBrowseModule']/" \
                                        "List[@Name='InterventionBrowseLeafList']/" \
                                        "Struct[@Name='InterventionBrowseLeaf']/" \
                                        "Field[@Name='InterventionBrowseLeafName']"
KEYWORDS_INTERVENTION_RELEVANCE = XML_ROOT_MESH + "Struct[@Name='InterventionBrowseModule']/" \
                                                  "List[@Name='InterventionBrowseLeafList']/" \
                                                  "Struct[@Name='InterventionBrowseLeaf']/" \
                                                  "Field[@Name='InterventionBrowseLeafRelevance']"

STUDY_TYPE = XML_ROOT + "Struct[@Name='DesignModule']/Field[@Name='StudyType']"
STUDY_PHASE = XML_ROOT + "Struct[@Name='DesignModule']/List[@Name='PhaseList']/Field[@Name='Phase']"
OBJECTIVE = XML_ROOT + "Struct[@Name='DesignModule']/Struct[@Name='DesignInfo']/Field[@Name='DesignPrimaryPurpose']"

OBSERVATIONAL_MODE = XML_ROOT + "Struct[@Name='DesignModule']/Struct[@Name='DesignInfo']" \
                                "/List[@Name='DesignObservationalModelList']/Field[@Name='DesignObservationalModel']"

RECRUITING_STATUS = XML_ROOT + "Struct[@Name='StatusModule']/Field[@Name='OverallStatus']"
START_DATE = XML_ROOT + "Struct[@Name='StatusModule']/Struct[@Name='StartDateStruct']/Field[@Name='StartDate']"
END_DATE = XML_ROOT + "Struct[@Name='StatusModule']/Struct[@Name='CompletionDateStruct']/Field[@Name='CompletionDate']"
PRIMARY_END_DATE = XML_ROOT + "Struct[@Name='StatusModule']/Struct[@Name='PrimaryCompletionDateStruct']" \
                              "/Field[@Name='PrimaryCompletionDate']"

SPONSOR_NAME = XML_ROOT + "Struct[@Name='SponsorCollaboratorsModule']/Struct[@Name='LeadSponsor']" \
                          "/Field[@Name='LeadSponsorName']"
SPONSOR_CLASS = XML_ROOT + "Struct[@Name='SponsorCollaboratorsModule']/Struct[@Name='LeadSponsor']" \
                           "/Field[@Name='LeadSponsorClass']"
RESPONSIBLE_NAME = XML_ROOT + "Struct[@Name='SponsorCollaboratorsModule']/Struct[@Name='ResponsibleParty']" \
                              "/Field[@Name='ResponsiblePartyInvestigatorFullName']"
RESPONSIBLE_ORG = XML_ROOT + "Struct[@Name='SponsorCollaboratorsModule']/Struct[@Name='ResponsibleParty']" \
                             "/Field[@Name='ResponsiblePartyInvestigatorAffiliation']"
RESPONSIBLE_TYPE = XML_ROOT + "Struct[@Name='SponsorCollaboratorsModule']/Struct[@Name='ResponsibleParty']" \
                              "/Field[@Name='ResponsiblePartyType']"

NUM_PARTICIPANTS = XML_ROOT + "Struct[@Name='DesignModule']/Struct[@Name='EnrollmentInfo']" \
                              "/Field[@Name='EnrollmentCount']"
INTERVENTIONS = XML_ROOT + "Struct[@Name='ArmsInterventionsModule']/List[@Name='InterventionList']" \
                           "/Struct[@Name='Intervention']"
INTERVENTION_NAME = "./Field[@Name='InterventionName']"
INTERVENTION_TYPE = "./Field[@Name='InterventionType']"
INTERVENTION_DESCR = "./Field[@Name='InterventionDescription']"
OUTCOMES = XML_ROOT + "Struct[@Name='OutcomesModule']/List[@Name='PrimaryOutcomeList']/Struct[@Name='PrimaryOutcome']"
OUTCOME_NAME = "./Field[@Name='PrimaryOutcomeMeasure']"
OUTCOME_DESCR = "./Field[@Name='PrimaryOutcomeDescription']"
OUTCOME_TIME = "./Field[@Name='PrimaryOutcomeTimeFrame']"

CRITERIA = XML_ROOT + "Struct[@Name='EligibilityModule']/Field[@Name='EligibilityCriteria']"
GENDER = XML_ROOT + "Struct[@Name='EligibilityModule']/Field[@Name='Gender']"
MAX_AGE = XML_ROOT + "Struct[@Name='EligibilityModule']/Field[@Name='MaximumAge']"
MIN_AGE = XML_ROOT + "Struct[@Name='EligibilityModule']/Field[@Name='MinimumAge']"

CONTACT_PERSONS = XML_ROOT + "Struct[@Name='ContactsLocationsModule']/List[@Name='CentralContactList']" \
                             "/Struct[@Name='CentralContact']"
CONTACT_NAME = "./Field[@Name='CentralContactName']"
CONTACT_ROLE = "./Field[@Name='CentralContactRole']"
CONTACT_PHONE = "./Field[@Name='CentralContactPhone']"
CONTACT_EMAIL = "./Field[@Name='CentralContactEMail']"

PRINCIPAL_INVESTIGATORS = XML_ROOT + "Struct[@Name='ContactsLocationsModule']/List[@Name='OverallOfficialList']" \
                                     "/Struct[@Name='OverallOfficial']"
INVESTIGATOR_NAME = "Field[@Name='OverallOfficialName']"
INVESTIGATOR_AFFILIATION = "./Field[@Name='OverallOfficialAffiliation']"
INVESTIGATOR_ROLE = "./Field[@Name='OverallOfficialRole']"

LOCATIONS = XML_ROOT + "Struct[@Name='ContactsLocationsModule']/List[@Name='LocationList']/Struct[@Name='Location']"
LOCATION_FACILITY = "./Field[@Name='LocationFacility']"
LOCATION_CITY = "./Field[@Name='LocationCity']"
LOCATION_COUNTRY = "./Field[@Name='LocationCountry']"
LOCATION_POSTCODE = "./Field[@Name='LocationZip']"
#LOCATION_FACILITY = "./Field[@Name='CentralContactName']"
LOCATION_COLLABORATORS = "./List[@Name='LocationContactList']/Struct[@Name='LocationContact']"
LOCATION_COLLAB_NAME = "./Field[@Name='LocationContactName']"
LOCATION_COLLAB_ROLE = "./Field[@Name='LocationContactRole']"
LOCATION_COLLAB_PHONE = "./Field[@Name='LocationContactPhone']"
LOCATION_COLLAB_EMAIL = "./Field[@Name='LocationContactEMail']"

