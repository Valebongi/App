"""
Database module for managing categories, goals, and progress tracking
"""
import sqlite3
from datetime import datetime, timedelta
import os


class Database:
    def __init__(self, db_name="daily_goals.db"):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.conn = None
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def init_db(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                color TEXT DEFAULT '#4CAF50',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Goals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                points_value INTEGER DEFAULT 10,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
            )
        ''')
        
        # Goal days table - associates goals with days of the week
        # day_of_week: 0=Monday, 1=Tuesday, ..., 6=Sunday
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goal_days (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_id INTEGER NOT NULL,
                day_of_week INTEGER NOT NULL,
                FOREIGN KEY (goal_id) REFERENCES goals (id) ON DELETE CASCADE,
                UNIQUE(goal_id, day_of_week)
            )
        ''')
        
        # Progress table - records daily progress
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_id INTEGER NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (goal_id) REFERENCES goals (id) ON DELETE CASCADE
            )
        ''')
        
        # Game state table - stores current streak and points
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                current_streak INTEGER DEFAULT 0,
                total_points INTEGER DEFAULT 0,
                last_activity TIMESTAMP,
                best_streak INTEGER DEFAULT 0,
                games_played INTEGER DEFAULT 0
            )
        ''')
        
        # Initialize game state if not exists
        cursor.execute('SELECT COUNT(*) FROM game_state')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO game_state (id, current_streak, total_points, last_activity, best_streak, games_played)
                VALUES (1, 0, 0, ?, 0, 0)
            ''', (datetime.now(),))
        
        conn.commit()
    
    # Category methods
    def add_category(self, name, color='#4CAF50'):
        """Add a new category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO categories (name, color) VALUES (?, ?)', (name, color))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def get_categories(self):
        """Get all categories"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM categories ORDER BY name')
        return cursor.fetchall()
    
    def delete_category(self, category_id):
        """Delete a category and all its goals"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
        conn.commit()
    
    # Goal methods
    def add_goal(self, category_id, name, description='', points_value=10, days_of_week=None):
        """Add a new goal to a category with optional days of week
        days_of_week: list of integers 0-6 (0=Monday, 6=Sunday)
        If None or empty, goal applies to all days
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO goals (category_id, name, description, points_value)
            VALUES (?, ?, ?, ?)
        ''', (category_id, name, description, points_value))
        goal_id = cursor.lastrowid
        
        # Add days of week
        if days_of_week:
            for day in days_of_week:
                cursor.execute('''
                    INSERT OR IGNORE INTO goal_days (goal_id, day_of_week)
                    VALUES (?, ?)
                ''', (goal_id, day))
        else:
            # If no days specified, add all days (0-6)
            for day in range(7):
                cursor.execute('''
                    INSERT OR IGNORE INTO goal_days (goal_id, day_of_week)
                    VALUES (?, ?)
                ''', (goal_id, day))
        
        conn.commit()
        return goal_id
    
    def get_goals(self, category_id=None):
        """Get all goals, optionally filtered by category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if category_id:
            cursor.execute('''
                SELECT g.*, c.name as category_name, c.color as category_color
                FROM goals g
                JOIN categories c ON g.category_id = c.id
                WHERE g.category_id = ?
                ORDER BY g.name
            ''', (category_id,))
        else:
            cursor.execute('''
                SELECT g.*, c.name as category_name, c.color as category_color
                FROM goals g
                JOIN categories c ON g.category_id = c.id
                ORDER BY c.name, g.name
            ''')
        return cursor.fetchall()
    
    def delete_goal(self, goal_id):
        """Delete a goal"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM goals WHERE id = ?', (goal_id,))
        conn.commit()
    
    def get_goals_for_day(self, day_of_week):
        """Get all goals for a specific day of week
        day_of_week: 0=Monday, 1=Tuesday, ..., 6=Sunday
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT g.*, c.name as category_name, c.color as category_color
            FROM goals g
            JOIN categories c ON g.category_id = c.id
            JOIN goal_days gd ON g.id = gd.goal_id
            WHERE gd.day_of_week = ?
            ORDER BY c.name, g.name
        ''', (day_of_week,))
        return cursor.fetchall()
    
    def get_goal_days(self, goal_id):
        """Get list of days (0-6) when a goal is active"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT day_of_week FROM goal_days
            WHERE goal_id = ?
            ORDER BY day_of_week
        ''', (goal_id,))
        return [row[0] for row in cursor.fetchall()]
    
    # Progress methods
    def add_progress(self, goal_id, notes=''):
        """Record progress for a goal"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO progress (goal_id, notes, completed_at)
            VALUES (?, ?, ?)
        ''', (goal_id, notes, datetime.now()))
        conn.commit()
        return cursor.lastrowid
    
    def get_today_progress(self):
        """Get all progress recorded today"""
        conn = self.get_connection()
        cursor = conn.cursor()
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cursor.execute('''
            SELECT p.*, g.name as goal_name, g.points_value, c.name as category_name
            FROM progress p
            JOIN goals g ON p.goal_id = g.id
            JOIN categories c ON g.category_id = c.id
            WHERE p.completed_at >= ?
            ORDER BY p.completed_at DESC
        ''', (today_start,))
        return cursor.fetchall()
    
    def get_goals_completed_today(self):
        """Get set of goal IDs completed today"""
        conn = self.get_connection()
        cursor = conn.cursor()
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cursor.execute('''
            SELECT DISTINCT goal_id
            FROM progress
            WHERE completed_at >= ?
        ''', (today_start,))
        return {row[0] for row in cursor.fetchall()}
    
    def get_goals_completed_on_date(self, date):
        """Get set of goal IDs completed on a specific date
        date: datetime object
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start.replace(hour=23, minute=59, second=59)
        cursor.execute('''
            SELECT DISTINCT goal_id
            FROM progress
            WHERE completed_at >= ? AND completed_at <= ?
        ''', (day_start, day_end))
        return {row[0] for row in cursor.fetchall()}
    
    def get_calendar_data(self, days=30):
        """Get calendar data for the last N days
        Returns list of dicts with date, goals_completed, goals_total, all_completed
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        calendar_data = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            day_of_week = date.weekday()
            
            # Get goals for that day of week
            goals_for_day = self.get_goals_for_day(day_of_week)
            total_goals = len(goals_for_day)
            
            # Get completed goals for that date
            completed_goals = self.get_goals_completed_on_date(date)
            completed_count = len(completed_goals)
            
            # Check if all goals were completed
            all_completed = total_goals > 0 and completed_count == total_goals
            
            calendar_data.append({
                'date': date,
                'day_of_week': day_of_week,
                'goals_total': total_goals,
                'goals_completed': completed_count,
                'all_completed': all_completed,
                'completion_rate': (completed_count / total_goals * 100) if total_goals > 0 else 0
            })
        
        return calendar_data
    
    def get_last_completion_time(self):
        """Get the timestamp of the last progress entry"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(completed_at) FROM progress')
        result = cursor.fetchone()[0]
        if result:
            return datetime.fromisoformat(result)
        return None
    
    # Game state methods
    def get_game_state(self):
        """Get current game state"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM game_state WHERE id = 1')
        return cursor.fetchone()
    
    def update_game_state(self, current_streak, total_points, last_activity=None):
        """Update game state"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if last_activity is None:
            last_activity = datetime.now()
        
        # Get current best streak
        cursor.execute('SELECT best_streak FROM game_state WHERE id = 1')
        best_streak = cursor.fetchone()[0]
        
        # Update best streak if current is higher
        new_best = max(best_streak, current_streak)
        
        cursor.execute('''
            UPDATE game_state
            SET current_streak = ?, total_points = ?, last_activity = ?, best_streak = ?
            WHERE id = 1
        ''', (current_streak, total_points, last_activity, new_best))
        conn.commit()
    
    def reset_game(self):
        """Reset the game (lose streak and points)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Increment games_played
        cursor.execute('''
            UPDATE game_state
            SET current_streak = 0, total_points = 0, last_activity = ?, games_played = games_played + 1
            WHERE id = 1
        ''', (datetime.now(),))
        conn.commit()
    
    def get_statistics(self):
        """Get general statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total categories and goals
        cursor.execute('SELECT COUNT(*) FROM categories')
        stats['total_categories'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM goals')
        stats['total_goals'] = cursor.fetchone()[0]
        
        # Total completions
        cursor.execute('SELECT COUNT(*) FROM progress')
        stats['total_completions'] = cursor.fetchone()[0]
        
        # Game state
        game_state = self.get_game_state()
        stats['current_streak'] = game_state['current_streak']
        stats['total_points'] = game_state['total_points']
        stats['best_streak'] = game_state['best_streak']
        stats['games_played'] = game_state['games_played']
        
        return stats
