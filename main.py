from mastodon import Mastodon
from dotenv import dotenv_values
from pathlib import Path

config = dotenv_values(".env")


def login():
    mastodon = Mastodon(client_id='mastotunes_clientcred.secret',
                        api_base_url=config["INSTANCE_ADDRESS"])
    mastodon.log_in(config["INSTANCE_EMAIL"],
                    config["INSTANCE_PASSWORD"],
                    to_file='mastotunes_usercred.secret')
    return mastodon


def setup_mastodon():
    print(config)

    mastodon = None
    does_client_credentials_path_exist = Path(
        "mastotunes_clientcred.secret").exists()
    does_user_credentials_path_exist = Path(
        "mastotunes_usercred.secret").exists()

    if not does_client_credentials_path_exist:
        Mastodon.create_app(config["APPLICATION_NAME"],
                            api_base_url=config["INSTANCE_ADDRESS"],
                            to_file='mastotunes_clientcred.secret')
        mastodon = login()

    elif not (does_user_credentials_path_exist):
        mastodon = login()

    else:
        mastodon = Mastodon(access_token='mastotunes_usercred.secret',
                            api_base_url=config["INSTANCE_ADDRESS"])
    return mastodon


mastodon = setup_mastodon()
mastodon.toot(f'Hey from {config["APPLICATION_NAME"]}')