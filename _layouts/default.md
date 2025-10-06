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
    {% include nav.html %}

    <main id="content">
        {{ content }}
        <script>initPage();</script>
    </main>

    {% include bottom-scripts.html %}
</body>
</html>
