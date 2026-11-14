#!/bin/bash
# Installiert alles für den täglichen Video-Ablauf (idempotent). Netz: PyPI/npm + huggingface.co nötig.
set -e
pip install --quiet --break-system-packages piper-tts==1.8.0 faster-whisper==1.2.1 numpy scipy 2>/dev/null \
  || pip install --quiet piper-tts==1.8.0 faster-whisper==1.2.1 numpy scipy
if [ ! -x /opt/omni/venv/bin/python ] || ! /opt/omni/venv/bin/python -c "import omnivoice" 2>/dev/null; then
  python3 -m venv /opt/omni/venv
  /opt/omni/venv/bin/pip install --quiet omnivoice==0.2.1 soundfile
fi
/opt/omni/venv/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download('k2-fsa/OmniVoice')" >/dev/null 2>&1 || true
python3 -c "from faster_whisper import WhisperModel; WhisperModel('small', compute_type='int8')" >/dev/null 2>&1 || true
npx -y hyperframes@0.8.228 --version >/dev/null 2>&1 || true
echo "storyfakten-pipeline: bereit"
