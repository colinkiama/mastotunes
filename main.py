import sys;
from pathlib import Path
from mastodon import Mastodon
from dotenv import dotenv_values

REQUIRED_ARGS_AMOUNT = 4;
config = dotenv_values(".env")

def login():
    mastodon = Mastodon(client_id='mastotunes_clientcred.secret',
                        api_base_url=config["INSTANCE_ADDRESS"])
    mastodon.log_in(config["INSTANCE_EMAIL"],
                    config["INSTANCE_PASSWORD"],
                    to_file='mastotunes_usercred.secret')
    return mastodon


def setup_mastodon():
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

if len(sys.argv) is not REQUIRED_ARGS_AMOUNT:
    print("Incorrect number of arguments");
    print("Should be in the format: <song_name> <artist_name> <link>")
    # Exit status 2 = Command line syntax error
    sys.exit(2);

song_name = sys.argv[1];
artist_name = sys.argv[2];
link = sys.argv[3];

mastodon = setup_mastodon();
mastodon.toot(f'{artist_name} - {song_name}\n{link}')


