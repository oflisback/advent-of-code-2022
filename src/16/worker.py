from collections import defaultdict


class Worker:
    def __init__(
        self,
        cur="AA",
        path=["AA"],
        points_at_minute=[0],
        minute=1,
        node_sum_map=defaultdict(lambda: 0),
    ):
        self._cur = cur
        self._path = path.copy()
        self._points_at_minute = points_at_minute.copy()
        self._minute = minute
        self._node_sum_map = node_sum_map.copy()

    @property
    def cur(self):
        return self._cur

    @cur.setter
    def cur(self, value):
        self._cur = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def points_at_minute(self):
        return self._points_at_minute

    @points_at_minute.setter
    def points_at_minute(self, value):
        self._points_at_minute = value

    @property
    def minute(self):
        return self._minute

    @minute.setter
    def minute(self, value):
        self._minute = value

    @property
    def node_sum_map(self):
        return self._node_sum_map

    @node_sum_map.setter
    def node_sum_map(self, value):
        self._node_sum_map = value
