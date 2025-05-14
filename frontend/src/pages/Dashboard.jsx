import { useState, useEffect } from "react";
import axios from "../api/axiosInstance";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";

function Dashboard() {
  const [entries, setEntries] = useState([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [editId, setEditId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
    } else {
      axios.get("/journal")
        .then(res => setEntries(res.data))
        .catch(err => console.error("Error fetching journals", err));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (isEditing) {
      axios.put(`/journal/${editId}`, { title, content })
        .then((res) => {
          setEntries(entries.map(entry => entry.id === editId ? res.data : entry));
          resetForm();
        });
    } else {
      axios.post("/journal", { title, content })
        .then((res) => {
          setEntries([...entries, res.data]);
          resetForm();
        });
    }
  };

  const handleDelete = (id) => {
    axios.delete(`/journal/${id}`)
      .then(() => {
        setEntries(entries.filter(entry => entry.id !== id));
      });
  };

  const handleEdit = (entry) => {
    setTitle(entry.title);
    setContent(entry.content);
    setIsEditing(true);
    setEditId(entry.id);
  };

  const resetForm = () => {
    setTitle("");
    setContent("");
    setIsEditing(false);
    setEditId(null);
  };

  return (
    <div className="container">
      <h2>Journal Dashboard</h2>
      <button onClick={handleLogout}>Logout</button>

      <form onSubmit={handleSubmit}>
        <input
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <textarea
          placeholder="Content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
        />
        <button type="submit">{isEditing ? "Update Entry" : "Add Entry"}</button>
        {isEditing && <button type="button" onClick={resetForm}>Cancel</button>}
      </form>

      <ul>
        {entries.map(entry => (
          <li key={entry.id}>
            <strong>{entry.title}</strong>: {entry.content}
            <div>
              <button onClick={() => handleEdit(entry)}>Edit</button>
              <button onClick={() => handleDelete(entry.id)}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
