package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"time"
)

type CronPulse struct {
	apiKey  string
	baseURL string
}

func NewCronPulse(apiKey string) *CronPulse {
	return &CronPulse{apiKey: apiKey, baseURL: "https://api.cronpulse.com"} // Replace with your API URL
}

type Monitor struct {
	monitorID string
	apiKey    string
	baseURL   string
}

func (cp *CronPulse) CreateMonitor(name string, interval int, email string, expiresAt time.Time) (*Monitor, error) {
	data := map[string]interface{}{"name": name, "interval": interval, "email": email, "expires_at": expiresAt.Format(time.RFC3339)}
	jsonData, _ := json.Marshal(data)
	resp, err := http.Post(cp.baseURL+"/monitors", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	var result map[string]string
	json.NewDecoder(resp.Body).Decode(&result)
	return &Monitor{monitorID: result["id"], apiKey: cp.apiKey, baseURL: cp.baseURL}, nil
}

func (m *Monitor) Ping() error {
	_, err := http.Post(m.baseURL+"/monitors/"+m.monitorID+"/ping", "", nil)
	return err
}

func (m *Monitor) Delete() error {
	_, err := http.Delete(m.baseURL+"/monitors/"+m.monitorID)
	return err
}
