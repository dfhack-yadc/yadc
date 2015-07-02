function game_list_msg(type, message) {
    $('#game-list-status').attr('class', 'alert alert-' + type).text(message);
}

$(function() {
    if (!window.PORTS) {
        game_list_msg('danger', 'Missing port information');
        return;
    }
    $.getJSON('/yadc/games.json', function(data) {
        if (!data.length) {
            game_list_msg('warning', 'No games');
            return;
        }
    })
})
