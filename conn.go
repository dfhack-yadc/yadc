package main

import (
	"github.com/gorilla/websocket"
	"net/http"
)

// connection is an middleman between the websocket connection and the hub.
type connection struct {
	// The websocket connection.
	ws *websocket.Conn

	// Buffered channel of outbound messages.
	send chan []byte
}

func serveWs(w http.ResponseWriter, r *http.Request) {
}
