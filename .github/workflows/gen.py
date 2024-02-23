original = """
name: "deploy"

"on":
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-20.04
    steps:
      - name: Checkout
        uses: actions/checkout@v3
"""

import yaml


for a in range(0, 99999):
    w = yaml.safe_load(original)
    w["name"] = f"example_{a:05}"
    with open(f"example_{a:05}.yaml", "w") as f:
        f.write(yaml.dump(w))
