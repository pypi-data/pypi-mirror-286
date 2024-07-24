import requests
import yaml

# requests.post("https://localhost:5056/api/v1/fleet/login", json={"email": "admin@mycroft.io", "password": "Loyal-Message-Pronounce-Anyway-7"}, verify=False)


class FleetDM:
    def __init__(self, url, verify=None):
        self.url = url
        self.verify = verify

        self.email = None
        self.password = None
        self.token = None

    def login(self, email, password):
        resp = self.post("fleet/login", data={"email": email, "password": password})
        if resp.status_code == 200:
            self.email = email
            self.password = password
            self.token = resp.json()["token"]
            return True
        return False

    def relogin(self):
        return self.login(self.email, self.password)

    def logout(self):
        return self.post("fleet/logout")

    def _headers(self):
        if self.token is not None:
            return {"Authorization": f"Bearer {self.token}"}

    def _raw_get(self, endpoint, version):
        return requests.get(
            f"{self.url}/api/{version}/{endpoint}",
            headers=self._headers(),
            verify=self.verify,
        )

    def get(self, endpoint, version="v1"):
        resp = self._raw_get(endpoint, version)
        if resp.status_code == 401 and self.email:
            self.relogin()
            return self._raw_get(endpoint, version)
        return resp

    def _raw_post(self, endpoint, data, version):
        return requests.post(
            f"{self.url}/api/{version}/{endpoint}",
            headers=self._headers(),
            json=data,
            verify=self.verify,
        )

    def post(self, endpoint, data=None, version="v1"):
        resp = self._raw_post(endpoint, data, version)
        if resp.status_code == 401 and self.email:
            self.relogin()
            return self._raw_post(endpoint, data, version)
        return resp

    def standard_query_library(self):
        resp = requests.get(
            "https://raw.githubusercontent.com/fleetdm/fleet/main/docs/01-Using-Fleet/standard-query-library/standard-query-library.yml"
        )
        if resp.status_code == 200:
            return [
                yaml.safe_load(s)["spec"]
                for s in resp.content.decode("utf-8").split("---\n")
                if s
            ]

    def add_query(self, query, name, description, platform, interval=None):
        if interval is None:
            interval = 60 * 60
        return self.post(
            "fleet/queries",
            data={
                "query": query,
                "name": name,
                "description": description,
                "interval": interval,
                "platform": platform,
            },
        )

    def hosts(self):
        resp = self.get("fleet/hosts")
        if resp.status_code == 401:
            raise PermissionError()
        if resp.status_code == 200:
            return resp.json()["hosts"]
        raise Exception(resp.status_code, resp.content)

    def host_livequery(self, host, query):
        resp = self.post(f"fleet/hosts/{host['id']}/query", data={"query": query})
        if resp.status_code == 401:
            raise PermissionError()
        if resp.status_code == 200:
            return resp.json()
        raise Exception(resp.status_code, resp.content)

    def host_encrypted(self, host):
        if host["platform_like"] == "windows":
            query = "SELECT 1 FROM bitlocker_info WHERE drive_letter='C:' AND protection_status=1;"
        elif host["platform_like"] == "darwin":
            query = """SELECT 1 FROM disk_encryption WHERE user_uuid IS NOT "" AND filevault_status = 'on' LIMIT 1;"""
        elif host["platform_like"] == "debian":
            query = "SELECT 1 FROM disk_encryption WHERE encrypted=1 AND name LIKE '/dev/dm-1';"
        return self.host_livequery(host, query)
