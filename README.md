# Important!
This project is **WIP**
Most things aren't supposed to work yet.
Feel free to try it, if you want to, but don't expect fireworks.

# Zut Calendar TUI client

This project aims to improve the life of ZUT students that love the terminal!

If you're tired of checking `https://plan.zut.edu.pl/` every day and don't like classic calendar integration, it's something for you.


*state of project as of 4.03.2026 with class info redacted*
![Screenshot](./assets/screenshot.png)

# Supported platforms
It's Python so I guess it will work on anything. I develop and test this on NixOS, but from what I tested it should work on Windows too. I'm pretty sure macOS will work too, but I have no way of checking that, since I don't own a macbook…

# Install
## Nix
Primary way of installing this is using [nix flake](https://wiki.nixos.org/wiki/Flakes). To run this once just type:
```bash
nix run github:szymon-jozef/zut-calendar
```

If you want to install this type:
```bash
nix profile add github:szymon-jozef/zut-calendar
```

Or install this declaratively, by adding this to your flake

```nix
inputs = {
    zut-calendar.url = "github:szymon-jozef/zut-calendar";
};

outputs = { self, nixpkgs, zut-calendar, ... }: {
    nixosConfigurations."<your-hostname>" = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        modules = [
            ({ pkgs, ... }: {
                environment.systemPackages = [
                    zut-calendar.packages.${pkgs.system}.default
                ];
            })
        ];
    };
};
```
*you can do the same thing in home-manager if you want to…*

## Other Linux distros
Most Linux distros environments are externally managed by your package manager, so normal pip won't work. Download [pipx](https://github.com/pypa/pipx) and run
```bash
pipx install git+https://github.com/szymon-jozef/zut-calendar
```

## Windows
Just use normal pip
```bash
pip install git+https://github.com/szymon-jozef/zut-calendar
```
## macOS
I have no idea tbh, but pipx will probably work too.

# How to use?
Just type `zut-calendar`. You can set everything in the TUI itself. There are some flags that you can check by typing `zut-calendar --help`, but they will change a lot.

# Config
- On Unix-like systems config is stored in `$XDG_CONFIG_HOME/zut-calendar/config.ini`
- On Windows it's in `%LocalAppData%\szymon-jozef\zut-calendar\config.ini`

Example config is stored at `examples/config.ini`. It's copied to your config dir by default.
Entry names are pretty self-explanatory.

# Localisation
As of now this project supports English and Polish. Your language will be selected based on `$LANG`. If you want to overwrite it just set it before starting the program: `LANG=en zut-calendar`

## Translating to other languages
As of now it doesn't make any sense to translate this, because a lot will probably change. When I finish this I will be open for PRs.

# TODO
- [x] Proper grid layout with hours shown
- [ ] Focusing, moving around and checking specific class info
- [x] Checking other weeks than current
- [ ] Good styles

---
*Project inspired by [zutui](https://github.com/shv187/zutui)
