package main

type game struct {
    id string
    name string
    df_version string
    dfhack_version string
    comm *hub
    screen *hub
}

var games []*game

func InitGames() {
    games = make([]*game, 0)
}

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

func NewGame(id string) *game {
    g := new(game)
    g.id = id
    g.comm = NewHub()
    g.screen = NewHub()
    return g
}

func FindGame(id string, create bool) *game {
    for _, g := range games {
        if g.id == id {
            return g
        }
    }
    if create {
        g := NewGame(id)
        games = append(games, g)
        return g
    }
    return nil
}
