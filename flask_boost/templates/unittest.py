# coding: utf-8
from .suite import BaseSuite


class Test#{controller|title}(BaseSuite):
    def test_action(self):
        rv = self.client.get('/#{controller}/action')
        assert rv.status_code == 200
