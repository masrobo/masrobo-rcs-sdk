package masrobo

import (
	"fmt"
	"strings"

	"github.com/go-playground/validator/v10"
)

var sdkValidator = validator.New()

func validateRequest(v any) error {
	if err := sdkValidator.Struct(v); err != nil {
		if validationErrors, ok := err.(validator.ValidationErrors); ok && len(validationErrors) > 0 {
			first := validationErrors[0]
			fieldName := lowerFirst(first.Field())

			switch first.Tag() {
			case "required":
				return fmt.Errorf("%s is required", fieldName)
			case "oneof":
				return fmt.Errorf("%s must be one of [%s]", fieldName, first.Param())
			}
		}

		return err
	}

	return nil
}

func lowerFirst(s string) string {
	if s == "" {
		return s
	}

	return strings.ToLower(s[:1]) + s[1:]
}
