// TenderMind Frontend Application State
const STATE = {
  currentTab: 'tab-command-center',
  activeTenderId: 'GEM/2026/B/123456',
  companyId: 'comp_nexus_01',
  companyData: null,
  tendersData: [],
  activeTenderData: null,
  eligibilityData: null,
  bidData: null
};

// Tab Switching
function switchTab(tabId) {
  STATE.currentTab = tabId;
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));

  const targetPanel = document.getElementById(tabId);
  if (targetPanel) targetPanel.classList.add('active');

  const navBtnId = tabId.replace('tab-', 'nav-');
  const targetNavBtn = document.getElementById(navBtnId);
  if (targetNavBtn) targetNavBtn.classList.add('active');

  if (window.lucide) lucide.createIcons();

  // Lazy load tab data
  if (tabId === 'tab-discovery') loadTenders();
  if (tabId === 'tab-document-intelligence') loadTenderIntelligence(STATE.activeTenderId);
  if (tabId === 'tab-company-profile') loadCompanyProfile();
  if (tabId === 'tab-eligibility') loadEligibility(STATE.activeTenderId);
  if (tabId === 'tab-bid-preparation') loadBidPackage(STATE.activeTenderId);
  if (tabId === 'tab-corrigenda') loadCorrigenda();
  if (tabId === 'tab-agent-activity') loadTraces();
}

// 1. Initial Load & Command Center
async function initApp() {
  await loadCompanyProfile();
  await loadCommandCenter();
  if (window.lucide) lucide.createIcons();
}

async function loadCommandCenter() {
  try {
    const [tenderRes, eligRes] = await Promise.all([
      fetch(`/api/tenders/${encodeURIComponent(STATE.activeTenderId)}`),
      fetch(`/api/eligibility/${encodeURIComponent(STATE.activeTenderId)}?company_id=${STATE.companyId}`)
    ]);

    STATE.activeTenderData = await tenderRes.json();
    STATE.eligibilityData = await eligRes.json();

    renderCommandCenter();
  } catch (err) {
    console.error("Failed to load command center:", err);
  }
}

function renderCommandCenter() {
  const tender = STATE.activeTenderData;
  const elig = STATE.eligibilityData;
  if (!tender || !elig) return;

  // Header and stats
  document.getElementById('dashTenderTitle').textContent = `${tender.tender_id} — ${tender.title}`;
  document.getElementById('dashTenderDept').textContent = tender.department;
  document.getElementById('dashTenderValue').textContent = `₹${tender.estimated_value_inr.toLocaleString('en-IN')}`;
  
  const deadlineDate = new Date(tender.submission_deadline);
  document.getElementById('dashTenderDeadline').textContent = deadlineDate.toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
  });

  document.getElementById('statReadiness').textContent = `${elig.readiness_percentage}%`;
  document.getElementById('statReadinessBar').style.width = `${elig.readiness_percentage}%`;

  const missingGaps = elig.gaps.filter(g => g.severity === 'BLOCKING');
  if (missingGaps.length === 0) {
    document.getElementById('statReadinessLabel').textContent = "100% Submission Ready!";
    document.getElementById('statReadinessLabel').className = "text-xs text-emerald-400 font-semibold";
    document.getElementById('dashGapCard').style.display = 'none';
    document.getElementById('statMissingDocsText').textContent = "Missing: 0";
    document.getElementById('statDocsCount').textContent = "7 / 7";
  } else {
    document.getElementById('statReadinessLabel').textContent = `${missingGaps.length} Blocking Gap`;
    document.getElementById('statReadinessLabel').className = "text-xs text-rose-400 font-semibold";
    document.getElementById('dashGapCard').style.display = 'block';
  }

  // Render requirement list snapshot
  const listEl = document.getElementById('dashRequirementsList');
  listEl.innerHTML = elig.assessments.map(a => {
    let badgeClass = 'badge-satisfied';
    let badgeIcon = 'check-circle';
    if (a.status === 'Not satisfied') {
      badgeClass = 'badge-not-satisfied';
      badgeIcon = 'x-circle';
    } else if (a.status === 'Needs verification') {
      badgeClass = 'badge-needs-verification';
      badgeIcon = 'alert-circle';
    }

    return `
      <div class="flex items-center justify-between p-2.5 rounded-xl bg-dark-850 border border-dark-750 text-xs">
        <div class="space-y-0.5">
          <div class="flex items-center gap-2">
            <span class="font-semibold text-white">${a.clause_title}</span>
            <span class="text-[10px] text-slate-400 font-mono">${a.source_citation}</span>
          </div>
          <p class="text-[11px] text-slate-400">${a.company_value_or_evidence}</p>
        </div>
        <span class="${badgeClass} flex items-center gap-1">
          <span>${a.status}</span>
        </span>
      </div>
    `;
  }).join('');

  if (window.lucide) lucide.createIcons();
}

