from datetime import datetime

from flask_restx import Namespace, Resource, fields
from config import messages, constants, constants_examples
from apis.api_insert import logger
from tfm.select.select_data import SelectData

api = Namespace(constants.FUNCTIONALITIES[constants.KEY_NETWORK][constants.KEY_TITLE],
                description=constants.FUNCTIONALITIES[constants.KEY_NETWORK][constants.KEY_DESCRIPTION])

""" Output data model definition """
insert_output_get_community = api.model('OutputGetCommunity', {
    constants.KEY_NAME_RESPONSE_DATA: fields.List(cls_or_instance=fields.List(cls_or_instance=fields.String),
                                                  description=constants.DESCRIPTION_NETWORK_MODEL_OUTPUT_DATA,
                                                  example=constants_examples.EXAMPLE_GET_COMMUNITIES_OUTPUT_DATA),
    constants.KEY_NAME_RESPONSE: fields.Boolean(description=constants.DESCRIPTION_NETWORK_MODEL_OUTPUT_RESPONSE,
                                                example=constants_examples.EXAMPLE_INSERT_MODEL_OUTPUT_RESPONSE)
})


@api.route(constants.FUNCTIONALITIES[constants.KEY_NETWORK_GET_COMMUNITIES][constants.KEY_TITLE_END_POINT])
class GetCommunities(Resource):
    @api.doc(constants.FUNCTIONALITIES[constants.KEY_NETWORK_GET_COMMUNITIES][constants.KEY_DOC])
    @api.response(200, messages.MESSAGE_200, insert_output_get_community)
    @api.response(400, messages.MESSAGE_400)
    @api.response(404, messages.MESSAGE_404)
    @api.response(500, messages.MESSAGE_500)
    def post(self):
        """
        Returns the list of clinical trials and the correspond community.
        """
        try:
            t0 = datetime.now()
            logger.info(f'Received: {t0}')
            data = SelectData().get_clinical_trials_community()
            return data
        except Exception as ex:
            message = f"{messages.MESSAGE_PROCESS_EXCEPTION} Exception: {ex}"
            logger.error(message)
            return []
