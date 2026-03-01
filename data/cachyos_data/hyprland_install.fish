#!/usr/bin/fish

echo "Hyprland is a tiling window manager for Linux."
echo ""
echo "It is a Wayland compositor that is designed to be lightweight, fast, and easy to configure."
echo ""
echo "It is a great choice for users who want a modern, customizable desktop experience."
echo ""
read -P "Do you want to install Hyprland? (y/n) " -l REPLY
echo ""
if string match -qr '^[Yy]$' -- "$REPLY"
   echo "Do you want to install (1) HyDE or (2) ML4W OS?"
   echo ""
   if string match -qr '^[1]$' -- "$REPLY"
      echo "Installing HyDE..."
      sudo pacman -S --needed git base-devel
      git clone --depth 1 https://github.com/HyDE-Project/HyDE ~/HyDE 
      cd ~/HyDE/Scripts
      ./install.sh
      echo "HyDE installation complete."
   else if string match -qr '^[2]$' -- "$REPLY"
      echo "Installing ML4W OS..."
      bash -c "bash <(curl -s https://ml4w.com/os/rolling)"
      echo "ML4W OS installation complete."
   else
      echo "Invalid choice. Installation aborted by user."
   end
else 
   echo "Hyprland installation aborted by user."
end