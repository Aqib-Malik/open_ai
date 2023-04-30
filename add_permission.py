from Api.models import Permission
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'Practice.settings')

django.setup()


all_permission = [
    {
        'name': 'Create Role', 'code_name': 'role_create', 'module_name': 'Role',
        'description': 'User can create role'
    },

]


def add_permission():
    for perm_dict in all_permission:
        try:
            Permission.objects.get(code_name=perm_dict['code_name'])
        except Permission.DoesNotExist:
            Permission.objects.create(
                name=perm_dict['name'],
                code_name=perm_dict['code_name'],
                module_name=perm_dict['module_name'],
                description=perm_dict['description'],
            )


if __name__ == '__main__':
    print("Adding permissions to HMS...")
    add_permission()
