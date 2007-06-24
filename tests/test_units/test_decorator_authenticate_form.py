# -*- coding: utf-8 -*-
from paste.fixture import TestApp
from paste.registry import RegistryManager

from pylons import Response
from pylons.decorators.secure_form import authenticate_form, denied_message

from pylons.controllers import WSGIController

from __init__ import ControllerWrap, SetupCacheGlobal, TestWSGIController

class ProtectedController(WSGIController):
    def protected(self):
        return Response("Authenticated form")
    protected = authenticate_form(protected)

class TestAuthenticateFormDecorator(TestWSGIController):
    def setUp(self):
        TestWSGIController.setUp(self)
        app = SetupCacheGlobal(ControllerWrap(ProtectedController),
                               self.environ, setup_cache=False)
        app = RegistryManager(app)
        self.app = TestApp(app)

    def test_unauthenticated(self):
        self.environ['pylons.routes_dict'].update(action='protected')
        response = self.app.post('/', extra_environ=self.environ,
                                 expect_errors=True)
        assert denied_message in response
