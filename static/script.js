const API = 'http://127.0.0.1:8000';

function showStatus(id, msg, type) {
    const el = document.getElementById(id);
    el.textContent = msg;
    el.className = `status ${type} show`;
}

function setLoading(btnId, textId, spinnerId, loading) {
    const btn = document.getElementById(btnId);
    btn.disabled = loading;
    document.getElementById(textId).style.display = loading ? 'none' : '';
    const sp = document.getElementById(spinnerId);
    sp.classList.toggle('show', loading);
}

async function submitChat() {
    const userId = parseInt(document.getElementById('chat-user-id').value);
    const message = document.getElementById('chat-message').value.trim();
    if (!message) return showStatus('chat-status', 'Please enter a message.', 'error');

    setLoading('chat-btn', 'chat-btn-text', 'chat-spinner', true);
    try {
        const res = await fetch(`${API}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, message })
        });
        const data = await res.json();
        if (res.ok) {
            showStatus('chat-status', `Saved — message #${data.message_id}`, 'success');
            document.getElementById('reg-user-id').value = userId;
            document.getElementById('analyze-user-id').value = userId;
        } else {
            showStatus('chat-status', `Error: ${JSON.stringify(data.detail)}`, 'error');
        }
    } catch { showStatus('chat-status', 'Server unreachable.', 'error'); }
    setLoading('chat-btn', 'chat-btn-text', 'chat-spinner', false);
}

async function registerGitHub() {
    const userId = parseInt(document.getElementById('reg-user-id').value);
    const username = document.getElementById('reg-username').value.trim();
    if (!username) return showStatus('reg-status', 'Enter a GitHub username.', 'error');

    setLoading('reg-btn', 'reg-btn-text', 'reg-spinner', true);
    try {
        const res = await fetch(`${API}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, github_username: username })
        });
        const data = await res.json();
        if (res.ok) {
            showStatus('reg-status', `Connected @${username}`, 'success');
            loadGitHubPanel(userId);
        } else {
            showStatus('reg-status', `Error: ${JSON.stringify(data.detail)}`, 'error');
        }
    } catch { showStatus('reg-status', 'Server unreachable.', 'error'); }
    setLoading('reg-btn', 'reg-btn-text', 'reg-spinner', false);
}

async function loadGitHubPanel(userId) {
    document.getElementById('gh-panel').innerHTML = '<div class="gh-empty">Loading activity...</div>';
    try {
        const res = await fetch(`${API}/github/${userId}`);
        if (!res.ok) throw new Error();
        const { username, profile, stats } = await res.json();
        const max = 30;

        document.getElementById('gh-panel').innerHTML = `
            <div class="gh-profile">
                <img class="gh-avatar" src="${profile.avatar_url}" alt="${username}">
                <div>
                    <div class="gh-name">${profile.name || username}</div>
                    <div class="gh-handle">@${username}</div>
                </div>
            </div>
            <div class="stat-row">
                <span class="stat-label">Public repos</span>
                <span class="stat-value">${profile.public_repos}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Followers</span>
                <span class="stat-value">${profile.followers.toLocaleString()}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Recent pushes</span>
                <span class="stat-value">${stats.recent_pushes}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Pull requests</span>
                <span class="stat-value">${stats.recent_prs}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Issues opened</span>
                <span class="stat-value">${stats.recent_issues}</span>
            </div>
            <div class="bars-section">
                <div class="bar-item">
                    <div class="bar-top"><span>Pushes</span><span>${stats.recent_pushes}</span></div>
                    <div class="bar-track"><div class="bar-fill bar-brass" style="width:${Math.min(stats.recent_pushes/max*100,100)}%"></div></div>
                </div>
                <div class="bar-item">
                    <div class="bar-top"><span>Pull Requests</span><span>${stats.recent_prs}</span></div>
                    <div class="bar-track"><div class="bar-fill bar-clay" style="width:${Math.min(stats.recent_prs/max*100,100)}%"></div></div>
                </div>
                <div class="bar-item">
                    <div class="bar-top"><span>Issues</span><span>${stats.recent_issues}</span></div>
                    <div class="bar-track"><div class="bar-fill bar-olive" style="width:${Math.min(stats.recent_issues/max*100,100)}%"></div></div>
                </div>
            </div>
        `;
    } catch {
        document.getElementById('gh-panel').innerHTML = '<div class="gh-empty">Could not load GitHub data.</div>';
    }
}

async function runAnalysis() {
    const userId = parseInt(document.getElementById('analyze-user-id').value);
    setLoading('analyze-btn', 'analyze-btn-text', 'analyze-spinner', true);
    showStatus('analyze-status', 'Running — this takes 15–30 seconds...', 'info');
    document.getElementById('analyze-status').classList.add('show');

    try {
        const res = await fetch(`${API}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId })
        });
        const data = await res.json();
        if (res.ok) {
            showStatus('analyze-status', `Report #${data.report_id} ready`, 'success');
            renderReport(data);
        } else {
            showStatus('analyze-status', `Error: ${JSON.stringify(data.detail)}`, 'error');
        }
    } catch { showStatus('analyze-status', 'Server unreachable.', 'error'); }
    setLoading('analyze-btn', 'analyze-btn-text', 'analyze-spinner', false);
}

function renderReport(data) {
    document.getElementById('report-empty').classList.add('hidden');
    document.getElementById('report-content').classList.remove('hidden');

    const list = document.getElementById('bottleneck-list');
    list.innerHTML = data.bottlenecks.map((b, i) => {
        const sev = b.severity;
        const cls = sev >= 7 ? 'sev-high' : sev >= 4 ? 'sev-mid' : 'sev-low';
        const name = b.item.length > 55 ? b.item.substring(0, 55) + '…' : b.item;
        return `<div class="bottleneck-item" style="animation-delay:${i*0.06}s">
            <div class="b-left">
                <div class="b-name">${name}</div>
                <div class="b-meta">${b.category} · ${b.sources.join(', ')}</div>
            </div>
            <div class="sev-badge ${cls}">${sev}</div>
        </div>`;
    }).join('');

    document.getElementById('explanation-text').textContent = data.explanation;
    document.getElementById('report-card').scrollIntoView({ behavior: 'smooth', block: 'start' });
}