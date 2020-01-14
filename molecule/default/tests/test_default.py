import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize(
    'service_name',
    [
        'rails.service',
        'rails-restart.service',
        'rails-restart.path',
        'rails-puma.service',
        'rails-sidekiq.service',
    ],
)
def test_services(host, service_name):
    assert host.service(service_name).is_enabled
