package main

type hub struct {
    dfconn *connection
    clients []*connection

    addconn chan *connection
    rmconn chan *connection
}

type game struct {
    id string
    name string
    df_version string
    dfhack_version string
    comm *hub
    screen *hub
}

var games []game

func ListGames() []map[string]string {
    list := make([]map[string]string, 0)
    for _, g := range games {
        gmap := make(map[string]string)
        gmap["id"] = g.id
        gmap["name"] = g.name
        gmap["df_version"] = g.df_version
        gmap["dfhack_version"] = g.dfhack_version
        list = append(list, gmap)
    }
    return list
}

func StartHub(host string, comm_port int, screen_port int) {
    games = make([]game, 0)
}
