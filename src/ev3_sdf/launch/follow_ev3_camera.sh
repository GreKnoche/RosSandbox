#!/usr/bin/env bash
# Chase-Cam fest hinter dem EV3, ohne weiches Nachdrehen (pgain = 1).
set -u

TARGET="${FOLLOW_TARGET:-ev3}"
OFFSET_X="${FOLLOW_OFFSET_X:--0.90}"
OFFSET_Y="${FOLLOW_OFFSET_Y:-0.0}"
OFFSET_Z="${FOLLOW_OFFSET_Z:-0.42}"

TRACK_MSG="track_mode: 2, follow_target: {name: \"${TARGET}\"}, follow_offset: {x: ${OFFSET_X}, y: ${OFFSET_Y}, z: ${OFFSET_Z}}, follow_pgain: 1.0, track_pgain: 1.0"

# Mehrfach senden: GUI-Kamera und Model sind nach dem Spawn oft noch nicht ready.
for _ in 1 2 3 4 5 6; do
  gz topic -t /gui/track -m gz.msgs.CameraTrack -p "${TRACK_MSG}" || true
  sleep 0.4
done

# Ältere Harmonic-Builds ohne /gui/track: Follow-Services.
gz service -s /gui/follow --reqtype gz.msgs.StringMsg --reptype gz.msgs.Boolean \
  --timeout 2000 --req "data: \"${TARGET}\"" || true
gz service -s /gui/follow/offset --reqtype gz.msgs.Vector3d --reptype gz.msgs.Boolean \
  --timeout 2000 --req "x: ${OFFSET_X}, y: ${OFFSET_Y}, z: ${OFFSET_Z}" || true
gz service -s /gui/follow/pgain --reqtype gz.msgs.Double --reptype gz.msgs.Boolean \
  --timeout 2000 --req 'data: 1.0' || \
gz service -s /gui/follow/pgain --reqtype gz.msgs.Float --reptype gz.msgs.Boolean \
  --timeout 2000 --req 'data: 1.0' || true

# pgain zuletzt nochmal setzen, falls die Follow-Services die Defaults zurückgesetzt haben.
gz topic -t /gui/track -m gz.msgs.CameraTrack -p "${TRACK_MSG}" || true
