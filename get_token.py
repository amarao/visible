import jwt
import time
import requests
import os
import sys


def make_jwt_token(private_key, app_id):
    jwt_payload = {
        "iat": int(time.time()),
        "exp": int(time.time() + 600),
        "iss": int(app_id),
    }
    print("Getting app JWT")
    jwt_token = jwt.encode(jwt_payload, private_key, algorithm="RS256")
    if isinstance(jwt_token, bytes):
        jwt_token = jwt_token.decode()
    print("Got app JWT")
    return jwt_token


def get_installation_id(jwt_token):

    return requests.get(
        "https://api.github.com/app/installations",
        headers={"Authorization": f"Bearer {jwt_token}"},
    ).json()[0]["id"]


def get_token(jwt_token, installation_id):
    print("Getting bot access token")
    token = requests.post(
        f"https://api.github.com/app/installations/{installation_id}/access_tokens",
        headers={"Authorization": f"Bearer {jwt_token}"},
    ).json()["token"]
    print("Got bot access token")
    return token


def mask(value):
    if not os.environ.get("GITHUB_ACTIONS"):
        print("error: GITHUB_ACTIONS is not detected", file=sys.stderr)
        sys.exit(1)
    print(f"::add-mask::{value}")


def set_env(key, value):
    output_file = os.environ.get("GITHUB_ENV")
    if not output_file:
        print("Unable to get GITHUB_ENV file name")
        sys.exit(1)
    with open(output_file, "ta") as f:
        f.write(f"{key}={value}\n")


def main():
    private_key = os.environ["PRIVATE_KEY"]
    app_id = "338962"
    jwt_token = make_jwt_token(private_key, app_id)
    ghs_token = get_token(jwt_token, get_installation_id(jwt_token))
    mask(ghs_token)
    set_env("ghs_token", ghs_token)


if __name__ == "__main__":
    main()
