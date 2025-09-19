var Lightbox = function(elem) {
    this.trigger = elem;
    this.el = document.querySelector('.lightbox');
    this.body = document.querySelector('.lightbox .body');
    this.content = document.querySelector('.lightbox .content');
    this.type = elem.getAttribute('lightbox');
    this.text = elem.getAttribute('video-description');
    this.title = elem.getAttribute('video-title');
    this.href = elem.getAttribute('url') || elem.getAttribute('href');
    this.gallery = elem.getAttribute('data-gallery');
    this.image = null;
    this.video = null;
    this.init();
}

Lightbox.prototype.init = function() {
    var _this = this;

    if (!this.el) this.create();

    if (this.gallery) {
        this.images = Array.from(document.querySelectorAll('[data-gallery="'+this.gallery+'"]'));

        // Masquer toutes sauf la première
        this.images.slice(1).forEach(function(el) {
            el.style.display = 'none';
        });
    }

    this.trigger.addEventListener('click', function(e) {
        e.preventDefault();
        _this.open();
    });
}


Lightbox.prototype.create = function() {
    var _this = this,
        cl = document.createElement('div'), // close
        bd = document.createElement('div'); // backdrop

    this.el = document.createElement('div');
    this.content = document.createElement('div');
    this.body = document.createElement('div');

    this.el.classList.add('lightbox');
    bd.classList.add('backdrop');
    cl.classList.add('close');
    this.content.classList.add('content');
    this.body.classList.add('body');

    cl.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 512 512" xml:space="preserve"><g><g><path d="M505.943,6.058c-8.077-8.077-21.172-8.077-29.249,0L6.058,476.693c-8.077,8.077-8.077,21.172,0,29.249C10.096,509.982,15.39,512,20.683,512c5.293,0,10.586-2.019,14.625-6.059L505.943,35.306C514.019,27.23,514.019,14.135,505.943,6.058z"></path></g></g><g><g><path d="M505.942,476.694L35.306,6.059c-8.076-8.077-21.172-8.077-29.248,0c-8.077,8.076-8.077,21.171,0,29.248l470.636,470.636c4.038,4.039,9.332,6.058,14.625,6.058c5.293,0,10.587-2.019,14.624-6.057C514.018,497.866,514.018,484.771,505.942,476.694z"></path></g></g></svg>';

    this.el.appendChild(bd);
    this.content.appendChild(cl);
    this.content.appendChild(this.body);
    this.el.appendChild(this.content);
    document.body.appendChild(this.el);

    cl.addEventListener('click', function() {
        _this.close();
    });

    bd.addEventListener('click', function() {
        _this.close();
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === "Escape" || e.key === "Esc" || e.keyCode === 27) {
            if (_this.isOpen()) {
                _this.close();
            }
        }
        if (e.key === "ArrowRight") {
            _this.next();
        }
        if (e.key === "ArrowLeft") {
            _this.prev();
        }
    });

    var f = function(e) {
        if (_this.isOpen()) return;
        _this.el.classList.remove('show');
        _this.body.innerHTML = '';
    }

    this.el.addEventListener('transitionend', f, false);
    this.el.addEventListener('webkitTransitionEnd', f, false);
    this.el.addEventListener('mozTransitionEnd', f, false);
    this.el.addEventListener('msTransitionEnd', f, false);

    if (this.gallery && this.type === 'image') {
        var prev = document.createElement('div');
        var next = document.createElement('div');
        prev.classList.add('nav', 'prev');
        next.classList.add('nav', 'next');
        prev.innerHTML = '&#10094;'; // chevron gauche
        next.innerHTML = '&#10095;'; // chevron droit

        this.content.appendChild(prev);
        this.content.appendChild(next);

        prev.addEventListener('click', function() { _this.prev(); });
        next.addEventListener('click', function() { _this.next(); });
    }
}

Lightbox.prototype.loadImage = function() {
    this.setDimensions(this.width, this.height);
    this.image = new Image();
    this.image.src = this.href;
    this.body.appendChild(this.image);
}

