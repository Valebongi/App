"""
Modern UI with KivyMD - Material Design
"""
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem, ThreeLineListItem, OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.chip import MDChip
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.selectioncontrol import MDCheckbox

from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle

from datetime import datetime, timedelta
from database import Database
from game_logic import GameLogic

# Set window size for development
Window.size = (360, 640)


class HomeScreen(MDScreen):
    """Modern home screen with calendar and goal cards"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_logic = GameLogic()
        self.db = Database()
        self.selected_day = datetime.now().weekday()
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', md_bg_color=(1, 1, 1, 1))
        
        # Top bar
        self.toolbar = MDTopAppBar(
            title="Daily Goals Challenge",
            md_bg_color=(0.12, 0.59, 0.95, 1),
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[["menu", lambda x: self.open_drawer()]],
            right_action_items=[["chart-line", lambda x: self.go_to_stats()]],
            anchor_title="left"
        )
        layout.add_widget(self.toolbar)
        
        # Scrollable content
        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', spacing=dp(15), padding=dp(15), size_hint_y=None, adaptive_height=True)
        
        # Status Card with modern design
        self.status_card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(180),
            padding=dp(20),
            spacing=dp(10),
            elevation=4,
            md_bg_color=(0.12, 0.59, 0.95, 1),
            radius=[15, 15, 15, 15]
        )
        
        self.streak_label = MDLabel(
            text="🔥 Racha: 0 días",
            font_style="H5",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            bold=True,
            size_hint=(1, None),
            height=dp(40)
        )
        
        self.points_label = MDLabel(
            text="⭐ Puntos: 0",
            font_style="H6",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(30)
        )
        
        self.progress_label = MDLabel(
            text="📊 Progreso hoy: 0%",
            font_style="Body1",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.9, 0.9, 0.9, 1),
            size_hint=(1, None),
            height=dp(25)
        )
        
        self.time_label = MDLabel(
            text="⏰ Tiempo restante: --",
            font_style="Caption",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(25)
        )
        
        self.status_card.add_widget(self.streak_label)
        self.status_card.add_widget(self.points_label)
        self.status_card.add_widget(self.progress_label)
        self.status_card.add_widget(self.time_label)
        
        content.add_widget(self.status_card)
        
        # Week Calendar
        calendar_label = MDLabel(
            text="Calendario Semanal",
            font_style="Subtitle1",
            bold=True,
            size_hint=(1, None),
            height=dp(30)
        )
        content.add_widget(calendar_label)
        
        self.week_calendar = self.create_week_calendar()
        content.add_widget(self.week_calendar)
        
        # Today's Goals Section
        goals_header = MDLabel(
            text="Metas de Hoy",
            font_style="Subtitle1",
            bold=True,
            size_hint=(1, None),
            height=dp(30)
        )
        content.add_widget(goals_header)
        
        # Goals container
        self.goals_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            adaptive_height=True
        )
        content.add_widget(self.goals_container)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
        
        # Update every second
        Clock.schedule_interval(self.update_status, 1.0)
    
    def create_week_calendar(self):
        """Create a horizontal week calendar view"""
        calendar_card = MDCard(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(80),
            padding=dp(5),
            spacing=dp(5),
            elevation=2,
            md_bg_color=(1, 1, 1, 1),  # Fondo blanco para mejor contraste
            radius=[10, 10, 10, 10]
        )
        
        days_names = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
        today = datetime.now()
        current_day_of_week = today.weekday()
        
        for i in range(7):
            day_date = today - timedelta(days=current_day_of_week - i)
            day_num = day_date.day
            is_today = (i == current_day_of_week)
            
            day_box = MDFloatLayout(size_hint=(1/7, 1))
            
            # Background circle
            with day_box.canvas.before:
                if is_today:
                    Color(0.3, 0.8, 0.3, 1)  # Verde brillante para día actual
                else:
                    Color(0.95, 0.95, 0.95, 1)  # Gris claro para otros días
                self.day_rect = RoundedRectangle(
                    pos=(day_box.x + dp(5), day_box.y + dp(10)),
                    size=(day_box.width - dp(10), dp(60)),
                    radius=[10]
                )
            
            day_content = MDBoxLayout(
                orientation='vertical',
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                size_hint=(None, None),
                size=(dp(40), dp(60))
            )
            
            day_name_label = MDLabel(
                text=days_names[i],
                halign='center',
                font_style='Caption',
                theme_text_color='Custom',
                text_color=(1, 1, 1, 1) if is_today else (0.3, 0.3, 0.3, 1),
                size_hint=(1, 0.4)
            )
            
            day_num_label = MDLabel(
                text=str(day_num),
                halign='center',
                font_style='Body1',
                bold=True,
                theme_text_color='Custom',
                text_color=(1, 1, 1, 1) if is_today else (0.2, 0.2, 0.2, 1),
                size_hint=(1, 0.6)
            )
            
            day_content.add_widget(day_name_label)
            day_content.add_widget(day_num_label)
            day_box.add_widget(day_content)
            
            calendar_card.add_widget(day_box)
        
        return calendar_card
    
    def refresh_goals(self):
        """Refresh the goals display for today"""
        self.goals_container.clear_widgets()
        
        today_day_of_week = datetime.now().weekday()
        goals_today = self.db.get_goals_for_day(today_day_of_week)
        completed_today = self.db.get_goals_completed_today()
        
        if not goals_today:
            no_goals_label = MDLabel(
                text="No hay metas para hoy.\nVe al menú para agregar metas.",
                halign='center',
                font_style='Body2',
                theme_text_color='Secondary',
                size_hint=(1, None),
                height=dp(60)
            )
            self.goals_container.add_widget(no_goals_label)
            return
        
        for goal in goals_today:
            is_completed = goal['id'] in completed_today
            goal_card = self.create_goal_card(goal, is_completed)
            self.goals_container.add_widget(goal_card)
    
    def create_goal_card(self, goal, is_completed):
        """Create a beautiful goal card"""
        card = MDCard(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(90),
            padding=dp(15),
            spacing=dp(15),
            elevation=3,
            md_bg_color=(0.3, 0.8, 0.3, 1) if is_completed else (1, 1, 1, 1),
            radius=[12, 12, 12, 12]
        )
        
        # Left side - Goal info
        info_layout = MDBoxLayout(
            orientation='vertical',
            size_hint=(0.7, 1),
            spacing=dp(5)
        )
        
        goal_name = MDLabel(
            text=goal['name'],
            font_style='Subtitle2',
            bold=True,
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1) if is_completed else (0.2, 0.2, 0.2, 1),
            size_hint=(1, 0.5)
        )
        
        goal_info = MDLabel(
            text=f"{goal['category_name']} • {goal['points_value']} pts",
            font_style='Caption',
            theme_text_color='Custom',
            text_color=(0.9, 0.9, 0.9, 1) if is_completed else (0.5, 0.5, 0.5, 1),
            size_hint=(1, 0.5)
        )
        
        info_layout.add_widget(goal_name)
        info_layout.add_widget(goal_info)
        
        # Right side - Complete button
        if not is_completed:
            complete_btn = MDRaisedButton(
                text="Completar",
                size_hint=(0.3, None),
                height=dp(40),
                md_bg_color=(0.12, 0.59, 0.95, 1),
                on_release=lambda x: self.complete_goal(goal['id'])
            )
        else:
            complete_btn = MDLabel(
                text="✓ Hecho",
                halign='center',
                font_style='Subtitle2',
                bold=True,
                theme_text_color='Custom',
                text_color=(1, 1, 1, 1),
                size_hint=(0.3, 1)
            )
        
        card.add_widget(info_layout)
        card.add_widget(complete_btn)
        
        return card
    
    def complete_goal(self, goal_id):
        """Complete a goal"""
        result = self.game_logic.complete_goal(goal_id)
        
        if result['success']:
            message = result['message']
            
            if result['streak_increased']:
                message += f"\n\n🔥 ¡Nueva racha: {result['new_streak']} días!"
            
            if result['all_goals_completed']:
                message += "\n\n🎉 ¡Todas las metas de hoy completadas!"
            
            self.show_dialog("¡Éxito!", message)
        else:
            self.show_dialog("Aviso", result['message'])
        
        self.refresh_goals()
        self.update_status(0)
    
    def show_dialog(self, title, text):
        """Show a modern dialog"""
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def update_status(self, dt):
        """Update status display"""
        status = self.game_logic.get_current_status()
        
        self.streak_label.text = f"🔥 Racha: {status['current_streak']} días"
        self.points_label.text = f"⭐ Puntos: {status['total_points']}"
        self.progress_label.text = f"📊 Progreso hoy: {int(status['progress_percentage'])}%"
        self.time_label.text = f"⏰ {self.game_logic.format_time_remaining()}"
        
        if status['was_reset']:
            self.show_dialog("Juego Reiniciado", "¡El juego se ha reiniciado!\n\nPasaron más de 24 horas\nsin completar todas las metas.")
    
    def open_drawer(self):
        """Open navigation drawer"""
        if hasattr(self.manager.parent.parent, 'set_state'):
            self.manager.parent.parent.set_state('open')
    
    def go_to_stats(self):
        """Navigate to stats screen"""
        self.manager.current = 'stats'
    
    def on_enter(self):
        """Called when screen is entered"""
        self.update_status(0)
        self.refresh_goals()


class ManageGoalsScreen(MDScreen):
    """Screen for managing goals with day selection"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.selected_days = []
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', md_bg_color=(1, 1, 1, 1))
        
        # Top bar
        toolbar = MDTopAppBar(
            title="Gestionar Metas",
            md_bg_color=(0.12, 0.59, 0.95, 1),
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[["plus", lambda x: self.show_add_goal_dialog()]]
        )
        layout.add_widget(toolbar)
        
        # Goals list
        scroll = MDScrollView()
        self.goals_list = MDList(spacing=dp(5), padding=dp(10))
        scroll.add_widget(self.goals_list)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def go_back(self):
        self.manager.current = 'home'
    
    def refresh(self):
        """Refresh goals list"""
        self.goals_list.clear_widgets()
        goals = self.db.get_goals()
        
        if not goals:
            item = OneLineListItem(text="No hay metas. Presiona + para agregar.")
            self.goals_list.add_widget(item)
            return
        
        for goal in goals:
            days = self.db.get_goal_days(goal['id'])
            days_str = self.format_days(days)
            
            item = ThreeLineListItem(
                text=goal['name'],
                secondary_text=f"{goal['category_name']} • {goal['points_value']} pts",
                tertiary_text=f"Días: {days_str}",
                on_release=lambda x, gid=goal['id']: self.confirm_delete_goal(gid)
            )
            self.goals_list.add_widget(item)
    
    def format_days(self, days):
        """Format days list to string"""
        if len(days) == 7:
            return "Todos los días"
        days_names = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        return ", ".join([days_names[d] for d in sorted(days)])
    
    def show_add_goal_dialog(self):
        """Show dialog to add new goal"""
        categories = self.db.get_categories()
        
        if not categories:
            self.show_dialog("Error", "Primero debes crear al menos una categoría")
            return
        
        self.selected_days = list(range(7))  # All days by default
        self.selected_category = categories[0]['id']
        
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10), size_hint_y=None, height=dp(400))
        
        self.name_field = MDTextField(
            hint_text="Nombre de la meta",
            mode="rectangle"
        )
        content.add_widget(self.name_field)
        
        self.desc_field = MDTextField(
            hint_text="Descripción (opcional)",
            mode="rectangle"
        )
        content.add_widget(self.desc_field)
        
        self.points_field = MDTextField(
            hint_text="Puntos",
            text="10",
            mode="rectangle",
            input_filter="int"
        )
        content.add_widget(self.points_field)
        
        # Days selection
        days_label = MDLabel(text="Días de la semana:", size_hint_y=None, height=dp(30))
        content.add_widget(days_label)
        
        days_grid = MDGridLayout(cols=4, spacing=dp(5), size_hint_y=None, height=dp(80))
        days_names = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        
        self.day_chips = []
        for i, day_name in enumerate(days_names):
            chip = MDChip(
                text=day_name,
                check=True,
                on_release=lambda x, idx=i: self.toggle_day(idx)
            )
            self.day_chips.append(chip)
            days_grid.add_widget(chip)
        
        content.add_widget(days_grid)
        
        self.dialog = MDDialog(
            title="Nueva Meta",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="Cancelar", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="Agregar", on_release=lambda x: self.add_goal())
            ]
        )
        self.dialog.open()
    
    def toggle_day(self, day_index):
        """Toggle day selection"""
        if day_index in self.selected_days:
            self.selected_days.remove(day_index)
        else:
            self.selected_days.append(day_index)
    
    def add_goal(self):
        """Add new goal"""
        name = self.name_field.text.strip()
        desc = self.desc_field.text.strip()
        points = self.points_field.text.strip()
        
        if not name:
            self.show_dialog("Error", "El nombre es obligatorio")
            return
        
        if not self.selected_days:
            self.show_dialog("Error", "Debes seleccionar al menos un día")
            return
        
        try:
            points_value = int(points) if points else 10
            self.db.add_goal(self.selected_category, name, desc, points_value, self.selected_days)
            self.dialog.dismiss()
            self.refresh()
        except ValueError:
            self.show_dialog("Error", "Puntos debe ser un número")
    
    def confirm_delete_goal(self, goal_id):
        """Confirm before deleting goal"""
        dialog = MDDialog(
            title="Eliminar Meta",
            text="¿Estás seguro de eliminar esta meta?",
            buttons=[
                MDFlatButton(text="Cancelar", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="Eliminar",
                    md_bg_color=(0.9, 0.2, 0.2, 1),
                    on_release=lambda x: self.delete_goal(goal_id, dialog)
                )
            ]
        )
        dialog.open()
    
    def delete_goal(self, goal_id, dialog):
        """Delete goal"""
        self.db.delete_goal(goal_id)
        dialog.dismiss()
        self.refresh()
    
    def show_dialog(self, title, text):
        """Show a dialog"""
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()
    
    def on_enter(self):
        self.refresh()


