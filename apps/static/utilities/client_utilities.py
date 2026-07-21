from apps.res.models import ClientExtension


# def get_client_extension(client_id: str):
#     client_extension, created = ClientExtension.objects.update_or_create(
#         client_id=client_id,
#         defaults={
#             'client_id': client_id}
#     )
#     return client_extension
def get_client_extension(client_id: str):
    client_extension, _ = ClientExtension.objects.get_or_create(
        client_id=client_id
    )
    return client_extension