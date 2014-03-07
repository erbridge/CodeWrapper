# CodeWrapper

Inspired by [consolewrap](https://github.com/unknownuser88/consolewrap), `CodeWrapper` wraps any code with other code at the touch of a button(ish).


## How?

To use, first set up some wrappings in `Packages/User/CodeWrapper.sublime-settings`. See the default settings for hints. It is also possible to add per-project settings to your `.project-settings` file. Just add the package settings to the key `CodeWrapper`.

Once a wrapper is set up, select some code to wrap, open the command palette and select `CodeWrapper`.

I don't like packages setting their own keybindings, so `CodeWrapper` doesn't. If you want to bind `CodeWrapper` to some keys (and you should), add the following to your `Packages/User/Default (${OS_NAME}),sublime-keymap` file:
```json
[
    // CodeWrapper
    { "keys": ["ctrl+shift+l"], "command": "code_wrapper" }
]
```


## Contributions

Bug reports, forks and pull requests are welcome.

Please make sure the tests all work before submitting anything, and add new ones for new features.
