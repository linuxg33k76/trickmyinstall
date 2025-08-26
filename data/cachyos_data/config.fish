source /usr/share/cachyos-fish-config/cachyos-config.fish

# overwrite greeting
# potentially disabling fastfetch
#function fish_greeting
#    # smth smth
#end

# Added by TrickMyInstall Script

set -x EDITOR /usr/bin/vim
echo && ~/code/bash_scripts/backupservercheck.sh && echo
alias git-update='git checkout main && git pull origin main && git checkout develop'
alias git-merge='git checkout main && git pull origin main && git merge main develop && git push origin main && git checkout develop'
alias update='sudo paru -Syyu && flatpak update -y'
alias wirelesspw='nmcli device wifi show-password'
