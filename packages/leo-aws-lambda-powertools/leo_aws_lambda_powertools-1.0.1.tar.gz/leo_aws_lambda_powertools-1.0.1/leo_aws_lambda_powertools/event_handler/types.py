from typing import TypeVar

from leo_aws_lambda_powertools.event_handler import ApiGatewayResolver

EventHandlerInstance = TypeVar("EventHandlerInstance", bound=ApiGatewayResolver)
