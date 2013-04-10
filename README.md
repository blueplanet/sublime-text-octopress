# Sublime Text 2 Octopress

## WARNING

- Only supports OS X, linux
- You must start the `Sublime Text 2` from the terminal (or configure *octopress_cmd_before_rake* in your settings)

## Preview
![image](http://d.pr/i/WUn+)

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
  // set to generate, deploy or generate_and_deploy if you wish to have your changes generated into the /public folder and/or deployed upon file save
  "octopress_onsave_action": "",
  // true or false
  "use_bundle": false
}
```

### Setting Example

For Rbenv or RVM

```
...
// If you use zsh, you can set to "/bin/zsh"
"octopress_shell_executable": "/bin/bash",

// If you use zsh, you can set to "source ~/.zshrc"
"octopress_cmd_before_rake" : "source ~/.bash_profile",
...
```

### In the case of an error, please see the [RVM or Rbenv errors](https://github.com/blueplanet/sublime-text-2-octopress/issues/5#issuecomment-14313965)

## Use
You can execute following commands of `octopress` with `command_palette`
- new_post
- edit_existing_post
- new_page
- edit_existing_page
- generate
- deploy
- gen_deploy
- preview
- isolate (current post)
- integrate

You can enable auto-generate or auto-deploy by setting the ```octopress_onsave_action``` variable to "generate" or "generate_and_deploy". This will only trigger if the file you're saving is inside your ```octopress_path```.

## History
### Ver 2013.03.19
- Added "Isolate" and "Integrate" support

### Ver 2013.03.15
- Added "Preview" support

### Ver 2013.03.13
- Bug fix

### Ver 2013.02.02
- Add `octopress_shell_executable`

### Ver 2012.11.08
- Add auto generate (and or deploy)
- Add find and edit existing pages/posts

### Ver 2012.11.03
- Add setting menu
- Add `octopress_cmd_before_rake`
