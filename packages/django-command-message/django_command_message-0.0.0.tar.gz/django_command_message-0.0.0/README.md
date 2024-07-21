### Installation
```bash
$ pip install django-command-message
```

#### `settings.py`
```python
INSTALLED_APPS+=['django_command_message']
```

#### `migrate`
```bash
$ python manage.py migrate
```

### Features
+   database messages
+   admin
+   print message if `settings.DEBUG==True`

### Models
model|table|columns/fields
-|-|-
`Command`|`django_command_message`|`id`,`command`,`message`,`created_at`

### Examples
`MessageMixin`
```python
from django_command_message.mixins import MessageMixin

class Command(MessageMixin,BaseCommand):
    def handle(self, *args, **options):
        self.message('message')
```

`Message` model
```python
from django_command_message.models import Message

Message(command='name',message="message").save()
```

