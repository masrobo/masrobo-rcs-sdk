package masrobo

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"reflect"
	"strings"
)

// Client is the entry point of the Open API SDK.
type Client struct {
	baseURL    string
	config     Config
	httpClient *http.Client

	IotDevice *IotDeviceService
}

func (c *Client) do(ctx context.Context, method, path string, query any, body any, out any) error {
	fullURL, err := c.buildURL(path, query)
	if err != nil {
		return err
	}

	var requestBody io.Reader
	if body != nil {
		payload, err := json.Marshal(body)
		if err != nil {
			return fmt.Errorf("marshal request body: %w", err)
		}
		requestBody = bytes.NewReader(payload)
	}

	req, err := http.NewRequestWithContext(ctx, method, fullURL, requestBody)
	if err != nil {
		return fmt.Errorf("create request: %w", err)
	}

	token, err := c.config.GenerateJWTToken()
	if err != nil {
		return fmt.Errorf("generate JWT token: %w", err)
	}

	req.Header.Set("Accept", "application/json")
	req.Header.Set("X-Token", token)
	if body != nil {
		req.Header.Set("Content-Type", "application/json")
	}

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return fmt.Errorf("send request: %w", err)
	}
	defer resp.Body.Close()

	rawBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("read response body: %w", err)
	}

	var env apiEnvelope
	if len(rawBody) > 0 {
		if err := json.Unmarshal(rawBody, &env); err != nil {
			if resp.StatusCode >= http.StatusBadRequest {
				return &APIError{
					StatusCode: resp.StatusCode,
					Message:    "invalid JSON response",
					RawBody:    rawBody,
				}
			}
			return fmt.Errorf("decode response body: %w", err)
		}
	}

	if resp.StatusCode >= http.StatusBadRequest || env.Code != successCode {
		return newAPIError(resp.StatusCode, &env, rawBody)
	}

	if err := decodeSuccessData(env.Data, out); err != nil {
		return fmt.Errorf("decode response data: %w", err)
	}

	return nil
}

func (c *Client) buildURL(path string, query any) (string, error) {
	fullURL := c.baseURL + "/" + strings.TrimLeft(path, "/")

	if query == nil {
		return fullURL, nil
	}

	values, err := encodeQuery(query)
	if err != nil {
		return "", err
	}
	if len(values) == 0 {
		return fullURL, nil
	}

	return fullURL + "?" + values.Encode(), nil
}

func encodeQuery(input any) (url.Values, error) {
	values := url.Values{}

	v := reflect.ValueOf(input)
	if !v.IsValid() {
		return values, nil
	}
	if v.Kind() == reflect.Pointer {
		if v.IsNil() {
			return values, nil
		}
		v = v.Elem()
	}
	if v.Kind() != reflect.Struct {
		return nil, fmt.Errorf("query params must be a struct")
	}

	t := v.Type()
	for i := 0; i < v.NumField(); i++ {
		field := t.Field(i)
		if !field.IsExported() {
			continue
		}

		tag := field.Tag.Get("url")
		if tag == "" || tag == "-" {
			continue
		}

		value := v.Field(i)
		if value.Kind() == reflect.Pointer {
			if value.IsNil() {
				continue
			}
			value = value.Elem()
		}

		stringValue := fmt.Sprint(value.Interface())
		if strings.TrimSpace(stringValue) == "" {
			continue
		}
		values.Set(tag, stringValue)
	}

	return values, nil
}
