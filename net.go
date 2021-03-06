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
    read_max = 2000000
    upgrader = websocket.Upgrader{
        ReadBufferSize:  1024,
        WriteBufferSize: 1024,
    }
)

type connection struct {
    ws *websocket.Conn
    send chan []byte
}

type hub struct {
    dfconn *net.Conn
    clients map[*connection]bool

    addconn chan *connection
    rmconn chan *connection
    broadcast chan []byte
}

func NewHub() *hub {
    return &hub{
        clients: make(map[*connection]bool),
        addconn: make(chan *connection),
        rmconn: make(chan *connection),
        broadcast: make(chan []byte),
    }
}

func (h *hub) Broadcast() {

}

type main_comm_data struct {
    Auth struct {
        Username string `json:"username"`
        Password string `json:"password"`
        Logged_in bool `json:"logged_in"`
        Id string `json:"id"`
    } `json:"auth"`
}

type df_comm_data struct {
    Info struct {
        Df_version string `json:"df_version"`
        Dfhack_version string `json:"dfhack_version"`
        Name string `json:"name"`
    } `json:"info"`
    Dims struct {
        X int `json:"x"`
        Y int `json:"y"`
    } `json:"dims"`
}

func StartServer(host string, port int, handler func(net.Conn), done *sem) {
    addr := host + ":" + strconv.Itoa(port)
    sock, err := net.Listen("tcp", addr)
    if err != nil {
        log.Fatalf("Could not bind to %s: %v", addr, err)
    }
    log.Printf("Listening on %s", addr)
    done.Inc()
    go func(){
        defer log.Printf("Shutting down %s", addr)
        defer sock.Close()
        defer done.Dec()
        for {
            conn, err := sock.Accept()
            if err != nil {
                log.Fatalf("Failed to accept connection on %s: %v", addr, err)
            }
            go handler(conn)
        }
    }()
}

func StartNet(host string, comm_port int, screen_port int, done *sem) {
    StartServer("localhost", comm_port, DFCommHandler, done)
    StartServer("localhost", screen_port, DFScreenHandler, done)
}

func readInt32(data []byte) (ret int32) {
    binary.Read(bytes.NewBuffer(data), binary.LittleEndian, &ret)
    return
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
    if count > read_max {
        log.Printf("Read failed: Maximum packet length exceeded (%d > %d)", count, read_max)
        return nil, false
    }
    buf := make([]byte, count)
    length, err := conn.Read(buf)
    if err != nil {
        buf = buf[:0]
        log.Printf("Read failed: %v", err)
        return nil, false
    }
    if length != count {
        buf = buf[:0]
        log.Printf("Read failed: Expected %d bytes, got %d", count, length)
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
        log.Printf("%s: comm connection already exists", game)
        return
    }
    log.Printf("%s: New connection (comm)", game)
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
        var data df_comm_data
        err := json.Unmarshal(raw_data, &data)
        if err != nil {
            log.Printf("%s: Invalid JSON: %v", game, err)
        } else {
            if data.Info.Df_version != "" {
                game.df_version = data.Info.Df_version
            }
            if data.Info.Dfhack_version != "" {
                game.dfhack_version = data.Info.Dfhack_version
            }
            if data.Info.Name != "" {
                game.name = data.Info.Name
                game.valid = true
                log.Printf("%s: Initialized", game)
            }
            x, y := data.Dims.X, data.Dims.Y
            if x != 0 && y != 0 {
                if x > 256 || y > 256 || x < 80 || y < 25 {
                    log.Printf("%s: Invalid dimensions: %d, %d", game, x, y)
                } else {
                    game.screen_data.dims.x = uint16(x)
                    game.screen_data.dims.y = uint16(y)
                    log.Printf("%s: Resized to %d, %d", game, x, y)
                }
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
        log.Printf("%s: screen connection already exists", game)
        return
    }
    log.Printf("%s: New connection (screen)", game)
    game.screen.dfconn = &conn
    defer func(){ game.screen.dfconn = nil }()
    for {
        buflength, ok := connReadInt32(conn)
        if !ok {
            return
        }
        data, ok := readBytes(conn, int(buflength))
        if !ok {
            return
        }
        for i := 0; i < len(data); i += 5 {
            off := game.screen_data.rawOffset(data[i], data[i + 1])
            copy(game.screen_data.raw[off:off+5], data[i:i+5])
        }
    }
}


// func serveWs(w http.ResponseWriter, r *http.Request) {
//     ws, err := upgrader.Upgrade(w, r, nil)
//     if err != nil {
//         log.Println(err)
//         return
//     }
//     c := &connection{send: make(chan []byte, 256), ws: ws}
//     h.register <- c
//     go c.writePump()
//     c.readPump()
// }

