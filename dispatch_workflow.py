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
    auth = {
        "Authorization": f"Token {token}",
        "Accept": "application/vnd.github.everest-preview+json"
    }
    print("Got bot access token")
    return auth


def main():
    private_key = os.environ["APP_PRIVATE_KEY"]
    installation_id = os.environ["INSTALLATION_ID"]
    repo = os.environ["TARGET_REPO"]
    workflow_name = os.environ["TARGET_WORKFLOW"]

    jwt_token = make_jwt_token(private_key)
    auth = prep_auth(jwt_token, installation_id)
    workflows = requests.get(
        f"https://api.github.com/repos/{repo}/actions/workflows", headers=auth
    ).json()
    for workflow in workflows["workflows"]:
        if workflow["name"] == workflow_name:
            res = requests.post(
                f"https://api.github.com/repos/{repo}/actions/workflows/{workflow['id']}/dispatches",
                headers=auth,
                json={"ref": "master"},
            )
            print(
                f"Dispatched workflow {workflow_name} for {repo}. status={res.status_code}, text={res.text}"
            )
            sys.exit(0)
    else:
        print(f"Unable to find workflow {workflow_name} in {repo}")
        sys.exit(-1)


if __name__ == "__main__":
    main()
