# 3.0.0

* Explicitly set `default_auto_field` to `django.db.models.BigAutoField`. If you were
  using a previous version and your `DEFAULT_AUTO_FIELD` setting is different, you may
  get a migration warning, or an unwanted migration created when running
  `makemigrations`.
* Switched to using [Rye](https://rye.astral.sh) and
  [Hatch](https://hatch.pypa.io/latest/) for local development.
* Updated testing matrix for currently supported versions of Django and Python.
