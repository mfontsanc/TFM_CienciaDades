from datetime import datetime

from flask_restx import Namespace, Resource, fields
from config import messages, constants, constants_examples
from apis.api_insert import logger
from tfm.select.select_data import SelectData
from flask import request

api = Namespace(constants.FUNCTIONALITIES[constants.KEY_NETWORK_GET_CLINICAL_TRIAL][constants.KEY_TITLE],
                description=constants.FUNCTIONALITIES[constants.KEY_NETWORK_GET_CLINICAL_TRIAL]
                [constants.KEY_DESCRIPTION])

""" Input data model definition """
insert_input_get_clinical_trial = api.model('InputInsertGetClinicalTrial', {
    constants.KEY_NAME_REQUEST_CT_ID: fields.String(
        description=constants.DESCRIPTION_NETWORK_MODEL_INPUT_CT_ID,
        required=True, example=constants_examples.EXAMPLE_CT_ID)
})

""" Output data model definition """
insert_output_get_clinical_trial = api.model('OutputGetClinicalTrial', {
    constants.KEY_NAME_RESPONSE_SPONSORS: fields.List(cls_or_instance=fields.List(cls_or_instance=fields.String),
                                                      description=constants.DESCRIPTION_NETWORK_MODEL_OUTPUT_SPONSORS,
                                                      example=constants_examples.
                                                      EXAMPLE_GET_COMMUNITIES_DETAIL_OUTPUT_SPONSORS),
    constants.KEY_NAME_RESPONSE_PRINCIPAL_INVESTIGATORS:
        fields.List(cls_or_instance=fields.List(cls_or_instance=fields.String),
                    description=constants.DESCRIPTION_NETWORK_MODEL_OUTPUT_PRINCIPAL_INVESTIGATORS,
                    example=constants_examples.EXAMPLE_GET_COMMUNITIES_DETAIL_OUTPUT_PRINCIPAL_INVESTIGATOR),
    constants.KEY_NAME_RESPONSE_COLLABORATORS:
        fields.List(cls_or_instance=fields.List(cls_or_instance=fields.String),
                    description=constants.DESCRIPTION_NETWORK_MODEL_OUTPUT_LOCATIONS,
                    example=constants_examples.EXAMPLE_GET_COMMUNITIES_DETAIL_OUTPUT_LOCATION),
    constants.KEY_NAME_RESPONSE: fields.Boolean(description=constants.DESCRIPTION_NETWORK_MODEL_OUTPUT_RESPONSE,
                                                example=constants_examples.EXAMPLE_INSERT_MODEL_OUTPUT_RESPONSE)
})


@api.route(constants.FUNCTIONALITIES[constants.KEY_NETWORK_GET_CLINICAL_TRIAL]
           [constants.KEY_TITLE_END_POINT])
class GetClinicalTrial(Resource):
    @api.doc(constants.FUNCTIONALITIES[constants.KEY_NETWORK_GET_CLINICAL_TRIAL][constants.KEY_DOC])
    @api.expect(insert_input_get_clinical_trial, validate=True)
    @api.response(200, messages.MESSAGE_200)
    @api.response(400, messages.MESSAGE_400)
    @api.response(404, messages.MESSAGE_404)
    @api.response(500, messages.MESSAGE_500)
    def post(self):
        """
        Returns all the data of a clinical trials send via parameter.
        """
        try:
            t0 = datetime.now()
            logger.info(f'Received: {t0}')
            json_in = request.json
            ct_id = json_in.get(constants.KEY_NAME_REQUEST_CT_ID)
            data = SelectData().get_clinical_trial_detail(clinical_trial_id=ct_id)

            return data
        except Exception as ex:
            message = f"{messages.MESSAGE_PROCESS_EXCEPTION} Exception: {ex}"
            logger.error(message)
            return []
