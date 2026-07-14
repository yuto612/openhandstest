from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)
DB_NAME = "notes.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # 既存テーブル確認とマイグレーション
    c.execute("PRAGMA table_info(notes)")
    columns = [row[1] for row in c.fetchall()]
    if 'created_at' not in columns:
        c.execute('ALTER TABLE notes ADD COLUMN created_at DATETIME')
        c.execute('UPDATE notes SET created_at = ?', (datetime.datetime.now(),))
    
    c.execute('''CREATE TABLE IF NOT EXISTS tags 
                 (id INTEGER PRIMARY KEY, name TEXT UNIQUE, color TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS note_tags 
                 (note_id INTEGER, tag_id INTEGER, 
                  FOREIGN KEY(note_id) REFERENCES notes(id), 
                  FOREIGN KEY(tag_id) REFERENCES tags(id))''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    search = request.args.get('search', '')
    tag_filter = request.args.get('tag', '')
    sort = request.args.get('sort', 'desc')
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    query = """
        SELECT DISTINCT n.id, n.content, n.created_at 
        FROM notes n
        LEFT JOIN note_tags nt ON n.id = nt.note_id
        LEFT JOIN tags t ON nt.tag_id = t.id
        WHERE 1=1
    """
    params = []
    
    if search:
        query += " AND n.content LIKE ?"
        params.append(f"%{search}%")
    if tag_filter:
        query += " AND t.name = ?"
        params.append(tag_filter)
        
    query += f" ORDER BY n.created_at {'DESC' if sort == 'desc' else 'ASC'}"
    
    c.execute(query, params)
    notes = c.fetchall()
    
    # 各ノートのタグを取得
    notes_with_tags = []
    for note in notes:
        c.execute('SELECT t.name, t.color FROM tags t JOIN note_tags nt ON t.id = nt.tag_id WHERE nt.note_id = ?', (note[0],))
        tags = c.fetchall()
        notes_with_tags.append({'id': note[0], 'content': note[1], 'created_at': note[2], 'tags': tags})
        
    c.execute('SELECT name FROM tags')
    all_tags = [row[0] for row in c.fetchall()]
    
    conn.close()
    return render_template('index.html', notes=notes_with_tags, all_tags=all_tags, search=search, tag_filter=tag_filter, sort=sort)

@app.route('/add', methods=['POST'])
def add():
    content = request.form.get('content')
    tags_str = request.form.get('tags', '') # カンマ区切り
    if content:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('INSERT INTO notes (content, created_at) VALUES (?, ?)', (content, datetime.datetime.now()))
        note_id = c.lastrowid
        
        if tags_str:
            for tag_name in tags_str.split(','):
                tag_name = tag_name.strip()
                if not tag_name: continue
                c.execute('INSERT OR IGNORE INTO tags (name, color) VALUES (?, ?)', (tag_name, 'bg-blue-200'))
                c.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
                tag_id = c.fetchone()[0]
                c.execute('INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)', (note_id, tag_id))
                
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM note_tags WHERE note_id = ?', (id,))
    c.execute('DELETE FROM notes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True, port=8011)
