from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'geco2studios'  # Must be replaced by your <storage_account_name>
    azure_container = 'studios'
    expiration_secs = None