// 2. Tender Discovery Tab
async function loadTenders() {
  const query = document.getElementById('filterQuery').value;
  const category = document.getElementById('filterCategory').value;
  const location = document.getElementById('filterLocation').value;

  let url = `/api/tenders?`;
  if (query) url += `query=${encodeURIComponent(query)}&`;
  if (category && category !== 'all') url += `category=${encodeURIComponent(category)}&`;
  if (location) url += `location=${encodeURIComponent(location)}&`;

  try {
    const res = await fetch(url);
    const tenders = await res.json();
    STATE.tendersData = tenders;

    const container = document.getElementById('tendersContainer');
    container.innerHTML = tenders.map(t => {
      const matchScore = t.suitability_score || 85;
      const scoreColor = matchScore >= 80 ? 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10' :
                         matchScore >= 50 ? 'text-amber-400 border-amber-500/30 bg-amber-500/10' :
                         'text-rose-400 border-rose-500/30 bg-rose-500/10';

      return `
        <div class="bg-dark-900 border border-dark-700/70 rounded-2xl p-5 hover:border-teal-500/40 transition space-y-3">
          <div class="flex items-start justify-between gap-4">
            <div>
              <div class="flex items-center gap-2">
                <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-dark-800 text-teal-400 border border-teal-500/20">${t.portal_source}</span>
                <span class="text-[10px] text-slate-400 font-mono">${t.reference_number}</span>
              </div>
              <h3 class="text-base font-bold text-white mt-1">${t.title}</h3>
              <p class="text-xs text-slate-400 mt-0.5">${t.department} • <span class="text-slate-300">${t.location}</span></p>
            </div>
            <div class="text-right">
              <span class="text-[10px] uppercase font-bold text-slate-400">Two-Way Match</span>
              <div class="px-2.5 py-1 rounded-lg border font-mono font-bold text-sm ${scoreColor} mt-0.5">
                ${matchScore}/100
              </div>
            </div>
          </div>

          <p class="text-xs text-slate-300 leading-relaxed">${t.summary}</p>

          <div class="flex flex-wrap items-center justify-between pt-3 border-t border-dark-800 text-xs">
            <div class="flex items-center gap-4 text-slate-400">
              <span>Value: <strong class="text-teal-300 font-mono">₹${t.estimated_value_inr.toLocaleString('en-IN')}</strong></span>
              <span>EMD: <strong class="text-white font-mono">₹${t.earnest_money_deposit_inr.toLocaleString('en-IN')}</strong></span>
              <span>Deadline: <strong class="text-amber-400">${t.submission_deadline.split('T')[0]}</strong></span>
            </div>
            <button onclick="selectAndInspectTender('${t.tender_id}')" class="px-3 py-1.5 rounded-lg bg-teal-500 hover:bg-teal-400 text-dark-950 font-bold text-xs flex items-center gap-1.5 transition">
              <span>Inspect & Evaluate</span>
              <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
            </button>
          </div>
        </div>
      `;
    }).join('');

    if (window.lucide) lucide.createIcons();
  } catch (err) {
    console.error("Failed to load tenders:", err);
  }
}

