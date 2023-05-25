import datetime
import json
import os
import re
from geopy.geocoders import Nominatim

from config import constants
from tfm.data_type.ct_gender import GenderType
from tfm.data_type.ct_intervention_model import InterventionModel
from tfm.data_type.ct_intervention_type import InterventionType
from tfm.data_type.ct_observational_model import ObservationalModel
from tfm.data_type.ct_phases import PhasesType
from tfm.data_type.ct_recruiting_status import RecruitingStatus
from tfm.data_type.ct_sponsor import SponsorClass
from tfm.data_type.ct_study_type import StudyType


class Utils:
    @staticmethod
    def get_text(root_element):
        """
            Method to return the text of an XML element, or None.

            Parameters:
                root_element (Element): XML element.

            Returns:
                str: The text from the root_element as str.
        """
        if root_element is not None:
            clean_text = root_element.text
            clean_text = clean_text.replace("≥", ">=")
            clean_text = clean_text.replace("≤", "<=")
            return clean_text
        else:
            return None

    @staticmethod
    def split_and_normalise_text(root_element):
        """
            Method to normalise text (lower case), split the text in multiple, or if empty, return none.

            Parameters:
                root_element (Element): XML element.

            Returns:
                str: The normalised text from the root_element as str.
        """
        text = Utils.get_text(root_element)

        if text is None:
            return []
        else:
            text = re.sub(r"\(.*?\)", "", text)
            multiple_text = re.split(r',|\+|&|and|/', text)
            multiple_text = [word.title() for word in multiple_text if word != ' ' and word != '']

        return multiple_text

    @staticmethod
    def get_int(root_element):
        """
            Method to return the integer of an XML element, or None.

            Parameters:
                root_element (Element): XML element.

            Returns:
                bool: The text from the root_element as boolean.
        """
        element_str = Utils.get_text(root_element)
        if element_str is None:
            return None
        else:
            return int(element_str)

    @staticmethod
    def get_enum(enum_element, enum_type):
        """
            Method to return the enum element of a String

            Parameters:
                enum_element (Element): XML element.
                enum_type (str): Type of enum

            Returns:
                str: The enum type as string
        """
        returned_element = None
        if enum_element is None:
            return returned_element
        enum_element = enum_element.text.upper().replace(" ", "_")
        enum_element = enum_element.replace(",", "")
        enum_element = enum_element.replace("-", "_")
        try:
            if enum_type == "STUDY":
                returned_element = getattr(StudyType, enum_element)

            if enum_type == "PHASE":
                returned_element = getattr(PhasesType, enum_element)

            if enum_type == "RECRUITING":
                returned_element = getattr(RecruitingStatus, enum_element)

            if enum_type == "SPONSOR":
                returned_element = getattr(SponsorClass, enum_element)

            if enum_type == "INTERVENTION":
                returned_element = getattr(InterventionType, enum_element)

            if enum_type == "GENDER":
                returned_element = getattr(GenderType, enum_element)

            if enum_type == "OBS_MODE":
                returned_element = getattr(ObservationalModel, enum_element)

            if enum_type == "INT_MODE":
                returned_element = getattr(InterventionModel, enum_element)

        except AttributeError as ex:
            pass

        return returned_element

    @staticmethod
    def get_date(date_string):
        """
            Method to return the date format of a string "month name year"

            Parameters:
                date_string (Element): XML element.

            Returns:
                str: The date of date_string as string.
        """
        if date_string is not None:
            date_string = date_string.text
            try:
                d = datetime.datetime.strptime(date_string, '%B %Y')
                return d.strftime('%Y-%m-%d')
            except ValueError as ex:
                d = datetime.datetime.strptime(date_string, '%B %d, %Y')
                return d.strftime('%Y-%m-%d')

    @staticmethod
    def get_hash(name: str, country: str):
        """
            Get the hash from a name, and country.

            Parameters:
                name (str): Name to be hashed.
                country (str): Country to be hashed

            Returns:
                str: Hash of the name and country
        """
        if name is None:
            return None

        name = "" if name is None else name
        country = "" if country is None else country
        hash_name = (name + country).replace(" ", "")

        return str(hash(hash_name))

    @staticmethod
    def normalise_text(text: str):
        """
            Return a text normalised: remove spaces

            Parameters:
                text (str): Text to be normalised.

            Returns:
                str: Normalised text.
        """
        text = text.title()
        text = text.replace(" ", "")

        return text

    @staticmethod
    def get_coordinates(city: str, country: str):
        """
            Return the longitude and latitude of a specific city

            Parameters:
                city (str): City.
                country (str): Country

            Returns:
                str: longitude
                str: latitude
        """
        geolocator = Nominatim(user_agent="tfm_xarxes")

        geolocation = city if country is None else city + ", " + country
        location = geolocator.geocode(geolocation)

        if location is None and country is not None:
            location = geolocator.geocode(country)

        if location is None:
            return None, None

        return location.latitude, location.longitude

    @staticmethod
    def get_all_coordinates():
        """
            Return the already processed coordinates

            Parameters:

            Returns:
                dict: dictionary of cities with its correspondance latitude and longitude
        """
        data = {}
        if os.path.exists(constants.JSON_COORDINATES):
            with open(constants.JSON_COORDINATES, 'r') as file:
                data = json.load(file)
        return data
