import React, { useEffect, useMemo, useState } from "react";
import { Routes, Route, Link } from "react-router-dom";
import FeedPage from "./pages/FeedPage.jsx";
import AdminPage from "./admin/AdminPage.jsx";
import { languages } from "./i18n.js";

const DEFAULT_LANG = "ua";

export default function App() {
  const [lang, setLang] = useState(DEFAULT_LANG);
  const t = useMemo(() => languages[lang], [lang]);

  useEffect(() => {
    const initData = window.Telegram?.WebApp?.initData || "";
    if (!initData) return;
    fetch(`${import.meta.env.VITE_API_BASE || "http://localhost:8000"}/api/auth/telegram`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ init_data: initData })
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.access_token) {
          localStorage.setItem("access_token", data.access_token);
          localStorage.setItem("refresh_token", data.refresh_token);
        }
      })
      .catch(() => {});
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <div className="logo">Telegram Social Platform</div>
        <nav className="nav-links">
          <Link to="/">{t.feed}</Link>
          <Link to="/admin">{t.admin}</Link>
        </nav>
        <select value={lang} onChange={(e) => setLang(e.target.value)}>
          {Object.entries(languages).map(([key, value]) => (
            <option key={key} value={key}>
              {value.label}
            </option>
          ))}
        </select>
      </header>
      <Routes>
        <Route path="/" element={<FeedPage t={t} />} />
        <Route path="/admin" element={<AdminPage t={t} />} />
      </Routes>
      <footer className="app-footer">
        <a href={import.meta.env.VITE_SUPPORT_URL || "https://t.me/support"} target="_blank">
          {t.support}
        </a>
        <a href={import.meta.env.VITE_PRIVACY_URL || "https://example.com/privacy"} target="_blank">
          {t.privacy}
        </a>
        <a href={import.meta.env.VITE_TERMS_URL || "https://example.com/terms"} target="_blank">
          {t.terms}
        </a>
        <a href={import.meta.env.VITE_ADULT_URL || "https://example.com/18plus"} target="_blank">
          {t.adult}
        </a>
      </footer>
    </div>
  );
}