function selectAndInspectTender(tenderId) {
  STATE.activeTenderId = tenderId;
  switchTab('tab-document-intelligence');
}

// 3. Document Intelligence Tab
async function loadTenderIntelligence(tenderId) {
  document.getElementById('activeIntelTenderId').textContent = tenderId;
  try {
    const res = await fetch(`/api/tenders/${encodeURIComponent(tenderId)}`);
    const tender = await res.json();
    STATE.activeTenderData = tender;

    document.getElementById('intelPortal').textContent = tender.portal_source;
    document.getElementById('intelValue').textContent = `₹${tender.estimated_value_inr.toLocaleString('en-IN')}`;
    document.getElementById('intelEmd').textContent = `₹${tender.earnest_money_deposit_inr.toLocaleString('en-IN')} (MSE Exempt)`;
    document.getElementById('intelDeadline').textContent = tender.submission_deadline.split('T')[0];
    document.getElementById('intelDocLink').href = tender.original_document_url || '#';

    const tbody = document.getElementById('intelClausesBody');
    tbody.innerHTML = tender.requirements.map(r => `
      <tr class="hover:bg-dark-850/50 transition">
        <td class="py-2.5 px-3 font-semibold text-white">${r.clause_title}</td>
        <td class="py-2.5 px-3 text-slate-300">${r.description}</td>
        <td class="py-2.5 px-3 font-mono text-teal-300 text-[11px]">Page ${r.source_page}, ${r.source_section}</td>
        <td class="py-2.5 px-3">
          ${r.relaxable_for_msme ? '<span class="text-emerald-400 text-[10px] bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Yes (MSE)</span>' : '<span class="text-slate-500 text-[10px]">Mandatory</span>'}
        </td>
      </tr>
    `).join('');

    if (window.lucide) lucide.createIcons();
  } catch (err) {
    console.error("Failed to load tender intelligence:", err);
  }
}

// 4. Company Profile & Document Vault Tab
async function loadCompanyProfile() {
  try {
    const res = await fetch(`/api/company?company_id=${STATE.companyId}`);
    const comp = await res.json();
    STATE.companyData = comp;

    document.getElementById('profName').textContent = comp.name;
    document.getElementById('profType').textContent = `${comp.business_type} • ${comp.enterprise_category} Enterprise`;
    document.getElementById('profLocation').textContent = `${comp.city}, ${comp.state}`;
    document.getElementById('profUdyam').textContent = comp.udyam_registration_number || 'N/A';
    document.getElementById('profGstin').textContent = comp.gstin;
    document.getElementById('profPan').textContent = comp.pan_number;
    document.getElementById('profExp').textContent = `${comp.years_of_operation} Years`;
    document.getElementById('profTurnover').textContent = `₹${Math.round(comp.average_annual_turnover_inr).toLocaleString('en-IN')}`;

    const tbody = document.getElementById('profDocsBody');
    tbody.innerHTML = comp.documents.map(d => {
      let badge = d.status === 'Uploaded' 
        ? '<span class="badge-satisfied">Uploaded & Verified</span>'
        : '<span class="badge-not-satisfied">Missing</span>';

      return `
        <tr class="hover:bg-dark-850/50 transition">
          <td class="py-2.5 px-3">
            <span class="font-semibold text-white block">${d.title || d.document_type}</span>
            <span class="text-[10px] text-slate-400 font-mono">${d.file_name || 'No file attached'}</span>
          </td>
          <td class="py-2.5 px-3">${badge}</td>
          <td class="py-2.5 px-3 text-slate-300 text-[11px]">${d.issuing_authority || 'Pending'}</td>
          <td class="py-2.5 px-3 text-right">
            ${d.status === 'Missing' ? `<button onclick="resolveGapDemo()" class="px-2 py-1 bg-indigo-600 hover:bg-indigo-500 text-white rounded text-[11px] font-semibold">Upload Now</button>` : `<span class="text-emerald-400 text-[11px]">Active</span>`}
          </td>
        </tr>
      `;
    }).join('');

    if (window.lucide) lucide.createIcons();
  } catch (err) {
    console.error("Failed to load company profile:", err);
  }
}

