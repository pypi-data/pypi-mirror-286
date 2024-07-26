# Setup dev environment

```bash
python3 -m pip install -r requirements.txt
pre-commit install
```

# Export environment variables

```bash
export MAIL_SERVER="smtp.gmail.com"
export MAIL_PORT=587
export MAIL_USERNAME="********************************"
export MAIL_RECEIPIENT="********************************"
export MAIL_PASSWORD="********************************"
export MAIL_USE_TLS=1
export MAIL_USER_SSL=0
```

# Run application

```bash
python3 -c "from notify_online import notify_online; notify_online()"
```

# Build package

```bash
python3 setup.py sdist bdist_wheel
```

# Publish package to Pypi

```bash
twine upload dist/*
```
