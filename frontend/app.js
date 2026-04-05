document.addEventListener('DOMContentLoaded', () => {
    console.log("LEGAL TRIAGE // SYSTEM INITIALIZING...");
    
    let currentObs = null;
    let isRunning = false;
    let totalReward = 0;

    const observationDisplay = document.getElementById('observation-display');
    const statusDisplay = document.getElementById('status-display');
    const rewardDisplay = document.getElementById('reward-display');
    const historyList = document.getElementById('history-list');
    const hfTokenInput = document.getElementById('hf-token');
    const loadingOverlay = document.getElementById('loading-overlay');
    
    function showLoading() { if (loadingOverlay) loadingOverlay.style.display = 'flex'; }
    function hideLoading() { if (loadingOverlay) loadingOverlay.style.display = 'none'; }

    async function saveToken() {
        const token = hfTokenInput.value;
        if (!token) {
            alert("INPUT REQUIRED // TOKEN EMPTY");
            return;
        }
        showLoading();
        try {
            const res = await fetch('/token', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ token })
            });
            if (res.ok) {
                hfTokenInput.value = '';
                alert("ACCESS GRANTED // TOKEN SECURED");
            } else {
                alert("ACCESS DENIED // TOKEN REJECTED");
            }
        } catch (e) {
            console.error("TOKEN ERROR:", e);
        } finally {
            hideLoading();
        }
    }

    async function resetEnv() {
        console.log("RESETTING ENVIRONMENT...");
        statusDisplay.textContent = "INITIALIZING...";
        showLoading();
        try {
            const res = await fetch('/reset', { method: 'POST' });
            if (!res.ok) throw new Error("Reset failed");
            currentObs = await res.json();
            totalReward = 0;
            updateUI(currentObs, 0, false, []);
            statusDisplay.textContent = "READY";
        } catch (e) {
            console.error("RESET ERROR:", e);
            statusDisplay.textContent = "RESET ERROR";
        } finally {
            hideLoading();
        }
    }

    async function stepEnv() {
        const actionType = document.getElementById('action-type').value;
        const actionContent = document.getElementById('action-content').value;
        console.log(`EXECUTING: ${actionType}`);

        showLoading();
        try {
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
        } catch (e) {
            console.error("STEP ERROR:", e);
        } finally {
            hideLoading();
        }
    }

    async function runAutoInference() {
        if (isRunning) return;
        isRunning = true;
        statusDisplay.textContent = "AGENT ACTIVE";
        
        try {
            // No full-screen loading for auto-inference loop to keep it visible,
            // but we can flash it on the very first reset.
            await resetEnv(); 
            
            let done = false;
            let stepCount = 0;
            const maxSteps = 8;

            while (!done && stepCount < maxSteps) {
                stepCount++;
                statusDisplay.textContent = `STEP ${stepCount} // EXECUTING`;

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
            statusDisplay.textContent = "MISSION COMPLETE";
        } catch (e) {
            console.error("AUTO ERROR:", e);
            statusDisplay.textContent = "SYSTEM ERROR";
            alert("Inference Error: " + e.message);
        } finally {
            isRunning = false;
        }
    }

    function updateUI(obs, lastReward, done, history) {
        observationDisplay.textContent = JSON.stringify(obs, null, 2);
        rewardDisplay.textContent = totalReward.toFixed(2);
        
        historyList.innerHTML = '';
        if (history && history.length > 0) {
            history.forEach((item, index) => {
                const parts = item.split(': ');
                const type = parts[0];
                const content = parts.slice(1).join(': ');
                
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
        }

        if (done) {
            statusDisplay.textContent = "EPISODE TERMINATED";
        }
    }

    // Attach Event Listeners
    document.getElementById('save-token-btn').addEventListener('click', saveToken);
    document.getElementById('reset-btn').addEventListener('click', resetEnv);
    document.getElementById('step-btn').addEventListener('click', stepEnv);
    document.getElementById('auto-run-btn').addEventListener('click', runAutoInference);

    console.log("LEGAL TRIAGE // SYSTEM ONLINE");
});