// 5. Eligibility & Gap Engine Tab
async function loadEligibility(tenderId) {
  try {
    const res = await fetch(`/api/eligibility/${encodeURIComponent(tenderId)}?company_id=${STATE.companyId}`);
    const elig = await res.json();
    STATE.eligibilityData = elig;

    document.getElementById('eligReadinessScore').textContent = `${elig.readiness_percentage}%`;
    document.getElementById('eligSatisfiedCount').textContent = elig.satisfied_count;
    document.getElementById('eligNotSatisfiedCount').textContent = elig.not_satisfied_count;
    document.getElementById('eligNeedsVerCount').textContent = elig.needs_verification_count;

    const badge = document.getElementById('eligVerdictBadge');
    if (elig.overall_status === 'SUBMISSION_READY') {
      badge.textContent = 'SUBMISSION READY';
      badge.className = 'px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30';
    } else {
      badge.textContent = 'POTENTIAL GAP DETECTED';
      badge.className = 'px-3 py-1 rounded-full text-xs font-bold bg-rose-500/20 text-rose-400 border border-rose-500/30';
    }

    const tbody = document.getElementById('eligAssessmentsBody');
    tbody.innerHTML = elig.assessments.map(a => {
      let badgeClass = a.status === 'Satisfied' ? 'badge-satisfied' :
                       a.status === 'Not satisfied' ? 'badge-not-satisfied' : 'badge-needs-verification';

      return `
        <tr class="hover:bg-dark-850/50 transition">
          <td class="py-3 px-3">
            <span class="font-bold text-white block">${a.clause_title}</span>
            <span class="text-[10px] text-teal-400 font-mono">${a.source_citation}</span>
          </td>
          <td class="py-3 px-3 text-slate-300">${a.tender_condition}</td>
          <td class="py-3 px-3 text-slate-200">
            <span>${a.company_value_or_evidence}</span>
            ${a.msme_benefit_applied ? `<span class="block text-[10px] text-teal-300 font-semibold mt-0.5">💡 ${a.msme_benefit_notes}</span>` : ''}
          </td>
          <td class="py-3 px-3"><span class="${badgeClass}">${a.status}</span></td>
        </tr>
      `;
    }).join('');

    // Gaps
    const gapsList = document.getElementById('eligGapsList');
    if (elig.gaps.length === 0) {
      gapsList.innerHTML = `<div class="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 text-emerald-400 text-xs font-medium">All conditions satisfied! Zero blocking gaps detected.</div>`;
    } else {
      gapsList.innerHTML = elig.gaps.map(g => `
        <div class="p-4 rounded-xl bg-rose-950/20 border border-rose-500/30 space-y-1.5 text-xs">
          <div class="flex items-center justify-between">
            <span class="font-bold text-rose-300">[${g.severity}] ${g.requirement_title}</span>
            <span class="text-[10px] font-mono text-slate-400">ID: ${g.gap_id}</span>
          </div>
          <p class="text-slate-300">${g.description}</p>
          <div class="text-[11px] text-teal-300 bg-dark-900/80 p-2.5 rounded-lg border border-dark-700">
            <strong>Remedy / Resolution:</strong> ${g.resolution_step}
          </div>
        </div>
      `).join('');
    }

    if (window.lucide) lucide.createIcons();
  } catch (err) {
    console.error("Failed to load eligibility:", err);
  }
}

// 6. Bid Preparation Workspace Tab
async function loadBidPackage(tenderId) {
  try {
    const res = await fetch(`/api/bids/${encodeURIComponent(tenderId)}?company_id=${STATE.companyId}`);
    const pkg = await res.json();
    STATE.bidData = pkg;

    document.getElementById('bidFractionBadge').textContent = `${pkg.readiness_fraction} Ready`;
    document.getElementById('bidCountSummary').textContent = `${pkg.completed_items_count}/${pkg.total_items_count} Completed`;

    // Render Checklist
    const chkList = document.getElementById('bidChecklistItems');
    chkList.innerHTML = pkg.checklist.map(item => {
      const isCompleted = item.status === 'COMPLETED';
      return `
        <div class="p-3 rounded-xl bg-dark-850 border border-dark-750 flex items-start gap-3 text-xs">
          <input type="checkbox" ${isCompleted ? 'checked' : ''} onchange="toggleChecklistItem('${item.item_id}')" class="mt-0.5 rounded text-teal-500 focus:ring-0">
          <div class="flex-1 space-y-0.5">
            <div class="flex items-center justify-between">
              <span class="font-semibold ${isCompleted ? 'text-slate-200 line-through' : 'text-white'}">${item.title}</span>
              <span class="text-[10px] text-slate-400">${item.tender_section.split(':')[0]}</span>
            </div>
            <p class="text-[11px] text-slate-400">${item.description}</p>
            ${item.associated_document_name ? `<span class="text-[10px] text-teal-400 font-mono block">Attached: ${item.associated_document_name}</span>` : '<span class="text-[10px] text-rose-400 font-mono block">Action Required: Upload Document</span>'}
          </div>
        </div>
      `;
    }).join('');

    // Render Proposals
    const propContainer = document.getElementById('proposalSectionsContainer');
    propContainer.innerHTML = pkg.proposals.map(s => `
      <div class="p-4 rounded-xl bg-dark-850 border border-dark-750 space-y-2 text-xs">
        <div class="flex items-center justify-between">
          <h4 class="font-bold text-teal-300">${s.title}</h4>
          <button onclick="approveProposalSection('${s.section_id}')" class="px-2.5 py-1 rounded text-[11px] font-semibold transition ${s.human_approved ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-dark-700 text-slate-300 hover:text-white'}">
            ${s.human_approved ? '✓ Approved' : 'Sign-Off'}
          </button>
        </div>
        <p class="text-slate-300 leading-relaxed whitespace-pre-line">${s.content}</p>
      </div>
    `).join('');

    // Render Undertakings
    const underContainer = document.getElementById('undertakingsContainer');
    underContainer.innerHTML = Object.entries(pkg.undertakings).map(([title, text]) => `
      <div class="p-3.5 rounded-xl bg-dark-850 border border-dark-750 space-y-1 text-xs">
        <span class="font-bold text-white block">${title}</span>
        <p class="text-slate-300 text-[11px] leading-relaxed">${text}</p>
      </div>
    `).join('');

    if (window.lucide) lucide.createIcons();
  } catch (err) {
    console.error("Failed to load bid package:", err);
  }
}

async function toggleChecklistItem(itemId) {
  try {
    await fetch(`/api/bids/${encodeURIComponent(STATE.activeTenderId)}/checklist/${itemId}/toggle?company_id=${STATE.companyId}`, {
      method: 'POST'
    });
    await loadBidPackage(STATE.activeTenderId);
  } catch (err) {
    console.error("Failed to toggle item:", err);
  }
}

async function approveProposalSection(sectionId) {
  try {
    await fetch(`/api/bids/${encodeURIComponent(STATE.activeTenderId)}/proposal/${sectionId}/approve?company_id=${STATE.companyId}`, {
      method: 'POST'
    });
    await loadBidPackage(STATE.activeTenderId);
  } catch (err) {
    console.error("Failed to approve proposal section:", err);
  }
}

