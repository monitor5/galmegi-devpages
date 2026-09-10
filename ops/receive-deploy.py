#!/usr/bin/env python3
"""Forced SSH command: accept only a static-site tar archive, then switch atomically."""
import fcntl, io, os, pathlib, re, shutil, subprocess, sys, tarfile, time
base = pathlib.Path('/opt/galmegi-dev')
command = os.environ.get('SSH_ORIGINAL_COMMAND', '')
if not re.fullmatch(r'deploy [a-f0-9]{40}-[0-9]+-[0-9]+', command):
    sys.exit('Only deploy SHA-RUN-ATTEMPT is allowed')
release_id = command.split()[1]
with (base / 'deploy.lock').open('w') as lock:
    fcntl.flock(lock, fcntl.LOCK_EX)
    payload = sys.stdin.buffer.read(10 * 1024 * 1024 + 1)
    if len(payload) > 10 * 1024 * 1024:
        sys.exit('Archive too large')
    release = base / 'releases' / release_id
    release.mkdir()
    previous = (base / 'current').resolve()
    switched = False
    try:
        with tarfile.open(fileobj=io.BytesIO(payload), mode='r:gz') as archive:
            members = archive.getmembers()
            if sum(m.size for m in members) > 20 * 1024 * 1024:
                raise ValueError('Expanded archive too large')
            for member in members:
                path = pathlib.PurePosixPath(member.name)
                if path.is_absolute() or '..' in path.parts or not member.isfile():
                    raise ValueError('Only regular relative files allowed')
                if member.name not in ('index.html', 'style.css', 'robots.txt', 'sitemap.xml') and not (path.parts[0] == 'assets' and path.suffix in ('.svg', '.png', '.jpeg', '.jpg', '.webp')):
                    raise ValueError('Unexpected file: ' + member.name)
                target = release / path
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.extractfile(member) as source, target.open('wb') as output:
                    shutil.copyfileobj(source, output)
                target.chmod(0o644)
        for name in ('index.html', 'style.css', 'robots.txt', 'sitemap.xml'):
            if not (release / name).is_file():
                raise ValueError('Missing required file')
        (release / 'revision.txt').write_text(release_id + '\n')
        temporary = base / 'current.next'
        temporary.unlink(missing_ok=True)
        temporary.symlink_to(release)
        temporary.replace(base / 'current')
        switched = True
        # HTTP read through local Nginx over TLS; verify using the installed origin certificate.
        served = subprocess.check_output(['curl', '-fsS', '--max-time', '15', '--cacert', '/opt/galmegi-dev/origin-public.pem', '--resolve', 'dev.galmegi.com:443:127.0.0.1', 'https://dev.galmegi.com/revision.txt'])
        if served.decode().strip() != release_id:
            raise ValueError('Release verification failed')
        print('Deployed ' + release_id)
    except Exception:
        if switched:
            temporary = base / 'current.next'
            temporary.unlink(missing_ok=True)
            temporary.symlink_to(previous)
            temporary.replace(base / 'current')
        shutil.rmtree(release)
        raise
