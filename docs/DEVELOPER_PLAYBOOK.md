# Developer Playbook

## LOCAL DEV
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash scripts/dev_setup.sh
```

## RUN APP
```bash
python -m plumbing_takeoff.app
```

## RUN TESTS
```bash
pytest --cov
```

## RUN CLI TAKEOFF
```bash
python -m plumbing_takeoff.cli /path/to/plan.pdf --output-dir outputs
```

## CUT RELEASE
```bash
semantic-release version
semantic-release publish
```

## BUILD LINUX
```bash
bash scripts/build_linux.sh
```

## BUILD WINDOWS
```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_windows.ps1
```
