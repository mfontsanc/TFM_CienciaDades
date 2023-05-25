from datetime import datetime

from flask import request
from flask_restx import Namespace, Resource, fields
from config import messages, constants, constants_examples
from apis.api_insert import logger
from tfm.similarity.community_relationship import CommunityRelationship

api = Namespace(constants.FUNCTIONALITIES[constants.KEY_NETWORK][constants.KEY_TITLE],
                description=constants.FUNCTIONALITIES[constants.KEY_NETWORK][constants.KEY_DESCRIPTION])

""" Input data model definition """
insert_input_community = api.model('InputInsertCommunity', {
    constants.KEY_NAME_COMMUNITY_PATH: fields.String(description=constants.DESCRIPTION_NETWORK_MODEL_INPUT_COMMUNITY,
                                                     required=True,
                                                     example=constants_examples.EXAMPLE_XML_PATH_INPUT)
})

""" Output data model definition """
insert_output_community = api.model('OutputInsertCommunity', {
    constants.KEY_NAME_RESPONSE_MESSAGE: fields.String(
        description=constants.DESCRIPTION_NETWORK_MODEL_OUTPUT_MESSAGE,
        example=constants_examples.EXAMPLE_INSERT_MODEL_OUTPUT_MESSAGE),
    constants.KEY_NAME_RESPONSE: fields.Boolean(description=constants.DESCRIPTION_NETWORK_MODEL_OUTPUT_RESPONSE,
                                                example=constants_examples.EXAMPLE_INSERT_MODEL_OUTPUT_RESPONSE)
})


@api.route(constants.FUNCTIONALITIES[constants.KEY_NETWORK_COMMUNITIES][constants.KEY_TITLE_END_POINT])
class InsertCommunities(Resource):
    @api.doc(constants.FUNCTIONALITIES[constants.KEY_NETWORK_COMMUNITIES][constants.KEY_DOC])
    @api.expect(insert_input_community, validate=True)
    @api.response(200, messages.MESSAGE_200, insert_output_community)
    @api.response(400, messages.MESSAGE_400)
    @api.response(404, messages.MESSAGE_404)
    @api.response(500, messages.MESSAGE_500)
    def post(self):
        """
        Returns whether the insertion of the clinical trials relationships have been done correctly.
        """
        try:
            t0 = datetime.now()
            logger.info(f'Received: {t0}')
            json_in = request.json
            folder_path = json_in.get(constants.KEY_NAME_COMMUNITY_PATH)
            result, message = CommunityRelationship(path=folder_path).start_process()
            # Return a response
            response_dict = {
                constants.KEY_NAME_RESPONSE_MESSAGE: message,
                constants.KEY_NAME_RESPONSE: result
            }
            return response_dict, 200
        except Exception as ex:
            message = f"{messages.MESSAGE_PROCESS_EXCEPTION} Exception: {ex}"
            logger.error(message)
            return {constants.KEY_NAME_RESPONSE_MESSAGE: message}, 500
