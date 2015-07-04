package main

import (
    "bytes"
    "encoding/binary"
    "encoding/json"
    "github.com/gorilla/websocket"
    "log"
    "net"
    "strconv"
)

var (
    server_count int
)

type connection struct {
    ws *websocket.Conn
    send chan []byte
}

type hub struct {
    dfconn *net.Conn
    clients []*connection

    addchan chan *connection
    rmchan chan *connection
}

type comm_data struct {
    Info comm_data_info `json:"info"`
}

type comm_data_info struct {
    Df_version string `json:"df_version"`
    Dfhack_version string `json:"dfhack_version"`
    Name string `json:"name"`
}

func NewHub() *hub {
    h := new(hub)
    h.clients = make([]*connection, 0)
    h.addchan = make(chan *connection)
    h.rmchan = make(chan *connection)
    return h
}

func StartServer(host string, port int, handler func(net.Conn), done chan <-bool) {
    addr := host + ":" + strconv.Itoa(port)
    sock, err := net.Listen("tcp", addr)
    if err != nil {
        log.Fatalf("Could not bind to %s: %v\n", addr, err)
    }
    log.Printf("Listening on %s\n", addr)
    go func(){
        defer log.Printf("Shutting down %s\n", addr)
        defer sock.Close()
        defer func(){done <-true}()
        for {
            conn, err := sock.Accept()
            if err != nil {
                log.Fatalf("Failed to accept connection on %s: %v\n", addr, err)
            }
            go handler(conn)
        }
    }()
    server_count++
}

func StartNet(host string, comm_port int, screen_port int, local_comm_port int, local_screen_port int, done chan <- bool) {
    server_count = 0
    ch := make(chan bool)
    StartServer("localhost", local_comm_port, DFCommHandler, ch)
    StartServer("localhost", local_screen_port, DFScreenHandler, ch)
    for i := 0; i < server_count; i++ {
        <-ch
    }
}

func readInt32(data []byte) int32 {
    var ret int32
    b := bytes.NewBuffer(data)
    binary.Read(b, binary.LittleEndian, &ret)
    return ret
}

func connReadInt32(conn net.Conn) (int32, bool) {
    raw, ok := readBytes(conn, 4)
    if !ok {
        return 0, false
    }
    return readInt32(raw), true
}

func readBytes(conn net.Conn, count int) ([]byte, bool) {
    if count == 0 {
        return make([]byte, 0), true
    }
    buf := make([]byte, count)
    length, err := conn.Read(buf)
    if err != nil {
        log.Printf("Read failed: %v\n", err)
        return nil, false
    }
    if length != count {
        log.Printf("Read failed: Expected %d bytes, got %d\n", count, length)
        return nil, false
    }
    return buf, true
}

func DFCommHandler(conn net.Conn) {
    defer conn.Close()
    df_id, ok := readBytes(conn, 8)
    if !ok {
        return
    }
    game := FindGame(string(df_id), true)
    if game.comm.dfconn != nil {
        log.Printf("DF %s comm connection already exists\n", df_id)
        return
    }
    log.Printf("New connection: %s (comm)\n", df_id)
    game.comm.dfconn = &conn
    defer func(){ game.comm.dfconn = nil }()
    for {
        buflength, ok := connReadInt32(conn)
        if !ok {
            return
        }
        raw_data, ok := readBytes(conn, int(buflength))
        if !ok {
            return
        }
        if buflength == 0 {
            continue
        }
        var data comm_data
        err := json.Unmarshal(raw_data, &data)
        if err != nil {
            log.Printf("Invalid JSON: %v\n", err)
        } else {
            if data.Info.Df_version != "" {
                game.df_version = data.Info.Df_version
            }
            if data.Info.Dfhack_version != "" {
                game.dfhack_version = data.Info.Dfhack_version
            }
            if data.Info.Name != "" {
                game.name = data.Info.Name
            }
        }
    }
}

func DFScreenHandler(conn net.Conn) {
    defer conn.Close()
    df_id, ok := readBytes(conn, 8)
    if !ok {
        return
    }
    game := FindGame(string(df_id), true)
    if game.screen.dfconn != nil {
        log.Printf("DF %s screen connection already exists\n", df_id)
        return
    }
    log.Printf("New connection: %s (screen)\n", df_id)
    game.screen.dfconn = &conn
    defer func(){ game.screen.dfconn = nil }()
    for {
        buflength, ok := connReadInt32(conn)
        if !ok {
            return
        }
        data, ok := readBytes(conn, int(buflength))
        _ = data
        if !ok {
            return
        }
    }
}