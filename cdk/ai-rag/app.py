from aws_cdk import App

from ai_rag.s3trigger.s3trigger_stack import S3TriggerStack
from ai_rag.s3.s3bucket_embeddings_stack import S3BucketEmbeddingsStack
from ai_rag.lambdas.lambda_answer_question_stack import LambdaAnswerQuestionStack

app = App()
S3TriggerStack(app, "s3trigger")
S3BucketEmbeddingsStack(app, "s3embeddings")
LambdaAnswerQuestionStack(app, "answerQuestion")


app.synth()