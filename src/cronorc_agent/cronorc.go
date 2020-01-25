package main

import (
	"bytes"
	"encoding/json"
	"log"
	"io/ioutil"
	"net"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"time"
)

const version = 1

type Message struct {
	Version  int    `json:"version"`
	Command  string `json:"command"`
	Exitcode int    `json:"exitcode"`
	Start    string `json:"start"`
	Elapsed  int64  `json:"elapsed"`
	Hostname string `json:"hostname"`
	IP       string `json:"ip"`
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: cronorc <command> <arg1> <arg2>...")
	}
	prog := os.Args[1]
	args := os.Args[2:]
	cmd := exec.Command(prog, args...)
	start := time.Now()
	cmd.CombinedOutput()
	end := time.Now()
	hostname, _ := os.Hostname()
	m := Message{
		Version:  version,
		Command:  strings.Join(os.Args[1:], " "),
		Exitcode: cmd.ProcessState.ExitCode(),
		Start:    start.UTC().Format(time.RFC3339),
		Elapsed:  int64(end.Sub(start) / time.Millisecond),
		Hostname: hostname,
		IP:       getLocalIP(),
	}
	// fmt.Printf("%+v\n", m)
	sendMessage(m)
}

// GetLocalIP returns the non loopback local IP of the host
func getLocalIP() string {
	addrs, err := net.InterfaceAddrs()
	if err != nil {
		return ""
	}
	for _, address := range addrs {
		// check the address type and if it is not a loopback the display it
		if ipnet, ok := address.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
			if ipnet.IP.To4() != nil {
				return ipnet.IP.String()
			}
		}
	}
	return ""
}

// Posts the message to the URL pointed to by the CRONORC_URL env variable
func sendMessage(message Message) {
	url := os.Getenv("CRONORC_URL")
	if url == "" {
		log.Fatal("The CRONORC_URL environment variable is missing")
	}
	data, json_err := json.Marshal(message)
	if json_err != nil {
		log.Fatal(json_err)
	}
	resp, err := http.Post(url, "application/json", bytes.NewBuffer(data))
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()
	ioutil.ReadAll(resp.Body) // prevents "Connection reset by peer" errors on server
	if resp.StatusCode != 200 {
		log.Fatal("Server responded: ", resp.Status)
	}
}
