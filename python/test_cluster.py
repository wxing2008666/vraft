from cluster import Cluster


class TestCluster:

    def test_len(self):
        cluster = Cluster()
        assert len(cluster) == 4



