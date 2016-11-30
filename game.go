package main

import (
    "fmt"
    "sync"
)

type game struct {
    valid bool
    id string
    name string
    df_version string
    dfhack_version string
    comm *hub
    screen *hub

    screen_data screen_data
}

func (g *game) String() string {
    return fmt.Sprintf("Game %s (%s)", g.id,
        ifexpr(g.name != "", g.name, "unknown"))
}

func (g *game) Active() bool {
    return g.comm.dfconn != nil && g.screen.dfconn != nil
}

type screen_data struct {
    raw []byte
    dims struct {
        // Screen dimensions in DF are capped at 256
        x uint16
        y uint16
    }
}

func (sd *screen_data) rawOffset(x uint8, y uint8) uint {
    return ((uint(x) * 256) + uint(y)) * 5
}

var (
    games []*game
    games_mutex sync.RWMutex
)

func ListGames() []map[string]string {
    list := make([]map[string]string, 0)
    for _, g := range games {
        if !g.valid {
            continue
        }
        gmap := make(map[string]string)
        gmap["id"] = g.id
        gmap["name"] = g.name
        gmap["df_version"] = g.df_version
        gmap["dfhack_version"] = g.dfhack_version
        if g.Active() {
            gmap["active"] = "true"
        }
        list = append(list, gmap)
    }
    return list
}

func NewGame(id string) *game {
    return &game{
        valid: false,
        id: id,
        comm: NewHub(),
        screen: NewHub(),
        screen_data: screen_data{
            raw: make([]byte, 256 * 256 * 5),
        },
    }
}

func FindGame(id string, create bool) *game {
    if (create) {
        // lock for writing, to be safe
        games_mutex.Lock()
        defer games_mutex.Unlock()
    } else {
        // lock for reading
        games_mutex.RLock()
        defer games_mutex.RUnlock()
    }
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
