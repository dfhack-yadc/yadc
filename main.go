package main

import (
    "flag"
)

var (
    local_only bool
    serve_fs bool
    web_port int
    comm_port int
    screen_port int
    ports map[string]int
)

func main() {
    flag.BoolVar(&local_only, "local", false, "only serve to localhost")
    flag.BoolVar(&serve_fs, "servefs", false, "serve from local filesystem")
    flag.IntVar(&web_port, "web", 8000, "web server port")
    flag.IntVar(&comm_port, "comm", 25143, "local communication port")
    flag.IntVar(&screen_port, "screen", 25144, "local screen data port")
    flag.Parse()
    ports = make(map[string]int)
    ports["web"] = web_port
    ports["comm"] = comm_port
    ports["screen"] = screen_port
    host := ""
    if local_only {
        host = "localhost"
    }
    done := NewSem()
    go StartNet(host, comm_port, screen_port, done)
    go StartWebServer(host, web_port, serve_fs, done)
    done.Wait()
}

func ListPorts() *map[string]int {
    return &ports
}
