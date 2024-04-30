from google.cloud import secretmanager

def get_secret(project_id: str, secret_id: str, version: str = "1") -> secretmanager.GetSecretRequest:

    client = secretmanager.SecretManagerServiceClient()

    name = client.secret_version_path(project_id, secret_id, version)

    response = client.access_secret_version(name=name)

    return response.payload.data.decode("UTF-8")