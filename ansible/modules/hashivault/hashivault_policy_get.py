#!/usr/bin/env python
DOCUMENTATION = '''
---
module: hashivault_policy_get
version_added: "2.1.0"
short_description: Hashicorp Vault policy get module
description:
    - Module to get a policy from Hashicorp Vault.
options:
    url:
        description:
            - url for vault
        default: to environment variable VAULT_ADDR
    verify:
        description:
            - verify TLS certificate
        default: to environment variable VAULT_SKIP_VERIFY
    authtype:
        description:
            - "authentication type to use: token, userpass, github, ldap"
        default: token
    token:
        description:
            - token for vault
        default: to environment variable VAULT_TOKEN
    username:
        description:
            - username to login to vault.
        default: False
    password:
        description:
            - password to login to vault.
        default: False
    name:
        description:
            - policy name.
        default: False
'''
EXAMPLES = '''
---
- hosts: localhost
  tasks:
    - hashivault_policy_get:
      name: 'annie'
      register: 'vault_policy_get'
    - debug: msg="User policy is {{vault_policy_get.policy}}"
'''


def main():
    argspec = hashivault_argspec()
    argspec['name'] = dict(required=True, type='str')
    module = hashivault_init(argspec)
    result = hashivault_policy_get(module.params)
    if result.get('failed'):
        module.fail_json(**result)
    else:
        module.exit_json(**result)


from ansible.module_utils.basic import *
from ansible.module_utils.hashivault import *


@hashiwrapper
def hashivault_policy_get(params):
    name = params.get('name')
    client = hashivault_auth_client(params)
    return {'rules': client.get_policy(name)}


if __name__ == '__main__':
    main()
