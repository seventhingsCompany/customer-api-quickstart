package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/SeventhingsCompany/customer-api-go/client"
	"github.com/SeventhingsCompany/customer-api-go/models"
)

func required(key string) string {
	value := os.Getenv(key)
	if value == "" {
		panic("Set " + key)
	}
	return value
}

func output(value any) error { return json.NewEncoder(os.Stdout).Encode(value) }

func run() error {
	action := "hello"
	if len(os.Args) > 1 {
		action = os.Args[1]
	}
	switch action {
	case "hello", "export", "lookup", "create", "update", "attach", "history":
	default:
		return fmt.Errorf("use hello, export, lookup, create, update, attach, or history")
	}
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
	defer cancel()
	url := required("SEVENTHINGS_INSTANCE_URL")
	var c *client.Client
	var err error
	if token := os.Getenv("SEVENTHINGS_TOKEN"); token != "" {
		c = client.NewWithToken(url, token)
	} else {
		c, err = client.NewWithCredentials(ctx, url, required("SEVENTHINGS_USERNAME"), required("SEVENTHINGS_PASSWORD"), required("SEVENTHINGS_CLIENT_ID"))
		if err != nil {
			return err
		}
	}
	opts := &models.ListOptions{Page: 1, PerPage: 100}
	if field := os.Getenv("SEVENTHINGS_FILTER_FIELD"); field != "" {
		opts.Filters = []models.FilterEntry{{Field: field, Operator: models.FilterLike, Values: []string{required("SEVENTHINGS_FILTER_VALUE")}}}
	}
	switch action {
	case "hello":
		ping, err := c.Ping(ctx)
		if err != nil {
			return err
		}
		definitions, err := c.FieldDefinitionsList(ctx, "asset")
		if err != nil {
			return err
		}
		objects, err := c.ObjectsList(ctx, opts)
		if err != nil {
			return err
		}
		return output(map[string]any{"ping": ping, "fieldDefinitions": definitions, "objects": objects})
	case "export":
		for obj, err := range c.ObjectsAll(ctx, opts) {
			if err != nil {
				return err
			}
			if err = output(obj); err != nil {
				return err
			}
		}
	case "lookup":
		obj, err := c.ObjectGetByBarcode(ctx, required("SEVENTHINGS_BARCODE"))
		if err != nil {
			return err
		}
		return output(obj)
	case "create", "update":
		data, err := os.ReadFile(required("SEVENTHINGS_PAYLOAD_FILE"))
		if err != nil {
			return err
		}
		var fields map[string]any
		if err = json.Unmarshal(data, &fields); err != nil {
			return err
		}
		if fields == nil {
			return fmt.Errorf("payload must be a JSON object")
		}
		if action == "create" {
			missing, err := c.MissingMandatoryFields(ctx, "asset", fields)
			if err != nil {
				return err
			}
			if len(missing) > 0 {
				return fmt.Errorf("missing required fields: %v", missing)
			}
			uuid, err := c.ObjectCreate(ctx, fields)
			if err != nil {
				return err
			}
			return output(map[string]any{"uuid": uuid})
		}
		uuid := required("SEVENTHINGS_OBJECT_UUID")
		if err := c.ObjectPatch(ctx, uuid, fields); err != nil {
			return err
		}
		return output(map[string]any{"uuid": uuid, "updated": true})
	case "attach":
		uuid := required("SEVENTHINGS_OBJECT_UUID")
		field := required("SEVENTHINGS_ATTACHMENT_FIELD")
		path := required("SEVENTHINGS_FILE")
		f, err := os.Open(path)
		if err != nil {
			return err
		}
		defer f.Close()
		fileUUID, err := c.FileUpload(ctx, filepath.Base(path), f)
		if err != nil {
			return err
		}
		resp, err := c.ObjectAddFiles(ctx, uuid, []models.FileAttachment{{FieldKey: field, FileUUID: fileUUID}})
		if err != nil {
			return err
		}
		if err = output(map[string]any{"fileUuid": fileUUID, "status": resp.StatusCode, "body": json.RawMessage(resp.Body)}); err != nil {
			return err
		}
		if resp.StatusCode == 207 {
			return fmt.Errorf("partial attachment result; inspect output before retrying")
		}
	case "history":
		uuid := required("SEVENTHINGS_OBJECT_UUID")
		for page := 1; ; page++ {
			result, err := c.ObjectHistory(ctx, uuid, &models.HistoryListOptions{Page: page, PerPage: 100})
			if err != nil {
				return err
			}
			for _, item := range result.Items {
				if err = output(item); err != nil {
					return err
				}
			}
			if result.Page*result.PerPage >= result.Total || len(result.Items) == 0 {
				break
			}
		}
	}
	return nil
}

func main() {
	defer func() {
		if err := recover(); err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
	}()
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
