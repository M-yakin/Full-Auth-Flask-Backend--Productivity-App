import React, { useEffect, useState } from "react";
import NavBar from "./NavBar";
import LoginForm from "./LoginForm";
import SignUpForm from "./SignUpForm";

function App() {
  const [user, setUser] = useState(null);
  const [workouts, setWorkouts] = useState([]);
  const [showLogin, setShowLogin] = useState(true);

  // Form states
 const [exercise, setExercise] = useState("");
 const [duration, setDuration] = useState("");
 const [notes, setNotes] = useState("");

  useEffect(() => {
    fetch("/me").then((response) => {
      if (response.ok) {
        response.json().then((user) => {
          setUser(user);
          fetchWorkouts();
        });
      }
    });
  }, []);

  const fetchWorkouts = () => {
    fetch("/workouts")
      .then((r) => {
        if (r.ok) return r.json();
      })
      .then((data) => {
        if (data) setWorkouts(data);
      });
  };

  const handleAddWorkout = (e) => {
    e.preventDefault();
    fetch("/workouts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        exercise,
        duration_minutes: parseInt(duration),
        notes,
      }),
    })
      .then((r) => {
        if (r.ok) return r.json();
        throw new Error("Failed to add workout");
      })
      .then((newWorkout) => {
        setWorkouts([newWorkout, ...workouts]);
        setExercise("");
        setDuration("");
        setNotes("");
      });
  };
  
  const handleDeleteWorkout = (id) => {
    fetch(`/workouts/${id}`, { method: "DELETE" }).then((r) => {
      if (r.ok) {
        setWorkouts(workouts.filter((w) => w.id !== id));
      }
    });
  };

  if (!user) {
    return (
      <>
        <NavBar user={user} setUser={setUser} />
        <div style={{ padding: "20px", maxWidth: "400px", margin: "auto" }}>
          {showLogin ? (
            <>
              <LoginForm onLogin={setUser} />
              <p style={{ marginTop: "15px" }}>
                Don't have an account?{" "}
                <button onClick={() => setShowLogin(false)}>Sign Up</button>
              </p>
            </>
          ) : (
            <>
              <SignUpForm onLogin={setUser} />
              <p style={{ marginTop: "15px" }}>
                Already have an account?{" "}
                <button onClick={() => setShowLogin(true)}>Log In</button>
              </p>
            </>
          )}
        </div>
      </>
    );
  }

  return (
    <>
      <NavBar user={user} setUser={setUser} />
      <div style={{ padding: "20px", maxWidth: "800px", margin: "auto" }}>
        <h2>Welcome back, {user.username}!</h2>

        <section style={{ background: "#f9f9f9", padding: "15px", borderRadius: "8px", marginBottom: "30px" }}>
          <h3>Log a New Workout</h3>
          <form onSubmit={handleAddWorkout} style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            <input
              type="text"
              placeholder="Exercise (e.g. Bench Press, Running)"
              value={exercise}
              onChange={(e) => setExercise(e.target.value)}
              required
              style={{ padding: "8px" }}
            />
            <input
              type="number"
              placeholder="Duration (minutes)"
              value={duration}
              onChange={(e) => setDuration(e.target.value)}
              required
              style={{ padding: "8px" }}
            />
            <textarea
              placeholder="Notes / Sets / Reps"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              style={{ padding: "8px", height: "60px" }}
            />
            <button type="submit" style={{ padding: "10px", background: "#8a2be2", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}>
              Add Workout
            </button>
          </form>
        </section>

        <section>
          <h3>🏋️ Your Workouts</h3>
          {workouts.length === 0 ? (
            <p>No workouts recorded yet. Get moving!</p>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
              {workouts.map((w) => (
                <div key={w.id} style={{ border: "1px solid #ddd", borderRadius: "6px", padding: "15px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div>
                    <h4 style={{ margin: "0 0 5px 0" }}>{w.exercise}</h4>
                    <p style={{ margin: "0 0 5px 0", color: "#666" }}>
                      ⏱️ {w.duration_minutes} mins | 📅 {w.date}
                    </p>
                    {w.notes && <p style={{ margin: 0, fontStyle: "italic" }}>"{w.notes}"</p>}
                  </div>
                  <button
                    onClick={() => handleDeleteWorkout(w.id)}
                    style={{ background: "#ff4d4d", color: "white", border: "none", padding: "6px 12px", borderRadius: "4px", cursor: "pointer" }}
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </>
  );
}

export default App;
    
      