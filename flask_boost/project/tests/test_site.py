# coding: utf-8
from .suite import BaseSuite


class TestSite(BaseSuite):
    def test_index(self):
        rv = self.client.get('/')
        assert rv.status_code == 200