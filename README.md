Maven repo backup script for repsy

This small script helps backing up your repository into a local directory

```python
################################################################################

repsy_repo_name = 'default' # change if different than default
repsy_username = 'FIX ME'
repsy_password = 'FIX ME'
destination_directory = '/path/to/local/backup/dir'

################################################################################
```

then you can start the backup:

```bash
python3 ./main.py
```