import sys
from pathlib import Path
from mastodon import Mastodon
from dotenv import dotenv_values

REQUIRED_ARGS_AMOUNT = 4
NOW_PLAYING_STRING = "🎶 Now playing:"
module_dir = Path(__file__).parent
env_file_dir = module_dir.joinpath(".env")
config = dotenv_values(env_file_dir)

def login(user_credentials_path):
    mastodon = Mastodon(client_id='mastotunes_clientcred.secret',
                        api_base_url=config["INSTANCE_ADDRESS"])
    mastodon.log_in(config["INSTANCE_EMAIL"],
                    config["INSTANCE_PASSWORD"],
                    to_file=user_credentials_path)
    return mastodon


def setup_mastodon():
    mastodon = None

    client_cedentials_path = module_dir.joinpath(
        "mastotunes_clientcred.secret")
    user_credentials_path = module_dir.joinpath("mastotunes_usercred.secret")

    does_client_credentials_path_exist = user_credentials_path.exists()
    does_user_credentials_path_exist = client_cedentials_path.exists()

    if not does_client_credentials_path_exist:
        Mastodon.create_app(config["APPLICATION_NAME"],
                            website=config["APPLICATION_WEBSITE"],
                            api_base_url=config["INSTANCE_ADDRESS"],
                            to_file=client_cedentials_path)
        mastodon = login(user_credentials_path)

    elif not (does_user_credentials_path_exist):
        mastodon = login(user_credentials_path)

    else:
        mastodon = Mastodon(access_token=user_credentials_path,
                            api_base_url=config["INSTANCE_ADDRESS"])
    return mastodon


if len(sys.argv) is not REQUIRED_ARGS_AMOUNT:
    print("Command-line syntax error: Incorrect number of arguments")
    print("Should be in the format: <song_name> <artist_name> <link>")
    # Exit status 2 = Command line syntax error
    sys.exit(2)

song_name = sys.argv[1]
artist_name = sys.argv[2]
link = sys.argv[3]

mastodon = setup_mastodon()
created_status = mastodon.status_post(
    f'{NOW_PLAYING_STRING}\n{artist_name} - {song_name}\n{link}')

print("Status posted successfully")
print("View it here:", created_status["url"])