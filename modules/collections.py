import config


def extract_collection(request):
    return request.path[len(config.rest.root):]


def get_collection(request):
    collection = extract_collection(request)
    if collection:
        if '/' in collection:
            collection = collection[:collection.index('/')]
        return collection
    return config.collections
