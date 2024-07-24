### Installation
```bash
$ pip install django-timestamp2datetime
```

### Examples
`models.py`
```python
class Obj(models.Model):
    created_at = models.IntegerField()
```

template
```html
{% load timestamp2datetime %}

{{ obj.created_at|timestamp2datetime }}
```

