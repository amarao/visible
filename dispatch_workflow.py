#!/usr/bin/python3
import jwt
import time
import requests
import os
import sys


def make_jwt_token(private_key):
    jwt_payload = {
        "iat": int(time.time()),
        "exp": int(time.time() + 600),
        "iss": 112156,
    }
    print("Getting app JWT")
    jwt_token = jwt.encode(jwt_payload, private_key, algorithm="RS256").decode()
    print("Got app JWT")
    return jwt_token


def prep_auth(jwt_token, installation_id):
    print("Getting bot access token")
    token = requests.post(
        f"https://api.github.com/app/installations/{installation_id}/access_tokens",
        headers={"Authorization": f"Bearer {jwt_token}"},
    ).json()["token"]
    auth = {"Authorization": f"Token {token}"}
    print("Got bot access token")
    return auth


def main():
    private_key = os.environ["APP_PRIVATE_KEY"]
    installation_id = os.environ["INSTALLATION_ID"]
    jwt_token = make_jwt_token(private_key)
    auth = prep_auth(jwt_token, installation_id)

    repo = "amarao/hiddentruth"
    workflow_name = "CI"
    workflows = requests.get(
        f"https://api.github.com/repos/{repo}/actions/workflows", headers=auth
    ).json()
    for workflow in workflows["workflows"]:
        if workflow["name"] == workflow_name:
            requests.post(
                f"https://api.github.com/repos/{repo}/actions/workflows/{workflow['id']}/dispatches"
            )
            print(f"Dispatched workflow {workflow_name} for {repo}")
            sys.exit(0)
    else:
        print(f"Unable to find workflow {workflow_name} in {repo}")
        sys.exit(-1)


if __name__ == "__main__":
    main()
