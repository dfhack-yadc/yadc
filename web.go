package main

import (
    "encoding/json"
    "github.com/gorilla/context"
    "github.com/gorilla/mux"
    "github.com/gorilla/sessions"
    "io/ioutil"
    "log"
    "net/http"
    "strconv"
)

var (
    fs http.FileSystem
    store = sessions.NewCookieStore()
)

func StartWebServer(host string, port int, serve_fs bool, done *sem) {
    done.Inc()
    defer done.Dec()
    addr := host + ":" + strconv.Itoa(port)
    log.Printf("Serving HTTP on %s (from %s)\n", addr, ifexpr(serve_fs, "filesystem", "package"))
    r := mux.NewRouter()
    r.NotFoundHandler = http.HandlerFunc(custom404Handler)
    r.HandleFunc("/yadc/{path}", yadcHandler)
    if (serve_fs) {
        fs = http.Dir("./web/")
    } else {
        fs = assetFS()
    }
    r.PathPrefix("/").Handler(http.FileServer(fs))
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

func custom404Handler(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(404)
    path := "/404.html"
    f, err := fs.Open(path)
    if err == nil {
        contents, err := ioutil.ReadAll(f)
        if err == nil {
            w.Write(contents)
        }
    }
    if err != nil {
        w.Write([]byte("not found and could not open " + path + ": " + err.Error()))
    }
}

func yadcHandler(w http.ResponseWriter, r *http.Request) {
    path := mux.Vars(r)["path"]
    if path == "ports.js" {
        j, ok := encodejson(ListPorts())
        if ok {
            w.Write([]byte("PORTS = "))
            w.Write(j)
            w.Write([]byte(";"))
        }
    } else if path == "games.json" {
        j, ok := encodejson(ListGames())
        if ok {
            w.Write(j)
        }
    } else {
        w.WriteHeader(404)
        w.Write([]byte("not found"))
    }
}
