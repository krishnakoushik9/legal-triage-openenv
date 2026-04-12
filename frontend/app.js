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
    const downloadBtn = document.getElementById('download-report-btn');
    
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
        downloadBtn.style.display = 'none';
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
        downloadBtn.style.display = 'none';
        
        try {
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
            downloadBtn.style.display = 'block';
        }
    }

    function downloadPDF() {
        if (!currentObs) return;
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        
        const orange = [255, 77, 0];
        const black = [0, 0, 0];
        
        // Header
        doc.setFillColor(...black);
        doc.rect(0, 0, 210, 40, 'F');
        doc.setTextColor(...orange);
        doc.setFont("helvetica", "bold");
        doc.setFontSize(24);
        doc.text("LEGAL TRIAGE // CASE REPORT", 20, 25);
        
        doc.setFontSize(10);
        doc.text(`GENERATED BY OPENENV AGENT // ${new Date().toLocaleString()}`, 20, 35);
        
        // Case Summary
        doc.setTextColor(...black);
        doc.setFontSize(14);
        doc.text("CASE CONTEXT", 20, 55);
        doc.setLineWidth(0.5);
        doc.line(20, 57, 190, 57);
        
        doc.setFont("helvetica", "normal");
        doc.setFontSize(10);
        const splitQuery = doc.splitTextToSize(currentObs.user_query, 170);
        doc.text(splitQuery, 20, 65);
        
        let yPos = 65 + (splitQuery.length * 5) + 10;
        
        // Action History
        doc.setFont("helvetica", "bold");
        doc.setFontSize(14);
        doc.text("EXECUTION LOG", 20, yPos);
        doc.line(20, yPos + 2, 190, yPos + 2);
        yPos += 10;
        
        doc.setFont("helvetica", "normal");
        doc.setFontSize(9);
        currentObs.history.forEach((step, i) => {
            if (yPos > 270) {
                doc.addPage();
                yPos = 20;
            }
            const text = `[STEP ${(i+1).toString().padStart(2, '0')}] ${step}`;
            const splitStep = doc.splitTextToSize(text, 170);
            doc.text(splitStep, 20, yPos);
            yPos += (splitStep.length * 5) + 2;
        });
        
        // Final Results
        yPos += 10;
        if (yPos > 250) { doc.addPage(); yPos = 20; }
        
        doc.setFillColor(...orange);
        doc.rect(20, yPos, 170, 20, 'F');
        doc.setTextColor(...black);
        doc.setFont("helvetica", "bold");
        doc.setFontSize(12);
        doc.text(`TOTAL REWARD SCORE: ${totalReward.toFixed(2)}`, 30, yPos + 12);
        
        // Footer
        doc.setFontSize(8);
        doc.setTextColor(150);
        doc.text("CONFIDENTIAL // FOR RL RESEARCH PURPOSES ONLY", 105, 285, { align: "center" });
        
        doc.save(`legal-triage-report-${Date.now()}.pdf`);
    }

    // Attach Event Listeners
    document.getElementById('save-token-btn').addEventListener('click', saveToken);
    document.getElementById('reset-btn').addEventListener('click', resetEnv);
    document.getElementById('step-btn').addEventListener('click', stepEnv);
    document.getElementById('auto-run-btn').addEventListener('click', runAutoInference);
    downloadBtn.addEventListener('click', downloadPDF);

    initChart();
    console.log("LEGAL TRIAGE // SYSTEM ONLINE");
});
dEventListener('click', downloadPDF);

    console.log("LEGAL TRIAGE // SYSTEM ONLINE");
});
) {
                doc.addPage();
                yPos = 20;
            }
            const text = `[STEP ${(i+1).toString().padStart(2, '0')}] ${step}`;
            const splitStep = doc.splitTextToSize(text, 170);
            doc.text(splitStep, 20, yPos);
            yPos += (splitStep.length * 5) + 2;
        });
        
        // Final Results
        yPos += 10;
        if (yPos > 250) { doc.addPage(); yPos = 20; }
        
        doc.setFillColor(...orange);
        doc.rect(20, yPos, 170, 20, 'F');
        doc.setTextColor(...black);
        doc.setFont("helvetica", "bold");
        doc.setFontSize(12);
        doc.text(`TOTAL REWARD SCORE: ${totalReward.toFixed(2)}`, 30, yPos + 12);
        
        // Footer
        doc.setFontSize(8);
        doc.setTextColor(150);
        doc.text("CONFIDENTIAL // FOR RL RESEARCH PURPOSES ONLY", 105, 285, { align: "center" });
        
        doc.save(`legal-triage-report-${Date.now()}.pdf`);
    }

    // Attach Event Listeners
    document.getElementById('save-token-btn').addEventListener('click', saveToken);
    document.getElementById('reset-btn').addEventListener('click', resetEnv);
    document.getElementById('step-btn').addEventListener('click', stepEnv);
    document.getElementById('auto-run-btn').addEventListener('click', runAutoInference);
    downloadBtn.addEventListener('click', downloadPDF);

    console.log("LEGAL TRIAGE // SYSTEM ONLINE");
});
