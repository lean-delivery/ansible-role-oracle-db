def test_oracledb_service(host):
    with host.sudo():
        assert host.service("oracledb").is_running
