#!/usr/bin/env bash
# Build the thesis: pdflatex -> biber -> pdflatex -> pdflatex.
# Usage:
#   ./build.sh              # full 4-pass build
#   ./build.sh quick        # single pdflatex pass (fastest, refs may be stale)
#   ./build.sh clean        # remove all build artifacts
#   ./build.sh errors       # build and show only errors/warnings

set -u

MAIN="main"
TEXBIN="/usr/local/texlive/2025/bin/universal-darwin"
PDFLATEX="$TEXBIN/pdflatex"
BIBER="$TEXBIN/biber"

# Fall back to PATH if the hard-coded TeX Live dir isn't there.
[ -x "$PDFLATEX" ] || PDFLATEX="pdflatex"
[ -x "$BIBER" ]    || BIBER="biber"

PDFLATEX_FLAGS="-interaction=nonstopmode -file-line-error -halt-on-error"

# Colours
RED=$'\033[1;31m'
YEL=$'\033[1;33m'
GRN=$'\033[1;32m'
DIM=$'\033[2m'
RST=$'\033[0m'

log()  { printf "%s==>%s %s\n" "$GRN" "$RST" "$*"; }
warn() { printf "%s!!%s  %s\n" "$YEL" "$RST" "$*"; }
err()  { printf "%sxx%s  %s\n" "$RED" "$RST" "$*"; }

# Filter pdflatex / biber output: show only errors (red) and warnings
# (orange) on the terminal. The full output still goes to the log file
# via tee, so nothing is lost.
colorize() {
    awk -v red=$'\033[1;31m' -v org=$'\033[38;5;208m' -v rst=$'\033[0m' '
        /^!|: LaTeX Error|: Emergency|Fatal error|Undefined control sequence|^Missing [\$}{]|^Extra [\$}{]|Runaway argument|You can.t use|Too many |Improper / {
            print red $0 rst; next
        }
        /[Ww]arning|Overfull|Underfull|didn.t find a database entry/ {
            print org $0 rst; next
        }
    '
}

run_pdflatex() {
    local pass="$1"
    log "pdflatex pass $pass"
    local flags="-interaction=nonstopmode -file-line-error"
    set -o pipefail
    "$PDFLATEX" $flags "$MAIN.tex" 2>&1 \
        | tee "build-pass-$pass.log" \
        | colorize
    local rc=${PIPESTATUS[0]}
    set +o pipefail
    if [ "$rc" -ne 0 ]; then
        err "pdflatex pass $pass failed (rc=$rc, full log: build-pass-$pass.log)"
        return 1
    fi
}

run_biber() {
    log "biber"
    set -o pipefail
    "$BIBER" "$MAIN" 2>&1 | tee build-biber.log | colorize
    local rc=${PIPESTATUS[0]}
    set +o pipefail
    if [ "$rc" -ne 0 ]; then
        warn "biber reported issues (full log: build-biber.log)"
    fi
}

cmd_clean() {
    log "cleaning build artifacts"
    rm -f \
        "$MAIN".aux "$MAIN".bbl "$MAIN".bcf "$MAIN".blg \
        "$MAIN".log "$MAIN".out "$MAIN".toc "$MAIN".lof "$MAIN".lot \
        "$MAIN".idx "$MAIN".ind "$MAIN".ilg "$MAIN".loa "$MAIN".lol \
        "$MAIN".run.xml "$MAIN".synctex.gz "$MAIN".fls "$MAIN".fdb_latexmk \
        "$MAIN".mw "$MAIN".pdf \
        output.aux output.bbl output.bcf output.blg output.log output.out \
        output.toc output.lof output.lot output.idx output.ind output.ilg \
        output.loa output.lol output.run.xml output.mw \
        build-pass-*.log build-biber.log
    log "done"
}

cmd_quick() {
    run_pdflatex 1
}

cmd_full() {
    run_pdflatex 1 || true
    run_biber
    run_pdflatex 2 || true
    run_pdflatex 3 || return 1
    log "build complete: $MAIN.pdf"
    ls -lh "$MAIN.pdf" 2>/dev/null
}

cmd_errors() {
    cmd_full
    echo
    log "summary of issues:"
    for f in build-pass-*.log; do
        [ -f "$f" ] || continue
        local n_err n_undef n_overfull n_missing_bib
        n_err=$(grep -cE "^\!|: LaTeX Error|: Emergency|Fatal" "$f" || true)
        n_undef=$(grep -cE "undefined" "$f" || true)
        n_overfull=$(grep -cE "Overfull|Underfull" "$f" || true)
        printf "  %s%s%s  errors=%s  undefined=%s  badboxes=%s\n" \
            "$DIM" "$f" "$RST" "$n_err" "$n_undef" "$n_overfull"
    done
    if [ -f build-biber.log ]; then
        n_missing_bib=$(grep -cE "didn't find a database entry" build-biber.log || true)
        printf "  %sbuild-biber.log%s  missing-bib-keys=%s\n" \
            "$DIM" "$RST" "$n_missing_bib"
    fi
    echo
    log "first 20 LaTeX errors (last pass):"
    last_log=$(ls -t build-pass-*.log 2>/dev/null | head -1)
    [ -n "$last_log" ] && grep -E "^\!|: LaTeX Error|: Emergency|Fatal" "$last_log" | head -20
    echo
    log "first 20 missing bib keys:"
    [ -f build-biber.log ] && grep "didn't find" build-biber.log | head -20
}

case "${1:-full}" in
    quick)  cmd_quick ;;
    clean)  cmd_clean ;;
    errors) cmd_errors ;;
    full|"") cmd_full ;;
    *)
        echo "usage: $0 [full|quick|clean|errors]"
        exit 2
        ;;
esac