class CategoriesScreen(MDScreen):
    """Modern categories management screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', md_bg_color=(1, 1, 1, 1))
        
        toolbar = MDTopAppBar(
            title="Categorías",
            md_bg_color=(0.12, 0.59, 0.95, 1),
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[["plus", lambda x: self.show_add_category_dialog()]]
        )
        layout.add_widget(toolbar)
        
        scroll = MDScrollView()
        self.categories_list = MDList(spacing=dp(5), padding=dp(10))
        scroll.add_widget(self.categories_list)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def go_back(self):
        self.manager.current = 'home'
    
    def refresh(self):
        """Refresh categories list"""
        self.categories_list.clear_widgets()
        categories = self.db.get_categories()
        
        if not categories:
            item = OneLineListItem(text="No hay categorías. Presiona + para agregar.")
            self.categories_list.add_widget(item)
            return
        
        for category in categories:
            item = TwoLineListItem(
                text=category['name'],
                secondary_text="Toca para eliminar",
                on_release=lambda x, cid=category['id']: self.confirm_delete_category(cid)
            )
            self.categories_list.add_widget(item)
    
    def show_add_category_dialog(self):
        """Show dialog to add category"""
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10), size_hint_y=None, height=dp(100))
        
        self.name_field = MDTextField(
            hint_text="Nombre de la categoría",
            mode="rectangle"
        )
        content.add_widget(self.name_field)
        
        self.dialog = MDDialog(
            title="Nueva Categoría",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="Cancelar", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="Agregar", on_release=lambda x: self.add_category())
            ]
        )
        self.dialog.open()
    
    def add_category(self):
        """Add new category"""
        name = self.name_field.text.strip()
        
        if not name:
            self.show_dialog("Error", "El nombre es obligatorio")
            return
        
        result = self.db.add_category(name)
        if result:
            self.dialog.dismiss()
            self.refresh()
        else:
            self.show_dialog("Error", "Ya existe una categoría con ese nombre")
    
    def confirm_delete_category(self, category_id):
        """Confirm before deleting"""
        dialog = MDDialog(
            title="Eliminar Categoría",
            text="¿Estás seguro? Se eliminarán todas las metas asociadas.",
            buttons=[
                MDFlatButton(text="Cancelar", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="Eliminar",
                    md_bg_color=(0.9, 0.2, 0.2, 1),
                    on_release=lambda x: self.delete_category(category_id, dialog)
                )
            ]
        )
        dialog.open()
    
    def delete_category(self, category_id, dialog):
        """Delete category"""
        self.db.delete_category(category_id)
        dialog.dismiss()
        self.refresh()
    
    def show_dialog(self, title, text):
        """Show a dialog"""
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()
    
    def on_enter(self):
        self.refresh()


class StatsScreen(MDScreen):
    """Modern statistics screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', md_bg_color=(1, 1, 1, 1))
        
        toolbar = MDTopAppBar(
            title="Estadísticas",
            md_bg_color=(0.12, 0.59, 0.95, 1),
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[["arrow-left", lambda x: self.go_back()]]
        )
        layout.add_widget(toolbar)
        
        scroll = MDScrollView()
        self.stats_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(15),
            size_hint_y=None,
            adaptive_height=True
        )
        scroll.add_widget(self.stats_container)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def go_back(self):
        self.manager.current = 'home'
    
    def refresh(self):
        """Refresh statistics"""
        self.stats_container.clear_widgets()
        stats = self.db.get_statistics()
        
        # Create stat cards
        stats_data = [
            ("🔥 Racha actual", f"{stats['current_streak']} días", (0.95, 0.4, 0.26, 1)),
            ("🏆 Mejor racha", f"{stats['best_streak']} días", (1, 0.84, 0, 1)),
            ("⭐ Puntos totales", str(stats['total_points']), (0.12, 0.59, 0.95, 1)),
            ("🎮 Partidas jugadas", str(stats['games_played']), (0.61, 0.35, 0.71, 1)),
            ("📁 Categorías", str(stats['total_categories']), (0.3, 0.69, 0.31, 1)),
            ("🎯 Metas totales", str(stats['total_goals']), (1, 0.6, 0, 1)),
            ("✅ Completadas (total)", str(stats['total_completions']), (0, 0.74, 0.83, 1)),
        ]
        
        for label, value, color in stats_data:
            card = self.create_stat_card(label, value, color)
            self.stats_container.add_widget(card)
    
    def create_stat_card(self, label, value, color):
        """Create a stat card"""
        card = MDCard(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(80),
            padding=dp(20),
            spacing=dp(15),
            elevation=3,
            md_bg_color=color,
            radius=[12, 12, 12, 12]
        )
        
        label_widget = MDLabel(
            text=label,
            font_style='Subtitle1',
            bold=True,
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            size_hint=(0.7, 1)
        )
        
        value_widget = MDLabel(
            text=value,
            font_style='H5',
            bold=True,
            halign='right',
            theme_text_color='Custom',
            text_color=(1, 1, 1, 1),
            size_hint=(0.3, 1)
        )
        
        card.add_widget(label_widget)
        card.add_widget(value_widget)
        
        return card
    
    def on_enter(self):
        self.refresh()


