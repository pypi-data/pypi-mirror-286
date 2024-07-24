"""
Event handler decorators for common Lambda events
"""

from leo_aws_lambda_powertools.event_handler.api_gateway import (
    ALBResolver,
    APIGatewayHttpResolver,
    ApiGatewayResolver,
    APIGatewayRestResolver,
    CORSConfig,
    Response,
)
from leo_aws_lambda_powertools.event_handler.appsync import AppSyncResolver
from leo_aws_lambda_powertools.event_handler.bedrock_agent import BedrockAgentResolver
from leo_aws_lambda_powertools.event_handler.lambda_function_url import (
    LambdaFunctionUrlResolver,
)
from leo_aws_lambda_powertools.event_handler.vpc_lattice import VPCLatticeResolver, VPCLatticeV2Resolver

__all__ = [
    "AppSyncResolver",
    "APIGatewayRestResolver",
    "APIGatewayHttpResolver",
    "ALBResolver",
    "ApiGatewayResolver",
    "BedrockAgentResolver",
    "CORSConfig",
    "LambdaFunctionUrlResolver",
    "Response",
    "VPCLatticeResolver",
    "VPCLatticeV2Resolver",
]
