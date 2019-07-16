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
    ]

    common_name_re = re.compile(r'^[a-z_][a-z0-9_-]{0,30}(\$|[a-z0-9_-])?$')

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        result['changed'] = False
        result['failed'] = False

        for var_name in self.private_var_names:
            validator = self.getattr('validate_' + var_name)
            value = task_vars[var_name]
            msg_part = validator(value)

            if msg_part is not None:
                full_msg = \
                    'Invalid var "%s__%s": %s' % (self.prefix, var_name, msg)
                result['failed'] = True
                result['msg'] = full_msg
                return result

        return result

    def validate_deploy_user(value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.common_name_re.fullmatch(value):
            return 'has invalid format'

    def validate_group(value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.common_name_re.fullmatch(value):
            return 'has invalid format'

    def validate_root_dir(value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.is_dir_path(value):
            return 'is not writable directory path'

    def validate_service(value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.common_name_re.fullmatch(value):
            return 'has invalid format'

    def validate_user(value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.common_name_re.fullmatch(value):
            return 'has invalid format'

    def is_dir_path(value):
        return os.path.isdir(value) or \
                not os.path.exists(value) and \
                os.access(os.path.dirname(value), os.W_OK)
