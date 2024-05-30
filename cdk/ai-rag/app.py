from aws_cdk import App

from s3trigger_stack import S3TriggerStack
from s3bucket_embeddings_stack import S3BucketEmbeddingsStack

app = App()
S3TriggerStack(app, "s3trigger")
S3BucketEmbeddingsStack(app, "s3embeddings")


app.synth()