# WexTerm

Create config
```lua tangle:tests/output/basic/wezterm.lua
local wezterm = require 'wezterm'
local config = wezterm.config_builder()
```

Set theme
```lua tangle:tests/output/basic/wezterm.lua
config.font = wezterm.font_with_fallback({
    { family = 'JetBrainsMono Nerd Font', weight = 'DemiBold' },
    { family = 'JetBrains Mono', weight = 'DemiBold' },
})
config.color_schemes = {
    ["redox"] = {
      foreground = "#DCE8E5",
      background = "#2E3434",
      cursor_bg = "#FFD7A0",
      cursor_fg = "#2E3434",
      cursor_border = "#FFD7A0",
      selection_bg = "#3F4A4A",
      selection_fg = "#E9F2EF",
      scrollbar_thumb = "#3A4141",
      split = "#3A4141",
      ansi = {
        "#2E3434", "#C26E63", "#7FB8A4", "#D6C38A",
        "#6FAFBD", "#B28FA3", "#8FC7B7", "#DCE8E5"
      },
      brights = {
        "#4A5353", "#E08A7F", "#A9D6C6", "#EBD9A8",
        "#92CAD4", "#D3ABC0", "#B6E3D5", "#F1F6F4"
      },
      tab_bar = {
        background = "#2E3434",
        active_tab = { bg_color = "#3A4141", fg_color = "#E9F2EF", intensity = "Bold" },
        inactive_tab = { bg_color = "#2E3434", fg_color = "#8FA7A3" },
        inactive_tab_hover = { bg_color = "#343A3A", fg_color = "#DCE8E5" },
        new_tab = { bg_color = "#2E3434", fg_color = "#8FA7A3" },
        new_tab_hover = { bg_color = "#343A3A", fg_color = "#E9F2EF" },
      },
    },
};
config.color_scheme = "redox";
```

Window decorations
```lua tangle:tests/output/basic/wezterm.lua
config.enable_tab_bar = false
config.window_decorations = 'RESIZE'

wezterm.on('toggle-window-decorations', function(window, pane)
    local overrides = window:get_config_overrides() or {}
    if overrides.window_decorations == 'RESIZE' then
        overrides.window_decorations = 'TITLE|RESIZE'
    else
        overrides.window_decorations = 'RESIZE'
    end
    window:set_config_overrides(overrides)
end)
```

Keymaps
```lua tangle:tests/output/basic/wezterm.lua
config.disable_default_key_bindings = true

local act = wezterm.action
config.keys = {
    { key = 'v',   mods = 'CTRL',                action = act.PasteFrom 'Clipboard' },
    { key = 'c',   mods = 'CTRL|SHIFT',          action = act.CopyTo 'ClipboardAndPrimarySelection' },
    { key = 'k',   mods = 'CTRL|SHIFT',          action = act.IncreaseFontSize },
    { key = 'j',   mods = 'CTRL|SHIFT',          action = act.DecreaseFontSize },
    { key = 'l',   mods = 'CTRL|SHIFT',          action = act.ResetFontSize },
    { key = 'n',   mods = 'CTRL|SHIFT',          action = act.SpawnWindow },
    { key = 'p',   mods = 'CTRL|SHIFT',          action = act.ActivateCommandPalette },
    { key = 'r',   mods = 'CTRL|SHIFT',          action = act.ReloadConfiguration },
    { key = 'w',   mods = 'CTRL|SHIFT',          action = act.EmitEvent 'toggle-window-decorations' },
    { key = 'f',   mods = 'CTRL|SHIFT',          action = act.ToggleFullScreen },
    { key = ' ',   mods = 'CTRL|SHIFT',          action = act.QuickSelect },
    { key = 'F11', action = act.ToggleFullScreen },
}
```

Return the final config
```lua tangle:tests/output/basic/wezterm.lua
return config
```

## Windows

If using WSL, add this:
```lua
config.wsl_domains = {
    {
        name = 'WSL:Ubuntu',
        distribution = 'Ubuntu',
        username = "zero_ir",
        default_cwd = "/home/zero_ir/"
    },
}
config.default_domain = 'WSL:Ubuntu'
```

