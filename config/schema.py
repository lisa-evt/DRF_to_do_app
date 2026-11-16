SCHEMA_FAKE_VIEW_ATTR = 'swagger_fake_view'


def is_schema_generation(view):
    """True while drf-spectacular introspects a view without a real request."""
    return getattr(view, SCHEMA_FAKE_VIEW_ATTR, False)
