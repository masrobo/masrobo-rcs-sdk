package masrobo

import (
	"errors"
	"net/http"
	"strings"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

const defaultTimeout = 30 * time.Second

// Config defines how the SDK connects to the Open API.
type Config struct {
	BaseURL    string
	AppID      string
	AppKey     string
	HTTPClient *http.Client
}

func (c Config) validate() error {
	if strings.TrimSpace(c.BaseURL) == "" {
		return errors.New("baseURL is required")
	}
	if strings.TrimSpace(c.AppID) == "" {
		return errors.New("appID is required")
	}
	if strings.TrimSpace(c.AppKey) == "" {
		return errors.New("appKey is required")
	}
	return nil
}

func (c Config) normalizedBaseURL() string {
	return strings.TrimRight(strings.TrimSpace(c.BaseURL), "/")
}

func (c Config) normalizedAppID() string {
	return strings.TrimSpace(c.AppID)
}

func (c Config) normalizedAppKey() string {
	return strings.TrimSpace(c.AppKey)
}

func (c Config) GenerateJWTToken() (string, error) {
	claims := jwt.MapClaims{
		"app_id": c.normalizedAppID(),
		"iat":    time.Now().Unix(),
		"exp":    time.Now().Add(time.Hour).Unix(), // 1 hour expiration
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(c.normalizedAppKey()))
}

func (c Config) normalizedHTTPClient() *http.Client {
	if c.HTTPClient != nil {
		return c.HTTPClient
	}
	return &http.Client{Timeout: defaultTimeout}
}
