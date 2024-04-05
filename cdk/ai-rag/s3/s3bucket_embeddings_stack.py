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

        bucket_name = os.environ.get('EMBEDDINGS_BUCKET_NAME')

        embed_destination = f"arn:aws:s3:::{bucket_name}/*"

        # create s3 bucket
        s3 = _s3.Bucket(
            self,
            "embeddings-bucket",
            bucket_name=bucket_name
        )
        try:
            s3.create()
            s3.wait_until_exists()
            print("S3 bucket created")
        except:
            print("Failed to create S3 bucket")

        embed_docs(destination=embed_destination)