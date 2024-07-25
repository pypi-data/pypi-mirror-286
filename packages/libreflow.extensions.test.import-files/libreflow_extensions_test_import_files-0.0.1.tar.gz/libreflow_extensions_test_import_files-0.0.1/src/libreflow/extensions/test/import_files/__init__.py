from kabaret import flow
from kabaret.flow.object import _Manager

class MyAction(flow.Action):
    _MANAGER_TYPE = _Manager


def create_action(parent):
    if 'extendable_object' in parent.oid():
        r = flow.Child(MyAction)
        r.name = 'dynamic_action'
        return r


def install_extensions(session):
    return {
        "demo": [
            create_action,
        ]
    }


from . import _version
__version__ = _version.get_versions()['version']
