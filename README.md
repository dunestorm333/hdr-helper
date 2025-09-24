# hdr-helper 💻
Linux script to control and automatically toggle HDR on KDE Plasma.

![image](https://github.com/user-attachments/assets/87bc05e1-9235-487c-a61f-c03f273b3e4a)

I've personally tested this on Fedora 41 & 42, and Arch Linux (all running the Plasma DE) on an RX 6800XT using the standard RADV drivers which
are built into the Linux Kernel. I only have one display, I've not accounted for multi-display scenarios so 
please take this into consideration :)

## Supported Features 📋
- Automatically & manually toggling HDR on and off.
- Notifying you whether HDR has been successfully activated.
- Setting a target SDR brightness level whilst in HDR mode.
- Setting a target SDR to HDR coversion brightness level in nits.
    - Your original non-HDR brightness level will be preserved when switching back.

# The Problem
At this moment in time, pretty much all games require HDR to be manually enabled for it to properly function. Normally
this isn't a problem when using Gamescope as your native compositor. Most people however run a fully fledged desktop
environment on their PCs unless they're using SteamOS or Bazzite.

This can be annoying because running Gamescope from within KDE Plasma with the HDR flag enabled still won't magically
make HDR work, unless it's also enabled from your compositor's side too; in this case, KWin. Although KWin has a way
to enable HDR from the command line, the implementation is flawed as most monitors will only properly display HDR
after also changing video modes. In other words, the HDR signal must be present BEFORE HDR-compatible monitors will
recognise what to do; this happens usually once the monitor is forced to change resolution or refresh rate.

# The Solution
I've created a script which will toggle HDR from KDE Plasma's in-built `kscreen-doctor` helper and also force change
video modes. This means that whenever you launch a HDR-compatible game, you won't ever need to manually enable HDR
again since this script can be used as a launch parameter for Steam and third party apps. Of course you may also call
this script manually and force HDR to be on or off if you so desire.

*Some configuration is required!*

---

# Setup
To start with, clone this repository and create a symbolic link to the file:
```bash
git clone https://github.com/dunestorm333/hdr-helper.git
cd hdr-helper

# Not all distros will create the below path, create it assuming that it doesn't
# exist on your system. Some distros can be fussy where they search for the path.
mkdir ~/.local/bin/
# For Fedora based distros (more portable)
ln -s $PWD/hdr-helper ~/.local/bin/
# For Arch based distros (more compatible)
sudo ln -s $PWD/hdr-helper /usr/bin/

chmod +x ~/.local/bin/hdr-helper

# You will also need to copy monitor.conf into ~/.config/hdr-helper
mkdir ~/.config/hdr-helper
cp monitor.conf ~/.config/hdr-helper
```

**Ensure to modify `monitor.conf` with your desired settings.**

`xrandr` will give you the following output; in the below example `DP-3` is the value we need to use to target
the active monitor.
```
Screen 0: minimum 16 x 16, current 3440 x 1440, maximum 32767 x 32767
DP-3 connected primary 3440x1440+0+0 (normal left inverted right x axis y axis) 800mm x 337mm
...
```

Below is an example of the help output of the script:
```
--- Usage ---
hdr-helper    | The default behaviour will automatically enable or disable HDR
hdr-helper -e | Force enables HDR
hdr-helper -d | Force disables HDR
hdr-helper -s | Shows detected HDR status as a system notification
hdr-helper -v | Displays version information
hdr-helper -h | Displays this help screen

--- Info ---
Currently only KDE Plasma is supported running Wayland. Ensure that kscreen-doctor
is present on your system for HDR Helper to function.

--- Config ---
Please modify the MONITOR, NATIVE_RES and TEMP_RES values in monitor.conf.
```

# Usage
## Using with Steam & Gamescope
Firstly, ensure that Gamescope is installed and working.
From Steam, right click on the game you'd like to automatically enable HDR for and click on **Properties...**

![image](https://github.com/user-attachments/assets/d8d654bf-3f74-4d7a-bb73-088674b73701)

Now enter the below command into the launch options:
![image](https://github.com/user-attachments/assets/5cbe5129-2d1c-48ab-82d0-5f19be39c15a)

Effectively what we're doing here is affixing and suffixing the standard Gamescope launch commands with `hdr-helper`.
``` bash
hdr-helper ; gamescope -W 3440 -H 1440 -r 165 -f --hdr-enabled -- %command% ; hdr-helper
```
## Using with standalone Apps & Gamescope
The commands you need to get this working with pretty much any app or game is very similar to the Steam method. Note that in both
cases, Gamescope is required as HDR requires a valid HDR layer and compositor to properly function in addition to working drivers.
``` bash
hdr-helper; gamescope -W 3440 -H 1440 -r 165 -f --hdr-enabled ~/my-app-or-game; hdr-helper
```
## Manual Approach
If you'd like to manually bind HDR Helper to a shortcut key for example, this can easily by configured in most desktop environments.

Using KDE Plasma, you may do this from the System Shortcuts page. Click **Add New > Command or Script...**
![image](https://github.com/user-attachments/assets/9bed0ef1-d299-4275-831b-2339bb7ebc45)

Now specify the `hdr-helper` command in the **command** field and give the shortcut a **name**.
![image](https://github.com/user-attachments/assets/bbe9b5cd-0e13-488f-a648-86ace98e8533)

You may now assign a key-combination to toggle the shortcut. Remember to click **Apply** when done!
![image](https://github.com/user-attachments/assets/fdd7742e-233b-411b-a4e1-134a88658f6b)


