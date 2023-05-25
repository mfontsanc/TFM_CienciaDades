from flask import Blueprint
from flask_restx import Api
import config.constants as constants

# APIs
from apis.api_insert.namespace_insert import api as namespace_insert
from apis.api_community.namespace_community import api as namespace_community
from apis.api_community.namespace_get_community import api as namespace_get_community
from apis.api_community.namespace_get_community_detail import api as namespace_get_community_detail
from apis.api_community.namespace_get_collaborators import api as namespace_get_collaborators
from apis.api_community.namespace_get_clinical_trial import api as namespace_get_clinical_trial

blueprint = Blueprint(name=constants.NAME_API, import_name=__name__, url_prefix=constants.END_POINT_API)
api = Api(blueprint,
          title=constants.TITLE_API,
          version=constants.VERSION,
          description=constants.DESCRIPTION_API
          )

# API 1
api.add_namespace(namespace_insert)
api.add_namespace(namespace_community)
api.add_namespace(namespace_get_community)
api.add_namespace(namespace_get_community_detail)
api.add_namespace(namespace_get_collaborators)
api.add_namespace(namespace_get_clinical_trial)