// 7. Corrigenda Tab
async function loadCorrigenda() {
  try {
    const res = await fetch(`/api/corrigenda`);
    const data = await res.json();
    const list = data.corrigenda || [];

    const container = document.getElementById('corrigendaCardsList');
    container.innerHTML = list.map(c => `
      <div class="bg-dark-900 border border-amber-500/30 rounded-2xl p-5 space-y-3">
        <div class="flex items-start justify-between">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30">CORRIGENDUM #${c.corrigendum_number}</span>
              <span class="text-xs text-slate-400">${c.issue_date}</span>
            </div>
            <h3 class="text-base font-bold text-white mt-1">${c.title}</h3>
            <p class="text-xs text-teal-300 font-mono">${c.tender_title}</p>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs bg-dark-850 p-3 rounded-xl border border-dark-700">
          <div>
            <span class="text-slate-400 text-[10px] block">PREVIOUS VALUE:</span>
            <p class="text-slate-300 line-through font-mono mt-0.5">${c.old_value || 'None'}</p>
          </div>
          <div>
            <span class="text-amber-400 text-[10px] block font-bold">REVISED VALUE:</span>
            <p class="text-emerald-400 font-bold font-mono mt-0.5">${c.new_value || 'None'}</p>
          </div>
        </div>

        <div class="text-xs text-slate-200">
          <strong>Impact & Action Required:</strong> ${c.action_required}
        </div>
      </div>
    `).join('');

    if (window.lucide) lucide.createIcons();
  } catch (err) {
    console.error("Failed to load corrigenda:", err);
  }
}

// 8. AI Agent Activity Inspector (MCP)
async function loadTraces() {
  try {
    const res = await fetch(`/api/mcp/traces`);
    const traces = await res.json();

    const tbody = document.getElementById('tracesTableBody');
    tbody.innerHTML = traces.map(t => `
      <tr class="hover:bg-dark-850/50 transition">
        <td class="py-2.5 px-3 text-slate-400 text-[10px]">${t.timestamp}</td>
        <td class="py-2.5 px-3 text-teal-300 font-semibold font-sans">${t.agent_name}</td>
        <td class="py-2.5 px-3 text-cyan-400">${t.mcp_server}</td>
        <td class="py-2.5 px-3 text-indigo-300 font-bold">${t.tool_called}</td>
        <td class="py-2.5 px-3 text-slate-300 font-sans text-[11px]">${t.summary_result}</td>
        <td class="py-2.5 px-3 text-right">
          <span class="badge-satisfied">Approved</span>
        </td>
      </tr>
    `).join('');

    if (window.lucide) lucide.createIcons();
  } catch (err) {
    console.error("Failed to load traces:", err);
  }
}

// 9. Interactive "Resolve Gap Demo"
async function resolveGapDemo() {
  const btn = document.getElementById('btnDemoResolve');
  if (btn) btn.innerHTML = 'Uploading & Verifying...';

  try {
    await fetch(`/api/company/documents/resolve-gap?company_id=${STATE.companyId}`, {
      method: 'POST'
    });
    await loadCompanyProfile();
    await loadCommandCenter();
    await loadEligibility(STATE.activeTenderId);
    await loadBidPackage(STATE.activeTenderId);

    alert("✅ SUCCESS: Completion Certificate uploaded and hash-verified! Eligibility engine recalculated readiness to 100% SUBMISSION READY.");
  } catch (err) {
    console.error("Failed to resolve gap:", err);
  } finally {
    if (btn) btn.innerHTML = '<i data-lucide="check" class="w-4 h-4"></i><span>Gap Resolved</span>';
    if (window.lucide) lucide.createIcons();
  }
}

