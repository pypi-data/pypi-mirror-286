from .utils import CallbackContext, tool_ui_callback
from typing import Dict, List


@tool_ui_callback
def list_pinecone_connections(context: CallbackContext) -> List[Dict[str, str]]:
    connections = context.ml_client.connections._operation.list(
        workspace_name=context.workspace_name,
        cls=lambda objs: objs,
        category=None,
        **context.ml_client.connections._scope_kwargs)

    options = []
    for connection in connections:
        if connection.properties.category == "CustomKeys":
            # Legacy pinecone connections are defined by `environment` and `project_id` metadata keys.
            if 'environment' in connection.properties.metadata and 'project_id' in connection.properties.metadata:
                options.append({'value': connection.name, 'display_value': connection.name})
            # Newer pinecone connections are defined by `connection_type=vectorindex` and `index_type=pinecone`
            elif connection.properties.metadata.get("connection_type") == "vectorindex" and\
                    connection.properties.metadata.get("index_type") == "pinecone":
                options.append({'value': connection.name, 'display_value': connection.name})

    return options


@tool_ui_callback
def list_pinecone_indices(context: CallbackContext, pinecone_connection_name: str) -> List[Dict[str, str]]:
    selected_connection = context.ml_client.connections._operation.get(
        workspace_name=context.workspace_name,
        connection_name=pinecone_connection_name,
        **context.ml_client.connections._scope_kwargs)

    url = f'https://management.azure.com{context.arm_id}' +\
        f'/connections/{selected_connection.name}/listSecrets?api-version=2022-01-01-preview'
    auth_header = f'Bearer {context.credential.get_token("https://management.azure.com/.default").token}'

    secrets_response = context.http.post(url, headers={'Authorization': auth_header}).json()
    pinecone_api_key = secrets_response.get('properties', {}).get('credentials', {}).get('keys', {}).get('api_key')

    list_indices_url = 'https://api.pinecone.io/indexes'
    indices_response = context.http.get(list_indices_url, headers={'Api-Key': pinecone_api_key}).json()

    return [{'value': index["name"], 'display_value': index["name"]} for index in indices_response["indexes"]]
