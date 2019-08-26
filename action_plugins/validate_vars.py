import re
import os

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    prefix = 'partynest'

    private_var_names = [
        'deploy_user',
        'group',
        'root_dir',
        'service',
        'user',
        'postgresql_host',
        'postgresql_port',
        'postgresql_db',
        'postgresql_user',
    ]

    common_name_re = re.compile(r'^[a-z_][a-z0-9_-]{0,30}(\$|[a-z0-9_-])?$')

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

    def validate_postgresql_host(self, value):
        if not isinstance(value, str):
            return 'is not str'

    def validate_postgresql_port(self, value):
        if not isinstance(value, int):
            return 'is not integer'
        if not (value > 0 and value < 2**16):
            return 'not in range'

    def validate_postgresql_db(self, value):
        if not isinstance(value, str):
            return 'is not str'

    def validate_postgresql_user(self, value):
        if not isinstance(value, str):
            return 'is not str'
