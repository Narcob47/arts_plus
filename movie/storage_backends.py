from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'geco2studios'  # Must be replaced by your <storage_account_name>
    AZURE_ACCOUNT_KEY = "2VqmDrYoffc1YwvH1+4aSTfbhoPf/YLJuJGpM0lkIJ/F5nzkC7AS8VFOicN/lXUU9zJRs12RLSKJ+AStgxnCVA=="
    azure_container = 'studios'
    expiration_secs = None
