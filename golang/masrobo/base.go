package masrobo

import (
	"encoding/json"
	"net/http"
)

const successCode = 200

type apiEnvelope struct {
	Code int             `json:"code"`
	Msg  string          `json:"msg"`
	Data json.RawMessage `json:"data"`
}

func decodeSuccessData(data json.RawMessage, out any) error {
	if out == nil || len(data) == 0 || string(data) == "null" {
		return nil
	}
	return json.Unmarshal(data, out)
}

func newAPIError(statusCode int, env *apiEnvelope, rawBody []byte) *APIError {
	if env != nil {
		return &APIError{
			StatusCode: statusCode,
			Code:       env.Code,
			Message:    env.Msg,
			RawBody:    rawBody,
		}
	}

	return &APIError{
		StatusCode: statusCode,
		Message:    http.StatusText(statusCode),
		RawBody:    rawBody,
	}
}
