#!/usr/bin/env python3

import sys
sys.path.insert(0, '/home/runner/work/AI-rag')

from aws_cdk import App

# from s3trigger.s3trigger_stack import S3TriggerStack
from s3.s3bucket_embeddings_stack import S3BucketEmbeddingsStack
from lambdas.lambda_answer_question_stack import LambdaAnswerQuestionStack

app = App()
# S3TriggerStack(app, "s3trigger")
S3BucketEmbeddingsStack(app, "s3embeddings")
LambdaAnswerQuestionStack(app, "answerQuestion")


app.synth()