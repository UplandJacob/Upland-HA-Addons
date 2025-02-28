#!/bin/bash

# rewrite of checkaptgpg
# fehlix Oct 2020
# 12.10.2020 - fixed expired key handling
# 24.05.2023 - add asc-keyrings

VERSION="230524-01"

# check bash
[ x"$BASHPID" = x"$$" ] || exec /usr/bin/bash -c "$0 $@"

# keyserver
KEYSERVER=(
    hkps://keys.openpgp.org
    hkps://keyserver.ubuntu.com
    hkps://pgpkeys.eu
    hkp://keyserver.ubuntu.com:80
    #--------------------------------------------------------------
    # below not used
    #hkp://pool.sks-keyservers.net
    #hkp://pgp.mit.edu
    #hkp://subkeys.pgp.net
    #hkp://eu.pool.sks-keyservers.net
    #hkp://keys.gnupg.net
    #hkp://keyservers.org
    #hkp://keyserver.linux.it
    )

# translations
export TEXTDOMAIN_DIR="/usr/share/locale"
export TEXTDOMAIN="mx-checkaptgpg"

# TRANSLATORS:
# The GPG signature of the repository release file was successfully verified.
GOOD_GPG_SIGNATURE_FOUND=$(gettext  "Good GPG signature found.")
# TRANSLATORS:
# The missing public GPG signing keys could not be found on any key server.
# Keys not found on keyserver: 0xABCDEFGH12345678
KEYS_NOT_FOUND_ON_KEYSERVER=$(gettext  "Keys not found on keyserver:")
PRESS_H_FOR_HELP_ANY_OTHER_KEY_TO_CLOSE=$(gettext  "Press 'H' for online help, press any other key to close this window.")
PLEASE_WAIT_WHILE_THE_LINK_OPENS=$(gettext  "Please wait while the link '%s' opens ...")
PRESS_ANY_KEY_TO_CLOSE_THIS_WINDOW=$(gettext  "Press any key to close this window.")
# TRANSLATORS:
# The GPG signature of the signed repository release file is verified:
# "Checking mxrepo.com_mx_repo_dists_bookworm_InRelease"
CHECKING=$(gettext  "Checking")

NEED_ROOT_TXT='This command needs %s privileges to be executed.\n'
# TRANSLATORS:
# The user must run this command as 'root'.
# This command needs 'root' privileges to be executed.
NEED_ROOT=$(gettext  'This command needs %s privileges to be executed.\n')
# translation fallback
if [ "$NEED_ROOT" = "$NEED_ROOT_TXT" ]; then
    GETTEXT=gettext
    NEED_ROOT=$($GETTEXT  -d su-to-root  "$NEED_ROOT_TXT")
fi
NEED_ROOT=$(printf "$NEED_ROOT" "'root'")

# set colors
    RED='\e[1;31m'
   BLUE='\e[1;34m'
  GREEN='\e[0;32m'
 yellow='\e[0;33m'
 YELLOW='\e[1;33m'
    END='\e[0m'
     NC='\e[0m'

# check root
if [ $(id -u) -ne 0 ]; then
   printf "\n\t ${YELLOW}%s${NC}\n\n" "$NEED_ROOT"
   sudo -kK
   exec sudo "$0" "$@"
   exit 1
fi

# check parameter
[ x"$1" == x"--wait-at-end" ] && WAITATEND="1" || WAITATEND="0"

# prepare gpg import key
CHECKAPTGPG_KEYRING=/etc/apt/trusted.gpg.d/checkaptgpg.gpg
TMP_GPG_HOME=$(mktemp -d /tmp/temp-checkaptgpg-home-$(date '+%y%m%d-%H%M%S')-XXXXXXXXXX)
TMP_KEYRING=$TMP_GPG_HOME/tempkeyring.kbx
TMP_PUBKEY=$TMP_GPG_HOME/tmp_pub_key.gpg
chmod 700 $TMP_GPG_HOME

# prepare tidy up
tidy_up() {
    rm -r /tmp/temp-checkaptgpg-home-* 2>/dev/null;
    }
trap tidy_up EXIT

# apt's trusted keyrings
declare -a APT_KEYRINGS DETACHED_SIGS SIGNED_RELEASES
shopt -s nullglob;
APT_KEYRINGS_LIST_GPG=( /etc/apt/trusted[.]gpg{,.d/*.gpg} )
APT_KEYRINGS_LIST_ASC=( /etc/apt/trusted.gpg.d/*.asc )

# detached Release signatures
DETACHED_SIGS=( /var/lib/apt/lists/{,partial/}*Release.gpg )
# inline signed Release
shopt -u nullglob
readarray -t SIGNED_RELEASES < <(grep -IFlsx  /var/lib/apt/lists/{,partial/}*Release -e '-----BEGIN PGP SIGNED MESSAGE-----' )

# keyring options for gpg
APT_KEYRINGS="${APT_KEYRINGS_LIST_GPG[@]///etc/--keyring gnupg-ring:/etc}"

ASC_KEYRINGS_DIR=${TMP_GPG_HOME}/asc_keyrings
mkdir $ASC_KEYRINGS_DIR

unset ASC_KEYRINGS_LIST
declare -a ASC_KEYRINGS_LIST
for ASC in "${APT_KEYRINGS_LIST_ASC[@]}"; do
    A=${ASC##*/}
    G=$ASC_KEYRINGS_DIR/${A%.asc}.gpg
    gpg -o "$G" --dearmor "$ASC"
    ASC_KEYRINGS_LIST+=("$G")
done

ASC_KEYRINGS=( "${ASC_KEYRINGS_LIST[@]///tmp/--keyring gnupg-ring:/tmp}" )

GPG_OPTS="--homedir=$TMP_GPG_HOME --keyid-format 0xlong --no-default-keyring"
EXPORT_OPTIONS="--export-options export-clean,export-minimal"
IMPORT_OPTIONS="--import-options import-clean,import-minimal"
KEYSERVER_OPTIONS="--keyserver-options import-clean,import-minimal"

for SIG in "${SIGNED_RELEASES[@]}" "${DETACHED_SIGS[@]}"; do
   if [ x"${SIG##*.gpg}" = x ]; then
        if [ -f "${SIG%.gpg}" ]; then
            REL="${SIG%.gpg}"
        elif  [ -f "${SIG%.gpg}.FAILED" ];  then
            REL="${SIG%.gpg}.FAILED"
        else
            continue
        fi
   else
        REL=""
   fi
   CHK=$(basename -s .gpg "$SIG")
   echo
   echo "${CHECKING} ${CHK}"
   CHECK=$(LC_ALL= LANGUAGE= LC_MESSAGES= LANG=C.UTF-8; gpg $GPG_OPTS ${APT_KEYRINGS[@]}  ${ASC_KEYRINGS[@]} --verify $SIG $REL 2>&1)
   RET=$?
   ((RET==0)) && grep -v expired <<<$CHECK | grep -q "Good signature"
   if ((RET==0)); then
        printf "$GREEN%s$END\n" "    ${GOOD_GPG_SIGNATURE_FOUND}"
   else
        # key expired or not available
        declare -a KEYS
        readarray -t KEYS < <( grep -oE '[[:xdigit:]]{16}\b' <<<$CHECK | sort -u)

        KEYS_FOUND="false"
        for keyserver in ${KEYSERVER[*]}; do
            [ -f $TMP_KEYRING ] && rm $TMP_KEYRING
            [ -f $TMP_PUBKEY  ] && rm $TMP_PUBKEY
            if gpg $GPG_OPTS --keyring=$TMP_KEYRING $KEYSERVER_OPTIONS --keyserver $keyserver  --recv-key ${KEYS[@]/#/0x} 1>/dev/null 2>&1; then
                [ $(gpg $GPG_OPTS --keyring=$TMP_KEYRING  --with-colons --list-keys 2>/dev/null | grep -c ^pub) = 0 ] && continue
                KEYS_FOUND="true"
                gpg $GPG_OPTS --keyring=$TMP_KEYRING --output $TMP_PUBKEY $EXPORT_OPTIONS --export ;  # 1>/dev/null 2>&1
                if [ ! -f ${CHECKAPTGPG_KEYRING} ]; then
                   touch  ${CHECKAPTGPG_KEYRING}
                fi
                GPG_KEYRINGS=("--keyring gnupg-ring:${CHECKAPTGPG_KEYRING}")

                for k in "${APT_KEYRINGS[@]}"; do
                    [ -z "${k##*${CHECKAPTGPG_KEYRING}}" ] && continue
                    GPG_KEYRINGS+=("$k")
                done

                gpg $GPG_OPTS ${GPG_KEYRINGS[@]} $IMPORT_OPTIONS --import $TMP_PUBKEY
                [ -f ${CHECKAPTGPG_KEYRING}~ ] && rm ${CHECKAPTGPG_KEYRING}~
                break
            fi
        done
        if [ "$KEYS_FOUND" != "true" ]; then
            printf "\n$BLUE%s$END\n" "*** ${KEYS_NOT_FOUND_ON_KEYSERVER} ${KEYS[*]/#/0x}"
            echo
        fi
   fi
done

echo

if [ "$WAITATEND" = "1" ]; then
    echo
    HELP_OR_QUIT=""
    read -sn 1 -t 999999999 -p "${PRESS_H_FOR_HELP_ANY_OTHER_KEY_TO_CLOSE}" HELP_OR_QUIT
    sleep .1

    lang=$(echo "$LANGUAGE $LC_ALL $LC_MESSAGES $LANG " |
           sed -r 's/:/ /g; 
                   s/[._][^[:space:]]*//;
                   s/^[[:space:]]*//; 
                   s/[[:space:]].*$//'
          )
    case "$lang" in
      fr) HelpUrl="https://mxlinux.org/wiki/help-files/help-controle-de-apt-gpg" ;;
       *) HelpUrl="https://mxlinux.org/wiki/help-files/help-mx-check-apt-gpg" ;;
    esac


    if [ "$HELP_OR_QUIT" = "h" ] || [ "$HELP_OR_QUIT" = "H" ]
      then
        echo
        echo
        printf "${PLEASE_WAIT_WHILE_THE_LINK_OPENS}\n" "$HelpUrl"
        echo
        if [ -e /usr/bin/mx-viewer ]; then helpViewer="mx-viewer"; else helpViewer="xdg-open"; fi
        runuser -s /bin/bash -l $(logname) -c  'env XAUTHORITY=/$HOME/.Xauthority DISPLAY=:0 '"$helpViewer $HelpUrl 2>/dev/null 1>&2  &" 2>/dev/null  1>&2
        sleep 2
        read -sn 1 -p "${PRESS_ANY_KEY_TO_CLOSE_THIS_WINDOW}" -t 999999999
        sleep .1
    fi
echo
fi

exit