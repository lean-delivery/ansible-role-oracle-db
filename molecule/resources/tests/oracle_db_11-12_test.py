def test_oracledb_is_listening(host):
    assert len(host.socket("tcp://1522").clients) != 0
