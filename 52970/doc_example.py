import requests

DASHBOARD = "http://localhost:8265"

details = requests.get(f"{DASHBOARD}/api/serve/applications/").json()
applications = [
    app["deployed_app_config"]
    for app in details["applications"].values()
    if app["deployed_app_config"]  # only applications deployed from a config
]

# Change one deployment's replica count, a lightweight update.
for app in applications:
    if app["name"] == "default":
        for deployment in app.get("deployments", []):
            if deployment["name"] == "Translator":
                deployment["num_replicas"] = 3

requests.put(
    f"{DASHBOARD}/api/serve/applications/", json={"applications": applications}
).raise_for_status()
