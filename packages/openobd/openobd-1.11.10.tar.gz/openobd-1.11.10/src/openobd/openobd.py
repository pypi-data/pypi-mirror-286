#!/usr/bin/env python3
import grpc
import os
import threading
import time
import functools

from openobd_protocol.Session import SessionServices_pb2_grpc as grpcService
from openobd_protocol.Session.Messages import BusConfiguration_pb2 as grpcBusConfiguration
from openobd_protocol.Session.Messages import Session_pb2 as grpcSession
from openobd_protocol.Messages import Empty_pb2 as grpcEmpty
from openobd_protocol.Session.Messages import ServiceResult_pb2 as grpcServiceResult
from openobd_protocol.SessionController.Messages import SessionController_pb2 as grpcSessionController
from openobd_protocol.SessionController import SessionControllerServices_pb2_grpc as grpcSessionControllerService
from openobd_protocol.Communication.Messages import Isotp_pb2 as grpcIsotp
from openobd_protocol.Communication.Messages import Raw_pb2 as grpcRaw
from openobd_protocol.Communication import CommunicationServices_pb2_grpc as grpcCommunicationService
from openobd_protocol.UserInterface.Messages import UserInterface_pb2 as grpcUserInterface
from openobd_protocol.UserInterface import UserInterfaceServices_pb2_grpc as grpcUserInterfaceService
from openobd_protocol.ConnectionMonitor.Messages import ConnectorInformation_pb2 as grpcConnectionInformation
from openobd_protocol.ConnectionMonitor import ConnectionMonitorServices_pb2_grpc as grpcConnectionMonitorService
from .openobd_exceptions import OpenOBDException
from collections.abc import Iterator


def _is_valid_response(response, response_object):
    try:
        if response is not None:
            assert isinstance(response, response_object), f"Expected {type(response).__name__} object, received: {type(response_object).__name__}"
            return True
    except AssertionError:
        pass
    return False


