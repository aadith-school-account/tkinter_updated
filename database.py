import sqlite3

# Initialize database
def setup_db():
    conn = sqlite3.connect("scores.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        player TEXT PRIMARY KEY,
        wins INTEGER
    )
    """)
    conn.commit()
    conn.close()

# Function to update wins
def update_score(player):
    conn = sqlite3.connect("scores.db")
    cursor = conn.cursor()

    cursor.execute("SELECT wins FROM scores WHERE player=?", (player,))
    result = cursor.fetchone()

    if result:
        cursor.execute("UPDATE scores SET wins = wins + 1 WHERE player=?", (player,))
    else:
        cursor.execute("INSERT INTO scores (player, wins) VALUES (?, 1)", (player,))

    conn.commit()  # ✅ Forces data to be saved
    conn.close()

    print(f"DEBUG: Score updated for {player}")  # ✅ Debug message to confirm execution

# Function to retrieve scores
def get_scores():
    conn = sqlite3.connect("scores.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scores ORDER BY wins DESC")
    scores = cursor.fetchall()
    
    conn.close()

    print("DEBUG - Retrieved Scores:", scores)  # ✅ This will print scores to help you debug!
    return scores


def clear_scores():
    conn = sqlite3.connect("scores.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scores")
    conn.commit()
    conn.close()
    print("DEBUG: All scores cleared")


