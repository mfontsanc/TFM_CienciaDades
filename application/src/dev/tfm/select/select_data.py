import json

from config import sparql, constants
from utils.database_manager import DatabaseManager
from utils.utils import Utils


class SelectData:
    @staticmethod
    def get_clinical_trials_community():
        """
            Method to get the clinical trials and community from GraphDB

            Parameters:

            Returns:
                list: List of clinical trials identifier and community identified.
        """
        query = sparql.GET_CT_COM
        db_manager = DatabaseManager()
        results = db_manager.run_select_data(query)

        output_result = []
        for result in results:
            ct_id = result['ct_id']['value']
            comm_id = result['comm_id']['value'] if result.get('comm_id') else -1
            output_result.append([ct_id, comm_id])
        return output_result

    @staticmethod
    def get_clinical_trials_community_detail(community_id: int):
        """
            Method to get the clinical trials and properties of a specific community from GraphDB

            Parameters:
                community_id (int): Identifier of the community.

            Returns:
                list: List of clinical trials properties.
        """
        query = sparql.GET_CT_COMM_ID % (community_id, community_id, community_id, community_id)
        db_manager = DatabaseManager()
        results = db_manager.run_select_data(query)

        output_result = []
        for result in results:
            ct_id = result['ct_id']['value'].replace("http://purl.org/net/OCRe/OCRe.owl#", "")
            property_name = result['property_name']['value']
            object_name = result['property_name']['value'] + ": " + result['object']['value']
            output_result.append([ct_id, property_name, object_name])

        return output_result

    @staticmethod
    def get_clinical_trials_collaborators(community_id: int):
        """
            Method to get the clinical trials and their collaborators of a specific community from GraphDB

            Parameters:
                community_id (int): Identifier of the community.

            Returns:
                list: List of clinical trials sponsors.
                list: List of clinical trials principal investigators.
                list: List of clinical trials locations.
        """
        # Get sponsors
        query = sparql.GET_SPONSORS_COMM_ID % community_id
        db_manager = DatabaseManager()
        results = db_manager.run_select_data(query)

        sponsors_results = []
        for result in results:
            ct_id = result['ct_id']['value'].replace("http://purl.org/net/OCRe/OCRe.owl#", "")
            sponsor_name = result['sponsor_name']['value']
            sponsors_results.append([ct_id, sponsor_name])

        # Get locations
        query = sparql.GET_LOCATION_COMM_ID % community_id
        db_manager = DatabaseManager()
        results = db_manager.run_select_data(query)

        location_results = []
        all_coordinates = Utils.get_all_coordinates()
        try:
            for result in results:
                ct_id = result['ct_id']['value'].replace("http://purl.org/net/OCRe/OCRe.owl#", "")
                collaborator_name = result['collaborator_name']['value'] if result.get('collaborator_name') else 'N/A'
                collaborator_city = result['collaborator_city']['value']
                collaborator_country = result['collaborator_country']['value']
                collaborator_zip = result['collaborator_zip']['value']
                location = collaborator_city.lower() + ", " + collaborator_country.lower() \
                    if collaborator_country.lower() else collaborator_city.lower()
                if not all_coordinates.get(location):
                    latitude, longitude = Utils.get_coordinates(collaborator_city, collaborator_country)

                    if latitude and longitude:
                        all_coordinates[location] = [latitude, longitude]
                else:
                    latitude = all_coordinates[location][0]
                    longitude = all_coordinates[location][1]

                location_results.append([ct_id, latitude, longitude, collaborator_name, collaborator_city,
                                         collaborator_country, collaborator_zip])
        except Exception as ex:
            pass

        # Get investigators
        query = sparql.GET_PRINCIPAL_INVESTIGATOR_COMM_ID % community_id
        db_manager = DatabaseManager()
        results = db_manager.run_select_data(query)

        investigator_results = []
        for result in results:
            ct_id = result['ct_id']['value'].replace("http://purl.org/net/OCRe/OCRe.owl#", "")
            investigator_name = result['investigator_name']['value']
            investigator_role = result['investigator_role']['value']
            investigator_affiliation = result['investigator_affiliation']['value']

            investigator_results.append([ct_id, investigator_name, investigator_role, investigator_affiliation])

        with open(constants.JSON_COORDINATES, "w") as outfile:
            json.dump(all_coordinates, outfile)

        return sponsors_results, location_results, investigator_results

    @staticmethod
    def get_clinical_trial_detail(clinical_trial_id: str):
        """
            Method to get all data from a specific clinical trial from GraphDB.

            Parameters:
                clinical_trial_id (str): Identifier of the clinical trial.

            Returns:
                dict: dictionary with all the data.
        """
        clinical_trial_uri = "ocre:" + clinical_trial_id
        results = {}

        # Get data properties
        query = sparql.GET_CLINICAL_TRIAL_DATA_PROPERTIES % (clinical_trial_uri, clinical_trial_uri, clinical_trial_uri)
        db_manager = DatabaseManager()
        query_results = db_manager.run_select_data(query)
        for result in query_results:
            result_property = result['property_study']['value']
            result_object = result['object']['value']

            if "OCRE058000" in result_property:
                results['Objectiu'] = result_object.replace("InterventionModel.", "").replace("ObservationalModel,", "")
            if "OCRE189000" in result_property:
                results['Descripció'] = result_object
            if "community_id" in result_property:
                results['Comunitat'] = result_object
            if "OCRE900210" in result_property:
                results['Data inici'] = result_object
            if "OCRE900211" in result_property:
                results['Data últim participant'] = result_object
            if "OCRE900213" in result_property:
                results['Títol'] = result_object
            if "OCRE900214" in result_property:
                results['Data finalització'] = result_object
            if "OCRE900237" in result_property:
                results['Número de participants'] = result_object
            if "OCRE820850" in result_property:
                results['Fase'] = result_object
            if "OCRE901007" in result_property:
                results['Estat participació'] = result_object

        # Get keywords
        query = sparql.GET_CLINICAL_TRIAL_KEYWORDS % clinical_trial_uri
        db_manager = DatabaseManager()
        query_results = db_manager.run_select_data(query)
        results['Paraules clau'] = []
        for result in query_results:
            result_object = result['object']['value']
            results['Paraules clau'].append(result_object)

        # Get locations
        query = sparql.GET_CLINICAL_TRIAL_LOCATIONS % clinical_trial_uri
        db_manager = DatabaseManager()
        query_results = db_manager.run_select_data(query)
        all_coordinates = Utils.get_all_coordinates()
        results['Col·laboradors'] = []
        for result in query_results:
            result_name = result['collaborator_name']['value'] if result.get('collaborator_name') else ""
            result_city = result['collaborator_city']['value']
            result_country = result['collaborator_country']['value']
            result_zip = result['collaborator_zip']['value']

            location = result_city.lower() + ", " + result_country.lower() \
                if result_country.lower() else result_city.lower()
            if not all_coordinates.get(location):
                latitude, longitude = Utils.get_coordinates(result_city, result_country)

                if latitude and longitude:
                    all_coordinates[location] = [latitude, longitude]
            else:
                latitude = all_coordinates[location][0]
                longitude = all_coordinates[location][1]

            location = {"Nom de organització": result_name, "Ciutat": result_city, "País": result_country,
                        "Codi postal": result_zip, "Latitud": latitude, "Longitud": longitude}
            results['Col·laboradors'].append(location)

        # Get investigators
        query = sparql.GET_CLINICAL_TRIAL_INVESTIGATORS % clinical_trial_uri
        db_manager = DatabaseManager()
        query_results = db_manager.run_select_data(query)
        results['Investigadors'] = []
        for result in query_results:
            result_name = result['investigator_name']['value']
            result_role = result['investigator_role']['value']
            result_affiliation = result['investigator_affiliation']['value']
            result_city = result['affiliation_city']['value'] if result.get('affiliation_city') else ""
            result_country = result['affiliation_country']['value'] if result.get('affiliation_country') else ""

            investigator = {"Nom investigador": result_name, "Rol": result_role, "Afiliació": result_affiliation,
                            "Ciutat": result_city, "País": result_country}
            results['Investigadors'].append(investigator)

        # Get sponsors
        query = sparql.GET_CLINICAL_TRIAL_SPONSORS % clinical_trial_uri
        db_manager = DatabaseManager()
        query_results = db_manager.run_select_data(query)
        for result in query_results:
            result_name = result['sponsor_name']['value']
            results['Patrocinador'] = result_name

        # Get results
        query = sparql.GET_CLINICAL_TRIAL_RESULTS % clinical_trial_uri
        db_manager = DatabaseManager()
        query_results = db_manager.run_select_data(query)
        for result in query_results:
            result_property = result['property_study']['value']
            result_object = result['object']['value']
            data_results = {}

            if "OCRE000021" in result_property:
                data_results['Temps'] = result_object
            if "OCRE900214" in result_property:
                data_results['Descripció'] = result_object
            if "OCRE900224" in result_property:
                data_results['Nom'] = result_object

            results['Resultat'] = data_results

        # Get eligibility criteria
        query = sparql.GET_CLINICAL_TRIAL_CRITERIA % (clinical_trial_uri, clinical_trial_uri)
        db_manager = DatabaseManager()
        query_results = db_manager.run_select_data(query)
        results['Criteris eligibilitat'] = []
        for result in query_results:
            result_object = result['object']['value']
            results['Criteris eligibilitat'].append(result_object)

        # Get intervention
        query = sparql.GET_CLINICAL_TRIAL_INTERVENTION % clinical_trial_uri
        db_manager = DatabaseManager()
        query_results = db_manager.run_select_data(query)
        results['Intervencions'] = []
        for result in query_results:
            result_name = result['name']['value']
            result_descr = result['description']['value']
            result_type = result['type']['value']

            intervencio = {"Nom intervenció": result_name, "Descripció": result_descr, "Tipus intervenció": result_type}
            results['Intervencions'].append(intervencio)

        # Get condition
        query = sparql.GET_CLINICAL_TRIAL_CONDITION % clinical_trial_uri
        db_manager = DatabaseManager()
        query_results = db_manager.run_select_data(query)
        results['Condicions'] = []
        for result in query_results:
            result_name = result['condition']['value']
            results['Condicions'].append(result_name)

        return results

