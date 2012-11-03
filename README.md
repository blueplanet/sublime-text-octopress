# Sublime Text 2 Octopress

## WARNING

- Only supports OS X, linux
- You must start the `Sublime Text 2` from the terminal (or configure *octopress_cmd_before_rake* in your settings)

## Preview
![image](https://lh3.googleusercontent.com/-yFnkYy_h9bo/UHlZwhPHNKI/AAAAAAAACCE/njGTdOMnoD8/s800/Screen%2520Shot%25202012-10-13%2520at%252020.33.03.png)

## Installation
### From [Sublime Package Control](http://wbond.net/sublime_packages/package_control)
Just open **"Package Control: Install Package"** in Command Palette and search for **"octopress"**

### Or from github
Clone or copy this repository into your Packages
- OS X: ~/Library/Application Support/Sublime Text 2/Packages/
- Linux: ~/.config/sublime-text-2/Packages/

### And change the setting to your env (Accessible via Preferences > Package Settings > Octopress > Settings - User)
```
{
  // path to your octopress
  "octopress_path": "/you_octopress_path",	
  // command to run before calling rake, eg source ~/.bash_profile to set up your local environment inc paths to ruby, rake etc.
  "octopress_cmd_before_rake" : "source ~/.bash_profile",
  // true or false
  "use_bundle": false
}
```

## Use
You can execute following commands of `octopress` with `command_palette`
- new_post
- new_page
- generate
- deploy
- gen_deploy

## History

### Ver 1.1
- Add setting menu
- Add `octopress_cmd_before_rake`
