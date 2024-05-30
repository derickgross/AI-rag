print("Loading requirements for embed_docs_handler.py")

from embed import embed_docs
import logging
import os

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def log_directory_contents():
    cwd = os.getcwd()
    files = os.listdir(cwd)
    logger.info(f"Contents of the current working directory ({cwd}): {files}")

def lambda_handler(event, context):
    logger.info("Inside lambda_handler")
    try:
        logger.info("Trying handle_embed_docs")
        # Attempt to call the original handler
        return handle_embed_docs(event, context)
    except Exception as e:
        logger.info(f"handle_embed_docs failed: {str(e)}")
        # Log the directory contents upon failure
        log_directory_contents()
        # Optionally, log any other details
        logger.error(f"Error during lambda execution: {str(e)}")
        # Re-raise the exception to ensure Lambda marks the invocation as failed
        raise

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