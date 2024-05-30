import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import Note from "../components/Note";
import "../styles/Home.css";
import { ACCESS_TOKEN } from "../constants";
import {jwtDecode} from "jwt-decode";

function Home() {
  const [notes, setNotes] = useState([]);
  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");
  const navigate = useNavigate();
  const [username, setUsername] = useState("");

  useEffect(() => {
    getNotes();
    getUsername();
  }, []);

  const getUsername = () => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      const decodedToken = jwtDecode(token); 
      setUsername(decodedToken.user_id);      //TODO after token fixed with username data, change to: setUsername(decodedToken.username);
    }
  };

  const getNotes = () => {
    api.get("/api/notes/")
      .then((res) => res.data)
      .then((data) => setNotes(data))
      .catch((err) => alert(err));
  };

  const deleteNote = (id) => {
    api.delete(`api/notes/delete/${id}/`)
      .then((res) => {
        if (res.status === 204) alert("Note deleted!");
        else alert("Failed to delete note!");
        getNotes();
      }).catch((error) => alert(error));
  };

  const createNote = (e) => {
    e.preventDefault();
    api.post("/api/notes/", { content, title })
      .then((res) => {
        if (res.status === 201) {
          alert("Note Created!");
          setTitle("");
          setContent("");
        } else {
          alert("Failed to create note!");
        }
        getNotes();
      })
      .catch((error) => alert(error));
  };

  const logout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <div>
      <div className="header">
        <h2>Notes of user id ({username})</h2>
        <button className="logout-button" onClick={logout}>Logout</button>
      </div>
      {notes.map((note) => (
        <Note note={note} onDelete={deleteNote} key={note.id} />
      ))}
      <h2>Create a note</h2>
      <form onSubmit={createNote}>
        <label htmlFor="title">Title:</label>
        <br />
        <input type="text" id="title" name="title" required onChange={(e) => setTitle(e.target.value)} value={title} />
        <label htmlFor="content">Content:</label>
        <br />
        <textarea id="content" name="content" required value={content} onChange={(e) => setContent(e.target.value)}></textarea>
        <br />
        <input type="submit" value="Submit"></input>
      </form>
    </div>
  );
}

export default Home;
