class UserDataMixin:

    def get_user_data(self):
        user_data ={
            'username': self.request.user,
            'ip': self.request.META['REMOTE_ADDR'],
            'path': self.request.path,
        }
        if self.request.method == 'POST':
            user_data['POST'] = self.request.POST
        return user_data
