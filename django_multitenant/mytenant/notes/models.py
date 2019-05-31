from django.contrib.auth import get_user_model
User = get_user_model()
from django.db import models, connection


class Note(models.Model):
    """
    def get_upload_path(instance, filename):
        print('*'*60)
        print(f'{instance}{connection.schema_name}.localhost/{filename}')
        return "%s.localhost/%s" % (connection.schema_name, filename)
    """
    sender = models.CharField(max_length=40)
    recipient = models.CharField(max_length=40)
    msj = models.TextField()
    img = models.ImageField(upload_to=connection.schema_name+'/img_notes') 
    # img = models.ImageField(upload_to=get_upload_path)
    created_at = models.DateField(auto_now_add=True)
