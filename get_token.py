#!/usr/bin/python3
import jwt
import time
import requests
import os
import sys
import time


def make_jwt_token(private_key, app_id):
    jwt_payload = {
        "iat": int(time.time()),
        "exp": int(time.time() + 600),
        "iss": int(app_id),
    }
    print("Getting app JWT")
    jwt_token = jwt.encode(jwt_payload, private_key, algorithm="RS256").decode()
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


def main():
    private_key = os.environ["APP_PRIVATE_KEY"]
    app_id = os.environ["APP_ID"]
    github_env_file = os.environ["GITHUB_ENV"]  # https://docs.github.com/en/actions/reference/workflow-commands-for-github-actions#setting-an-environment-variable
    jwt_token = make_jwt_token(private_key, app_id)
    ghs_token = get_token(jwt_token, get_installation_id(jwt_token))
    print(f"::add-mask::SECRET_LEAK")
    print(f"::set-output name=ghs_token::{ghs_token}")
    print(f"::add-mask::{ghs_token}")
    print(f"::set-output name=leak::SECRET_LEAK")
    print("Set output variable ghs_token")


if __name__ == "__main__":
    main()
