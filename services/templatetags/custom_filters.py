from django import template

register = template.Library()

@register.filter
def add_class(value, class_name):
    """Adds a class to a form field."""
    if hasattr(value, 'as_widget'):
        return value.as_widget(attrs={"class": class_name})
    return value  # Return the original value if it doesn't have as_widget
