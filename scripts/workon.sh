#!/bin/bash
# delegates function execution to script

PYTHON_EXEC="$(command \which python)"

# from: https://bitbucket.org/virtualenvwrapper/virtualenvwrapper/src/cee707f128e39623718568b47b6038e8d62c5f34/virtualenvwrapper.sh?at=master&fileviewer=file-view-default#virtualenvwrapper.sh-99
function _cd {
    if [ -n "$BASH" ]
    then
        builtin \cd "$@"
    elif [ -n "$ZSH_VERSION" ]
    then
        builtin \cd -q "$@"
    else
        command \cd "$@"
    fi
}


function work {
    typeset result
    typeset output
    cwd=$(pwd)

    output=$(\
        command \cd ~ && \
        "$PYTHON_EXEC" "/work/labs/workon/workon/workon.py" "$@" --default_path="$cwd" \
    )
    result=$?

    if [ $result -eq 0 ]; then
        if [ -d "$output" ]; then
            _cd $output
        else
            echo "$output"
        fi
    elif [ $result -eq 1 ]; then
        echo $output
        cat - 1>&2 <<EOF
workon.sh: There was a problem running program.

If Python could not import the module workon.main,
check that workon has been installed with -- pip install workon
EOF
    fi

    return $result
}
