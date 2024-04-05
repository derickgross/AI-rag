from aws_cdk import(
    aws_apigateway as apigw,
    Stack,
    aws_lambda as _lambda,
)
from constructs import Construct
import os

class LambdaAnswerQuestionStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cwd = os.getcwd()

        # create lambda function
        question_handler = _lambda.Function(
            self, "handle_question_function",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="question-handler.handle_question",
            code=_lambda.Code.from_asset(os.path.join(cwd, 'question-handler.py'))
        )

        # create API Gateway endpoint that handles questions
        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=question_handler,
        )