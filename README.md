# Mediahome
Simple web interface for Samba Servers

## Installation
you need to have Docker installed 

```bash
pip3 install -r requirements.txt
```

```bash
python3 app.py
```

## Usage

```python
# On line 13, you can set your configurations as IP server and Workgroup
self.smb_server = SmbConnection('127.0.0.1')
```
