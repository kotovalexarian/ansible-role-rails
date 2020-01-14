import re
import os

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    prefix = 'rails'

    private_var_names = [
        'deploy_user',
        'env',
        'gemset',
        'group',
        'root_dir',
        'ruby',
        'service',
        'user',
    ]

    common_name_re = re.compile(r'^[a-z_][a-z0-9_-]{0,30}(\$|[a-z0-9_-])?$')

    ruby_version_re = re.compile(r'^ruby-[0-9]+\.[0-9]+\.[0-9]+$')

    domain_name_re = re.compile(
        r'^(?:[a-z0-9]'  # First character of the domain
        r'(?:[a-z0-9-_]{0,61}[a-z0-9])?\.)'  # Sub domain + hostname
        r'+[a-z0-9][a-z0-9-_]{0,61}'  # First 61 characters of the gTLD
        r'[a-z0-9]$'  # Last character of the gTLD
    )

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        result['changed'] = False
        result['failed'] = False

        for var_name in self.private_var_names:
            full_var_name = '%s__%s' % (self.prefix, var_name)
            validator = getattr(self, 'validate_' + var_name)
            value = task_vars[full_var_name]
            msg_part = validator(value)

            if msg_part is not None:
                full_msg = "Invalid var '%s': %s" % (full_var_name, msg_part)
                result['failed'] = True
                result['msg'] = full_msg
                return result

        return result

    def validate_deploy_user(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.common_name_re.fullmatch(value):
            return 'has invalid format'

    def validate_env(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if value not in ['production', 'staging']:
            return 'is invalid'

    def validate_gemset(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.common_name_re.fullmatch(value):
            return 'has invalid format'

    def validate_group(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.common_name_re.fullmatch(value):
            return 'has invalid format'

    def validate_root_dir(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not os.path.isdir(os.path.dirname(value)):
            return 'is not writable directory path'

    def validate_ruby(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.ruby_version_re.fullmatch(value):
            return 'has invalid format'

    def validate_service(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.common_name_re.fullmatch(value):
            return 'has invalid format'

    def validate_user(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.common_name_re.fullmatch(value):
            return 'has invalid format'
