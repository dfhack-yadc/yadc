package main

import (
    "flag"
    "fmt"
)

var (
    local_only bool
    http_port int
    comm_port int
    screen_port int
    local_comm_port int
    local_screen_port int
    ports map[string]int
)

func main() {
    flag.BoolVar(&local_only, "local", false, "only serve to localhost")
    flag.IntVar(&http_port, "http", 8000, "http server port")
    flag.IntVar(&comm_port, "comm", 25143, "websocket communication port")
    flag.IntVar(&screen_port, "screen", 25144, "websocket screen data port")
    flag.IntVar(&local_comm_port, "local-comm", 25145, "local communication port")
    flag.IntVar(&local_screen_port, "local-screen", 25146, "local screen data port")
    ports = make(map[string]int)
    ports["http"] = http_port
    ports["comm"] = comm_port
    ports["screen"] = screen_port
    flag.Parse()
    host := ""
    if local_only {
        host = "localhost"
    }
    fmt.Printf("Websocket ports: %d, %d\n", comm_port, screen_port)
    InitGames()
    done := make(chan bool)
    go StartNet(host, comm_port, screen_port, local_comm_port, local_screen_port, done)
    go StartWebServer(host, http_port, done)
    <-done
    <-done
}

func ListPorts() *map[string]int {
    return &ports
}
