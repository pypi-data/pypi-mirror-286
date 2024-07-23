#! /usr/bin/env bash

function kamangir_action_git_before_push() {
    if [[ "$(abcli_git get_branch)" == "main" ]]; then
        kamangir build_README
        kamangir pypi build
    fi
}
