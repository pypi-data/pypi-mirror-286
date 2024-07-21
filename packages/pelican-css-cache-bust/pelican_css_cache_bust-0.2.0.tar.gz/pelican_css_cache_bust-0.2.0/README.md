# pelican-css-cache-bust
A Pelican plugin to append a cache buster query string to your `CSS_FILE`.

## Set up
* Define `CSS_FILE` in `pelicanconf.py`
* `CSS_FILE` can be a filename or partial path
* `CSS_FILE` should be findable in any of `THEME_STATIC_PATHS`

### Use in templates
* Use `{{ CSS_FILE }}{{ CSS_FILE_CACHE_BUST }}` in your templates
* `CSS_FILE_CACHE_BUST` already includes a query prefix: `?`

## Example
```python
# pelicanconf.py
CSS_FILE = "css/main.css"
THEME = "custom_theme"
THEME_STATIC_PATHS = ["static", "other"]
# You can explicitly enable this plugin. Note this disables auto discovery
# PLUGINS = ["css_cache_bust"]
```

Pelican will resolve `THEME` to a full path and the plugin will search
for:
```
(resolved-path)/custom_theme/static/css/main.css
(resolved-path)/custom_theme/other/css/main.css
```

Any template can use the generated setting like:
```jinja
<link rel="stylesheet" href="{{ SITEURL }}/{{ THEME_STATIC_DIR }}/{{ CSS_FILE }}{{ CSS_FILE_CACHE_BUST }}" />
```

Adjust as necessary for your specific theme.
