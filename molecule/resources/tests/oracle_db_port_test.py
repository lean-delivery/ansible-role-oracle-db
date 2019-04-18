def test_oracledb_is_listening(host):
    assert len(host.socket("tcp://1521").clients) is not 0 or len(host.socket("tcp://1522").clients) is not 0
