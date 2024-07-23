from . import ContainerImageList, ContainerImage
import logging
import os
import tempfile
import requests
import tarfile
import typer

from docker import DockerClient

logger = logging.getLogger("otimages." + os.path.basename(__file__))


class CSAIImages(ContainerImageList):
    def __init__(
        self,
        docker_client: DockerClient,
        version: str,
        repository: str = "artifactory.otxlab.net",
        path: str = "/ot2-paas-dev/csai/",
        helm_base_url: str = "https://artifactory.otxlab.net/artifactory/ot2-helm-dev/csai",
        helm_dir: str = "",
        latest: bool = False,
    ):
        self.version = version
        self.repository = repository
        self.docker_client = docker_client
        self.helm_base_url = helm_base_url
        self.path = path
        self.latest = latest

        if helm_dir == "":
            self.helm_dir = self.helm_base_url + "/csai-" + self.version + ".tgz"
        else:
            self.helm_dir = helm_dir

        self.images = self.__get_images()

    def __get_images(self):

        logger.info(
            "Running helm template for %s in %s",
            self.version,
            self.helm_dir,
        )

        command = f"helm template {self.helm_dir} --set global.imageSource=registry.opentext.com| yq '..|.image? | select(.)' | sort -u | grep registry.opentext.com | sed 's/registry.opentext.com\///g'"
        logger.debug("%s", command)
        images = os.popen(command).readlines()

        assert images != []

        all_images = []

        for image in images:
            name = image.split(":")[0]
            version = image.split(":")[1]
            version_overwrite = version

            all_images.append(
                ContainerImage(
                    repository=self.repository,
                    path=self.path,
                    name=name,
                    version=version,
                    version_overwrite=version_overwrite,
                    docker_client=self.docker_client,
                )
            )

        return all_images
