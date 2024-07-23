from racs.racs_exceptions import NoUpdatesMadeException, FailedDeletePostException
import warnings
import requests
import json


class Racs:
    def __init__(
            self,
            resource: str | None = None,
            dataset: str | None = None
    ):
        self.resource = resource
        self.dataset = dataset
        self.headers = {'Content-Type': 'application/json'}
        self.base_url = "https://racs.rest/v3"

        if not self.resource:
            raise ValueError("resource can't be None")

        if not self.dataset:
            raise ValueError("dataset can't be None")

    def create_post(
            self,
            data: dict | None = None
    ):
        if not data:
            raise ValueError('Argument "data" is required')
        url: str = f"{self.base_url}?resource={self.resource}&dataset={self.dataset}"
        payload = json.dumps(data)

        return requests.post(url, headers=self.headers, data=payload).json()

    def create_file(
            self,
            file_path: str | None = None
    ):
        if not file_path:
            raise ValueError('Argument "file_path" is required')

        url: str = f"{self.base_url}?resource={self.resource}&dataset={self.dataset}"
        headers = {"Content-Type": "application/json"}

        with open(file_path, 'rb') as file:
            files = {'file': file}
            req = requests.post(url, files=files, headers=headers)

        return req.json()

    def read_post_by_id(
            self,
            post_id: str | None = None
    ):
        if not post_id:
            raise ValueError('Argument "post_id" is required')

        url: str = f"{self.base_url}/{post_id}?resource={self.resource}&dataset={self.dataset}"

        return requests.get(url=url, headers=self.headers).json()

    def read_post_by_filter(
            self,
            filter_data: dict | None = None,
            sort: dict | None = {"_created": -1},
            limit: int | None = 1
    ):

        if not filter_data:
            raise ValueError('Argument "filter_data" is required')

        url: str = f"{self.base_url}/get?resource={self.resource}&dataset={self.dataset}"
        payload = json.dumps({
            "filter": filter_data,
            "sort": sort,
            "limit": limit
        })
        print(payload)
        res = requests.post(url=url, headers=self.headers, data=payload).json()
        return res

    def read_file_by_id(
            self,
            post_id: str | None = None
    ):
        if not post_id:
            raise ValueError('Argument "post_id" is required')

        url: str = f"{self.base_url}/file/{post_id}?resource={self.resource}&dataset={self.dataset}"

        headers = {"Accept": "application/octet-stream"}

        return requests.get(url, headers).json()

    def update_post_by_id(
            self,
            post_id: str | None = None,
            update_options: dict | None = None
    ):
        if not post_id:
            raise ValueError('Argument "post_id" is required')
        if not update_options:
            raise ValueError('Argument "update_options" is required')

        url: str = f'{self.base_url}/{post_id}?resource={self.resource}&dataset={self.dataset}'
        payload = json.dumps({
            "update": {
                "$set": update_options
            }
        })

        res = requests.patch(url, headers=self.headers, data=payload).json()
        if res["matchedCount"] == 0 and res["modifiedCount"] == 0:
            raise NoUpdatesMadeException(res)
        elif res["matchedCount"] > res["modifiedCount"]:
            warnings.warn(f"Warning: matchedCount ({res['matchedCount']})"
                          f" is greater than modifiedCount ({res['modifiedCount']}).")

        return res

    def update_post_by_filter(
            self,
            filter_data: dict | None = None,
            update_options: dict | None = None
    ):
        if not filter_data:
            raise ValueError('Argument "filter_data" is required')
        if not update_options:
            raise ValueError('Argument "update_options" is required')

        url: str = f"{self.base_url}?resource={self.resource}&dataset={self.dataset}"
        payload = json.dumps({
            "filter": filter_data,
            "update": {
                "$set": update_options
            }
        })

        res = requests.patch(url, headers=self.headers, data=payload).json()
        if res["matchedCount"] == 0 and res["modifiedCount"] == 0:
            raise NoUpdatesMadeException(res)
        elif res["matchedCount"] > res["modifiedCount"]:
            warnings.warn(f"Warning: matchedCount ({res['matchedCount']})"
                          f" is greater than modifiedCount ({res['modifiedCount']}).")

        return res

    def delete_post_by_id(
            self,
            post_id: str | None = None
    ):
        if not post_id:
            raise ValueError('Argument "post_id" is required')

        url = f"{self.base_url}/{post_id}?resource={self.resource}&dataset={self.dataset}"
        res = requests.delete(url, headers=self.headers).json()
        if res["deletedCount"] == 0:
            raise FailedDeletePostException(res)

        return res

    def delete_post_by_filter(
            self,
            filter_data: dict | None = None
    ):
        if not filter_data:
            raise ValueError('Argument "filter_data" is required')

        url = f"{self.base_url}?resource={self.resource}&dataset={self.dataset}"
        payload = json.dumps({
            "filter": filter_data
        })

        res = requests.delete(url, headers=self.headers, data=payload).json()

        if res["deletedCount"] == 0:
            raise FailedDeletePostException(res)

        return res
