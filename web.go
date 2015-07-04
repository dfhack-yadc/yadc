package main

import (
    "encoding/json"
    "fmt"
    "github.com/gorilla/context"
    "github.com/gorilla/mux"
    "github.com/gorilla/sessions"
    "log"
    "net/http"
    "strconv"
)

var store = sessions.NewCookieStore()

func StartWebServer(host string, port int, done chan <- bool) {
    addr := host + ":" + strconv.Itoa(http_port)
    fmt.Printf("Serving HTTP on %s\n", addr)
    r := mux.NewRouter()
    r.HandleFunc("/yadc/{path}", yadcHandler)
    r.PathPrefix("/").Handler(http.FileServer(http.Dir("./web/")))
    http.Handle("/", r)
    err := http.ListenAndServe(addr, context.ClearHandler(http.DefaultServeMux))
    if err != nil {
        log.Fatal(err)
    }
}

func encodejson(v interface{}) ([]byte, bool) {
    j, err := json.Marshal(v)
    if err != nil {
        log.Printf("Could not encode JSON: %v\n", err)
        return []byte(""), false
    }
    return j, true
}

func yadcHandler(w http.ResponseWriter, r *http.Request) {
    path := mux.Vars(r)["path"]
    if path == "ports.js" {
        j, ok := encodejson(ListPorts())
        if ok {
            w.Write([]byte("PORTS = "))
            w.Write(j)
        }
    } else if path == "games.json" {
        j, ok := encodejson(ListGames())
        if ok {
            w.Write(j)
        }
    }
}