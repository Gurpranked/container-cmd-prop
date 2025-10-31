/*
Copyright © 2025 NAME HERE <EMAIL ADDRESS>
*/
package cmd

import (
	"fmt"
	"bytes"
	"encoding/json"
	"log"
	"os"
	"os/exec"

	"github.com/spf13/cobra"
)


var (
	parallel bool
	all bool
	cmdStrs []string
	containers []string		// arr of container names
)


// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "ccp",
	Short: "Execute commands to every container parallely or sequentially",
	Long: `A longer description that spans multiple lines and likely contains
examples and usage of using your application. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	// Uncomment the following line if your bare application
	// has an action associated with it:
	// Run: func(cmd *cobra.Command, args []string) { },
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}

	if (parallel && len(cmdStrs) > 0) {
		if len(containers) > 0 {
			go parallel_exec(containers, cmdStrs)
		} else if all {
			cr := os.Getenv("RUNC_CMD")		// container runtime, docker or podman
			if cr == "" {
				log.Fatal("RUNC_CMD not set")
			}

			command := fmt.Sprintf("%s ps --format json", cr)
			cmd := exec.Command("bash", "-c", command)

			// Create buffers to capture stdout and stderr
			var stdout, stderr bytes.Buffer
			cmd.Stdout = &stdout
			cmd.Stderr = &stderr

			err := cmd.Run()
			if err != nil {
				log.Fatalf("Command failed: %v\nStderr: %s", err, stderr.String())
			}

			var conts []map[string]any	// holds json in Go's way
			json.Unmarshal(stdout.Bytes(), &conts)

			for _, c := range conts {
				if names, ok := c["Names"].([]any); ok && len(names) > 0 {
					containers = append(containers, names[0].(string))
				}
			}

			go parallel_exec(containers, cmdStrs)
		}
		
		return
	}
}

func init() {
	// Here you will define your flags and configuration settings.
	// Cobra supports persistent flags, which, if defined here,
	// will be global for your application.

	// rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.ccp.yaml)")

	// Cobra also supports local flags, which will only run
	// when this action is called directly.


	// All the necessary flags
	rootCmd.Flags().BoolVarP(&all, "all", "A", true, "Execute command for all containers")
	rootCmd.PersistentFlags().BoolVarP(&parallel, "parallel", "p", true, "Run commands in parallel")
	rootCmd.Flags().StringSliceVar(&cmdStrs, "cmd", nil, "The command to execute")
	rootCmd.Flags().StringSliceVarP(&containers, "containers", "c", nil, "The containers to execute the command on")
}

func parallel_exec(containers []string, cmd []string) {
	
}


