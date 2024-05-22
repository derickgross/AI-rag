from embed_docs_handler.embedding.embed import embed_docs
import os

def handle_embed_docs(event, context):
    # TODO: save event to logs
    print(event)

    bucket_name = os.environ.get('EMBEDDINGS_BUCKET_NAME')

    embed_destination = f"s3//{bucket_name}/embeddings/embeddings.csv" ## 's3://bucket/folder/path/file.csv

    answer = embed_docs(destination=embed_destination)

    return {
        'statusCode': 200,
        'body': answer
    }