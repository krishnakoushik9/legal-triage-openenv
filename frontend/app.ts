let currentObs: any = null;
let isRunning = false;
let totalReward = 0;

async function saveToken() {
    const tokenInput = document.getElementById('hf-token') as HTMLInputElement;
    const token = tokenInput.value;
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
        tokenInput.value = '';
        alert("TOKEN SECURED // ACCESS GRANTED");
    } else {
        alert("TOKEN REJECTED");
    }
}

async function resetEnv() {
    const res = await fetch('/reset', { method: 'POST' });
    currentObs = await res.json();
    totalReward = 0;
    updateUI(currentObs, 0, false, []);
    document.getElementById('status-display')!.textContent = "READY";
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
    totalReward += data.reward;
    updateUI(data.observation, data.reward, data.done, data.observation.history);
}

async function runAutoInference() {
    if (isRunning) return;
    isRunning = true;
    document.getElementById('status-display')!.textContent = "AGENT ACTIVE";
    
    try {
        await resetEnv();
        let done = false;
        let stepCount = 0;
        const maxSteps = 8;

        while (!done && stepCount < maxSteps) {
            stepCount++;
            document.getElementById('status-display')!.textContent = `STEP ${stepCount} // EXECUTING`;

            const res = await fetch('/auto-step', { method: 'POST' });
            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || "Inference failed");
            }
            const data = await res.json();
            currentObs = data.observation;
            totalReward += data.reward;
            done = data.done;
            updateUI(data.observation, data.reward, data.done, data.observation.history);
            
            if (done) break;
            await new Promise(r => setTimeout(r, 1500)); 
        }
        document.getElementById('status-display')!.textContent = "MISSION COMPLETE";
    } catch (e: any) {
        console.error(e);
        document.getElementById('status-display')!.textContent = "SYSTEM ERROR";
    } finally {
        isRunning = false;
    }
}

function updateUI(obs: any, lastReward: number, done: boolean, history: string[]) {
    document.getElementById('observation-display')!.textContent = JSON.stringify(obs, null, 2);
    document.getElementById('reward-display')!.textContent = totalReward.toFixed(2);
    
    const historyList = document.getElementById('history-list')!;
    historyList.innerHTML = '';
    
    history.forEach((item, index) => {
        const [type, ...contentParts] = item.split(': ');
        const content = contentParts.join(': ');
        
        const itemDiv = document.createElement('div');
        itemDiv.className = 'history-item';
        itemDiv.innerHTML = `
            <div class="history-index">${(index + 1).toString().padStart(2, '0')}</div>
            <div class="history-content">
                <div class="history-type">${type}</div>
                <div class="history-text">${content}</div>
            </div>
        `;
        historyList.appendChild(itemDiv);
    });

    if (done) {
        document.getElementById('status-display')!.textContent = "EPISODE TERMINATED";
    }
}

document.getElementById('save-token-btn')!.addEventListener('click', saveToken);
document.getElementById('reset-btn')!.addEventListener('click', resetEnv);
document.getElementById('step-btn')!.addEventListener('click', stepEnv);
document.getElementById('auto-run-btn')!.addEventListener('click', runAutoInference);
