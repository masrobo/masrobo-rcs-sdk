package masrobo

import "fmt"

// APIError represents an HTTP or business error returned by the Open API.
type APIError struct {
	StatusCode int
	Code       int
	Message    string
	RawBody    []byte
}

func (e *APIError) Error() string {
	if e == nil {
		return ""
	}
	if e.Code != 0 {
		return fmt.Sprintf("open api error: status=%d code=%d message=%s", e.StatusCode, e.Code, e.Message)
	}
	return fmt.Sprintf("open api error: status=%d message=%s", e.StatusCode, e.Message)
}
