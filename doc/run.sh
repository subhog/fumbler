#!/bin/zsh

pandoc index.md -o index.html --from=markdown+fenced_code_blocks+backtick_code_blocks+pipe_tables+grid_tables


