function hasSocketSupport() {
    return !!(window.WebSocket && window.Uint8Array);
}

function BaseSocket(path) {
    var open = false;
    var self = {};
    self.events = $({});
    self.ws = new WebSocket("ws://" + window.location.host + "/" + path);
    self.ws.onopen = function() {
        open = true;
        self.events.trigger('open');
    }
    self.ws.onclose = function() {
        open = false;
        self.events.trigger('close');
    }
    self.ws.onmessage = function (event) {
        self.events.trigger('message', event.data);
    }

    self.isOpen = function() { return open; }
    self.send = function(msg) {
        if (!open)
            throw Error('Socket closed');
        if (typeof msg == 'object')
            msg = JSON.stringify(msg);
        self.ws.send(msg);
    }

    return self;
}

function MainSocket() {
    var self = BaseSocket('comm/main');
    var loggedIn = false;
    self.events.on('message', function(data) {
        data = JSON.parse(data);
        if (data.auth) {
            loggedIn = data.auth.logged_in;
            self.events.trigger(loggedIn ? 'login' : 'login-invalid', data.auth);
        }
    })

    self.login = function(user, pass) {
        self.send({auth: {username: user, password: pass}});
    }
    self.isLoggedIn = function() { return loggedIn; }

}
