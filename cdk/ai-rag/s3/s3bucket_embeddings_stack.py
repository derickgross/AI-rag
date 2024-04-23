from aws_cdk import(
    aws_lambda as _lambda,
    aws_s3 as _s3,
    aws_ecr as ecr,
    Stack
)
from constructs import Construct
from embedding.embed import embed_docs
import os
from dotenv import load_dotenv

load_dotenv()

class S3BucketEmbeddingsStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cwd = os.getcwd()

        bucket_name = os.environ.get('EMBEDDINGS_BUCKET_NAME')

        # embed_destination = f"arn:aws:s3:::{bucket_name}/*"
        embed_destination = f"s3://{bucket_name}/embeddings/embeddings.csv" ## 's3://bucket/folder/path/file.csv

        # create s3 bucket
        s3 = _s3.Bucket(
            self,
            "dag211-embeddings-bucket",
            bucket_name=bucket_name
        )

        # Get the ECR repository
        ecr_repository = ecr.Repository.from_repository_name(
            self, "EmbedLambdaRepository", "embed-lambda"
        )

        # create embed docs lambda function
        embed_docs_handler = _lambda.DockerImageFunction(
            self, "handle_embed_docs_function",
            code=_lambda.DockerImageCode.from_ecr(repository=ecr_repository, tag="latest"),
        )

        try:
            embed_docs_handler.add_environment("DESTINATION", embed_destination)
            print("Lambda function created successfully")
        except Exception as e:
            print(f"Failed to create Lambda function: {e}")