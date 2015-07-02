package main

import (
    "fmt"
    "github.com/gorilla/context"
    "github.com/gorilla/mux"
    "github.com/gorilla/sessions"
    "log"
    "net/http"
)

var store = sessions.NewCookieStore()

func startServer(addr *string) {
    r := mux.NewRouter()
    r.HandleFunc("/yadc/{info}", yadcHandler)
    r.PathPrefix("/").Handler(http.FileServer(http.Dir("./web/")))
    http.Handle("/", r)
    err := http.ListenAndServe(*addr, context.ClearHandler(http.DefaultServeMux))
    if err != nil {
        log.Fatal(err)
    }
}

func yadcHandler(w http.ResponseWriter, r *http.Request) {
    path := string(r.URL.Path)
    if (path == "") {
        path = "index.html"
    }
    fmt.Printf("Request %s\n", path)
}
