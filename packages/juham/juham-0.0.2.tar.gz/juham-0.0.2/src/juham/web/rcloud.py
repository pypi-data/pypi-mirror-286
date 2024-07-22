import requests
from typing import Any
from juham.web.rthread import RThread, IWorkerThread


class RCloudThread(IWorkerThread):
    """Base class for thread that query data from clouds and other web
    resources via url.

    Can be configured how often the query is being run.
    """

    timeout: float = 60

    def __init__(self, client=None):
        super().__init__()

    def make_url(self) -> str:
        """Build http url for acquiring data from the web resource. Up to the
        sub classes to implement.

        This method is periodically called by update method.

        Returns: Url to be used as parameter to requests.get().
        """
        return ""

    def update(self) -> bool:
        """Acquire and process.

        This method is periodically called to acquire data from a the configured web url
        and publish it to respective MQTT topic in the process_data() method.

        Returns: True if the update succeeded. Returning False implies an error and
        in which case the method should be called shortly again to retry. It is up
        to the caller to decide the number of failed attempts before giving up.
        """

        headers: dict = {}
        params: dict = {}
        url = self.make_url()

        try:

            response = requests.get(
                url, headers=headers, params=params, timeout=self.timeout
            )

            if response.status_code == 200:
                self.process_data(response)
                return True
            else:
                self.error(f"Reading {url}  failed: {str(response)}")
        except Exception as e:
            self.error(f"Requesting data from {url} failed", str(e))
        return False

    def process_data(self, data: Any) -> None:
        """Process the acquired data.

        This method is called from the update method, to process the
        data from the acquired data source. It is up to the sub classes
        to implement this.
        """

    @classmethod
    def register(cls):
        IWorkerThread.register()


class RCloud(RThread):
    """Base class for automation objects that query data using a URL.

    Spawns an asynchronous thread to acquire data at a specified time
    interval.
    """

    @classmethod
    def register(cls):
        RThread.register()
