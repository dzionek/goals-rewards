def is_based_on_template(response, template):
    return template in (t.name for t in response.templates)
