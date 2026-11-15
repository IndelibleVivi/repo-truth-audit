package main

import (
    "encoding/json"
    "fmt"
    "os"
    "sort"

    "github.com/spf13/viper"
)

type Config struct {
    Host string `mapstructure:"host" json:"host"`
}

type Reading struct {
    Environment string `json:"environment"`
    Direct string `json:"direct"`
    Decoded Config `json:"decoded"`
    KnownKeys []string `json:"known_keys"`
    Error string `json:"error"`
}

type Observation struct {
    Variant string `json:"variant"`
    Readings []Reading `json:"readings"`
}

func check(err error) {
    if err != nil { panic(err) }
}

func read(v *viper.Viper, value string) Reading {
    check(os.Setenv("RTA_TRANSFER_HOST", value))
    var cfg Config
    err := v.Unmarshal(&cfg)
    errText := ""
    if err != nil { errText = err.Error() }
    keys := v.AllKeys()
    sort.Strings(keys)
    return Reading{value, v.GetString("host"), cfg, keys, errText}
}

func main() {
    out := []Observation{}
    for _, variant := range []string{"automatic-only", "bound-key", "default-key", "experimental-struct", "snapshot-override"} {
        check(os.Setenv("RTA_TRANSFER_HOST", "alpha"))
        var v *viper.Viper
        if variant == "experimental-struct" {
            v = viper.NewWithOptions(viper.ExperimentalBindStruct())
        } else {
            v = viper.New()
        }
        v.SetEnvPrefix("RTA_TRANSFER")
        v.AutomaticEnv()
        switch variant {
        case "bound-key": check(v.BindEnv("host"))
        case "default-key": v.SetDefault("host", "fallback")
        case "snapshot-override": v.Set("host", v.GetString("host"))
        }
        out = append(out, Observation{variant, []Reading{read(v, "alpha"), read(v, "beta")}})
    }
    for _, allow := range []bool{false, true} {
        v := viper.New()
        v.SetEnvPrefix("RTA_TRANSFER")
        v.AutomaticEnv()
        v.SetDefault("host", "fallback")
        v.AllowEmptyEnv(allow)
        out = append(out, Observation{fmt.Sprintf("empty-allowed-%t", allow), []Reading{read(v, "")}})
    }
    encoder := json.NewEncoder(os.Stdout)
    encoder.SetIndent("", "  ")
    check(encoder.Encode(out))
}
