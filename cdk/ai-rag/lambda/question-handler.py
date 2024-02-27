from questions import answer_question

def handle_question(event, context):
    # save event to logs
    print(event)

    question = event['body']['question']

    answer = answer_question(question=question)

    return {
        'statusCode': 200,
        'body': answer
    }