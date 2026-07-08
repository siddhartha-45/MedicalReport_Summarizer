// HealthScan AI Frontend Engine

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const browseBtn = document.getElementById('browseBtn');
    const fileCard = document.getElementById('fileCard');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const removeFileBtn = document.getElementById('removeFileBtn');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultsSection = document.getElementById('resultsSection');
    
    // Theme Switcher Elements
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeBtnIcon = themeToggleBtn.querySelector('.theme-btn-icon');
    
    // Summary Metrics Elements
    const metricsRow = document.getElementById('metricsRow');
    const metricConditions = document.getElementById('metricConditions');
    const metricSpecialist = document.getElementById('metricSpecialist');
    const metricActions = document.getElementById('metricActions');

    // Loader elements
    const btnText = analyzeBtn.querySelector('.btn-text');
    const btnLoader = analyzeBtn.querySelector('.btn-loader');
    const loaderText = document.getElementById('loaderText');
    
    // Tab Elements
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    // Data Storage
    let selectedFile = null;
    let analysisResultData = null;

    // --- Theme Swapping System ---

    // Initialize theme from cache
    const savedTheme = localStorage.getItem('theme') || 'dark';
    setTheme(savedTheme);

    themeToggleBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
        const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(nextTheme);
    });

    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        // Update Icon representation
        if (theme === 'light') {
            themeBtnIcon.textContent = '☀️';
            themeToggleBtn.title = 'Switch to Dark Mode';
        } else {
            themeBtnIcon.textContent = '🌙';
            themeToggleBtn.title = 'Switch to Light Mode';
        }
    }

    // --- Drag & Drop Operations ---
    
    // Open file chooser on Browse click
    browseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    dropzone.addEventListener('click', () => {
        fileInput.click();
    });

    // File Input change
    fileInput.addEventListener('change', (e) => {
        handleFileSelect(e.target.files[0]);
    });

    // Dragover state
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    // Dragleave state
    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('dragover');
    });

    // Drop file
    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    // Remove file click
    removeFileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetFileSelection();
    });

    // --- File Selection Core Logic ---
    
    function handleFileSelect(file) {
        if (!file) return;
        
        // Supported types
        const allowedExtensions = /(\.pdf|\.png|\.jpg|\.jpeg|\.tiff|\.bmp)$/i;
        if (!allowedExtensions.exec(file.name)) {
            alert('Unsupported file format! Please upload PDF or image documents.');
            resetFileSelection();
            return;
        }

        selectedFile = file;
        
        // Show file details card
        fileName.textContent = file.name;
        fileSize.textContent = formatBytes(file.size);
        
        // Set document icons
        const ext = file.name.split('.').pop().toLowerCase();
        if (ext === 'pdf') {
            document.getElementById('fileIcon').textContent = '📄';
        } else {
            document.getElementById('fileIcon').textContent = '🖼️';
        }

        fileCard.style.display = 'block';
        dropzone.style.display = 'none';
        
        // Enable click analyzer
        analyzeBtn.removeAttribute('disabled');
    }

    function resetFileSelection() {
        selectedFile = null;
        fileInput.value = '';
        fileCard.style.display = 'none';
        dropzone.style.display = 'block';
        analyzeBtn.setAttribute('disabled', 'true');
        resultsSection.style.display = 'none';
        metricsRow.style.display = 'none';
    }

    function formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }

    // --- Tab Switching Logic ---

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            
            // Remove active classes
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));
            
            // Set active class
            btn.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });

    // --- API Call Analysis Trigger ---

    analyzeBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        // Set Loading State
        analyzeBtn.setAttribute('disabled', 'true');
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-flex';
        
        // Progressive Loading Text Messages
        const statusMessages = [
            "Extracting text from report...",
            "Decrypting clinical labels...",
            "Synthesizing medical parameters...",
            "Structuring diagnosis data..."
        ];
        
        let msgIndex = 0;
        loaderText.textContent = statusMessages[0];
        
        const messageInterval = setInterval(() => {
            msgIndex = (msgIndex + 1) % statusMessages.length;
            loaderText.textContent = statusMessages[msgIndex];
        }, 4000);

        // Build FormData payload
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            clearInterval(messageInterval);

            if (!response.ok) {
                throw new Error(data.error || 'Server error occurred during analysis');
            }

            analysisResultData = data;
            renderResults(data);
            
        } catch (error) {
            console.error(error);
            alert(`Analysis failed: ${error.message}`);
        } finally {
            // Restore Button State
            analyzeBtn.removeAttribute('disabled');
            btnText.style.display = 'inline';
            btnLoader.style.display = 'none';
            clearInterval(messageInterval);
        }
    });

    // --- Dynamic DOM Results Rendering ---

    function renderResults(data) {
        const analysis = data.analysis;
        
        if (analysis.error) {
            alert(`AI Analysis Warning: ${analysis.error}\n\nDisplaying raw text response.`);
            renderFallbackText(analysis.raw_text);
            return;
        }

        // 1. Overall Severity Card Setup
        const severity = analysis.overall_severity || { level: "Unknown", explanation: "" };
        const sevLevel = (severity.level || "Unknown").trim().toLowerCase();
        
        const severityCard = document.getElementById('severityCard');
        const severityLabel = document.getElementById('overallSeverityLevel');
        const severityExplanation = document.getElementById('severityExplanation');
        
        // Reset classes
        severityCard.className = 'severity-card';
        
        // Apply target layout matching level
        if (sevLevel === 'normal' || sevLevel === 'healthy') {
            severityCard.classList.add('severity-card-normal');
            severityLabel.textContent = '🟢 Normal / Healthy';
        } else if (sevLevel === 'mild') {
            severityCard.classList.add('severity-card-mild');
            severityLabel.textContent = '🟡 Mild Attention';
        } else if (sevLevel === 'moderate') {
            severityCard.classList.add('severity-card-moderate');
            severityLabel.textContent = '🟠 Moderate Warning';
        } else if (sevLevel === 'severe' || sevLevel === 'high') {
            severityCard.classList.add('severity-card-severe');
            severityLabel.textContent = '🔴 Severe Assessment';
        } else {
            severityCard.classList.add('severity-card-moderate');
            severityLabel.textContent = severity.level;
        }
        severityExplanation.textContent = severity.explanation;

        // 2. Doctor details
        const doc = analysis.doctor || { specialist: "Physician", timeline: "Routine", reason: "" };
        document.getElementById('doctorSpecialist').textContent = doc.specialist || 'General Practitioner';
        
        const timelineElement = document.getElementById('doctorTimeline');
        timelineElement.textContent = doc.timeline || 'Routine';
        if ((doc.timeline || '').toLowerCase() === 'urgent' || (doc.timeline || '').toLowerCase() === 'immediate') {
            timelineElement.className = 'detail-value warning';
        } else {
            timelineElement.className = 'detail-value';
        }
        document.getElementById('doctorReason').textContent = doc.reason || 'To confirm findings.';

        // 3. Connections
        document.getElementById('connectionsText').textContent = analysis.connections || 'No major clinical dependencies identified between symptoms.';

        // 4. Problems list (Diagnosis)
        const problems = analysis.problems || [];
        const problemsList = document.getElementById('problemsList');
        problemsList.innerHTML = ''; // reset

        if (problems.length === 0) {
            problemsList.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 20px;">No diagnostic abnormalities found in the text.</p>';
        } else {
            problems.forEach((prob, idx) => {
                const item = document.createElement('div');
                item.className = 'problem-item';
                
                const sevBadgeClass = getSeverityBadgeClass(prob.severity);
                
                item.innerHTML = `
                    <div class="problem-header">
                        <div class="problem-title-group">
                            <span class="problem-title">${prob.name || 'Diagnosed Condition'}</span>
                            <span class="problem-badge ${sevBadgeClass}">${prob.severity || 'Normal'}</span>
                        </div>
                        <span class="accordion-arrow">▼</span>
                    </div>
                    <div class="problem-body">
                        <div class="problem-details-grid">
                            <div class="problem-detail-block">
                                <h5>What is this?</h5>
                                <p>${prob.what_is_it || 'N/A'}</p>
                            </div>
                            <div class="problem-detail-block">
                                <h5>How does it affect the body?</h5>
                                <p>${prob.body_effect || 'N/A'}</p>
                            </div>
                            <div class="problem-detail-block">
                                <h5>Why did this happen?</h5>
                                <p>${prob.causes || 'N/A'}</p>
                            </div>
                            <div class="problem-detail-block">
                                <h5>What do your numbers mean?</h5>
                                <p>${prob.numbers_meaning || 'N/A'}</p>
                            </div>
                        </div>
                        <div class="problem-detail-block" style="border-top: 1px solid var(--border-color); padding-top: 15px; margin-top: 5px;">
                            <h5>Is this serious?</h5>
                            <p>${prob.is_serious || 'N/A'}</p>
                        </div>
                    </div>
                `;
                
                // Toggle Accordion Click Event
                const header = item.querySelector('.problem-header');
                header.addEventListener('click', () => {
                    const isExpanded = item.classList.contains('expanded');
                    // Collapse all others
                    document.querySelectorAll('.problem-item').forEach(el => el.classList.remove('expanded'));
                    if (!isExpanded) {
                        item.classList.add('expanded');
                    }
                });

                // Expand first problem by default
                if (idx === 0) {
                    item.classList.add('expanded');
                }

                problemsList.appendChild(item);
            });
        }

        // 5. Diet Tab Rendering
        const diet = analysis.diet || { helpful_foods: [], avoid_foods: [], tips: [] };
        
        // Helpful foods
        const helpfulList = document.getElementById('helpfulFoodsList');
        helpfulList.innerHTML = '';
        if ((diet.helpful_foods || []).length === 0) {
            helpfulList.innerHTML = '<li>General healthy balanced diet.</li>';
        } else {
            diet.helpful_foods.forEach(f => {
                const li = document.createElement('li');
                li.innerHTML = typeof f === 'object' ? `<strong>${f.food}:</strong> ${f.reason}` : f;
                helpfulList.appendChild(li);
            });
        }

        // Avoid foods
        const avoidList = document.getElementById('avoidFoodsList');
        avoidList.innerHTML = '';
        if ((diet.avoid_foods || []).length === 0) {
            avoidList.innerHTML = '<li>No specific foods to restrict.</li>';
        } else {
            diet.avoid_foods.forEach(f => {
                const li = document.createElement('li');
                li.innerHTML = typeof f === 'object' ? `<strong>${f.food}:</strong> ${f.reason}` : f;
                avoidList.appendChild(li);
            });
        }

        // Tips
        const dietTipsWrapper = document.getElementById('dietTipsWrapper');
        const tipsList = document.getElementById('dietTipsList');
        tipsList.innerHTML = '';
        if ((diet.tips || []).length === 0) {
            dietTipsWrapper.style.display = 'none';
        } else {
            dietTipsWrapper.style.display = 'block';
            diet.tips.forEach(t => {
                const li = document.createElement('li');
                li.textContent = t;
                tipsList.appendChild(li);
            });
        }

        // 6. Lifestyle Tab Rendering
        const lifestyle = analysis.lifestyle || { immediate_actions: [], daily_changes: [], precautions: [] };
        
        // Immediate Actions
        const immediateList = document.getElementById('immediateActionsList');
        immediateList.innerHTML = '';
        if ((lifestyle.immediate_actions || []).length === 0) {
            immediateList.parentNode.style.display = 'none';
        } else {
            immediateList.parentNode.style.display = 'block';
            lifestyle.immediate_actions.forEach(act => {
                const li = document.createElement('li');
                li.textContent = act;
                immediateList.appendChild(li);
            });
        }

        // Daily changes
        const dailyList = document.getElementById('dailyChangesList');
        dailyList.innerHTML = '';
        if ((lifestyle.daily_changes || []).length === 0) {
            dailyList.parentNode.style.display = 'none';
        } else {
            dailyList.parentNode.style.display = 'block';
            lifestyle.daily_changes.forEach(chg => {
                const li = document.createElement('li');
                li.textContent = chg;
                dailyList.appendChild(li);
            });
        }

        // Precautions
        const precsList = document.getElementById('precautionsList');
        precsList.innerHTML = '';
        if ((lifestyle.precautions || []).length === 0) {
            precsList.parentNode.style.display = 'none';
        } else {
            precsList.parentNode.style.display = 'block';
            lifestyle.precautions.forEach(prec => {
                const li = document.createElement('li');
                li.textContent = prec;
                precsList.appendChild(li);
            });
        }

        // 7. Care & Expectation Tab
        const treatments = analysis.treatment || [];
        const treatmentList = document.getElementById('treatmentList');
        treatmentList.innerHTML = '';
        if (treatments.length === 0) {
            treatmentList.innerHTML = '<li>Confirm treatment directives with your doctor.</li>';
        } else {
            treatments.forEach(t => {
                const li = document.createElement('li');
                li.textContent = t;
                treatmentList.appendChild(li);
            });
        }

        const followUps = analysis.follow_up || [];
        const followUpList = document.getElementById('followUpList');
        followUpList.innerHTML = '';
        if (followUps.length === 0) {
            followUpList.innerHTML = '<li>General follow-up as scheduled by clinic.</li>';
        } else {
            followUps.forEach(f => {
                const li = document.createElement('li');
                li.textContent = f;
                followUpList.appendChild(li);
            });
        }

        // --- Render Summary Metric Cards ---
        metricConditions.textContent = problems.length;
        metricSpecialist.textContent = doc.specialist || 'None';
        metricActions.textContent = (lifestyle.immediate_actions || []).length;
        
        metricsRow.style.display = 'grid';

        // Reset to first tab
        tabBtns[0].click();

        // Reveal Results with slide transition
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function renderFallbackText(rawText) {
        const problemsList = document.getElementById('problemsList');
        problemsList.innerHTML = `<pre style="white-space: pre-wrap; font-family: sans-serif; font-size: 0.95rem; color: var(--text-primary);">${rawText}</pre>`;
        
        metricsRow.style.display = 'none';
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function getSeverityBadgeClass(severity) {
        const sev = (severity || '').toLowerCase();
        if (sev.includes('normal') || sev.includes('healthy')) return 'badge-normal';
        if (sev.includes('mild')) return 'badge-mild';
        if (sev.includes('moderate')) return 'badge-moderate';
        if (sev.includes('severe') || sev.includes('high')) return 'badge-severe';
        return 'badge-moderate';
    }

    // --- Footer Action Event Handlers ---

    // Print Action
    document.getElementById('printReportBtn').addEventListener('click', () => {
        window.print();
    });

    // JSON Raw download action
    document.getElementById('rawReportDownloadBtn').addEventListener('click', () => {
        if (!analysisResultData) return;
        
        const jsonString = JSON.stringify(analysisResultData.analysis, null, 2);
        const blob = new Blob([jsonString], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `medical_analysis_${selectedFile.name.replace(/\.[^/.]+$/, "")}.json`;
        document.body.appendChild(a);
        a.click();
        
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
});
