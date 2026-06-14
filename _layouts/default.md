<!DOCTYPE html>
<html lang="fr">

<head>
    {% include headers.html %}
    {% if page.layout == "showcase" %}
        <meta name="robots" content="noindex" />
    {% endif %}
    <script>let simple_layout = {{ page.simple_layout }}</script>
    {% include top-scripts.html %}
</head>
<body>

    {% include nav.html %}

    <main id="content">
        {{ content }}
        <script>initPage();</script>
    </main>

    {% if page.simple_layout == false %}
        {% include bottom-scripts.html %}
    {% endif %}
</body>
</html>
