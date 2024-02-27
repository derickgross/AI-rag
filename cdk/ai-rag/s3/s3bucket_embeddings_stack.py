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

class S3BucketEmbeddingsStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create lambda function
        function = _lambda.Function(self, "embeddings_function",
                                    runtime=_lambda.Runtime.PYTHON_3_7,
                                    handler="question-handler.handle_question",
                                    code=_lambda.Code.from_asset("./lambda"))

        # create s3 bucket
        s3 = _s3.Bucket(self, "embeddingsBucket")