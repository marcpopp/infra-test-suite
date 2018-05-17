from testHelpers import *

# Basischecks fuer alle Hosts

testinfra_hosts = [
    "all",
]

# Important OS Components installed and started
@pytest.mark.parametrize("pkg_name,service_name", [
    ("cronie-anacron", "crond"),
    ("rsyslog", None),
])
def test_software(host, pkg_name, service_name):
    check_software(host, pkg_name, service_name)

# Test available memory
def test_mem(host):
    check_nrpe(host, "check_mem")


# vim: set expandtab ts=4 sw=4 ai:
