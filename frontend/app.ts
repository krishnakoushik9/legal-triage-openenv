let currentObs: any = null;
let isRunning = false;

async function saveToken() {
    const token = (document.getElementById('hf-token') as HTMLInputElement).value;
    if (!token) {
        alert("Please enter a token");
        return;
    }
    const res = await fetch('/token', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ token })
    });
    if (res.ok) {
        alert("Token saved successfully!");
    } else {
        alert("Failed to save token");
    }
}

async function resetEnv() {
    const res = await fetch('/reset', { method: 'POST' });
    currentObs = await res.json();
    updateUI(currentObs, 0, false, []);
    document.getElementById('status-display')!.textContent = "Ready";
}

async function stepEnv() {
    const actionType = (document.getElementById('action-type') as HTMLSelectElement).value;
    const actionContent = (document.getElementById('action-content') as HTMLInputElement).value;

    const res = await fetch('/step', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            action_type: actionType,
            content: actionContent
        })
    });

    const data = await res.json();
    currentObs = data.observation;
    updateUI(data.observation, data.reward, data.done, data.observation.history);
}

async function runAutoInference() {
    if (isRunning) return;
    isRunning = true;
    document.getElementById('status-display')!.textContent = "Running Automated Inference...";
    
    try {
        await resetEnv();
        let done = false;
        let stepCount = 0;
        const maxSteps = 8;

        while (!done && stepCount < maxSteps) {
            stepCount++;
            document.getElementById('status-display')!.textContent = `Running Step ${stepCount}...`;

            // We'll use a simplified version of the logic from inference.py but via client-side fetch 
            // to a helper if we had one, but since we don't want to expose keys, we'll 
            // actually just mock the call or assume the server handles it? 
            // Actually, the server doesn't have an 'auto-step' endpoint.
            // Let's implement a small proxy in the backend or just use a mock action for visualization
            // since this is a "demo" frontend.
            
            // To make it REAL, we'd need the browser to call HF API or our backend to do it.
            // Let's add a /auto-step to api/main.py that uses the saved token.
            
            const res = await fetch('/auto-step', { method: 'POST' });
            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || "Inference failed");
            }
            const data = await res.json();
            currentObs = data.observation;
            done = data.done;
            updateUI(data.observation, data.reward, data.done, data.observation.history);
            
            if (done) break;
            await new Promise(r => setTimeout(r, 1000)); // Delay for visualization
        }
        document.getElementById('status-display')!.textContent = "Finished";
    } catch (e: any) {
        alert("Error: " + e.message);
        document.getElementById('status-display')!.textContent = "Error";
    } finally {
        isRunning = false;
    }
}

function updateUI(obs: any, reward: number, done: boolean, history: string[]) {
    document.getElementById('observation-display')!.textContent = JSON.stringify(obs, null, 2);
    document.getElementById('reward-display')!.textContent = reward.toFixed(2);
    
    const historyList = document.getElementById('history-list')!;
    historyList.innerHTML = '';
    history.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        historyList.appendChild(li);
    });

    if (done) {
        document.getElementById('status-display')!.textContent = "Episode Done";
    }
}

document.getElementById('save-token-btn')!.addEventListener('click', saveToken);
document.getElementById('reset-btn')!.addEventListener('click', resetEnv);
document.getElementById('step-btn')!.addEventListener('click', stepEnv);
document.getElementById('auto-run-btn')!.addEventListener('click', runAutoInference);
