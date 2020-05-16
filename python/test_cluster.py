from cluster import Cluster


class TestCluster:

    def test_len(self):
        cluster = Cluster()
        assert len(cluster) == 4

    def test_get(self):
        cluster = Cluster()
        for index in range(0, 4):
            assert cluster[index].id == index
            assert cluster[index].uri == f'localhost:500{index}'



