"""
Game logic module - handles streaks, points, and 24-hour timeout
"""
from datetime import datetime, timedelta
from database import Database


class GameLogic:
    def __init__(self):
        self.db = Database()
    
    def check_24_hour_timeout(self):
        """
        Check if 24 hours have passed since last activity.
        If so, reset the game.
        Returns True if game was reset, False otherwise.
        """
        game_state = self.db.get_game_state()
        last_activity = game_state['last_activity']
        
        if last_activity:
            last_activity_dt = datetime.fromisoformat(last_activity)
            time_diff = datetime.now() - last_activity_dt
            
            # If more than 24 hours have passed
            if time_diff > timedelta(hours=24):
                self.db.reset_game()
                return True
        
        return False
    
    def check_all_goals_completed_today(self):
        """
        Check if all active goals for today have been completed.
        Returns True if all goals are completed, False otherwise.
        """
        # Get today's day of week (0=Monday, 6=Sunday)
        today_day_of_week = datetime.now().weekday()
        
        # Get goals for today
        goals_today = self.db.get_goals_for_day(today_day_of_week)
        if not goals_today:
            return False
        
        completed_today = self.db.get_goals_completed_today()
        goals_today_ids = {goal['id'] for goal in goals_today}
        
        return goals_today_ids == completed_today
    
    def complete_goal(self, goal_id, notes=''):
        """
        Complete a goal and update game state.
        Returns dict with success status, points earned, and new streak.
        """
        # First check if 24 hours have passed
        was_reset = self.check_24_hour_timeout()
        
        # Check if goal was already completed today
        completed_today = self.db.get_goals_completed_today()
        if goal_id in completed_today:
            return {
                'success': False,
                'message': '¡Esta meta ya fue completada hoy!',
                'was_reset': was_reset
            }
        
        # Get goal info
        goals = self.db.get_goals()
        goal = next((g for g in goals if g['id'] == goal_id), None)
        
        if not goal:
            return {
                'success': False,
                'message': 'Meta no encontrada',
                'was_reset': was_reset
            }
        
        # Record progress
        self.db.add_progress(goal_id, notes)
        
        # Get current game state
        game_state = self.db.get_game_state()
        current_streak = game_state['current_streak']
        total_points = game_state['total_points']
        points_earned = goal['points_value']
        
        # Add points
        new_total_points = total_points + points_earned
        
        # Check if all goals are now completed today
        all_completed = self.check_all_goals_completed_today()
        
        new_streak = current_streak
        streak_increased = False
        
        if all_completed:
            # Check if this is a new day completion (increase streak)
            last_completion = self.db.get_last_completion_time()
            
            # If this is the first completion or it's been more than a day, increase streak
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Count completions today
            today_progress = self.db.get_today_progress()
            
            # If this brings us to complete all goals today and we haven't incremented streak today
            # We check if the last activity was yesterday or before
            if last_completion:
                last_activity_day = last_completion.replace(hour=0, minute=0, second=0, microsecond=0)
                today_day = today_start
                
                # Only increase streak if we completed all goals and it's a new day
                if last_activity_day < today_day:
                    new_streak = current_streak + 1
                    streak_increased = True
            else:
                # First time completing all goals
                new_streak = 1
                streak_increased = True
        
        # Update game state
        self.db.update_game_state(new_streak, new_total_points)
        
        return {
            'success': True,
            'message': f'¡+{points_earned} puntos!',
            'points_earned': points_earned,
            'new_total_points': new_total_points,
            'new_streak': new_streak,
            'streak_increased': streak_increased,
            'all_goals_completed': all_completed,
            'was_reset': was_reset
        }
    
    def get_current_status(self):
        """
        Get current game status including whether game needs reset.
        """
        was_reset = self.check_24_hour_timeout()
        game_state = self.db.get_game_state()
        
        # Get today's day of week
        today_day_of_week = datetime.now().weekday()
        
        # Get goals for today only
        goals_today = self.db.get_goals_for_day(today_day_of_week)
        completed_today = self.db.get_goals_completed_today()
        
        goals_remaining = len(goals_today) - len(completed_today)
        progress_percentage = 0
        if goals_today:
            progress_percentage = (len(completed_today) / len(goals_today)) * 100
        
        return {
            'was_reset': was_reset,
            'current_streak': game_state['current_streak'],
            'total_points': game_state['total_points'],
            'best_streak': game_state['best_streak'],
            'total_goals': len(goals_today),
            'goals_completed_today': len(completed_today),
            'goals_remaining': goals_remaining,
            'progress_percentage': progress_percentage,
            'all_completed': len(goals_today) > 0 and goals_remaining == 0,
            'today_day_of_week': today_day_of_week
        }
    
    def get_time_until_reset(self):
        """
        Get time remaining until 24-hour reset.
        Returns timedelta or None if no activity yet.
        """
        game_state = self.db.get_game_state()
        last_activity = game_state['last_activity']
        
        if last_activity:
            last_activity_dt = datetime.fromisoformat(last_activity)
            reset_time = last_activity_dt + timedelta(hours=24)
            time_remaining = reset_time - datetime.now()
            
            if time_remaining.total_seconds() > 0:
                return time_remaining
            else:
                return timedelta(0)
        
        return None
    
    def format_time_remaining(self):
        """
        Format time remaining as human-readable string.
        """
        time_remaining = self.get_time_until_reset()
        
        if time_remaining is None:
            return "Sin actividad reciente"
        
        if time_remaining.total_seconds() <= 0:
            return "¡Tiempo agotado!"
        
        hours = int(time_remaining.total_seconds() // 3600)
        minutes = int((time_remaining.total_seconds() % 3600) // 60)
        
        return f"{hours}h {minutes}m restantes"
