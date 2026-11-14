#!/usr/bin/env python3
"""Update the Cortex dashboard from a completed FAFB T4 workflow run.

Uses GitHub REST with GITHUB_TOKEN. Treats artifacts as data, never as executable code.
"""
import io
import json
import os
import re
import urllib.error
import urllib.request
import urllib.parse
import zipfile
from datetime import datetime, timezone

REPO = os.environ["GITHUB_REPOSITORY"]
TOKEN = os.environ["GITHUB_TOKEN"]
RUN_ID = int(os.environ["SOURCE_RUN_ID"])
PATH = "docs/CORTEX_STATUS.md"
START = "<!-- T4-AUTO-START -->"
END = "<!-- T4-AUTO-END -->"


class ArtifactRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Do not forward the GitHub API bearer token to artifact storage hosts."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        if redirected and urllib.parse.urlsplit(newurl).hostname != urllib.parse.urlsplit(req.full_url).hostname:
            for key in list(redirected.headers):
                if key.lower() in ("authorization", "x-github-api-version", "accept"):
                    del redirected.headers[key]
        return redirected


def request(method, path, payload=None, accept="application/vnd.github+json", binary=False):
    url = "https://api.github.com/repos/" + REPO + "/" + path
    data = None if payload is None else json.dumps(payload).encode()
    headers = {
        "Authorization": "Bearer " + TOKEN,
        "Accept": accept,
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "cortex-dashboard",
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
    with urllib.request.build_opener(ArtifactRedirectHandler()).open(urllib.request.Request(url, data=data, headers=headers, method=method), timeout=40) as res:
        return res.read() if binary else json.load(res)


def safe(value):
    return re.sub(r"[^A-Za-z0-9._/-]", "", str(value))


def artifact_data(run):
    if run.get("conclusion") != "success":
        return {}, None
    artifacts = request("GET", f"actions/runs/{RUN_ID}/artifacts?per_page=100")["artifacts"]
    matching = [a for a in artifacts if a["name"] == "fafb-t4-auto-validation" and not a.get("expired")]
    if not matching:
        return {}, None
    art = matching[-1]
    archive = request("GET", f"actions/artifacts/{art['id']}/zip", accept="application/vnd.github+json", binary=True)
    result = {}
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        for filename in ("t4-normalized-response.json", "t4-validation-gates.json", "t4-direction-selectivity-summary.json"):
            if filename in z.namelist():
                result[filename] = json.loads(z.read(filename))
    return result, art["id"]


def render(run, data, artifact_id):
    status = safe(run.get("conclusion") or run.get("status") or "unknown")
    branch = safe(run.get("head_branch") or "unknown")
    sha = safe(run.get("head_sha") or "")[:12]
    when = safe(run.get("updated_at") or "")
    url = f"https://github.com/{REPO}/actions/runs/{RUN_ID}"
    lines = [
        START,
        "## Atualização automática — validação FAFB T4",
        "",
        f"- **Execução:** [#{RUN_ID}]({url})",
        f"- **Resultado técnico do workflow:** `{status}`",
        f"- **Branch / commit:** `{branch}` / `{sha}`",
        f"- **Atualizado pelo GitHub em:** `{when}` (UTC)",
    ]
    if artifact_id:
        lines.append(f"- **Relatórios:** [artifact #{artifact_id}]({url}/artifacts/{artifact_id})")
    summary = data.get("t4-direction-selectivity-summary.json", {})
    gates = data.get("t4-validation-gates.json", {})
    response = data.get("t4-normalized-response.json", {})
    if response:
        edges = response.get("retained_edges")
        if isinstance(edges, int):
            lines.append(f"- **Conexões analisadas:** {edges:,}".replace(",", "."))
        audit = response.get("stimulus_drive_audit", {})
        if audit:
            lines.append(f"- **Frames iguais por direção:** {audit.get('equal_frame_counts')}; **eventos de entrada iguais:** {audit.get('equal_total_input_events')}")
    if gates:
        lines.append("- **Gates numéricos:** " + ", ".join(
            f"`{k}`={v}" for k, v in sorted(gates.items()) if isinstance(v, bool)
        ))
    subtypes = summary.get("subtypes", {})
    if subtypes:
        lines.extend(["", "| Subtipo | Direção preferida simulada | DSI descritivo |", "| --- | --- | ---: |"])
        for subtype in ("T4a", "T4b", "T4c", "T4d"):
            entry = subtypes.get(subtype, {})
            dsi = entry.get("direction_selectivity_index")
            number = f"{dsi:.6f}" if isinstance(dsi, (int, float)) else "indefinido"
            lines.append(f"| {subtype} | {safe(entry.get('preferred_condition') or 'indefinido')} | {number} |")
    lines.extend([
        "",
        "**Limite científico:** sucesso da CI não prova seletividade direcional biológica. "
        "Calibração anatômica e comparação fisiológica independente continuam pendentes.",
        "O histórico anterior permanece no link de cada execução e em seus artifacts.",
        END,
    ])
    return "\n".join(lines)


def main():
    run = request("GET", f"actions/runs/{RUN_ID}")
    if run.get("name") != "FAFB T4 automatic validation":
        raise ValueError("Run is not FAFB T4 automatic validation")
    if run.get("status") != "completed":
        raise ValueError("Run has not completed")
    data, artifact_id = artifact_data(run)
    section = render(run, data, artifact_id)
    for attempt in range(3):
        current = request("GET", f"contents/{PATH}?ref=main")
        import base64
        original = base64.b64decode(current["content"]).decode("utf-8")
        existing = re.search(re.escape(START) + r".*?" + re.escape(END), original, flags=re.S)
        if existing:
            previous = re.search(r"\*\*Execução:\*\* \[#(\d+)\]", existing.group())
            if previous and int(previous.group(1)) > RUN_ID:
                print("Skipping older workflow run", RUN_ID)
                return
            updated = original[:existing.start()] + section + original[existing.end():]
        else:
            updated = original.rstrip() + "\n\n" + section + "\n"
        if updated == original:
            print("Dashboard already current")
            return
        body = {
            "message": f"docs: update T4 dashboard from run {RUN_ID}",
            "content": base64.b64encode(updated.encode()).decode(),
            "sha": current["sha"],
            "branch": "main",
        }
        try:
            request("PUT", f"contents/{PATH}", body)
            print("Updated dashboard from", RUN_ID)
            return
        except urllib.error.HTTPError as exc:
            if exc.code not in (409, 422) or attempt == 2:
                raise
    raise RuntimeError("Failed to update dashboard")


if __name__ == "__main__":
    main()
