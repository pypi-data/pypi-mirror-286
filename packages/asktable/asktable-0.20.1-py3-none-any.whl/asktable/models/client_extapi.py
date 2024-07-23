from asktable.models.client_base import convert_to_object, BaseResourceList
from asktable.api import APIRequest
from atcommon.exceptions import server as errors
from atcommon.models.extapi import ExtAPICore, ExtAPIRouteCore


class ExtAPIClient(ExtAPICore):
    api: APIRequest
    endpoint: str

    def delete(self):
        return self.api.send(endpoint=f"{self.endpoint}/{self.id}", method="DELETE")

    @convert_to_object(cls=ExtAPICore)
    def update(self, name=None, base_url=None, headers=None):
        return self.api.send(
            endpoint=f"{self.endpoint}/{self.id}",
            method="POST",
            data={
                "name": name,
                "base_url": base_url,
                "headers": headers,
            },
        )

    @property
    def routes(self):
        return ExtAPIRouteList(
            api=self.api, endpoint=f"{self.endpoint}/{self.id}/routes"
        )


class ExtAPIRouteClient(ExtAPIRouteCore):
    api: APIRequest
    endpoint: str

    def delete(self):
        return self.api.send(endpoint=f"{self.endpoint}/{self.id}", method="DELETE")

    @convert_to_object(cls=ExtAPIRouteCore)
    def update(
        self,
        name=None,
        path=None,
        method=None,
        path_params_desc=None,
        query_params_desc=None,
        body_params_desc=None,
    ):
        return self.api.send(
            endpoint=f"{self.endpoint}/{self.id}",
            method="POST",
            data={
                "name": name,
                "path": path,
                "method": method,
                "path_params_desc": path_params_desc,
                "query_params_desc": query_params_desc,
                "body_params_desc": body_params_desc,
            },
        )


class ExtAPIList(BaseResourceList):
    __do_not_print_properties__ = ["tenant_id", "created_at"]

    @convert_to_object(cls=ExtAPIClient)
    def _get_all_resources(self):
        return self._get_all_resources_request()

    @convert_to_object(cls=ExtAPIClient)
    def get(self, id=None, name=None):
        if id:
            return self.api.send(endpoint=f"{self.endpoint}/{id}", method="GET")
        elif name:
            response = self.api.send(
                endpoint=self.endpoint, method="GET", params={"name": name}
            )
            data = response.get("data", [])
            if data:
                return data[0]
            else:
                raise errors.NotFound(f"Endpoint with name {name} not found")
        else:
            raise ValueError("id or name must be provided")

    @property
    @convert_to_object(cls=ExtAPIClient)
    def latest(self):
        return self._get_latest_one_or_none()

    @convert_to_object(cls=ExtAPIClient)
    def create(self, name: str, base_url: str, headers: dict = None):
        return self.api.send(
            endpoint=self.endpoint,
            method="POST",
            data={
                "name": name,
                "base_url": base_url,
                "headers": headers,
            },
        )


class ExtAPIRouteList(BaseResourceList):
    __do_not_print_properties__ = ["tenant_id", "created_at"]

    @convert_to_object(cls=ExtAPIRouteClient)
    def _get_all_resources(self):
        return self._get_all_resources_request(with_pagination=False)

    @convert_to_object(cls=ExtAPIRouteClient)
    def get(self, id=None, name=None):
        if id:
            return self.api.send(endpoint=f"{self.endpoint}/{id}", method="GET")
        elif name:
            response = self.api.send(
                endpoint=self.endpoint, method="GET", params={"name": name}
            )
            data = response.get("data", [])
            if data:
                return data[0]
            else:
                raise errors.NotFound(f"Route with name {name} not found")
        else:
            raise ValueError("id or name must be provided")

    @property
    @convert_to_object(cls=ExtAPIRouteClient)
    def latest(self):
        return self._get_latest_one_or_none()

    @convert_to_object(cls=ExtAPIRouteClient)
    def create(
        self,
        name: str,
        path: str,
        method: str,
        path_params_desc: str = None,
        query_params_desc: str = None,
        body_params_desc: str = None,
    ):
        return self.api.send(
            endpoint=self.endpoint,
            method="POST",
            data={
                "name": name,
                "path": path,
                "method": method,
                "path_params_desc": path_params_desc,
                "query_params_desc": query_params_desc,
                "body_params_desc": body_params_desc,
            },
        )
