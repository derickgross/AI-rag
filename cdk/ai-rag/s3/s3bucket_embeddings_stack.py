# export class S3BucketStack extends cdk.Stack {
#   constructor(scope: Construct, id: string, props?: cdk.StackProps) {
#     super(scope, id, props);

#     const s3Bucket = new s3.Bucket(this, 'exampleBucket', {
#       objectOwnership: s3.ObjectOwnership.BUCKET_OWNER_ENFORCED,
#       blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
#       encryptionKey: new kms.Key(this, 's3BucketKMSKey'),
#     });

#     s3Bucket.grantRead(new iam.AccountRootPrincipal());
#   }
# }

from aws_cdk import(
    aws_lambda as _lambda,
    aws_s3 as _s3,
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

        cwd = os.getcwd() ##

        bucket_name = os.environ.get('EMBEDDINGS_BUCKET_NAME')

        # embed_destination = f"arn:aws:s3:::{bucket_name}/*"
        embed_destination = f"s3//{bucket_name}/embeddings/embeddings.csv" ## 's3://bucket/folder/path/file.csv

        # create s3 bucket
        s3 = _s3.Bucket(
            self,
            "dag211-embeddings-bucket",
            bucket_name=bucket_name
        )
        try:
            s3.create()
            s3.wait_until_exists()
            print("S3 bucket created")
            embed_docs(destination=embed_destination)
        except:
            print("Failed to create S3 bucket")

        # # create embed docs lambda function
        embed_docs_handler = _lambda.Function(
            self, "handle_embed_docs_function",
            runtime=_lambda.Runtime.PYTHON_3_11,
            architecture=_lambda.Architecture.ARM_64,
            handler="embed-docs-handler.handle_embed_docs",
            code=_lambda.Code.from_asset(os.path.join(cwd, 'cdk/ai-rag/lambdas/embed_docs_handler.zip'))
            # code=_lambda.Code.from_asset(os.path.join(cwd, 'cdk/ai-rag/lambdas/embed_docs_handler_layer_content.zip'))
        )

        # embed_docs(destination=embed_destination)