from typing import Optional, List
from pydantic import BaseModel, Field
from .model import HSAPICall
from .schemas import v1Route


class v1ListRoutesResponse(BaseModel):
    routes: Optional[List[Optional[v1Route]]] = Field(
        alias="routes", default=None)


class Route(HSAPICall):

    objectPath = "routes"

    def list(self) -> v1ListRoutesResponse:
        response = self.call('get')
        return v1ListRoutesResponse(**response.json())

    def delete(self, routeId: str) -> None:
        self.call('delete', call_path=routeId)

    def enable(self, routeId: int) -> None:
        self.call('post', f'{routeId}/enable')

    def disable(self, routeId: int) -> None:
        self.call('post', f'{routeId}/disable')
