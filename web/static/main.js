(function($) {
    var gameData = {};
    ui = {
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
                a.addClass('disabled').attr({title: "Disconnected"});
            return a;
        },
    };

    function showPage (name) {
        var p = $('.page#page-' + name);
        if (!p.length)
            throw new Error('Invalid page: ' + name);
        $('.page').hide();
        p.show();
    }

    function onHashChange() {
        var parts = location.hash.split('-');
        if (parts.length == 1 && !parts[0]) {
            showPage('select');
        }
        else {
            showPage('unknown');
        }
    }

    function findGame (id) {
        for (var i = 0; i < gameData.length; i++)
            if (gameData[i].id == id)
                return gameData[i];
    }

    function loadGames (callback) {
        $.getJSON('/yadc/games.json', function(data) {
            gameData = data;
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
            if (callback && callback.call)
                callback();
        });
    }
    setInterval(loadGames, 60000);

    $(window).on('hashchange', onHashChange);

    $(function() {
        onHashChange();
        if (!window.PORTS) {
            ui.GameListMessage('danger', 'Missing port information');
            return;
        }
        loadGames();
    })
})(jQuery);
