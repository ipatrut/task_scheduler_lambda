
def get_path_parameters(event):
    try:
        parameters = event['pathParameters']
    except KeyError:
        try:
            parameters = event['path']
        except KeyError:
            parameters = {}
    return parameters

def get_query_parameters(event):
    try:
        parameters = event['queryStringParameters']
    except KeyError:
        parameters = {}

    return parameters