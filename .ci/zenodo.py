# -*- coding: utf-8 -*-
# Python wrapper for the Zenodo REST API
# http://developers.zenodo.org/#rest-api


import datetime
import pathlib
import tomli

import argparse
import requests
import re
from typing import Optional, Iterable, Dict, List, Tuple
import logging


logger = logging.getLogger(__name__)


class Zenodo:
    """A wrapper around the Zenodo API"""

    def __init__(
        self, access_token: str, sandbox: bool = False, zenodo_url: Optional[str] = None
    ) -> None:
        self.access_token = access_token

        if zenodo_url is None:
            sandbox_subdomain = "sandbox." if sandbox else ""
            self.zenodo_url = f"https://{sandbox_subdomain}zenodo.org"
        else:
            self.zenodo_url = zenodo_url

    @property
    def api_base(self):
        return f"{self.zenodo_url}/api"

    @property
    def depositions_base(self):
        return f"{self.api_base}/deposit/depositions"

    def raise_for_status(self, response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logger.error(f"An error occured: {err}")
            logger.error(f"error message: {err.response.text}")
            raise

    def _update(self, deposit_id: str) -> Tuple:
        """Create a new version of the given record with the given files."""

        # prepare a new version based on the previous one
        # see: https://developers.zenodo.org/#new-version)
        response = requests.post(
            f"{self.depositions_base}/{deposit_id}/actions/newversion",
            params={"access_token": self.access_token},
        )
        self.raise_for_status(response)

        # parse the response to get the deposit if of the new version
        new_deposit_id = response.json()["links"]["latest_draft"].split("/")[-1]

        # get metadata associated with the new version
        # see: https://developers.zenodo.org/#retrieve
        response = requests.get(
            f"{self.depositions_base}/{new_deposit_id}",
            params={"access_token": self.access_token},
        )
        self.raise_for_status(response)
        new_deposit_data = response.json()

        return new_deposit_id, new_deposit_data

    def _create(self) -> str:
        # post an empty request to optain a deposit id
        response = requests.post(
            self.depositions_base,
            json={},
            params={"access_token": self.access_token},
        )

        self.raise_for_status(response)

        deposition_id = response.json()["id"]

        return deposition_id

    def create_or_update(
        self,
        metadata: Dict,
        paths: Iterable[pathlib.Path],
        publish: bool = False,
        deposit_id: Optional[str] = None,
    ) -> requests.Response:
        """Create a new or update an existing record on Zenodo

        Args:
            metadata (Dict): Zenodo metadata
            paths (Iterable[pathlib.Path]): path to the files to archive
            publish (bool, optional): auto publish the record without any manual validation. Defaults to False.
            deposit_id (Optional[str], optional): ID of a existing record on Zenodo. If no ID is provided, a new one will be created. Defaults to None.

        Raises:
            Exception: _description_
            ValueError: _description_

        Returns:
            requests.Response: _description_
        """

        if deposit_id:
            new_deposition_id, new_deposition_data = self._update(deposit_id)

            # get the metadata from previous versions
            data = new_deposition_data

            # and update the dict with new values
            data["metadata"] = {**new_deposition_data["metadata"], **metadata}

        else:
            data = {"metadata": metadata}
            new_deposition_id = self._create()

        response = requests.put(
            f"{self.depositions_base}/{new_deposition_id}",
            json=data,
            params={"access_token": self.access_token},
        )

        self.raise_for_status(response)

        json_response = response.json()
        bucket = json_response.get("links", {}).get("bucket")
        if bucket is None:
            raise ValueError(f"No bucket in response. Got: {json_response}")

        self._upload_files(bucket=bucket, paths=paths)

        if publish:
            return self.publish(json_response["id"])
        else:
            return response

    def publish(self, deposit_id: str) -> requests.Response:
        """Publish the project"""

        response = requests.post(
            f"{self.depositions_base}/{deposit_id}/actions/publish",
            params={"access_token": self.access_token},
        )
        self.raise_for_status(response)
        return response

    def _upload_files(
        self,
        *,
        bucket: str,
        paths: Iterable[pathlib.Path],
    ) -> List[requests.Response]:

        response_list = []
        # see https://developers.zenodo.org/#quickstart-upload
        for path in paths:
            with open(path, "rb") as file:
                response = requests.put(
                    f"{bucket}/{path.name}",
                    data=file,
                    params={"access_token": self.access_token},
                )

            self.raise_for_status(response)
            response_list.append(response)
        return response_list


def get_author_name(author):
    match = re.match(r"(.+) <(.+)>", author.strip())

    try:
        name = match.groups()[0]
    except Exception as e:
        raise RuntimeError(
            f'An error occurred during authors parsing: "{author}". Authors shall match the following pattern: "my name <my.mail@mail.com>"'
        ) from e

    return name


def make_metadata(project_root_path):
    with open(project_root_path / "pyproject.toml", "rb") as f:
        data = tomli.load(f)
        project_metadata = data["tool"]["poetry"]

    creators = [
        {"name": get_author_name(author)} for author in project_metadata["authors"]
    ]

    metadata = {
        "title": project_metadata["name"],
        "upload_type": "software",
        "version": project_metadata["version"],
        "publication_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "description": project_metadata["description"],
        "keywords": ["python", *project_metadata["keywords"]],
        "access_right": "open",
        "license": project_metadata["license"],
        "creators": creators,
    }

    return metadata


def deposit(
    *,
    project_root_path: pathlib.Path,
    zenodo_url: Optional[str],
    access_token: str,
    deposit_id,
    archive_filepath: pathlib.Path,
    publish=False,
    sandbox,
):
    metadata = make_metadata(project_root_path)

    client = Zenodo(access_token=access_token, sandbox=sandbox, zenodo_url=zenodo_url)

    client.create_or_update(
        metadata=metadata,
        paths=[archive_filepath],
        deposit_id=deposit_id,
        publish=publish,
    )


if __name__ == "__main__":
    parser = parser = argparse.ArgumentParser(description="Zenodo client.")
    parser.add_argument(
        "--zenodo-url", default=None, help="Override the default Zenodo URL"
    )
    parser.add_argument(
        "--sandbox",
        action="store_true",
        help="Use the sandbox URL as the default Zenodo URL",
    )
    parser.add_argument(
        "--publish", action="store_true", help="Auto publish the new project version"
    )
    parser.add_argument(
        "-p",
        "--root-project-path",
        required=True,
        type=pathlib.Path,
        help="Path to the root directory containing the pyproject.toml file",
    )
    # token shall be something like: amdIeOkXJAgveMxJtkAiDHZGr1e3jhA7QqWHsCNVqPtRc2YjwFH9CJ2hpwmA
    parser.add_argument(
        "-t", "--token", required=True, type=pathlib.Path, help="Zenodo access token"
    )
    parser.add_argument(
        "-id",
        "--deposit-id",
        required=False,
        type=pathlib.Path,
        help="Project ID used on Zenodo",
    )
    parser.add_argument(
        "-a",
        "--archive-filepath",
        type=pathlib.Path,
        required=True,
        help="Path to the project archive file",
    )

    args = parser.parse_args()

    deposit(
        project_root_path=args.root_project_path,
        zenodo_url=args.zenodo_url,
        sandbox=args.sandbox,
        access_token=args.token,
        deposit_id=args.deposit_id,
        archive_filepath=args.archive_filepath,
        publish=args.publish,
    )
