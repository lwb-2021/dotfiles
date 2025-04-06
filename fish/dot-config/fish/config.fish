# Put system-wide fish configuration entries here
# or in .fish files in conf.d/
# Files in conf.d can be overridden by the user
# by files with the same name in $XDG_CONFIG_HOME/fish/conf.d

# This file is run by all fish instances.
# To include configuration only for login shells, use
# if status is-login
#    ...
# end
# To include configuration only for interactive shells, use

setenv SSH_AUTH_SOCK $XDG_RUNTIME_DIR/gcr/ssh

function y
	set tmp (mktemp -t "yazi-cwd.XXXXXX")
	yazi $argv --cwd-file="$tmp"
	if set cwd (command cat -- "$tmp"); and [ -n "$cwd" ]; and [ "$cwd" != "$PWD" ]
		builtin cd -- "$cwd"
	end
	rm -f -- "$tmp"
end

alias "pandoc-zh"='pandoc --pdf-engine xelatex -V CJKmainfont="微软雅黑"'

if status is-interactive
    thefuck --alias | source
    fzf --fish | source
    starship init fish | source
    fastfetch
end


