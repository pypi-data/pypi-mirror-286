from pathlib import Path
import logging
import json

from .git import GitRepo, GitRemote, GitUser
from .gitlab import GitlabInstance, GitlabToken, GitlabReleaseManifest
from iccore.network import HttpClient
from iccore.project import Milestone


class GitlabClient:
    def __init__(
        self,
        instance: GitlabInstance | None = None,
        token: GitlabToken | None = None,
        user: GitUser | None = None,
        local_repo: GitRepo | None = None,
        http_client: HttpClient = HttpClient(),
    ) -> None:

        self.token = token
        self.instance = instance
        self.user = user
        self.local_repo = local_repo
        self.remote_initialized = False
        self.http_client: HttpClient = http_client

    def initialize_oath_remote(self, name: str = "oath_origin"):

        err_msg = "Attempted to init oath remote with no "
        if not self.instance:
            raise RuntimeError(f"{err_msg} instance set")

        if not self.local_repo:
            raise RuntimeError(f"{err_msg} repo set")

        if not self.token:
            raise RuntimeError(f"{err_msg} token")

        url_prefix = f"https://oauth2:{self.token.value}"
        url = f"{url_prefix}@{self.instance.url}.git"
        remote = GitRemote(name, url)
        self.local_repo.add_remote(remote)

    def upload_release_asset(self, endpoint: str, token: GitlabToken, path: Path):

        logging.info("Uploading release asset %s, to %s", path, endpoint)

        headers = {token.type: token.value}
        response = self.http_client.upload_file(endpoint, path, headers)

        logging.info("Finished upload with response %s", response)

    def upload_release_manifest(
        self, endpoint: str, manifest: GitlabReleaseManifest, token: GitlabToken
    ):

        logging.info("Uploading release manifest to %s", endpoint)

        headers = {token.type: token.value}
        response = self.http_client.post_json(endpoint, headers, manifest.serialize())
        logging.info("Finished uploading manifest with response %s", response)

    def push_change(self, message: str, target_branch="main", remote_name="origin"):

        if not self.local_repo:
            return

        if not self.user:
            raise RuntimeError("Attempted to init oath remote with no user")

        self.local_repo.set_user(self.user)

        if not self.remote_initialized:
            self.initialize_oath_remote()
            self.remote_initialized = True

        self.local_repo.add_all()
        self.local_repo.commit(message)
        self.local_repo.push(remote_name, "HEAD", target_branch, "-o ci.skip")

    def set_ci_variable(self, endpoint: str, key: str, value: str, token: GitlabToken):

        logging.info("Setting CI variable %s", key)

        headers = {token.type: token.value}
        payload = f"value={value}"

        response = self.http_client.make_put_request(endpoint, headers, payload)

        logging.info("Finished setting CI variable with response %s", response)

    def download_release_package(self):
        pass

    def get_milestones(self, id: int, resource_type: str) -> list[Milestone]:
        milestones_json = self._make_request(f"{resource_type}s/{id}/milestones")
        milestones = [Milestone(j) for j in milestones_json]
        return milestones

    def _make_request(self, url: str):

        if not self.instance:
            raise RuntimeError(
                "Attempted to make api request with no Gitlab instance set"
            )

        if self.token:
            headers = {"Authorization": f"Bearer {self.token.value}"}
        else:
            headers = {}

        full_url = f"{self.instance.api_url}/{url}"
        logging.info("Making request to %s", full_url)
        logging.info(headers)
        response = self.http_client.make_get_request(full_url, headers)
        return json.loads(response)
