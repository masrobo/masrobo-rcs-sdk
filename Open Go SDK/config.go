package boticzopen

import (
	"errors"
	"net/http"
	"strings"
	"time"
)

const defaultTimeout = 30 * time.Second

// Config defines how the SDK connects to the Open API.
type Config struct {
	BaseURL    string
	Token      string
	HTTPClient *http.Client
}

func (c Config) validate() error {
	if strings.TrimSpace(c.BaseURL) == "" {
		return errors.New("baseURL is required")
	}
	if strings.TrimSpace(c.Token) == "" {
		return errors.New("token is required")
	}
	return nil
}

func (c Config) normalizedBaseURL() string {
	return strings.TrimRight(strings.TrimSpace(c.BaseURL), "/")
}

func (c Config) normalizedHTTPClient() *http.Client {
	if c.HTTPClient != nil {
		return c.HTTPClient
	}
	return &http.Client{Timeout: defaultTimeout}
}