def raises_openobd_exceptions(func):
    """
    If the wrapped function raises a gRPC exception, it will be cast and raised as an OpenOBDException.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, grpc.Call):
                # Encountered an exception raised by gRPC, so cast it to an OpenOBDException
                raise OpenOBDException(details=e.details(), status=e.code().value[0], status_description=e.code().value[1])
            else:
                # The exception wasn't raised by gRPC, so just raise it as is
                raise e

    return wrapper


class GrpcChannel(object):

    grpc_host = None
    grpc_port = 443
    connected = False
    channel = None

    def _connect(self):
        if not self.connected:
            ''' Check if local grpc-proxy is running '''
            if self.grpc_port == 443:
                self.channel = grpc.secure_channel(self.grpc_host, grpc.ssl_channel_credentials())
            else:
                ''' NOTE: Only use this for development purposes '''
                self.channel = grpc.insecure_channel('{}:{}'.format(self.grpc_host, self.grpc_port))

            ''' TODO: Exceptions and stuff '''
            self.connected = True


class OpenOBDSession(GrpcChannel):

    session_info = None

    """
    Client for gRPC functionality
    """
    def __init__(self, session_info: grpcSessionController.SessionInfo, grpc_port=443):
        self.active = True
        self.session_info = session_info

        '''Initially the session token is the authentication token for the session'''
        self.session_token = self.session_info.authentication_token

        self.grpc_host = self.session_info.grpc_endpoint
        self.grpc_port = grpc_port
        self._connect()

        self.session = grpcService.sessionStub(self.channel)
        self.can = grpcCommunicationService.canStub(self.channel)
        self.ui = grpcUserInterfaceService.userInterfaceStub(self.channel)
        self.connector_monitor = grpcConnectionMonitorService.connectionMonitorStub(self.channel)

    def id(self):
        return self.session_info.id

    def _metadata(self):
        metadata = []
        metadata.append(("authorization", "Bearer {}".format(self.session_token)))
        metadata = tuple(metadata)
        return metadata

    def update_session_token(self, session_token):
        self.session_token = session_token

    @raises_openobd_exceptions
    def configure_bus(self, bus_configuration: grpcBusConfiguration.BusConfiguration) -> grpcEmpty.EmptyMessage:
        """
        Client function to call the rpc
        :param bus_configuration:
        :return: Status of the bus configuration request
        """
        return self.session.configureBus(request=bus_configuration, metadata=self._metadata())

    @raises_openobd_exceptions
    def configure_buses(self, bus_configurations: Iterator[grpcBusConfiguration.BusConfiguration]) -> grpcEmpty.EmptyMessage:
        """
        client function to set up multiple buses
        :param bus_configurations: An iterator containing the buses that are requested to be set
        :return: Status of the bus configuration request
        """
        return self.session.configureBuses(bus_configurations, metadata=self._metadata())

    @raises_openobd_exceptions
    def open_isotp_stream(self, isotp_messages: Iterator[grpcIsotp.IsotpMessage]) -> Iterator[grpcIsotp.IsotpMessage]:
        """
        Client function to send and receive a stream of ISOTP format messages
        :param isotp_messages: An iterator containing the ISOTP messages that are requested to be sent
        :return: A list of ISOTP response messages
        """
        return self.can.openIsotpStream(isotp_messages, metadata=self._metadata())

    @raises_openobd_exceptions
    def open_raw_stream(self, raw_frames: Iterator[grpcRaw.RawFrame]) -> Iterator[grpcRaw.RawFrame]:
        """
        Client function to send out and receive a stream of RAW format messages
        :param raw_frames: An iterator containing the RAW messages that are requested to be sent
        :return: A list of RAW response messages
        """
        return self.can.openRawStream(raw_frames, metadata=self._metadata())

    @raises_openobd_exceptions
    def open_control_stream(self, user_interface_messages: Iterator[grpcUserInterface.Control]) -> Iterator[grpcUserInterface.Control]:
        """
        Client function to control various components of the user interface
        :param user_interface_messages: An iterator containing the user interface message to be controlled
        :return: User interface component with output or answers depending upon the control fields sent
        """
        return self.ui.openControlStream(user_interface_messages, metadata=self._metadata())

    @raises_openobd_exceptions
    def get_connector_information(self, request: grpcEmpty.EmptyMessage | None = None) -> grpcConnectionInformation.ConnectorInformation:
        """
        Client function to retrieve connector information at the give instant
        :return: gRPC Connector Information object
        """
        if request is None:
            request = grpcEmpty.EmptyMessage()
        return self.connector_monitor.getConnectorInformation(request=request, metadata=self._metadata())

    @raises_openobd_exceptions
    def open_connector_information_stream(self, request: grpcEmpty.EmptyMessage | None = None) -> Iterator[grpcConnectionInformation.ConnectorInformation]:
        """
        Client function to stream connector information every second until server is shutdown
        :return: An iterator consisting of gRPC Connector Information object
        """
        if request is None:
            request = grpcEmpty.EmptyMessage()
        return self.connector_monitor.openConnectorInformationStream(request=request, metadata=self._metadata())

    @raises_openobd_exceptions
    def authenticate(self, request: grpcEmpty.EmptyMessage | None = None) -> grpcSession.SessionToken:
        """
        Client function to authenticate the openOBD session
        :return: gRPC SessionToken object
        """
        if request is None:
            request = grpcEmpty.EmptyMessage()
        return self.session.authenticate(request=request, metadata=self._metadata())

    @raises_openobd_exceptions
    def open_session_token_stream(self, request: grpcEmpty.EmptyMessage | None = None) -> Iterator[grpcSession.SessionToken]:
        """
        Client function to stream fresh session tokens that keep the connection alive
        :return: An iterator consisting of gRPC SessionToken object
        """
        if request is None:
            request = grpcEmpty.EmptyMessage()
        return self.session.openSessionTokenStream(request=request, metadata=self._metadata())

    @raises_openobd_exceptions
    def finish(self, service_result: grpcServiceResult.ServiceResult) -> grpcEmpty.EmptyMessage:
        """
        Client function to finish the procedure and close the session from client side
        :param service_result: The result to be set indicating if the desired diagnostic procedure was successfully carried out
        :return: Status of the service request
        """
        self.active = False
        return self.session.finish(service_result, metadata=self._metadata())

    def __str__(self):
        return (f"ID: {self.session_info.id}, "
                f"state: {self.session_info.state}, "
                f"created at: {self.session_info.created_at}, "
                f"gRPC endpoint: {self.session_info.grpc_endpoint}, "
                f"authentication token: {self.session_info.authentication_token}")


class OpenOBD(object):
    """
    Client for gRPC functionality
    """
    session_controller = None

    def __init__(self, **kwargs):
        """
        Initialize openOBD with provided partner credentials

        Keyword Args:
            client_id(str):
            client_secret(str):
            partner_api_key(str):
            cluster_id(str):
            grpc_host(str):
            grpc_port(int):
        """
        self.session_controller = OpenOBDSessionController(**kwargs)

    @raises_openobd_exceptions
    def start_session_on_connector(self, connector_id: str) -> OpenOBDSession:
        response = self.session_controller.start_session_on_connector(grpcSessionController.ConnectorId(value=connector_id))
        return OpenOBDSession(response)

    @raises_openobd_exceptions
    def start_session_on_ticket(self, ticket_id: str) -> OpenOBDSession:
        response = self.session_controller.start_session_on_ticket(grpcSessionController.TicketId(value=ticket_id))
        return OpenOBDSession(response)

    @raises_openobd_exceptions
    def get_session(self, session_id: grpcSessionController.SessionId) -> grpcSessionController.SessionInfo:
        return self.session_controller.get_session(session_id)

    @raises_openobd_exceptions
    def interrupt_session(self, session_id: grpcSessionController.SessionId) -> grpcSessionController.SessionInfo:
        return self.session_controller.interrupt_session(session_id)

    @raises_openobd_exceptions
    def get_session_list(self) -> grpcSessionController.SessionInfoList:
        return self.session_controller.get_session_list()


class OpenOBDSessionController(GrpcChannel):

    client_id = None
    client_secret = None
    partner_api_key = None
    cluster_id = None

    session_controller_token = None

    """
    gRPC Client for SessionController
    """
    def __init__(self, **kwargs):
        """Initialize openobd session controller

        Keyword Args:
            client_id(str):
            client_secret(str):
            partner_api_key(str):
            cluster_id(str):
            grpc_host(str):
            grpc_port(int):
        """
        self.client_id = self._get_value_from_kwargs_or_env(kwargs, "client_id", "OPENOBD_PARTNER_CLIENT_ID")
        self.client_secret = self._get_value_from_kwargs_or_env(kwargs, "client_secret", "OPENOBD_PARTNER_CLIENT_SECRET")
        self.partner_api_key = self._get_value_from_kwargs_or_env(kwargs, "partner_api_key", "OPENOBD_PARTNER_API_KEY")
        self.cluster_id = self._get_value_from_kwargs_or_env(kwargs, "cluster_id", "OPENOBD_CLUSTER_ID")

        self.grpc_host = self._get_value_from_kwargs_or_env(kwargs, "grpc_host", "OPENOBD_GRPC_HOST")
        self.grpc_port = kwargs.get('grpc_port') if 'grpc_port' in kwargs else 443
        self._connect()

        self.session_controller = grpcSessionControllerService.sessionControllerStub(self.channel)
        self._get_session_controller_token()

    @staticmethod
    def _get_value_from_kwargs_or_env(kwargs, kwarg_key, env_key):
        if kwarg_key in kwargs:
            return kwargs[kwarg_key]
        elif env_key in os.environ:
            return os.environ[env_key]
        else:
            raise AssertionError(f"Argument \"{kwarg_key}\" could not be found. Pass it explicitly, or ensure it is available as an environment variable named \"{env_key}\".")

    def _metadata(self):
        metadata = []
        if self.session_controller_token:
            metadata.append(("authorization", "Bearer {}".format(self.session_controller_token)))
        metadata = tuple(metadata)
        return metadata

    @raises_openobd_exceptions
    def _get_session_controller_token(self) -> grpcSessionController.SessionControllerToken:
        # retrieve the session token and add it to the metadata
        response = self.session_controller.getSessionControllerToken(
            grpcSessionController.Authenticate(
                client_id=self.client_id,
                client_secret=self.client_secret,
                api_key=self.partner_api_key,
                cluster_id=self.cluster_id
            ))  # type: grpcSessionController.SessionControllerToken

        # before setting the session token in the metadata ensure session token exists in the response
        if _is_valid_response(response, grpcSessionController.SessionControllerToken):
            self.session_controller_token = response.value
        return response

    @raises_openobd_exceptions
    def start_session_on_ticket(self, ticket_id: grpcSessionController.TicketId) -> grpcSessionController.SessionInfo:

        return self.session_controller.startSessionOnTicket(ticket_id, metadata=self._metadata())

    @raises_openobd_exceptions
    def start_session_on_connector(self, connector_id: grpcSessionController.ConnectorId) -> grpcSessionController.SessionInfo:

        return self.session_controller.startSessionOnConnector(connector_id, metadata=self._metadata())

    @raises_openobd_exceptions
    def get_session(self, session_id: grpcSessionController.SessionId) -> grpcSessionController.SessionInfo:

        return self.session_controller.getSession(session_id, metadata=self._metadata())

    @raises_openobd_exceptions
    def interrupt_session(self, session_id: grpcSessionController.SessionId) -> grpcSessionController.SessionInfo:
        """
        Manager function to interrupt active session
        :param session_id:
        :return: interrupted Session object
        """
        return self.session_controller.interruptSession(session_id, metadata=self._metadata())

    @raises_openobd_exceptions
    def get_session_list(self) -> grpcSessionController.SessionInfoList:
        """
        Manager function to request a list of active sessions
        :return: List of sessions
        """

        return self.session_controller.getSessionList(request=grpcEmpty.EmptyMessage(), metadata=self._metadata())


