package masrobo

type RcsController struct {
	client *Client
}

// NewRcsController creates a new RCS controller.
func NewRcsController(cfg Config) (*RcsController, error) {
	if err := cfg.validate(); err != nil {
		return nil, err
	}

	client := &Client{
		baseURL:    cfg.normalizedBaseURL(),
		config:     cfg,
		httpClient: cfg.normalizedHTTPClient(),
	}

	client.IotDevice = &IotDeviceService{client: client}
	return &RcsController{client: client}, nil
}
