from django.contrib.auth.models import User

from common.models import AccountUserProfile

class VerifiedBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                try:
                    aup = AccountUserProfile.objects.get(user=user)
                    if aup.is_verified:
                        return user
                    else:
                        return None
                except:
                    return user
        except User.DoesNotExist:
            return None 
            
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None