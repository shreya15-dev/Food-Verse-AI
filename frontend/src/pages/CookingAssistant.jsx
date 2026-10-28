import React, { useState, useRef, useEffect } from "react";
import {
  ChefHat,
  Send,
  Plus,
  X,
  Sparkles,
  RotateCcw,
  Clock,
  Utensils,
  Copy,
  Printer,
  Check,
  Loader2
} from "lucide-react";
import { askCookingAssistant } from "../services/api";
import { useToast } from "../components/Toast";

export default function CookingAssistant() {
  const [messages, setMessages] = useState([
    {
      id: "welcome",
      role: "assistant",
      text: "👋 Hello! I am your **Food Verse Smart Cooking Assistant**. Tell me what ingredients you have in your fridge or pantry, any dietary goals, or how much time you have. I'll craft delicious, step-by-step recipes with smart ingredient substitutions!",
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    }
  ]);
  const [inputText, setInputText] = useState("");
  const [ingredients, setIngredients] = useState(["Eggs", "Tomatoes", "Garlic"]);
  const [newIngredient, setNewIngredient] = useState("");
  const [cuisine, setCuisine] = useState("");
  const [maxTime, setMaxTime] = useState("");
  const [dietary, setDietary] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [copiedId, setCopiedId] = useState(null);

  const messagesEndRef = useRef(null);
  const { addToast } = useToast();

  const dietaryOptions = ["Vegetarian", "Vegan", "High-Protein", "Gluten-Free", "Dairy-Free", "Keto"];
  const quickPrompts = [
    "Quick 15-min dinner with eggs and veggies",
    "High-protein vegetarian lunch under 30 mins",
    "Cozy comforting stew with canned beans and spinach",
    "Healthy low-carb stir fry with crispy tofu"
  ];

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleAddIngredient = (e) => {
    e.preventDefault();
    const clean = newIngredient.trim();
    if (clean && !ingredients.map((i) => i.toLowerCase()).includes(clean.toLowerCase())) {
      setIngredients([...ingredients, clean]);
      setNewIngredient("");
    }
  };

  const handleRemoveIngredient = (item) => {
    setIngredients(ingredients.filter((i) => i !== item));
  };

  const toggleDietary = (item) => {
    if (dietary.includes(item)) {
      setDietary(dietary.filter((d) => d !== item));
    } else {
      setDietary([...dietary, item]);
    }
  };

  const handleSendMessage = async (textToSend = null) => {
    const prompt = (textToSend || inputText).trim();
    if (!prompt && ingredients.length === 0) {
      addToast("Please enter a question or add some pantry ingredients.", "info");
      return;
    }

    const userMsg = {
      id: Date.now().toString(),
      role: "user",
      text: prompt || `Find me a recipe using: ${ingredients.join(", ")}`,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputText("");
    setIsLoading(true);

    const payload = {
      prompt: userMsg.text,
      ingredients,
      cuisine: cuisine || undefined,
      max_time_min: maxTime ? parseInt(maxTime) : undefined,
      dietary_restrictions: dietary,
      conversation_history: messages.slice(-4)
    };

    const res = await askCookingAssistant(payload);
    setIsLoading(false);

    if (res.success && res.data) {
      const assistantMsg = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        text: res.data.reply_text,
        is_demo: res.data.is_demo,
        provider: res.data.provider,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } else {
      addToast(res.error || "Failed to generate recipe.", "error");
    }
  };

  const handleCopy = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    addToast("Recipe copied to clipboard!", "success");
    setTimeout(() => setCopiedId(null), 2500);
  };

  const handleReset = () => {
    setMessages([
      {
        id: "welcome",
        role: "assistant",
        text: "👋 Chat reset. Let's make something delicious! What ingredients are you working with today?",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
      }
    ]);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
      <div className="page-header" style={{ marginBottom: "12px" }}>
        <div>
          <h1 className="page-title">
            <ChefHat size={28} color="var(--brand-primary)" />
            Smart Cooking Assistant
          </h1>
          <p className="page-description">
            Your conversational culinary partner. Enter ingredients available in your pantry, configure dietary
            filters, and generate tested recipes complete with step-by-step instructions and smart substitutions.
          </p>
        </div>
      </div>

      {/* Pantry & Filter Bar */}
      <div className="card" style={{ padding: "18px 22px", display: "flex", flexDirection: "column", gap: "14px" }}>
        {/* Ingredients Tags */}
        <div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
            <span style={{ fontSize: "0.85rem", fontWeight: 700, color: "var(--text-primary)" }}>
              My Pantry Ingredients:
            </span>
            <span style={{ fontSize: "0.78rem", color: "var(--text-muted)" }}>
              {ingredients.length} items active
            </span>
          </div>

          <div style={{ display: "flex", flexWrap: "wrap", gap: "8px", alignItems: "center" }}>
            {ingredients.map((ing) => (
              <span
                key={ing}
                className="badge"
                style={{
                  backgroundColor: "var(--brand-light)",
                  color: "var(--brand-primary)",
                  padding: "6px 10px",
                  fontSize: "0.84rem"
                }}
              >
                {ing}
                <X
                  size={14}
                  style={{ cursor: "pointer", marginLeft: "4px" }}
                  onClick={() => handleRemoveIngredient(ing)}
                />
              </span>
            ))}

            <form onSubmit={handleAddIngredient} style={{ display: "inline-flex", gap: "6px" }}>
              <input
                type="text"
                placeholder="+ Add ingredient..."
                value={newIngredient}
                onChange={(e) => setNewIngredient(e.target.value)}
                style={{ padding: "4px 10px", fontSize: "0.82rem", width: "140px" }}
              />
              <button type="submit" className="btn btn-outline" style={{ padding: "4px 8px" }}>
                <Plus size={14} />
              </button>
            </form>
          </div>
        </div>

        {/* Filters row: Cuisine, Max Time, Dietary */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: "12px", alignItems: "center", paddingTop: "10px", borderTop: "1px solid var(--border-color)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <span style={{ fontSize: "0.8rem", fontWeight: 600, color: "var(--text-muted)" }}>Cuisine:</span>
            <select
              value={cuisine}
              onChange={(e) => setCuisine(e.target.value)}
              style={{ padding: "6px 10px", fontSize: "0.82rem" }}
            >
              <option value="">Any Cuisine</option>
              <option value="Mediterranean">Mediterranean</option>
              <option value="Italian">Italian</option>
              <option value="Asian">Asian</option>
              <option value="Indian">Indian</option>
              <option value="American">American</option>
            </select>
          </div>

          <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <Clock size={15} color="var(--text-muted)" />
            <select
              value={maxTime}
              onChange={(e) => setMaxTime(e.target.value)}
              style={{ padding: "6px 10px", fontSize: "0.82rem" }}
            >
              <option value="">Any Time</option>
              <option value="15">&le; 15 mins</option>
              <option value="30">&le; 30 mins</option>
              <option value="45">&le; 45 mins</option>
            </select>
          </div>

          <div style={{ display: "flex", gap: "6px", flexWrap: "wrap", marginLeft: "auto" }}>
            {dietaryOptions.map((opt) => {
              const active = dietary.includes(opt);
              return (
                <button
                  key={opt}
                  type="button"
                  onClick={() => toggleDietary(opt)}
                  className={`badge ${active ? "badge-success" : "badge-neutral"}`}
                  style={{ cursor: "pointer", padding: "5px 10px" }}
                >
                  {opt}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Chat Messages Feed */}
      <div
        className="card"
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "16px",
          minHeight: "420px",
          maxHeight: "620px",
          overflowY: "auto",
          padding: "24px"
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", paddingBottom: "10px", borderBottom: "1px solid var(--border-color)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <ChefHat size={18} color="var(--brand-primary)" />
            <span style={{ fontSize: "0.9rem", fontWeight: 700, color: "var(--text-primary)" }}>
              Cooking Conversation
            </span>
          </div>
          <button onClick={handleReset} className="btn btn-outline" style={{ padding: "4px 10px", fontSize: "0.78rem" }}>
            <RotateCcw size={13} /> Reset Chat
          </button>
        </div>

        {messages.map((msg) => {
          const isUser = msg.role === "user";
          return (
            <div
              key={msg.id}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: isUser ? "flex-end" : "flex-start",
                gap: "4px"
              }}
            >
              <div
                style={{
                  maxWidth: "85%",
                  padding: "14px 18px",
                  borderRadius: isUser ? "16px 16px 2px 16px" : "16px 16px 16px 2px",
                  backgroundColor: isUser ? "var(--brand-primary)" : "var(--bg-card-subtle)",
                  color: isUser ? "#FFFFFF" : "var(--text-primary)",
                  boxShadow: "var(--shadow-sm)",
                  fontSize: "0.92rem",
                  lineHeight: 1.55,
                  whiteSpace: "pre-wrap",
                  position: "relative"
                }}
              >
                {!isUser && msg.provider && (
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                    <span className="badge badge-demo" style={{ fontSize: "0.68rem" }}>
                      <Sparkles size={11} /> {msg.provider}
                    </span>
                    <button
                      onClick={() => handleCopy(msg.text, msg.id)}
                      className="btn btn-outline"
                      style={{ padding: "2px 8px", fontSize: "0.74rem" }}
                      title="Copy recipe"
                    >
                      {copiedId === msg.id ? <Check size={12} color="var(--status-success)" /> : <Copy size={12} />}
                      {copiedId === msg.id ? "Copied" : "Copy"}
                    </button>
                  </div>
                )}
                {msg.text}
              </div>
              <span style={{ fontSize: "0.72rem", color: "var(--text-muted)", padding: "0 6px" }}>
                {msg.timestamp}
              </span>
            </div>
          );
        })}

        {isLoading && (
          <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "var(--text-muted)", fontSize: "0.85rem", padding: "10px" }}>
            <Loader2 size={16} className="spin-icon" style={{ animation: "spin 1s linear infinite" }} />
            Chef AI is matching ingredients and crafting recipe...
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompts Bar */}
      <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", alignItems: "center" }}>
        <span style={{ fontSize: "0.78rem", fontWeight: 600, color: "var(--text-muted)" }}>
          Suggestions:
        </span>
        {quickPrompts.map((qp, idx) => (
          <button
            key={idx}
            onClick={() => handleSendMessage(qp)}
            className="badge badge-neutral"
            style={{ cursor: "pointer", padding: "6px 12px", border: "1px solid var(--border-color)" }}
          >
            {qp}
          </button>
        ))}
      </div>

      {/* Input Box */}
      <div style={{ display: "flex", gap: "10px" }}>
        <input
          type="text"
          placeholder="Ask for recipe ideas, cooking tips, substitutions, or side dish ideas..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleSendMessage();
          }}
          style={{ flex: 1, padding: "12px 18px", fontSize: "0.95rem" }}
          disabled={isLoading}
        />
        <button
          onClick={() => handleSendMessage()}
          className="btn btn-primary"
          style={{ padding: "0 24px" }}
          disabled={isLoading}
        >
          {isLoading ? <Loader2 size={18} style={{ animation: "spin 1s linear infinite" }} /> : <Send size={18} />}
          <span>Send</span>
        </button>
      </div>
    </div>
  );
}
