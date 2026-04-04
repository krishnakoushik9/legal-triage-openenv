async function resetEnv() {
    const res = await fetch('/reset');
    const data = await res.json();
    updateUI(data, 0, false, []);
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
    updateUI(data.observation, data.reward, data.done, data.observation.history);
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
        alert("Task Complete!");
    }
}

document.getElementById('reset-btn')!.addEventListener('click', resetEnv);
document.getElementById('step-btn')!.addEventListener('click', stepEnv);
