import json
from datetime import datetime, timezone


metadata = {
  'system': 'triple-j-playlist-maker',
  'timestamp': datetime.now(timezone.utc).strftime("%Y-%m-%d:%H:%M:%S%Z")
}

class StructuredMessage(object):
  def __init__(self, message, **kwargs):
    self.message = message
    self.kwargs = kwargs

  def __str__(self):
    return '{\"message\": \"%s\", "metadata": %s, "extras": %s}' % (self.message, json.dumps(metadata), json.dumps(self.kwargs))

_ = StructuredMessage
