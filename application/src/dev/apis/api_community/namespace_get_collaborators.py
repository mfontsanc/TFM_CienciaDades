from datetime import datetime

from flask_restx import Namespace, Resource, fields
from config import messages, constants, constants_examples
from apis.api_insert import logger
from tfm.select.select_data import SelectData
from flask import request

api = Namespace(constants.FUNCTIONALITIES[constants.KEY_NETWORK_GET_COLLABORATORS][constants.KEY_TITLE],
                description=constants.FUNCTIONALITIES[constants.KEY_NETWORK_GET_COLLABORATORS]
                [constants.KEY_DESCRIPTION])

""" Input data model definition """
insert_input_get_collaborators = api.model('InputInsertGetCollaborators', {
    constants.KEY_NAME_REQUEST_COMMUNITY_ID: fields.String(
        description=constants.DESCRIPTION_NETWORK_MODEL_INPUT_COMMUNITY_ID,
        required=True, example=constants_examples.EXAMPLE_COMMUNITY_ID)
})

""" Output data model definition """
insert_output_get_collaborators = api.model('OutputGetCollaborators', {
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


@api.route(constants.FUNCTIONALITIES[constants.KEY_NETWORK_GET_COLLABORATORS]
           [constants.KEY_TITLE_END_POINT])
class GetCollaboratorsDetail(Resource):
    @api.doc(constants.FUNCTIONALITIES[constants.KEY_NETWORK_GET_COLLABORATORS][constants.KEY_DOC])
    @api.expect(insert_input_get_collaborators, validate=True)
    @api.response(200, messages.MESSAGE_200, insert_output_get_collaborators)
    @api.response(400, messages.MESSAGE_400)
    @api.response(404, messages.MESSAGE_404)
    @api.response(500, messages.MESSAGE_500)
    def post(self):
        """
        Returns the list clinical trials and the list of collaborators of a specific community.
        """
        try:
            t0 = datetime.now()
            logger.info(f'Received: {t0}')
            json_in = request.json
            community_id = json_in.get(constants.KEY_NAME_REQUEST_COMMUNITY_ID)
            community_id = int(community_id) if type(community_id) is str else community_id
            data = SelectData().get_clinical_trials_collaborators(community_id=community_id)
            results = {
                constants.KEY_NAME_RESPONSE_SPONSORS: data[0],
                constants.KEY_NAME_RESPONSE_PRINCIPAL_INVESTIGATORS: data[2],
                constants.KEY_NAME_RESPONSE_COLLABORATORS: data[1]
            }
            return results
        except Exception as ex:
            message = f"{messages.MESSAGE_PROCESS_EXCEPTION} Exception: {ex}"
            logger.error(message)
            return []
