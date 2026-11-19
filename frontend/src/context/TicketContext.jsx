import React, { createContext, useContext, useState, useMemo, useEffect } from 'react';
import Papa from 'papaparse';
import { DEFAULT_TICKETS } from '../data/defaultTickets';

const TicketContext = createContext(null);

export function TicketProvider({ children }) {
  const [activeTab, setActiveTab] = useState('triage');
  const [tickets, setTickets] = useState([]);
  const [defaultTickets, setDefaultTickets] = useState([]);
  const [selectedTicketId, setSelectedTicketId] = useState(null);
  const [deflectedCount, setDeflectedCount] = useState(0);
  const [isBacklogFiltered, setIsBacklogFiltered] = useState(false);
  const [isCustomDataset, setIsCustomDataset] = useState(false);
  const [activeDatasetName, setActiveDatasetName] = useState('Default Q3 (1,444 Tickets)');
  const [toast, setToast] = useState(null);

  // Filters
  const [searchQuery, setSearchQuery] = useState('');
  const [filterCategory, setFilterCategory] = useState('ALL');
  const [filterPriority, setFilterPriority] = useState('ALL');
  const [filterRisk, setFilterRisk] = useState('ALL');
  const [filterAgent, setFilterAgent] = useState('ALL');

  // Checklist state for active ticket
  const [checklist, setChecklist] = useState({ c1: false, c2: false, c3: false });

  // Slide state for Executive Deck
  const [currentSlide, setCurrentSlide] = useState(1);
  const totalSlides = 8;

  // Initialize with pre-bundled default dataset
  useEffect(() => {
    loadDataset(DEFAULT_TICKETS, 'Default RideOps Dataset (1,444 Tickets)', false);
  }, []);

  const showToast = (title, msg) => {
    setToast({ title, msg });
    setTimeout(() => {
      setToast(null);
    }, 3500);
  };

  // Universal dataset loader (Default or uploaded CSV)
  const loadDataset = (data, sourceLabel, isCustom = false, filename = '') => {
    const processed = data.map((t, idx) => {
      const c = new Date(t.created_at);
      const f = t.final_closed_at ? new Date(t.final_closed_at) : new Date();
      const res_hrs = Math.max(0.5, (f - c) / (1000 * 3600));
      return {
        ...t,
        ticket_id: t.ticket_id || `SUP-${idx + 1000}`,
        res_hrs: isNaN(res_hrs) ? 12.0 : res_hrs,
        status: t.status || 'Closed',
        priority: t.priority || 'P3',
        category: t.category || 'General Issue',
        client_name: t.client_name || 'Corporate Client',
        client_id: t.client_id || 'CL-000',
        client_tier: t.client_tier || 'Enterprise',
        assigned_agent: t.assigned_agent || 'Support Team',
        isResolvedLive: false
      };
    });

    if (!isCustom) {
      setDefaultTickets(processed);
    }

    setTickets(processed);
    setIsCustomDataset(isCustom);
    setActiveDatasetName(isCustom ? filename : 'Default Q3 (1,444 Tickets)');
    setDeflectedCount(0);
    setSearchQuery('');
    setFilterCategory('ALL');
    setFilterPriority('ALL');
    setFilterRisk('ALL');
    setFilterAgent('ALL');
    setIsBacklogFiltered(false);
    setChecklist({ c1: false, c2: false, c3: false });

    if (processed.length > 0) {
      setSelectedTicketId(processed[0].ticket_id);
    }

    showToast(isCustom ? 'New CSV Loaded' : 'Default Dataset Loaded', sourceLabel);
  };

  // Reset to default 1,444 tickets
  const resetToDefault = () => {
    if (defaultTickets.length > 0) {
      loadDataset(defaultTickets, 'Restored Default 1,444 Tickets', false);
    }
  };

  // Upload custom CSV
  const handleFileUpload = (file) => {
    if (!file) return;
    Papa.parse(file, {
      header: true,
      dynamicTyping: true,
      skipEmptyLines: true,
      complete: (results) => {
        if (results.data && results.data.length > 0) {
          loadDataset(results.data, `Uploaded: ${file.name} (${results.data.length} tickets)`, true, file.name);
        } else {
          alert('Uploaded CSV file was empty or improperly formatted.');
        }
      },
      error: (err) => {
        alert(`Error reading CSV: ${err.message}`);
      }
    });
  };

  // Live 1-click resolve
  const resolveTicketLive = (ticketId) => {
    setTickets((prev) =>
      prev.map((t) => {
        if (t.ticket_id === ticketId) {
          return {
            ...t,
            isResolvedLive: true,
            status: 'Closed - Resolved at L1'
          };
        }
        return t;
      })
    );
    setDeflectedCount((prev) => prev + 1);
    showToast('Resolved at L1 in 8 Mins! 🎉', `Ticket ${ticketId} resolved! Saved ~128 hours of bounce delay.`);
  };

  // Filtered tickets
  const filteredTickets = useMemo(() => {
    return tickets.filter((t) => {
      if (filterCategory !== 'ALL' && t.category !== filterCategory) return false;
      if (filterPriority !== 'ALL' && t.priority !== filterPriority) return false;
      if (filterAgent !== 'ALL' && t.assigned_agent !== filterAgent) return false;

      if (filterRisk === 'OPEN' && (t.status === 'Closed' || t.isResolvedLive)) return false;
      if (filterRisk === 'ESCALATED' && t.escalated_to_eng !== 'Yes') return false;
      if (filterRisk === 'RESOLVED_L1' && !t.isResolvedLive) return false;
      if (filterRisk === 'HIGH_RISK') {
        const desc = (t.description || '').toLowerCase();
        const isHigh =
          desc.includes('cutoff') ||
          desc.includes('date range') ||
          desc.includes('> 15 days') ||
          desc.includes('stuck at loading') ||
          desc.includes('insurance expired') ||
          desc.includes('frozen') ||
          desc.includes('gps') ||
          desc.includes('duplicate');
        if (!isHigh) return false;
      }

      if (searchQuery) {
        const text = `${t.ticket_id} ${t.client_name} ${t.client_id} ${t.category} ${t.description}`.toLowerCase();
        if (!text.includes(searchQuery.toLowerCase().trim())) return false;
      }

      return true;
    });
  }, [tickets, filterCategory, filterPriority, filterRisk, filterAgent, searchQuery]);

  // Selected ticket object
  const selectedTicket = useMemo(() => {
    const found = filteredTickets.find((t) => t.ticket_id === selectedTicketId);
    return found || filteredTickets[0] || null;
  }, [filteredTickets, selectedTicketId]);

  // When selected ticket changes, reset checklist
  useEffect(() => {
    setChecklist({ c1: false, c2: false, c3: false });
  }, [selectedTicketId]);

  // Open backlog count
  const openBacklogCount = useMemo(() => {
    return tickets.filter((t) => t.status !== 'Closed' && !t.isResolvedLive).length;
  }, [tickets]);

  // Toggle 1-click backlog filter
  const toggleBacklogFilter = () => {
    if (isBacklogFiltered) {
      setIsBacklogFiltered(false);
      setFilterRisk('ALL');
    } else {
      setIsBacklogFiltered(true);
      setFilterRisk('OPEN');
    }
  };

  const filterToBacklogOnly = () => {
    setIsBacklogFiltered(true);
    setFilterRisk('OPEN');
  };

  // Next / Prev ticket
  const nextTicket = () => {
    const idx = filteredTickets.findIndex((t) => t.ticket_id === selectedTicketId);
    if (idx < filteredTickets.length - 1) {
      setSelectedTicketId(filteredTickets[idx + 1].ticket_id);
    }
  };

  const prevTicket = () => {
    const idx = filteredTickets.findIndex((t) => t.ticket_id === selectedTicketId);
    if (idx > 0) {
      setSelectedTicketId(filteredTickets[idx - 1].ticket_id);
    }
  };

  // Export current queue to CSV
  const exportQueueCsv = () => {
    if (filteredTickets.length === 0) {
      showToast('Queue Empty', 'No tickets in current filtered queue.');
      return;
    }
    const rows = filteredTickets.map((t) => ({
      ticket_id: t.ticket_id,
      created_at: t.created_at,
      channel: t.channel,
      client_name: t.client_name,
      client_tier: t.client_tier,
      category: t.category,
      priority: t.priority,
      description: t.description,
      assigned_agent: t.assigned_agent,
      escalated_to_eng: t.escalated_to_eng,
      status: t.isResolvedLive ? 'Resolved at L1' : t.status,
      res_hours: t.res_hrs
    }));
    const csv = Papa.unparse(rows);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `RideOps_Triage_${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast('Queue Exported', `Downloaded ${rows.length} tickets as CSV.`);
  };

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement?.tagName)) return;
      if (e.key === 'ArrowDown' || e.key === 'j') {
        e.preventDefault();
        nextTicket();
      } else if (e.key === 'ArrowUp' || e.key === 'k') {
        e.preventDefault();
        prevTicket();
      } else if (e.key === 'ArrowRight' && activeTab === 'deck') {
        setCurrentSlide((s) => Math.min(totalSlides, s + 1));
      } else if (e.key === 'ArrowLeft' && activeTab === 'deck') {
        setCurrentSlide((s) => Math.max(1, s - 1));
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  });

  return (
    <TicketContext.Provider
      value={{
        activeTab,
        setActiveTab,
        tickets,
        filteredTickets,
        selectedTicket,
        selectedTicketId,
        setSelectedTicketId,
        deflectedCount,
        openBacklogCount,
        isBacklogFiltered,
        toggleBacklogFilter,
        filterToBacklogOnly,
        isCustomDataset,
        activeDatasetName,
        resetToDefault,
        handleFileUpload,
        resolveTicketLive,
        nextTicket,
        prevTicket,
        exportQueueCsv,
        searchQuery,
        setSearchQuery,
        filterCategory,
        setFilterCategory,
        filterPriority,
        setFilterPriority,
        filterRisk,
        setFilterRisk,
        filterAgent,
        setFilterAgent,
        checklist,
        setChecklist,
        currentSlide,
        setCurrentSlide,
        totalSlides,
        toast,
        showToast
      }}
    >
      {children}
    </TicketContext.Provider>
  );
}

export function useTickets() {
  const context = useContext(TicketContext);
  if (!context) throw new Error('useTickets must be used within a TicketProvider');
  return context;
}
