package main

import (
    "github.com/gorilla/websocket"
)

type connection struct {
    ws *websocket.Conn
    send chan []byte
}
