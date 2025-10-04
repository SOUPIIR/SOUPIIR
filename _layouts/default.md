<!DOCTYPE html>
<html lang="fr">

<head>
    {% include headers.html title=page.title %}
    {% if page.layout == "showcase" %}
        <meta name="robots" content="noindex" />
    {% endif %}
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
        {% include scripts.html %}
    </main>

    <script>initPage();</script>
</body>
</html>
