from oocas.process import Process


def test_process():
    fn = Process()
    x = [1, 2, 3]
    assert fn(x) == x
