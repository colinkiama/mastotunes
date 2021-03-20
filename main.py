from mastodon import Mastodon
from dotenv import dotenv_values

config = dotenv_values(".env");
print(config)

Mastodon.create_app(
     config["APPLICATION_NAME"],
     api_base_url = config["INSTANCE_ADDRESS"],
     to_file = 'mastotunes_clientcred.secret'
)

mastodon = Mastodon(
    client_id = 'mastotunes_clientcred.secret',
    api_base_url = config["INSTANCE_ADDRESS"]
)

mastodon.log_in(
    config["INSTANCE_EMAIL"],
    config["INSTANCE_PASSWORD"],
    to_file = 'mastotunes_usercred.secret'
)

mastodon.toot(f'{config["APPLICATION_NAME"]} is ready!')