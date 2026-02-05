import React, { useEffect, useState } from "react";
import { apiFetch } from "../api.js";

export default function AdminPage({ t }) {
  const [pending, setPending] = useState([]);
  const [thresholds, setThresholds] = useState({
    text_threshold: 0.6,
    media_threshold: 0.6,
    uniqueness_threshold: 0.7
  });
  const [message, setMessage] = useState("");

  useEffect(() => {
    apiFetch("/api/admin/posts/pending")
      .then(setPending)
      .catch(() => setPending([]));
    apiFetch("/api/admin/ai-thresholds")
      .then(setThresholds)
      .catch(() => {});
  }, []);

  const updateThresholds = async () => {
    const updated = await apiFetch("/api/admin/ai-thresholds", {
      method: "POST",
      body: JSON.stringify(thresholds)
    });
    setThresholds(updated);
    setMessage("Thresholds saved");
  };

  return (
    <section className="admin">
      <h2>{t.admin}</h2>
      <div className="admin-block">
        <h3>AI Thresholds</h3>
        <label>
          Text
          <input
            type="number"
            step="0.1"
            value={thresholds.text_threshold}
            onChange={(e) => setThresholds({ ...thresholds, text_threshold: Number(e.target.value) })}
          />
        </label>
        <label>
          Media
          <input
            type="number"
            step="0.1"
            value={thresholds.media_threshold}
            onChange={(e) => setThresholds({ ...thresholds, media_threshold: Number(e.target.value) })}
          />
        </label>
        <label>
          Uniqueness
          <input
            type="number"
            step="0.1"
            value={thresholds.uniqueness_threshold}
            onChange={(e) => setThresholds({ ...thresholds, uniqueness_threshold: Number(e.target.value) })}
          />
        </label>
        <button onClick={updateThresholds}>Save</button>
        {message && <div className="success">{message}</div>}
      </div>
      <div className="admin-block">
        <h3>Pending Reviews</h3>
        {pending.length === 0 && <p>No pending posts.</p>}
        <ul>
          {pending.map((id) => (
            <li key={id}>Post #{id}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}
