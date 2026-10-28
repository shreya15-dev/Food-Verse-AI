import React, { useState, useEffect } from "react";
import { History, Search, Trash2, Eye, Sparkles, Filter, AlertCircle, RefreshCw } from "lucide-react";
import Modal from "../components/Modal";
import NutritionCard from "../components/NutritionCard";
import FreshnessMeter from "../components/FreshnessMeter";
import HygieneAuditCard from "../components/HygieneAuditCard";
import { getHistory, deleteHistoryItem, clearAllHistory } from "../services/api";
import { useToast } from "../components/Toast";

export default function HistoryPage() {
  const [historyList, setHistoryList] = useState([]);
  const [filterType, setFilterType] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showClearConfirm, setShowClearConfirm] = useState(false);
  const { addToast } = useToast();

  const fetchHistory = async () => {
    setIsLoading(true);
    const res = await getHistory(100, filterType || null);
    setIsLoading(false);
    if (res?.success) {
      setHistoryList(res.data);
    } else {
      addToast("Failed to fetch analysis history.", "error");
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [filterType]);

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm("Are you sure you want to delete this scan record?")) return;

    const res = await deleteHistoryItem(id);
    if (res?.success) {
      setHistoryList((prev) => prev.filter((item) => item.id !== id));
      addToast("Record deleted from history.", "success");
      if (selectedRecord?.id === id) setSelectedRecord(null);
    } else {
      addToast(res.error || "Failed to delete record.", "error");
    }
  };

  const handleClearAll = async () => {
    setShowClearConfirm(false);
    const res = await clearAllHistory();
    if (res?.success) {
      setHistoryList([]);
      addToast(res.message || "History cleared successfully.", "success");
    } else {
      addToast(res.error || "Failed to clear history.", "error");
    }
  };

  const filteredItems = historyList.filter((item) => {
    const matchesSearch =
      (item.title || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
      (item.summary || "").toLowerCase().includes(searchQuery.toLowerCase());
    return matchesSearch;
  });

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">
            <History size={28} color="var(--brand-primary)" />
            Analysis Scan History
          </h1>
          <p className="page-description">
            Audit logs and previous scanner results stored locally in your SQLite database.
            Search, filter, inspect past findings, or clear stored records.
          </p>
        </div>

        {historyList.length > 0 && (
          <button
            onClick={() => setShowClearConfirm(true)}
            className="btn btn-danger"
            style={{ padding: "8px 16px", fontSize: "0.85rem" }}
          >
            <Trash2 size={15} /> Clear All History
          </button>
        )}
      </div>

      {/* Filter and Search Bar */}
      <div className="card" style={{ padding: "16px 20px", display: "flex", flexWrap: "wrap", gap: "12px", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "8px", flex: 1, minWidth: "240px" }}>
          <Search size={18} color="var(--text-muted)" />
          <input
            type="text"
            placeholder="Search scans by dish name or findings..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{ width: "100%", border: "none", backgroundColor: "transparent", padding: "6px" }}
          />
        </div>

        <div style={{ display: "flex", gap: "8px", alignItems: "center", flexWrap: "wrap" }}>
          <Filter size={16} color="var(--text-muted)" />
          <button
            onClick={() => setFilterType("")}
            className={`badge ${filterType === "" ? "badge-success" : "badge-neutral"}`}
            style={{ cursor: "pointer", padding: "6px 12px" }}
          >
            All Modules
          </button>
          <button
            onClick={() => setFilterType("food")}
            className={`badge ${filterType === "food" ? "badge-success" : "badge-neutral"}`}
            style={{ cursor: "pointer", padding: "6px 12px" }}
          >
            Food Recognition
          </button>
          <button
            onClick={() => setFilterType("freshness")}
            className={`badge ${filterType === "freshness" ? "badge-success" : "badge-neutral"}`}
            style={{ cursor: "pointer", padding: "6px 12px" }}
          >
            Freshness Check
          </button>
          <button
            onClick={() => setFilterType("hygiene")}
            className={`badge ${filterType === "hygiene" ? "badge-success" : "badge-neutral"}`}
            style={{ cursor: "pointer", padding: "6px 12px" }}
          >
            Hygiene Audits
          </button>
          <button
            onClick={fetchHistory}
            className="btn btn-outline"
            style={{ padding: "6px 10px" }}
            title="Refresh history"
          >
            <RefreshCw size={14} />
          </button>
        </div>
      </div>

      {/* History Items List */}
      <div className="card" style={{ padding: "20px" }}>
        {isLoading ? (
          <div style={{ textAlign: "center", padding: "32px", color: "var(--text-muted)" }}>
            Loading past records from SQLite...
          </div>
        ) : filteredItems.length === 0 ? (
          <div style={{ textAlign: "center", padding: "40px 20px", color: "var(--text-muted)" }}>
            <p style={{ fontSize: "1rem", fontWeight: 600 }}>No history records found.</p>
            <p style={{ fontSize: "0.85rem", marginTop: "6px" }}>
              Run a scan in Food Recognition, Freshness, or Hygiene to generate records.
            </p>
          </div>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
            {filteredItems.map((item) => (
              <div
                key={item.id}
                onClick={() => setSelectedRecord(item)}
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  padding: "16px 18px",
                  borderRadius: "var(--radius-md)",
                  backgroundColor: "var(--bg-card-subtle)",
                  border: "1px solid var(--border-color)",
                  cursor: "pointer",
                  transition: "var(--transition)",
                  flexWrap: "wrap",
                  gap: "12px"
                }}
              >
                <div style={{ display: "flex", flexDirection: "column", gap: "4px", flex: 1, minWidth: "260px" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px", flexWrap: "wrap" }}>
                    <span className="badge badge-neutral" style={{ textTransform: "capitalize" }}>
                      {item.module_type}
                    </span>
                    <strong style={{ fontSize: "0.98rem", color: "var(--text-primary)" }}>
                      {item.title}
                    </strong>
                    {item.is_demo && (
                      <span className="badge badge-demo" style={{ fontSize: "0.68rem" }}>
                        <Sparkles size={10} /> Demo Simulation
                      </span>
                    )}
                  </div>
                  <p style={{ fontSize: "0.84rem", color: "var(--text-secondary)" }}>
                    {item.summary}
                  </p>
                </div>

                <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                  <span style={{ fontSize: "0.78rem", color: "var(--text-muted)" }}>
                    {new Date(item.created_at).toLocaleDateString()} {new Date(item.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                  </span>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedRecord(item);
                    }}
                    className="btn btn-outline"
                    style={{ padding: "6px 10px", fontSize: "0.8rem" }}
                    title="View details"
                  >
                    <Eye size={14} /> View
                  </button>

                  <button
                    onClick={(e) => handleDelete(item.id, e)}
                    className="btn btn-danger"
                    style={{ padding: "6px 10px", fontSize: "0.8rem" }}
                    title="Delete record"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Record Detail Modal */}
      <Modal
        isOpen={!!selectedRecord}
        onClose={() => setSelectedRecord(null)}
        title={selectedRecord?.title || "Scan Details"}
        maxWidth="750px"
      >
        {selectedRecord && (
          <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            {selectedRecord.module_type === "food" && (
              <NutritionCard data={selectedRecord.data} />
            )}
            {selectedRecord.module_type === "freshness" && (
              <FreshnessMeter data={selectedRecord.data} />
            )}
            {selectedRecord.module_type === "hygiene" && (
              <HygieneAuditCard data={selectedRecord.data} />
            )}
          </div>
        )}
      </Modal>

      {/* Clear Confirmation Modal */}
      <Modal
        isOpen={showClearConfirm}
        onClose={() => setShowClearConfirm(false)}
        title="Confirm Clear History"
        maxWidth="440px"
      >
        <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
          <p style={{ fontSize: "0.92rem", color: "var(--text-secondary)" }}>
            Are you sure you want to permanently clear all {historyList.length} analysis records from your SQLite database?
            This action cannot be undone.
          </p>
          <div style={{ display: "flex", justifyContent: "flex-end", gap: "10px", marginTop: "8px" }}>
            <button onClick={() => setShowClearConfirm(false)} className="btn btn-outline">
              Cancel
            </button>
            <button onClick={handleClearAll} className="btn btn-danger">
              Yes, Clear All
            </button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