class DailyGoalsApp(MDApp):
    """Main application with Material Design"""
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        # Navigation layout
        nav_layout = MDNavigationLayout()
        
        # Screen manager
        sm = MDScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ManageGoalsScreen(name='manage_goals'))
        sm.add_widget(CategoriesScreen(name='categories'))
        sm.add_widget(StatsScreen(name='stats'))
        
        # Navigation drawer
        drawer = MDNavigationDrawer()
        drawer_content = MDBoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        drawer_content.add_widget(MDLabel(
            text="Daily Goals",
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height=dp(50)
        ))
        
        menu_items = [
            ("home", "Inicio", "home"),
            ("checkbox-marked-outline", "Gestionar Metas", "manage_goals"),
            ("folder-multiple", "Categorías", "categories"),
            ("chart-line", "Estadísticas", "stats"),
        ]
        
        for icon, text, screen in menu_items:
            item = OneLineAvatarIconListItem(
                text=text,
                on_release=lambda x, s=screen: self.go_to_screen(sm, drawer, s)
            )
            item.add_widget(IconLeftWidget(icon=icon))
            drawer_content.add_widget(item)
        
        drawer.add_widget(drawer_content)
        
        nav_layout.add_widget(sm)
        nav_layout.add_widget(drawer)
        
        return nav_layout
    
    def go_to_screen(self, screen_manager, drawer, screen_name):
        """Navigate to screen and close drawer"""
        screen_manager.current = screen_name
        drawer.set_state('close')


if __name__ == '__main__':
    DailyGoalsApp().run()
