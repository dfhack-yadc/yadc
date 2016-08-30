(function($) {
    var gameData = [],
        creds = {},
        hashData = {};

    comm = {};

    ui = {
        events: $({}),

        GameListMessage: function(type, message) {
            if (type && message)
                $('#game-list-status').attr('class', 'alert alert-' + type).text(message);
            else
                $('#game-list-status').hide();
        },

        GameListItem: function(game_data) {
            var a = $('<a>').addClass('list-group-item').attr({
                'href': '#game-' + game_data.id,
            });
            $('<h4>').addClass('list-group-item-heading').text(game_data.name).appendTo(a);
            $('<p>').addClass('list-group-item-text').text(
                "DF " + game_data.df_version + "; DFHack " + game_data.dfhack_version
            ).appendTo(a);
            if (!game_data.active)
                a.addClass('disabled').attr({title: "Disconnected"}).removeAttr('href');
            return a;
        },

        Spinner: null,

        spinnerOpts: {
            lines: 13,
            length: 28,
            width: 14,
            radius: 42,
            scale: 0.3,
            corners: 1,
            color: '#000',
            opacity: 0.2,
            rotate: 0,
            direction: 1,
            speed: 1,
            trail: 40,
            fps: 20,
            zIndex: 2e9,
            className: 'spinner',
            top: '50%',
            left: '50%',
            shadow: false,
            hwaccel: false,
            position: 'absolute'
        },

        ActionsMenu: {
            enable: function() {
                $('#actions-menu').removeClass('disabled').find('a.dropdown-toggle').attr('data-toggle', 'dropdown');
            },
            disable: function() {
                $('#actions-menu').addClass('disabled').find('a.dropdown-toggle').attr('data-toggle', '');
            }
        },

    };

    var pageHandlers = {
        'nosockets': {
            actions_disabled: true,
        },
        'login': {
            redirect: function() {
                if (validCreds())
                    return 'list';
            },
            actions_disabled: true,
        },
        'list': {
            redirect: function() {
                if (!validCreds())
                    return 'login';
            }
        },
        'game': {
            redirect: function() {
                if (!validCreds())
                    return 'login';
            },
            show: function() {
                $('#spinner').show();
                loadGames(function() {
                    var g = findGame(hashData[1]);
                    if (!g)
                        return showPage('gameerr', 'unknown');
                    if (!g.active)
                        return showPage('gameerr', 'inactive');
                    $('#cur-game').show().find('a').text(g.name);
                    $('#spinner').hide();
                });
            },
            hide: function() {
                $('#spinner').hide();
                $('#cur-game').hide();
            }
        },
        'gameerr': {
            show: function() {
                $('#page-gameerr').find('.alert').hide();
                var msg = $('#page-gameerr').find('#gameerr-' + hashData[1]);
                if (!msg.length)
                    msg = $('#gameerr-unknown');
                msg.show();
            }
        }
    }

    function showPage() {
        var hash = '#' + [].slice.apply(arguments).join('-');
        if (hash != window.location.hash)
            window.location.hash = hash;
    }

    var curPage;
    function onHashChange() {
        function _getPageHandler (page, event) {
            if (!page)
                return function(){};
            var name = page.data('pageName');
            return (pageHandlers[name] && pageHandlers[name][event]) || function(){};
        }
        function _showPage (name) {
            var p = $('.page#page-' + name);
            var pdata = pageHandlers[p.data('pageName')] || {};
            if (!p.length)
                throw new Error('Invalid page: ' + name);
            if (curPage) {
                curPage.hide();
                _getPageHandler(curPage, 'hide')();
            }
            var dest = _getPageHandler(p, 'redirect')();
            if (dest) {
                showPage(dest);
                return;
            }
            if (pdata.actions_disabled)
                ui.ActionsMenu.disable();
            else
                ui.ActionsMenu.enable();
            p.show();
            curPage = p;
            ui.events.trigger('page.show', name);
        }
        hashData = location.hash.replace(/^#/, '').split('-');
        if (!hasSocketSupport()) {
            _showPage('nosockets');
        }
        else if (hashData.length <= 1 && !hashData[0]) {
            _showPage('login');
        }
        else if (hashData[0] == 'logout') {
            deauth();
            _showPage('login');
        }
        else {
            if ($('.page#page-' + hashData[0]).length)
                _showPage(hashData[0]);
            else
                _showPage('unknown');
        }
        _getPageHandler(curPage, 'show')();
    }

    function findGame (id) {
        for (var i = 0; i < gameData.length; i++)
            if (gameData[i].id == id)
                return gameData[i];
    }

    function auth() {
        if (!creds.username) {
            showPage('login');
            return false;
        }
        else {
            localStorage.setItem('yadc-creds', JSON.stringify(creds));
            return true;
        }
    }

    function authForm(form) {
        creds = {
            username: form.find('#username').val()
        }
        if (auth())
            showPage('list');
    }

    function authLocalStorage() {
        if (!window.localStorage || !window.JSON)
            return false;
        var item = localStorage.getItem('yadc-creds');
        if (!item)
            return false;
        creds = JSON.parse(item);
        return auth();
    }

    function deauth() {
        creds = {};
        if (window.localStorage)
            localStorage.removeItem('yadc-creds');
    }

    function validCreds() { return !!creds.username; }

    function loadGames (callback) {
        $.getJSON('/yadc/games.json', function(data) {
            gameData = data;
            if (callback && callback.call)
                callback();
            if (!data.length) {
                ui.GameListMessage('warning', 'No games');
                return;
            }
            ui.GameListMessage(false);
            var list = $('#game-list-form .list-group').text('');
            for (var i = 0; i < data.length; i++) {
                ui.GameListItem(data[i]).appendTo(list).click(function(e) {
                    if ($(this).hasClass('disabled'))
                        e.preventDefault();
                });
            }
        });
    }
    setInterval(loadGames, 60000);

    $(window).on('hashchange', onHashChange);

    ui.events.on('page.show', function() {
        if (creds && creds.username)
            $('#cur-user').show().find('a').text(creds.username);
        else
            $('#cur-user').hide();
    })

    $(function() {
        ui.Spinner = new Spinner(ui.spinnerOpts).spin($('#spinner')[0]);
        $('.page').each(function (_, elt) {
            $(elt).data({pageName: $(elt).attr('id').replace('page-', '')});
        });
        $('.hidden').hide().removeClass('hidden');
        if (!hasSocketSupport()) {
            showPage('nosockets');
            return;
        }
        // comm.main = MainSocket();
        if (!authLocalStorage()) {
            location.hash = '';
            showPage('login');
        }
        else {
            onHashChange();
        }
        if (!window.PORTS) {
            ui.GameListMessage('danger', 'Missing port information');
            return;
        }
        loadGames();
        $('#login-form').submit(function(e) {
            e.preventDefault();
            authForm($(this));
        });
        $(document).on('click', '.no-click', function(e) {
            e.preventDefault();
        });
    });
})(jQuery);
