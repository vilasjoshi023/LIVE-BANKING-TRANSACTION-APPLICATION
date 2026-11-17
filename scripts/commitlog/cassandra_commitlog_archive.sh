#!/bin/bash
# Cassandra Commit Log Archive Script
# Version: 2.0 - Improved error logging
#
# This script is currently validated with dummy files only.
# Do not enable in Cassandra until callback semantics, retry behaviour,
# restore workflow, concurrency safety and PITR have been reviewed.

set -u
set -o pipefail
umask 077

LOG_DIR="/var/log/cassandra-commitlog-archive"
LOG_FILE="${LOG_DIR}/archive.log"

log_message() {
    printf '%s | %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" >> "$LOG_FILE"
}

fail() {
    log_message "ERROR | $1"
    echo "ERROR: $1" >&2
    exit 1
}

if [[ ! -d "$LOG_DIR" || ! -w "$LOG_DIR" ]]; then
    echo "ERROR: Logging directory unavailable or not writable" >&2
    exit 1
fi

if [[ $# -ne 3 ]]; then
    fail "Invalid arguments"
fi

SOURCE="$1"
SEGMENT_NAME="$2"
ARCHIVE_DIR="$3"

if [[ ! -f "$SOURCE" ]]; then
    fail "Source file does not exist: $SOURCE"
fi

if [[ "$(basename "$SOURCE")" != "$SEGMENT_NAME" ]]; then
    fail "Segment name does not match source filename"
fi

if [[ ! -d "$ARCHIVE_DIR" || ! -w "$ARCHIVE_DIR" ]]; then
    fail "Archive directory unavailable or not writable: $ARCHIVE_DIR"
fi

DESTINATION="${ARCHIVE_DIR}/${SEGMENT_NAME}"

if [[ -e "$DESTINATION" ]]; then
    if cmp -s "$SOURCE" "$DESTINATION"; then
        log_message "ALREADY ARCHIVED | $SEGMENT_NAME"
        exit 0
    else
        fail "Existing archive differs: $SEGMENT_NAME"
    fi
fi

TEMP_FILE=$(mktemp "${ARCHIVE_DIR}/.${SEGMENT_NAME}.tmp.XXXXXX") \
    || fail "Unable to create temporary archive file"

cleanup() {
    [[ -n "${TEMP_FILE:-}" && -e "$TEMP_FILE" ]] && rm -f -- "$TEMP_FILE"
}
trap cleanup EXIT

if ! cp -- "$SOURCE" "$TEMP_FILE"; then
    fail "Copy failed: $SEGMENT_NAME"
fi

if ! cmp -s "$SOURCE" "$TEMP_FILE"; then
    fail "Integrity verification failed: $SEGMENT_NAME"
fi

if ! mv -- "$TEMP_FILE" "$DESTINATION"; then
    fail "Archive move failed: $SEGMENT_NAME"
fi

TEMP_FILE=""

log_message "SUCCESS | $SEGMENT_NAME"
exit 0
