from datetime import datetime

from flask import request
from flask_restx import Namespace, Resource, fields
from config import messages, constants, constants_examples
from apis.api_insert import logger
from tfm.xml2rdf.transformation_xml2rdf import TransformationXML2RDF

api = Namespace(constants.FUNCTIONALITIES[constants.KEY_NETWORK][constants.KEY_TITLE],
                description=constants.FUNCTIONALITIES[constants.KEY_NETWORK][constants.KEY_DESCRIPTION])

""" Input data model definition """
insert_input = api.model('InputInsert', {
    constants.KEY_NAME_PATH: fields.String(description=constants.DESCRIPTION_NETWORK_MODEL_INPUT_FOLDER,
                                           required=True,
                                           example=constants_examples.EXAMPLE_XML_PATH_INPUT),
    constants.KEY_NAME_OUTPUT: fields.String(description=constants.DESCRIPTION_NETWORK_MODEL_INPUT_RESULT,
                                             required=False,
                                             example=constants_examples.EXAMPLE_XML_PATH_INPUT_RESULT),
    constants.KEY_NAME_REQUEST_DB_INSERT: fields.Boolean(description=constants.DESCRIPTION_NETWORK_MODEL_INPUT_DB,
                                                         required=False,
                                                         example=constants_examples.EXAMPLE_INSERT_MODEL_OUTPUT_RESPONSE)
})

""" Output data model definition """
insert_output = api.model('OutputInsert', {
    constants.KEY_NAME_RESPONSE_MESSAGE: fields.String(
        description=constants.DESCRIPTION_NETWORK_MODEL_OUTPUT_MESSAGE,
        example=constants_examples.EXAMPLE_INSERT_MODEL_OUTPUT_MESSAGE),
    constants.KEY_NAME_OUTPUT: fields.Boolean(description=constants.DESCRIPTION_NETWORK_MODEL_OUTPUT_RESULT,
                                              example=constants_examples.EXAMPLE_XML_PATH_INPUT_RESULT),
    constants.KEY_NAME_RESPONSE: fields.Boolean(description=constants.DESCRIPTION_NETWORK_MODEL_OUTPUT_RESPONSE,
                                                example=constants_examples.EXAMPLE_INSERT_MODEL_OUTPUT_RESPONSE)
})


@api.route(constants.FUNCTIONALITIES[constants.KEY_NETWORK][constants.KEY_TITLE_END_POINT])
class Insert(Resource):
    @api.doc(constants.FUNCTIONALITIES[constants.KEY_NETWORK][constants.KEY_DOC])
    @api.expect(insert_input, validate=True)
    @api.response(200, messages.MESSAGE_200, insert_output)
    @api.response(400, messages.MESSAGE_400)
    @api.response(404, messages.MESSAGE_404)
    @api.response(500, messages.MESSAGE_500)
    def post(self):
        """
        Returns whether the transformation and insertion has been done correctly.
        """
        try:
            t0 = datetime.now()
            logger.info(f'Received: {t0}')
            json_in = request.json
            folder_path = json_in.get(constants.KEY_NAME_PATH)
            save_database = json_in.get(constants.KEY_NAME_REQUEST_DB_INSERT, True)
            folder_results = json_in.get(constants.KEY_NAME_OUTPUT, constants.TEMP_TTL_FOLDER)
            result, message = TransformationXML2RDF(folder_path=folder_path,
                                                    store_db=save_database,
                                                    output_path=folder_results).start_process()
            # Return a response
            response_dict = {
                constants.KEY_NAME_RESPONSE_MESSAGE: message,
                constants.KEY_NAME_RESPONSE: result,
                constants.KEY_NAME_OUTPUT: folder_results
            }
            return response_dict, 200
        except Exception as ex:
            message = f"{messages.MESSAGE_PROCESS_EXCEPTION} Exception: {ex}"
            logger.error(message)
            return {constants.KEY_NAME_RESPONSE_MESSAGE: message}, 500
