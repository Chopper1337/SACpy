# SACpy Rofi

This is an example of using SACpy along with Rofi

## Setup

1. Install `rofi`

2. Set up SACpy

3. Move (or copy) your encrypted accounts file `accounts.sacpy.des3` to your home directory.

    * If Rofi runs from some other directory, move the accounts file to it.

        If you don't know where Rofi runs from, it's probably your home directory.

4. Modify the `sac` script in this folder to fit your setup
    
    * Search for the term "EDIT_ME" and you'll find the things to modify

5. Run the `sac` script

If you dislike the colours in use for the Rofi menu, modify the `theme.rasi` file

If you dislike the menu size or position, modify the `sac.rasi` and `sacpass.rasi` files.

  `sac.rasi` is used by the main account selecting menu

  `sacpass.rasi` is used by the password input "menu"

## To note

This is all hacked together but it *does* work.

Until I create (or someone else creates) a GUI for SACpy, this is my solution.
