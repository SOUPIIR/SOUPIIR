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
    {% if page.layout == "showcase" %}
        <header id="header">
            <h1 class="home-title"><span class="logo">{{ site.title }}</span></h1>
        </header>
    {% else %}
        {% include nav.html %}
    {% endif %}

    <main id="content">
        {{ content }}
        <script>initPage();</script>
    </main>

    {% include bottom-scripts.html %}
</body>
</html>
