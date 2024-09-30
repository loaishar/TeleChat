from azure.communication.identity import CommunicationIdentityClient
import os

ACS_CONNECTION_STRING = os.getenv('ACS_CONNECTION_STRING')

def create_acs_user():
    client = CommunicationIdentityClient.from_connection_string(ACS_CONNECTION_STRING)
    user = client.create_user()
    token_response = client.get_token(user, scopes=['chat'])
    return user, token_response.token
