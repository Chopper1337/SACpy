#!/usr/bin/env bash

# If this script contains more than it should, it's because I just pasted
# one of the EndeavourOS provided i3 scripts and modified it til it worked :)

# EDIT_ME (Change to the Rofi arg to set your preferred theme)
# Path to your desired Rofi theme
ROFI_OPTIONS=(-theme ./sac.rasi)

# Preferred launcher if both are available 
preferred_launcher="rofi"

# Check whether the user-defined launcher is valid
launcher_list=(rofi zenity)
function check_launcher() {
  if [[ ! "${launcher_list[@]}" =~ (^|[[:space:]])"$1"($|[[:space:]]) ]]; then
    echo "Supported launchers: ${launcher_list[*]}"
    exit 1
  else
    # Get array with unique elements and preferred launcher first
    # Note: uniq expects a sorted list, so we cannot use it
    i=1
    launcher_list=($(for l in "$1" "${launcher_list[@]}"; do printf "%i %s\n" "$i" "$l"; let i+=1; done \
      | sort -uk2 | sort -nk1 | cut -d' ' -f2- | tr '\n' ' '))
  fi
}

# Parse CLI arguments
while getopts "hcp:" option; do
  case "${option}" in
    h) echo "${usage}"
       exit 0
       ;;
    c) enable_confirmation=true
       ;;
    p) preferred_launcher="${OPTARG}"
       check_launcher "${preferred_launcher}"
       ;;
    *) exit 1
       ;;
  esac
done

# Check whether a command exists
function command_exists() {
  command -v "$1" &> /dev/null 2>&1
}

# EDIT_ME (Set to the path to your sac.py script)
# Path to the sac.py script
sacpy_path="../sac.py"

# EDIT_ME (Just change the path to your preferred rofi theme or remove the theme arg)
# Prompt the user for the password before showing the rest of the menu
password=$(rofi -dmenu -p Pass: -theme ./sacpass.rasi)

# menu defined as an associative array
typeset -A menu

# Menu with keys/commands

# EDIT_ME (Replace the placeholder usernames with those of your own accounts as in your accounts file)
menu=(
  [1. Exit Steam]="$sacpy_path kill" # Exit Steam
  [2. yourusernamehere1 ]="$sacpy_path yourusernamehere1 $password" # Log in to an account
  [3. yourusernamehere2 ]="$sacpy_path yourusernamehere2 $password" # Log in to an account
  [[decrypt file]]="$sacpy_path decrypt $password" # Decrypt the accounts file (for modification)
)

menu_nrows=${#menu[@]}

launcher_exe=""
launcher_options=""
rofi_colors=""

function prepare_launcher() {
  if [[ "$1" == "rofi" ]]; then
    rofi_colors=(-bc "${BORDER_COLOR}" -bg "${BG_COLOR}" -fg "${FG_COLOR}" \
        -hlfg "${HLFG_COLOR}" -hlbg "${HLBG_COLOR}")
    launcher_exe="rofi"
    launcher_options=(-dmenu -i -lines "${menu_nrows}" -p "${ROFI_TEXT}" \
        "${rofi_colors}" "${ROFI_OPTIONS[@]}")
  elif [[ "$1" == "zenity" ]]; then
    launcher_exe="zenity"
    launcher_options=(--list --title="${ZENITY_TITLE}" --text="${ZENITY_TEXT}" \
        "${ZENITY_OPTIONS[@]}")
  fi
}

for l in "${launcher_list[@]}"; do
  if command_exists "${l}" ; then
    prepare_launcher "${l}"
    break
  fi
done

# No launcher available
if [[ -z "${launcher_exe}" ]]; then
  exit 1
fi

launcher=(${launcher_exe} "${launcher_options[@]}")
selection="$(printf '%s\n' "${!menu[@]}" | sort | "${launcher[@]}")"

function ask_confirmation() {
  if [ "${launcher_exe}" == "rofi" ]; then
    confirmed=$(echo -e "Yes\nNo" | rofi -dmenu -i -lines 2 -p "${selection}?" \
      "${rofi_colors}" "${ROFI_OPTIONS[@]}")
    [ "${confirmed}" == "Yes" ] && confirmed=0
  elif [ "${launcher_exe}" == "zenity" ]; then
    zenity --question --text "Are you sure you want to ${selection,,}?"
    confirmed=$?
  fi

  if [ "${confirmed}" == 0 ]; then
    i3-msg -q "exec ${menu[${selection}]}"
  fi
}

if [[ $? -eq 0 && ! -z ${selection} ]]; then
  if [[ "${enable_confirmation}" = true && \
        ${menu_confirm} =~ (^|[[:space:]])"${selection}"($|[[:space:]]) ]]; then
    ask_confirmation
  else
    i3-msg -q "exec ${menu[${selection}]}"
  fi
fi
