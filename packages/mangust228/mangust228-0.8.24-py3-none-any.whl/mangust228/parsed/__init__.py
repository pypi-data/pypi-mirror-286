'''
Class for checking if a file or URL has been processed. Creates two files:
- `data/wrong.csv` (if errors occurred)
- `data/success.csv` (if no errors occurred)

Example usage:

```python
from parsed_manager import AsyncParsedManager as ParsedManager

# Adds an erroneous record
await ParsedManager.wrong.add("url/path", reason) 
# Adds a successfully parsed record
await ParsedManager.success.add("url/path")  

if ParsedManager.wrong.is_exist("url/path"):
    pass  # This block is executed if the URL/path has been parsed before.
    
'''

from .async_manager import AsyncParsedManager
from .sync_manager import SyncParsedManager