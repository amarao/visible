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


for a in range(2, 501):
    w = yaml.safe_load(original)
    w["name"] = f"example_{a}"
    with open(f"example_{a}.yaml", "w") as f:
        f.write(yaml.dump(w))
