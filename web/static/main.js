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
        }).data({game: game_data});
        $('<h4>').addClass('list-group-item-heading').text(game_data.name).appendTo(a);
        $('<p>').addClass('list-group-item-text').text(
            "DF " + game_data.df_version + "; DFHack " + game_data.dfhack_version
        ).appendTo(a);
        if (!game_data.active)
            a.addClass('disabled').attr({title: "Disconnected"});
        return a;
    },
};

$(window).on('hashchange', function() {
    var parts = location.hash.split('-');
});

$(function() {
    if (!window.PORTS) {
        ui.GameListMessage('danger', 'Missing port information');
        return;
    }
    $.getJSON('/yadc/games.json', function(data) {
        if (!data.length) {
            ui.GameListMessage('warning', 'No games');
            return;
        }
        ui.GameListMessage(false);
        var list = $('#game-list-form .list-group').text('');
        for (var i = 0; i < data.length; i++) {
            ui.GameListItem(data[i]).appendTo(list);
        }
    })
})
