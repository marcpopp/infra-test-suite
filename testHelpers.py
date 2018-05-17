import pytest

# check_software(host, name)
# Parameter:
#   host:       the testinfra host object
#   name:       the name of the software package
#   service_name:       the name of the service of the software
#
def check_software(host, pkg_name, service_name=None):
    if service_name is None:
        service_name = pkg_name
    pkg = host.package(pkg_name)
    assert pkg.is_installed
    service = host.service(service_name)
    assert service.is_enabled
    assert service.is_running


# check_nrpe(host, check_name)
# Parameter:
#   host:       the testinfra host object
#   check_name: the name of the nrpe check to run
# Returns:
#   the check output
#
def check_nrpe(host, check_name):
    # Read NRPE config
    command = host.file("/etc/nrpe.d/%s.cfg" % check_name).content_string\
    # Remove the definition part (everything before the first '=') and only use the command
    tmp = command.split('=')
    tmp.pop(0) # Remove first item from list tmp
    command = "=".join(tmp)
    # Execute the command on the host
    return host.check_output(command)


# get_ansible_variable(self, host, variable_name)
# Parsing the templates in an ansible variable is a bit tricky
# Parameter:
#   host:          the testinfra host object
#   variable_name: the ansible variable to return
def get_ansible_variable(host, variable_name):
    return host.check_output( "echo %s" % host.ansible.get_variables()[variable_name] )


# vim: set expandtab ts=4 sw=4 ai:
