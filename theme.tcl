# Copyright (c) 2021 rdbende <rdbende@gmail.com>

# The Forest theme is a beautiful and modern ttk theme inspired by Excel.

package require Tk 8.6

namespace eval ttk::theme::theme {

    variable version 1.0
    package provide ttk::theme::theme $version
    variable colors
    array set colors {
        -fg             "#eeeeee"
        -bg             "#2A3439"
        -disabledfg     "gray"
        -disabledbg     "#ffffff"
        -selectfg       "#ffffff"
        -selectbg       "#2A3439"
    }

    proc LoadImages {imgdir} {
        variable I
        foreach file [glob -directory $imgdir *.png] {
            set img [file tail [file rootname $file]]
            set I($img) [image create photo -file $file -format png]
        }
    }

    LoadImages [file join [file dirname [info script]] theme]

    # Settings
    ttk::style theme create theme -parent default -settings {
        ttk::style configure . \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -troughcolor $colors(-bg) \
            -focuscolor $colors(-selectbg) \
            -selectbackground $colors(-selectbg) \
            -selectforeground $colors(-selectfg) \
            -insertwidth 1 \
            -insertcolor $colors(-fg) \
            -fieldbackground $colors(-selectbg) \
            -font {TkDefaultFont 10} \
            -borderwidth 1 \
            -relief flat

        ttk::style map . -foreground [list disabled $colors(-disabledfg)]

        tk_setPalette background [ttk::style lookup . -background] \
            foreground [ttk::style lookup . -foreground] \
            highlightColor [ttk::style lookup . -focuscolor] \
            selectBackground [ttk::style lookup . -selectbackground] \
            selectForeground [ttk::style lookup . -selectforeground] \
            activeBackground [ttk::style lookup . -selectbackground] \
            activeForeground [ttk::style lookup . -selectforeground]
        
        option add *font [ttk::style lookup . -font]

        ttk::style layout Accent.TButton {
            AccentButton.button -children {
                AccentButton.padding -children {
                    AccentButton.label -side left -expand true
                } 
            }
        }

        ttk::style layout simagomb.TButton {
            simagomb.TButton.button -children {
                simagomb.TButton.padding -children {
                    simagomb.TButton.label -side left -expand true
                } 
            }
        }

        ttk::style layout foglaltAsztal.TButton {
            foglaltAsztal.button -children {
                foglaltAsztal.padding -children {
                    foglaltAsztal.label -side left -expand true
                } 
            }
        }

        ttk::style layout kivalasztottAsztal.TButton {
            kivalasztottAsztal.button -children {
                kivalasztottAsztal.padding -children {
                    kivalasztottAsztal.label -side left -expand true
                } 
            }
        }

        ttk::style layout szelesGomb.TButton {
            szelesGomb.button -children {
                szelesGomb.padding -children {
                    szelesGomb.label -side left -expand true
                } 
            }
        }

        ttk::style layout szelesGombFelso.TButton {
            szelesGombFelso.button -children {
                szelesGombFelso.padding -children {
                    szelesGombFelso.label -side left -expand true
                } 
            }
        }

        ttk::style layout szelesGombFelsoDisabled.TButton {
            szelesGombFelsoDisabled.button -children {
                szelesGombFelsoDisabled.padding -children {
                    szelesGombFelsoDisabled.label -side left -expand true
                } 
            }
        }

        ttk::style layout rendelesekGomb.TButton {
            rendelesekGomb.button -children {
                rendelesekGomb.padding -children {
                    rendelesekGomb.label -side left -expand true
                } 
            }
        }

        ttk::style layout szabadAsztal.TButton {
            szabadAsztal.button -children {
                szabadAsztal.padding -children {
                    szabadAsztal.label -side left -expand true
                } 
            }
        }

        ttk::style layout kisGomb.TButton {
            kisGomb.button -children {
                kisGomb.padding -children {
                    kisGomb.label -side left -expand true
                } 
            }
        }

        ttk::style layout nostyleGomb.TButton {
            nostyleGomb.button -children {
                nostyleGomb.padding -children {
                    nostyleGomb.label -side left -expand true
                } 
            }
        }
            
        # simagomb
        ttk::style configure simagomb.TButton -padding {10 10 10 10} -width -15 -anchor w -foreground #eeeeee -background "#002D62"\
        ttk::style element create AccentButton.button image \
            [list $I(rect-accent) \
                {selected disabled} $I(rect-accent-hover) \
                disabled $I(rect-accent-hover) \
                selected $I(rect-accent) \
                pressed $I(rect-accent) \
                active $I(rect-accent-hover) \
                
            ] -border 4 -sticky nsew

        # foglaltAsztal
        ttk::style configure foglaltAsztal.TButton -padding {10 10 10 10} -width 15 -anchor center -foreground #eeeeee -background "#54626F"\
        ttk::style element create AccentButton.button image \
            [list $I(rect-accent) \
                {selected disabled} $I(rect-accent-hover) \
                disabled $I(rect-accent-hover) \
                selected $I(rect-accent) \
                pressed $I(rect-accent) \
                active $I(rect-accent-hover) \
                
            ] -border 4 -sticky nsew

        # szabadAsztal
        ttk::style configure szabadAsztal.TButton -padding {10 10 10 10} -width 15 -anchor center -foreground #eeeeee -background "#009900" \
        ttk::style element create AccentButton.button image \
            [list $I(rect-accent) \
                {selected disabled} $I(rect-accent-hover) \
                disabled $I(rect-accent-hover) \
                selected $I(rect-accent) \
                pressed $I(rect-accent) \
                active $I(rect-accent-hover) \
                
            ] -border 4 -sticky nsew
        
        # kivalasztottAsztal
        ttk::style configure kivalasztottAsztal.TButton -padding {10 10 10 10} -width 15 -anchor center -foreground #eeeeee -background "#B22222" \
        ttk::style element create kivalasztottAsztal.button image \
            [list $I(rect-accent) \
                {selected disabled} $I(rect-accent-hover) \
                disabled $I(rect-accent-hover) \
                selected $I(rect-accent) \
                pressed $I(rect-accent) \
                active $I(rect-accent-hover) \
                
            ] -border 4 -sticky nsew

        # szelesGomb (főmenü)
        ttk::style configure szelesGomb.TButton -padding {15} -width 40  -anchor center -foreground #eeeeee -background "#002D62" -font "Comfortaa, 15"  \
        ttk::style element create szelesGomb.button image \
            [list $I(rect-accent) \
                {selected disabled} $I(rect-accent-hover) \
                disabled $I(rect-accent-hover) \
                selected $I(rect-accent) \
                pressed $I(rect-accent) \
                active $I(rect-accent-hover) \
                
            ] -border 4 -sticky nsew

        # szelesGomb (felső sáv) szelesGombFelso
        ttk::style configure szelesGombFelso.TButton -padding {15} -width 30  -anchor center -foreground #eeeeee -background "#002D62" -font "Comfortaa, 10"  \
        ttk::style element create szelesGombFelso.button image \
            [list $I(rect-accent) \
                {selected disabled} $I(rect-accent-hover) \
                disabled $I(rect-accent-hover) \
                selected $I(rect-accent) \
                pressed $I(rect-accent) \
                active $I(rect-accent-hover) \
                
            ] -border 4 -sticky nsew

        # szelesGomb disabled state (felső sáv) szelesGombFelsoDisabled
        ttk::style configure szelesGombFelsoDisabled.TButton -padding {15} -width 30  -anchor center -foreground white -background "#00563B" -font "Comfortaa, 10"  \
        ttk::style element create szelesGombFelsoDisabled.button image \
            [list $I(rect-accent) \
                {selected disabled} $I(rect-accent-hover) \
                disabled $I(rect-accent-hover) \
                selected $I(rect-accent) \
                pressed $I(rect-accent) \
                active $I(rect-accent-hover) \
                
            ] -border 4 -sticky nsew

        # rendelesekGomb
        ttk::style configure rendelesekGomb.TButton -padding {8 9 8 9} -width -16  -anchor center -foreground #eeeeee -background "#808000" \
        ttk::style element create rendelesekGomb.button image \
            [list $I(rect-accent) \
                {selected disabled} $I(rect-accent-hover) \
                disabled $I(rect-accent-hover) \
                selected $I(rect-accent) \
                pressed $I(rect-accent) \
                active $I(rect-accent-hover) \
                
            ] -border 4 -sticky nsew

        # kisGomb
        ttk::style configure kisGomb.TButton -padding {8 9 8 9} -width -4  -anchor center -foreground #eeeeee -background "#002D62" -font "Comfortaa, 15"\
        ttk::style element create kisGomb.button image \
            [list $I(rect-accent) \
                {selected disabled} $I(rect-accent-hover) \
                disabled $I(rect-accent-hover) \
                selected $I(rect-accent) \
                pressed $I(rect-accent) \
                active $I(rect-accent-hover) \
                
            ] -border 4 -sticky nsew

        # nostyleGomb
        ttk::style configure nostyleGomb.TButton -padding {8 9 8 9} -width -4  -anchor center -font "Comfortaa, 15"\
        ttk::style element create nostyleGomb.button image \
            [list $I(rect-accent) \
                {selected disabled} $I(rect-accent-hover) \
                disabled $I(rect-accent-hover) \
                selected $I(rect-accent) \
                pressed $I(rect-accent) \
                active $I(rect-accent-hover) \
                
            ] -border 4 -sticky nsew
    }
}
