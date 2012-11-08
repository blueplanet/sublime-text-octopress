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
  // set to generate, deploy or generate_and_deploy if you wish to have your changes generated into the /public folder and/or deployed upon file save
  "octopress_onsave_action": "",
  // true or false
  "use_bundle": false
}
```

## Use
You can execute following commands of `octopress` with `command_palette`
- new_post
- edit_existing_post
- new_page
- edit_existing_page
- generate
- deploy
- gen_deploy

You can enable auto-generate or auto-deploy by setting the ```octopress_onsave_action``` variable to "generate" or "generate_and_deploy". This will only trigger if the file you're saving is inside your ```octopress_path```.
## History
### Ver 2012.11.08
- Add auto generate (and or deploy) 
- Add find and edit existing pages/posts

### Ver 2012.11.03
- Add setting menu
- Add `octopress_cmd_before_rake`
