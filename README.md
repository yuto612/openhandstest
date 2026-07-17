# openhandstest

このリポジトリには以下のプロジェクトが含まれています。

1. Pythonでの簡単なFizzBuzzの実装。
2. Pythonでの簡単なTODO CLIツール。
3. 簡単なFlaskメモWebアプリ。

## 実行方法

### FizzBuzz
```bash
python3 fizzbuzz.py
```

### TODO CLI
```bash
# タスクの追加
python3 todo.py add "タスク名"

# タスクの一覧表示
python3 todo.py list

# タスクの削除
python3 todo.py remove "タスク名"
```

### テスト
TODO CLIツールのテストを実行するには:
```bash
pytest test_todo.py
```

### Flask メモアプリ
```bash
python3 app.py
```
その後、 http://localhost:8011/ にアクセスしてください。
- タグ付け、検索、フィルタリング、並べ替え機能が含まれています。