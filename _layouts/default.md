<!DOCTYPE html>
<html lang="fr">

<head>
    {% include headers.html %}
    {% if page.layout == "showcase" %}
        <meta name="robots" content="noindex" />
    {% endif %}
    {% include top-scripts.html %}
</head>
<body>
    {% if page.simple_layout != false %}
        {% include nav.html %}
    {% endif %}

    <main id="content">
        {{ content }}
        <script>initPage();</script>
    </main>

    {% if page.simple_layout != false %}
        {% include bottom-scripts.html %}
    {% endif %}
</body>
</html>
