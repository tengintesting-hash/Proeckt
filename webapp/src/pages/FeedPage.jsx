import React, { useEffect, useState } from "react";
import { apiFetch } from "../api.js";

const FEEDS = ["recommended", "popular", "new"];

export default function FeedPage({ t }) {
  const [feedType, setFeedType] = useState("recommended");
  const [posts, setPosts] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    apiFetch(`/api/feed/${feedType}?limit=20&offset=0`)
      .then((data) => {
        if (active) setPosts(data);
      })
      .catch((err) => {
        if (active) setError(err.message);
      });
    return () => {
      active = false;
    };
  }, [feedType]);

  return (
    <section className="feed">
      <div className="feed-controls">
        {FEEDS.map((type) => (
          <button key={type} onClick={() => setFeedType(type)} className={type === feedType ? "active" : ""}>
            {type === "recommended" ? t.recommended : type === "popular" ? t.popular : t.latest}
          </button>
        ))}
      </div>
      {error && <div className="error">{error}</div>}
      <div className="feed-list">
        {posts.map((post) => (
          <article key={post.id} className="post-card">
            <div className="post-header">
              <div className="channel">Channel #{post.channel_id}</div>
              <span className={`status ${post.status}`}>{post.status}</span>
            </div>
            <p>{post.text}</p>
            {post.media_url && (
              <div className="media">
                {post.media_type?.startsWith("video") ? (
                  <video controls src={`${import.meta.env.VITE_MEDIA_BASE || ""}${post.media_url}`} />
                ) : (
                  <img src={`${import.meta.env.VITE_MEDIA_BASE || ""}${post.media_url}`} alt="media" />
                )}
              </div>
            )}
            <div className="actions">
              <span>👍 {post.likes_count}</span>
              <span>👎 {post.dislikes_count}</span>
              <span>💬 {post.comments_count}</span>
              <span>🔁 {post.reposts_count}</span>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