Lightbox.prototype.loadVideo = function() {
    var _this = this;
    this.setDimensions(this.width, this.height);

    if (!this.video) {
        this.video = document.createElement('video');
        this.video.addEventListener('loadedmetadata', function() {
            var dim = _this.fitToSize(this.videoWidth, this.videoHeight, _this.width, _this.height);
            _this.setDimensions(dim.width, dim.height);
        });
        this.video.src = this.href;
        this.video.autoplay = true;
        this.video.controls = true;
    }

    this.body.appendChild(this.video);
}

Lightbox.prototype.loadIframe = function() {
    this.setDimensions(this.width, this.height);
    this.body.innerHTML = '<iframe src="' + this.href + '" frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share" referrerpolicy="strict-origin-when-cross-origin"></iframe>' + '<h2>' + this.title + '</h2>' + '<p>' + this.text + '</p>';
}

Lightbox.prototype.open = function() {
    if (this.gallery) {
        // récupère toutes les images de ce groupe
        this.images = Array.from(document.querySelectorAll('[data-gallery="' + this.gallery + '"]'));

        // trouve l’index de l’image cliquée
        this.index = this.images.indexOf(this.trigger);

        // met à jour href/type
        this.href = this.images[this.index].getAttribute('href');
        this.type = this.images[this.index].getAttribute('lightbox');

        this.showMedia();

        // création dynamique des boutons nav
        this.addNav();
    } else {
        this.showMedia();

        // supprime les nav existantes si c'est une vidéo
        this.content.querySelectorAll('.nav').forEach(el => el.remove());
    }

    this.el.classList.add('show');
    this.el.offsetHeight; // force render
    this.el.classList.add('open');
}

Lightbox.prototype.addNav = function() {
    var _this = this;

    // Supprime les nav existantes
    this.content.querySelectorAll('.nav').forEach(el => el.remove());

    // Création seulement pour galerie d'images avec 2+ éléments
    if (this.gallery) {
        var prev = document.createElement('div');
        var next = document.createElement('div');
        prev.classList.add('nav', 'prev');
        next.classList.add('nav', 'next');
        prev.innerHTML = '&#10094;'; // chevron gauche
        next.innerHTML = '&#10095;'; // chevron droit
        this.content.appendChild(prev);
        this.content.appendChild(next);

        prev.addEventListener('click', function() { _this.prev(); });
        next.addEventListener('click', function() { _this.next(); });
    }
}

Lightbox.prototype.showMedia = function() {
    this.body.innerHTML = '';
    switch(this.type) {
        case 'image': this.loadImage(); break;
        case 'video': this.loadVideo(); break;
        default: this.loadIframe();
    }
}

Lightbox.prototype.close = function() {
    this.el.classList.remove('open');
}

Lightbox.prototype.isOpen = function() {
    return this.el.classList.contains('open');
}

Lightbox.prototype.next = function() {
    if (!this.gallery) return;
    this.index = (this.index + 1) % this.images.length;
    this.href = this.images[this.index].getAttribute('href');
    this.type = this.images[this.index].getAttribute('lightbox');
    this.body.innerHTML = '';
    this.showMedia();
}

Lightbox.prototype.prev = function() {
    if (!this.gallery) return;
    this.index = (this.index - 1 + this.images.length) % this.images.length;
    this.href = this.images[this.index].getAttribute('href');
    this.type = this.images[this.index].getAttribute('lightbox');
    this.body.innerHTML = '';
    this.showMedia();
}

Lightbox.prototype.setDimensions = function(w, h) {
    this.width = w;
    this.height = h;
    this.content.style.width = w + 'px';
    this.content.style.height = h + 'px';
}

Lightbox.prototype.fitToSize = function(w, h, maxW, maxH) {
    var r = h / w;

    if(w >= maxW && r <= 1){
        w = maxW;
        h = w * r;
    } else if(h >= maxH) {
        h = maxH;
        w = h / r;
    }

    return {
        width: w,
        height: h,
    }
}
