# detail-sdk

Add this snippet to your app to generate traces.
It's important for it to run as early as possible before other imports:

```python
from detail.client import instrument
instrument()
```