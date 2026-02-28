#!/usr/bin/fish

echo "Setting up ML4W OS"
echo ""
if test -d "$HOME/.config/hypr/"
   echo "Hypr config directory exists. Installing ML4W OS?"
   # Note: Fish uses 'read' slightly differently than bash
   read -P "Do you want to install ML4W OS? (y/n) " -l REPLY
   if string match -qr '^[Yy]$' -- "$REPLY"
      curl -s https://ml4w.com/os/rolling | bash
      echo "ML4W OS installation complete."
   else
      echo "Installation aborted by user."
   end
else
   echo "Error: Hypr config directory not found at $HOME/.config/hypr/"
end