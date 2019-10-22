from flask_restplus import Api

from .views import api as ns1

api = Api(title="CBOE PITCH API", version="1.0", description="Allows users to upload pitch data")

api.add_namespace(ns1, path="/api/v1")

