local wezterm = require 'wezterm'
local config = wezterm.config_builder()
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
return config
