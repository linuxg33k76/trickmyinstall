# This script applies a fix for VS Code Flatpak to work with KDE Wallet

if grep -q '"password-store":"kwallet5"' /home/${USER}/.vscode/argv.json; then
    echo "VS Code Flatpak already configured for KDE Wallet."
    exit 1
fi

# Modify argv.json to include the password-store setting
# sed command to insert the line before the closing brace and adds a tab before the text for proper JSON formatting

echo "Applying VS Code Flatpak KDE Wallet fix..."
sed -i '/}/i\\t// Password Store Setup for VS Code Flatpak on KDE Plasma' /home/${USER}/.vscode/argv.json
sed -i '/}/i\\t"password-store": "kwallet5"' /home/${USER}/.vscode/argv.json

exit 0