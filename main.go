package main

import (
    "flag"
    "fmt"
    "strconv"
)

var (
    local_only bool
    http_port int
    comm_port int
    screen_port int
    ports map[string]int
)

func main() {
    flag.BoolVar(&local_only, "local", false, "only serve to localhost")
    flag.IntVar(&http_port, "http", 8000, "http server port")
    flag.IntVar(&comm_port, "comm", 25143, "communication port")
    flag.IntVar(&screen_port, "screen", 25144, "screen data port")
    ports = make(map[string]int)
    ports["http"] = http_port
    ports["comm"] = comm_port
    ports["screen"] = screen_port
    flag.Parse()
    host := ""
    if local_only {
        host = "localhost"
    }
    fmt.Printf("Serving HTTP on %s:%d\n", host, http_port)
    fmt.Printf("Websocket ports: %d, %d\n", comm_port, screen_port)
    StartHub(host, comm_port, screen_port)
    addr := host + ":" + strconv.Itoa(http_port)
    StartWebServer(addr)
}

func ListPorts() *map[string]int {
    return &ports
}
