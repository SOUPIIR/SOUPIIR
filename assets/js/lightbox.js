let activeLightbox = null;

var Lightbox = function(elem) {
    this.trigger = elem;
    this.el = document.querySelector('.lightbox');
    this.body = document.querySelector('.lightbox .body');
    this.content = document.querySelector('.lightbox .content');
    this.type = elem.getAttribute('lightbox');
    this.text = elem.getAttribute('data-description');
    this.title = elem.getAttribute('data-title');
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
        this.images = Array.from(document.querySelectorAll('[data-gallery="' + this.gallery + '"]'));
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
        cl = document.createElement('div'),
        bd = document.createElement('div');

    this.el = document.createElement('div');
    this.content = document.createElement('div');
    this.body = document.createElement('div');

    this.el.classList.add('lightbox');
    bd.classList.add('backdrop');
    cl.classList.add('close');
    this.content.classList.add('content');
    this.body.classList.add('body');

    cl.innerHTML = '✕';

    this.el.appendChild(bd);
    this.content.appendChild(cl);
    this.content.appendChild(this.body);
    this.el.appendChild(this.content);
    document.body.appendChild(this.el);

    cl.addEventListener('click', function() { _this.close(); });
    bd.addEventListener('click', function() { _this.close(); });

    var f = function() {
        if (_this.isOpen()) return;
        _this.el.classList.remove('show');
        _this.body.innerHTML = '';
    }
    this.el.addEventListener('transitionend', f, false);
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
    this.body.innerHTML = '<iframe src="' + this.href + '" frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share" referrerpolicy="strict-origin-when-cross-origin"></iframe>'
        + '<h2 class="glitch">' + this.title + '</h2>'
        + '<p>' + this.text + '</p>';
}

Lightbox.prototype.open = function() {
    if (this.gallery) {
        this.images = Array.from(document.querySelectorAll('[data-gallery="' + this.gallery + '"]'));
        this.index = this.images.indexOf(this.trigger);
        this.href = this.images[this.index].getAttribute('href');
        this.type = this.images[this.index].getAttribute('lightbox');
        this.showMedia();
        this.addNav();
    } else {
        this.showMedia();
        this.content.querySelectorAll('.nav').forEach(el => el.remove());
    }

    activeLightbox = this; // 🔑 référence globale
    this.el.classList.add('show');
    this.el.offsetHeight;
    this.el.classList.add('open');
}

Lightbox.prototype.addNav = function() {
    var _this = this;
    this.content.querySelectorAll('.nav').forEach(el => el.remove());

    if (this.gallery && this.images && this.images.length > 1) {
        var prev = document.createElement('div');
        var next = document.createElement('div');
        prev.classList.add('nav', 'prev');
        next.classList.add('nav', 'next');
        prev.innerHTML = '&#10094;';
        next.innerHTML = '&#10095;';
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
    if (activeLightbox === this) {
        activeLightbox = null; // 🔑 reset
    }
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
    if (w >= maxW && r <= 1) {
        w = maxW;
        h = w * r;
    } else if (h >= maxH) {
        h = maxH;
        w = h / r;
    }
    return { width: w, height: h }
}

// === Global keydown handler ===
document.addEventListener("keydown", function(e) {
    if (!activeLightbox) return;

    if (e.key === "Escape") {
        activeLightbox.close();
    } else if (e.key === "ArrowRight") {
        activeLightbox.next();
    } else if (e.key === "ArrowLeft") {
        activeLightbox.prev();
    }
});