// 10. Multi-Agent Pipeline Runner
async function runFullPipeline() {
  switchTab('tab-agent-activity');
  try {
    await fetch(`/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: "Can my company apply for this tender? What exactly is preventing us from being submission-ready?",
        active_tender_id: STATE.activeTenderId,
        company_id: STATE.companyId
      })
    });
    await loadTraces();
  } catch (err) {
    console.error(err);
  }
}

// 11. Conversational Agent ("The Killer Moment")
function triggerQuickPrompt(promptText) {
  document.getElementById('chatInput').value = promptText;
  sendChatMessage();
}

function askKillerQuestion() {
  switchTab('tab-agent-chat');
  triggerQuickPrompt("Can my company apply for this tender? What exactly is preventing us from being submission-ready?");
}

async function sendChatMessage() {
  const input = document.getElementById('chatInput');
  const query = input.value.trim();
  if (!query) return;

  const messagesContainer = document.getElementById('chatMessages');

  // Add User Message
  messagesContainer.innerHTML += `
    <div class="flex items-start justify-end gap-3">
      <div class="bg-teal-600 p-3.5 rounded-2xl text-xs text-white max-w-xl shadow-md">
        ${query}
      </div>
      <div class="w-8 h-8 rounded-lg bg-teal-400 flex items-center justify-center text-dark-950 font-bold shrink-0">
        You
      </div>
    </div>
  `;
  input.value = '';
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  // Add Loading State
  const loadingId = `load_${Date.now()}`;
  messagesContainer.innerHTML += `
    <div id="${loadingId}" class="flex items-start gap-3">
      <div class="w-8 h-8 rounded-lg bg-teal-500 flex items-center justify-center text-dark-950 font-bold shrink-0">
        <i data-lucide="bot" class="w-5 h-5"></i>
      </div>
      <div class="bg-dark-800 border border-dark-700 p-4 rounded-2xl text-xs text-slate-400">
        Consulting MCP servers and cross-verifying verified documents...
      </div>
    </div>
  `;
  if (window.lucide) lucide.createIcons();
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  try {
    const res = await fetch(`/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: query,
        active_tender_id: STATE.activeTenderId,
        company_id: STATE.companyId
      })
    });
    const data = await res.json();

    document.getElementById(loadingId)?.remove();

    // Render Agent Response
    const formattedAnswer = data.answer
      .replace(/\n/g, '<br>')
      .replace(/### (.*?)<br>/g, '<h3 class="text-sm font-bold text-white mt-1 mb-1">$1</h3>')
      .replace(/#### (.*?)<br>/g, '<h4 class="text-xs font-bold text-teal-300 mt-2 mb-1">$1</h4>')
      .replace(/\*\*(.*?)\*\*/g, '<strong class="text-white">$1</strong>')
      .replace(/`(.*?)`/g, '<code class="font-mono bg-dark-950 text-cyan-300 px-1 py-0.5 rounded text-[11px]">$1</code>');

    messagesContainer.innerHTML += `
      <div class="flex items-start gap-3">
        <div class="w-8 h-8 rounded-lg bg-teal-500 flex items-center justify-center text-dark-950 font-bold shrink-0">
          <i data-lucide="bot" class="w-5 h-5"></i>
        </div>
        <div class="bg-dark-800 border border-dark-700 p-4 rounded-2xl text-xs text-slate-200 space-y-2 max-w-xl">
          <div class="leading-relaxed">${formattedAnswer}</div>
          ${data.tools_used && data.tools_used.length > 0 ? `
            <div class="pt-2 border-t border-dark-700/60 text-[10px] font-mono text-slate-400 flex flex-wrap gap-1">
              <span class="text-slate-500">MCP Tools:</span>
              ${data.tools_used.map(t => `<span class="bg-dark-900 text-teal-400 px-1.5 py-0.5 rounded border border-dark-750">${t}</span>`).join('')}
            </div>
          ` : ''}
        </div>
      </div>
    `;

    if (window.lucide) lucide.createIcons();
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  } catch (err) {
    document.getElementById(loadingId)?.remove();
    console.error("Chat error:", err);
  }
}

// Initialize on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  initApp();
});
