def oracledb_service_is_running(host):
    assert host.service('oracledb').is_running
