from sigma.jupyterhub import JupyterHub, JupyterUser

class TestJupyterUser:
    def test_from_response_data(self):
        data = {
            'roles': ['user'],
            'created': '2024-06-11T04:26:11.365394Z',
            'kind': 'user',
            'pending': None,
            'server': None,
            'admin': False,
            'name': 'alice',
            'auth_state': None,
            'last_activity': '2024-06-11T05:17:28.728392Z',
            'groups': [],
            'servers': {}
        }
        hub = JupyterHub()
        user = JupyterUser.from_response_dict(hub, data)
        assert user.name == "alice"
        assert user.admin == False

