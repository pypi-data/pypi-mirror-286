import solara
#%%
class DataContainer(dict):

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

class SessionManager():
    sessions = {}

    @property
    def session_state(self):
        try:
            session_id = f'session-{solara.get_session_id()}'
        except:
            try:
                session_id = f'kernel-{solara.get_kernel_id()}'
            except:
                session_id = 'local'

        if session_id not in self.sessions:
            self.sessions[session_id] = DataContainer()
        return self.sessions[session_id]

st=SessionManager()

