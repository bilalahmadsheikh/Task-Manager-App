import json
import time
from datetime import datetime, timedelta
from collections import Counter
import matplotlib
from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Rectangle
from kivy.uix.modalview import ModalView
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.core.text import LabelBase

 # Action for the "Send Suggestion" button
from kivy.clock import Clock
import os
import warnings
matplotlib.use('Agg')

#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg


TASKS_FILE = "tasks.json"
def get_font_size():
    base_width = 360  # Base width of the screen (from Window.size)
    base_font_size = 14  # Base font size
    
    # Scale the font size based on the width of the screen
    return base_font_size * (Window.width / base_width)
# Helper functions for file handling
def save_tasks_to_file(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def load_tasks_from_file():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Helper function for creating a gradient background
# Helper function for creating a gradient background
class GradientBackground(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.1, 0.1, 0.2, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

        
# Floating Action Button
class FloatingActionButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = kwargs.get('source', '')
        self.size_hint = (None, None)
        self.size = (38, 38)
        self.pos_hint = {'right': 0.98, 'top': 0.95}

class LabelButton(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_color = self.color
        self.hover_color = [0.5, 0.5, 1, 1]  # Optional hover color

    def on_enter(self):
        self.color = self.hover_color

    def on_leave(self):
        self.color = self.default_color

        
def on_hover(self, instance, value):
    if value:
        instance.background_color = (0.6, 0.1, 0.96, 1)
    else:
        instance.background_color = (0.8, 0.4, 0.7, 1)
class FloatingButtonTemplate(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (56, 56)
        self.pos_hint = {'right': 0.75, 'top': 0.98}  # Positioned bottom-right
        self.background_color = (0.2, 0.6, 0.86, 1)  # Blue color
        self.color = (1, 1, 1, 1)  # White text/icon
        self.font_size = 24
        self.opacity = 0.7
        self.text = '\uf067'  # Font Awesome 'plus' icon
         # Path to the Font Awesome TTF file


    def on_press(self):
        self.opacity = 1

    def on_release(self):
        self.opacity = 0.7

  
class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a canvas with a dark blue shiny background
        with self.canvas.before:
            # Set a shiny dark blue color
            Color(0.1, 0.1, 0.2, 0.6) # RGBA for dark blue
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

        # Bind the rectangle to update on size/position changes
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Centered overlay layout
        overlay_layout = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(300, 150),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=20,
        )

        # Add loading label
        label = Label(
            text="Task Manager Loading...",
            font_size=24,
            size_hint=(1, None),
            height=50,
            halign='center',
            valign='middle',
        )
        label.bind(size=label.setter('text_size'))  # Center text within the label
        overlay_layout.add_widget(label)

        # Add progress bar
        self.progress_bar = AnimatedProgressBar(size_hint=(1, None), height=30)
        overlay_layout.add_widget(self.progress_bar)

        # Add the overlay layout to the screen
        self.add_widget(overlay_layout)

    def _update_rect(self, instance, value):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
# Home Page
class HomePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GradientBackground(orientation='vertical', spacing=5, padding=(5, 5))
        
        # Header with suggestion button
        header_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=2,pos_hint={'center_x': 0.5, 'center_y': 0.95})
        header = Label(
            text="Task Manager", 
            font_size=30, 
            size_hint=(1, 1), 
            halign='left', 
            valign='middle',
            color= (0.7, 0.6, 0.9, 1) # Aesthetic color for the header text
        )
        header.font_name = 'Lobster'  
        LabelBase.register(name='Lobster', fn_regular=r)  # Ensure the font file is correctly placed
        header.bind(size=header.setter('text_size'))

        header_layout.add_widget(header)
        self.layout.add_widget(header_layout)
        
        self.tasks = load_tasks_from_file()
        self.current_tasks = []
        self.completed_tasks = []

        # Scrollable Task List
        self.scroll_area = ScrollView(size_hint=(1, 0.8))
        self.task_list = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.task_list.bind(minimum_height=self.task_list.setter('height'))
        self.scroll_area.add_widget(self.task_list)
        self.layout.add_widget(self.scroll_area)
        
        
        
        # Floating Action Button
        image_path = r
        fab = FloatingActionButton(source=image_path)
        fab.bind(on_release=self.show_add_task_popup)
        
        # Create a new Floating Action Button for "History & Tracking"
        history_image_path = r

        # Create the History & Tracking Button
        history_btn = FloatingActionButton(source=history_image_path)
        history_btn.size_hint = (None, None)
        history_btn.size = (38, 38)  # Standard FAB size
        history_btn.pos_hint = {'right': 0.87, 'top': 0.95}  # Position it near the bottom-right
        history_btn.bind(on_release=self.goto_history)

        
        # Add floating suggestion button
        suggestion_image_path = r

        # Create the Floating Suggestion Button
        suggestion_button = FloatingActionButton(source=suggestion_image_path)
        suggestion_button.size_hint = (None, None)
        suggestion_button.size = (47, 47)  # Standard FAB size
        suggestion_button.pos_hint = {'right': 0.67, 'top': 0.96}  # Center of the screen
        suggestion_button.bind(on_release=lambda _: self.usersuggestion())

        # Path to the "info" image
        info_image_path = r

        # Create the About Us Button as a Floating Action Button
        about_us_button = FloatingActionButton(source=info_image_path)
        about_us_button.size_hint = (None, None)
        about_us_button.size = (35, 35)  # Standard size for the button
        about_us_button.pos_hint = {'right': 0.76, 'top': 0.948}  # Adjust position to align with header
        about_us_button.bind(on_release=lambda _: setattr(self.manager, 'current', 'about_us'))


        
        # Add it to the FloatLayout
        float_layout = FloatLayout()
        float_layout.add_widget(self.layout)  # Main layout
        float_layout.add_widget(history_btn)  # Add the floating History button
        float_layout.add_widget(fab)  # Add the floating Add Task button
        float_layout.add_widget(suggestion_button) # Add the floating Suggestion button
        float_layout.add_widget(about_us_button)  # Add the About Us button
        

        self.add_widget(float_layout)

        # Load tasks from file
        
        self.refresh_task_list()
        
    def load_tasks(self):
        tasks = load_tasks_from_file()
        self.task_list.clear_widgets()
        for task in tasks:
            task_button = Button(text=task['name'], size_hint_y=None, height=40)
            task_button.bind(on_release=lambda instance, t=task: self.show_task_details(t))
            self.task_list.add_widget(task_button)
    
    def show_task_details(self, task):
        task_details_screen = TaskDetailsScreen(task, self, name="task_details")
        self.manager.add_widget(task_details_screen)
        self.manager.current = "task_details"
            
    def refresh_task_list(self):
        self.current_tasks = [task for task in self.tasks if not task["completed"]]
        self.completed_tasks = [task for task in self.tasks if task["completed"]]
        self.task_list.clear_widgets()
        for task in self.current_tasks:
            self.add_task_to_ui(task)

    def show_add_task_popup(self, instance):
        popup = AddTaskPopup(self)
        popup.open()

    def goto_history(self, instance):
        self.manager.current = "history"

    def add_task(self, task_name, task_type, duration=None, notes=None, start_time=None, completion_date=None):
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        new_task = {
            "name": task_name,
            "type": task_type,
            "duration": duration,
            "notes": notes,
            "progress": 0,
            "completed": False,
            "start_time": start_time
        }
        self.tasks.append(new_task)
        save_tasks_to_file(self.tasks)
        self.refresh_task_list()

    def add_task_to_ui(self, task):
        task_card = BoxLayout(orientation='horizontal', size_hint_y=None, height=80)

    # Calculate time remaining
        try:
            if task.get('completion_date'):
            # Parse completion date
                completion_time = time.mktime(time.strptime(task['completion_date'], "%Y-%m-%d"))
                time_remaining = completion_time - time.time()
                days_remaining = max(0, int(time_remaining // 86400))  # 86400 seconds in a day
                time_remaining_text = f"Time Remaining: {days_remaining} days"
            elif task.get('duration'):
            # Handle task duration
                duration_days = int(task['duration'])
                start_time = time.strptime(task['start_time'], "%Y-%m-%d %H:%M:%S")
                end_time = time.mktime(start_time) + duration_days * 86400
                time_remaining = end_time - time.time()
                days_remaining = max(0, int(time_remaining // 86400))
                time_remaining_text = f"Time Remaining: {days_remaining} days"
            else:
                time_remaining_text = "Time Remaining: N/A"
        except Exception as e:
        # Handle any parsing or logic errors gracefully
            time_remaining_text = "Time Remaining: Error"
            print(f"Error calculating time remaining: {e}")

    # Clickable task name as a LabelButton
        task_label = LabelButton(
            text = f"[ref=task][color=#FF6347][u]{task['name']}[/u][/color][/ref]\nStart: {task.get('start_time', 'N/A')}\nType: {task['type']}\n{time_remaining_text}",
            markup=True,
            size_hint=(0.5, 1),
            font_size=12
    )

    # Semi-transparent box for task details
        with task_card.canvas.before:
            Color(0.2, 0.2, 0.4, 0.7)  # Darker blue color with 70% opacity
            task_card.rect = Rectangle(size=task_card.size, pos=task_card.pos)
            task_card.bind(size=lambda instance, value: setattr(task_card.rect, 'size', value))
            task_card.bind(pos=lambda instance, value: setattr(task_card.rect, 'pos', value))
        task_label.bind(on_ref_press=lambda instance, ref: self.show_task_details(task))

    # Progress bar
        progress_layout = BoxLayout(orientation='horizontal', size_hint=(0.3, 1))
        progress = ProgressBar(value=task["progress"], max=100, size_hint=(0.7, 1))
        progress_label = Label(text=f"{format(task['progress'], '.1f')}%", size_hint=(0.35, 1),padding=(13, 0, 0, 0))
        progress_layout.add_widget(progress)
        progress_layout.add_widget(progress_label)

    # Quick complete checkbox
        quick_complete = CheckBox(size_hint=(None, None), size=(40, 40), pos_hint={'center_y': 0.5})
        quick_complete.bind(active=lambda _, active: self.complete_task(task) if active else None)

    # Update button
        update_btn = Button(
        text="Update", 
        size_hint=(0.2, 0.4), 
        pos_hint={'center_y': 0.5},
        background_color=(0.2, 0.6, 0.86, 1)  # Initial button color
    )
        update_btn.bind(on_release=lambda _: self.show_update_task_popup(task))

        def on_enter(instance):
            instance.background_color = (0.3, 0.7, 0.96, 1)  # Hover color

        def on_leave(instance):
            instance.background_color = (0.2, 0.6, 0.86, 1)  # Original color

        update_btn.bind(on_enter=on_enter, on_leave=on_leave)

    # Add widgets to the task card
        task_card.add_widget(task_label)
        task_card.add_widget(progress_layout)
        task_card.add_widget(quick_complete)
        task_card.add_widget(update_btn)

    # Add the task card to the task list
        self.task_list.add_widget(task_card)

    def show_update_task_popup(self, task):
        popup = UpdateTaskPopup(self, task)
        popup.notes_input.text = task.get('notes', '')
        popup.notes_input.height = '400dp'  # Set the height to 200 density-independent pixels
        popup.notes_input.width = '300dp'  # Set the width to 300 density-independent pixels
        popup.open()

    def complete_task(self, task):
        if task['type'] == 'Daily':
            task["progress"] += 100 / int(task['duration'])
            task["notes"] += f"\nDays Completed {int(task['progress'] / (100 / int(task['duration'])))} Days Remaining: {int(task['duration']) - int(task['progress'] / (100 / int(task['duration'])))}\n"
            popup = Popup(title="Daily Task", size_hint=(0.8, 0.4))
            layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
            label = Label(text="Task completed name")
            layout.add_widget(label)
            name_input = TextInput(hint_text="Task Name", size_hint=(1, 0.2))
            layout.add_widget(name_input)
            def on_submit(instance):
                task["notes"] += f"\nCompleted daily task name: {name_input.text}\n"
                popup.dismiss()
            submit_button = Button(text="Submit", size_hint=(1, 0.2))
            submit_button.bind(on_release=on_submit)
            layout.add_widget(submit_button)
            popup.content = layout
            popup.open()
            if task["progress"] >= 100:
                task["completed"] = True
                task["progress"] = 100
                task["completion_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        else:
            task["completed"] = True
            task["progress"] = 100
            task["completion_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        save_tasks_to_file(self.tasks)
        self.refresh_task_list()

    def show_task_details(self, task):
        self.layout.clear_widgets()

    # Set background color
        with self.layout.canvas.before:
            Color(0.0, 0.3, 0.4, 1)  
            self.bg_rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
            self.layout.bind(size=lambda instance, value: setattr(self.bg_rect, 'size', value))
            self.layout.bind(pos=lambda instance, value: setattr(self.bg_rect, 'pos', value))

        task_details = BoxLayout(orientation='vertical', spacing=10, padding=10)

    # Task details labels
        task_details.add_widget(Label(text=f"Task Name: {task['name']}", size_hint=(1, 0.1), color=(1, 1, 1, 1)))  # White text
        task_details.add_widget(Label(text=f"Task Type: {task['type']}", size_hint=(1, 0.1), color=(1, 1, 1, 1)))  # White text
        task_details.add_widget(Label(text=f"Start Time: {task.get('start_time', 'N/A')}", size_hint=(1, 0.1), color=(1, 1, 1, 1)))  # White text

    # Buttons with royal colors
        edit_button = Button(
            text="Edit Task",
            size_hint=(1, 0.2),
            background_color=(0.9, 0.6, 0.1, 1),  # Royal emerald green
            color=(1, 1, 1, 1)  # White text
    )
        edit_button.bind(on_release=lambda instance: self.edit_task(task))
        task_details.add_widget(edit_button)

        delete_button = Button(
            text="Delete Task",
            size_hint=(1, 0.2),
            background_color=(0.7, 0.2, 0.1, 1),  # Rich ruby red
            color=(1, 1, 1, 1)  # White text
    )
        delete_button.bind(on_release=lambda instance: self.delete_task(task))
        task_details.add_widget(delete_button)

        back_button = Button(
            text="Back",
            size_hint=(1, 0.2),
            background_color=(0.1, 0.4, 0.6, 1),  # Majestic sapphire blue
            color=(1, 1, 1, 1)  # White text
    )
        back_button.bind(on_release=lambda instance: self.go_back())
        task_details.add_widget(back_button)

        self.layout.add_widget(task_details)

        
    def edit_task(self, task):
        popup = Popup(
            title="Edit Task",
            size_hint=(0.9, 0.9),
            title_color=(1, 1, 1, 1),  # White title text
            title_align='center',  # Center the title
    )

    # Popup background
        with popup.canvas.before:
            Color(0.0, 0.2, 0.4, 1)  # Deep Navy Blue
            self.bg_rect = Rectangle(size=popup.size, pos=popup.pos)
            popup.bind(size=lambda instance, value: setattr(self.bg_rect, 'size', value))
            popup.bind(pos=lambda instance, value: setattr(self.bg_rect, 'pos', value))

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

    # TextInput styling
        text_input_style = {
            "background_color": (0.95, 0.95, 0.9, 1),  # Ivory White
            "foreground_color": (0.1, 0.4, 0.6, 1),  # Sapphire Blue text
            "cursor_color": (0.9, 0.7, 0.2, 1),  # Golden Amber cursor
            "size_hint": (1, 0.2),
    }

        task_name_input = TextInput(text=task['name'], hint_text="Task Name", **text_input_style)
        task_type_input = TextInput(text=task['type'], hint_text="Task Type", **text_input_style)
        duration_input = TextInput(text=str(task.get('duration', '')), hint_text="Duration (in days)", **text_input_style)
        notes_input = TextInput(text=task.get('notes', ''), hint_text="Notes", multiline=True, **text_input_style)

    # Save Button
        save_button = Button(
            text="Save Changes",
            size_hint=(1, 0.2),
            background_color=(0.9, 0.7, 0.2, 1),  # Golden Amber
            color=(1, 1, 1, 1),  # White text
            font_size=16,
    )
        save_button.bind(on_release=lambda instance: self.save_task_changes(
            task,
            task_name_input.text,
            task_type_input.text,
            duration_input.text,
            notes_input.text,
            popup
    ))
        back_button = Button(
            text="Back",
            size_hint=(1, 0.2),
            background_color=(0.2, 0.2, 0.3, 1),  # Moody Dark Blue
            color=(1, 1, 1, 1),  # White text
            font_size=16,
    )
        back_button.bind(on_release=popup.dismiss)

    # Adding widgets to the layout
        layout.add_widget(task_name_input)
        layout.add_widget(task_type_input)
        layout.add_widget(duration_input)
        layout.add_widget(notes_input)
        layout.add_widget(save_button)
        layout.add_widget(back_button)

        popup.content = layout
        popup.open()


    def save_task_changes(self, task, name, task_type, duration, notes, popup):
        task['name'] = name
        task['type'] = task_type
        task['duration'] = duration
        task['notes'] = notes
        save_tasks_to_file(self.tasks)
        self.refresh_task_list()
        popup.dismiss()
        
    
    def delete_task(self, task):
        self.tasks = [t for t in self.tasks if t['name'] != task['name']]
        save_tasks_to_file(self.tasks)
        self.refresh_task_list()
    
    def go_back(self, *args):
        self.__init__()
    
    

    def usersuggestion(self):
        popup = Popup(title="User Suggestion", size_hint=(0.8, 0.6), background_color=(0.1, 0.1, 0.1, 1))  # Dark background for the popup
        layout = BoxLayout(orientation='vertical', spacing=15, padding=15)
    
    # Suggestion input field with a clean modern background
        suggestion_input = TextInput(hint_text="Enter your suggestion here", size_hint=(1, 0.7), 
                                 background_color=(0.95, 0.95, 0.95, 1), foreground_color=(0, 0, 0, 1), 
                                 font_size=16)
        layout.add_widget(suggestion_input)
    
    # Create button layout for the two buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.2))
    
    # Send Suggestion button with an advanced, deep blue color
        send_button = Button(text="Send Suggestion", size_hint=(0.45, 1), 
                         background_normal='', background_color=(0.2, 0.2, 0.3, 1), color=(1, 1, 1, 1), 
                         font_size=13, bold=True)
        button_layout.add_widget(send_button)
    
    # Cancel button with a stylish deep red gradient
        cancel_button = Button(text="Cancel", size_hint=(0.45, 1), 
                           background_normal='', background_color=(0.6, 0.2, 0.2, 1), color=(1, 1, 1, 1),
                           font_size=16, bold=True)
        button_layout.add_widget(cancel_button)
    
    # Add button layout to the main layout
        layout.add_widget(button_layout)
    
   

        def on_send(instance):
            popup = Popup(
                title="Success",
                content=Label(text="Suggestion sent successfully!"),
                size_hint=(0.6, 0.4),
                background_color=(0.15, 0.6, 0.15, 1),
            )
            popup.open()
            # Schedule the popup to close after 4 seconds
            Clock.schedule_once(lambda dt: popup.dismiss(), 4)


    # Action for the "Cancel" button (going back to main screen)
        def on_cancel(instance):
            popup.dismiss()

    # Bind actions to buttons
        send_button.bind(on_release=on_send)
        cancel_button.bind(on_release=on_cancel)

    # Open the popup
        popup.content = layout
        popup.open()





# Add Task Popup
# Updated Add Task Popup with separate forms for Daily and One-Time Tasks
# Add Task Popup
class AddTaskPopup(Popup):
    def __init__(self, home_page, **kwargs):
        super().__init__(**kwargs)
        self.home_page = home_page
        self.title = "Add New Task"
        self.size_hint = (0.9, 0.9)

        # Popup Background
        with self.canvas.before:
            Color(0.2, 0.3, 0.6, 1)  # Slate Blue
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=lambda instance, value: setattr(self.bg_rect, 'size', value))
            self.bind(pos=lambda instance, value: setattr(self.bg_rect, 'pos', value))

        layout = BoxLayout(orientation='vertical', spacing=15, padding=20)

        # Tabs for Daily and One-Time tasks
        self.tab_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        self.daily_btn = Button(
            text="Daily Task",
            background_color=(0.4, 0.6, 0.8, 1),  # Muted Sky Blue
            color=(1, 1, 1, 1),  # White text
            bold=True
        )
        self.daily_btn.bind(on_release=self.show_daily_form)
        self.one_time_btn = Button(
            text="One-Time Task",
            background_color=(0.7, 0.8, 0.9, 1),  # Light Grayish Blue
            color=(0, 0, 0, 1),  # Black text
            bold=True
        )
        self.one_time_btn.bind(on_release=self.show_one_time_form)

        self.tab_box.add_widget(self.daily_btn)
        self.tab_box.add_widget(self.one_time_btn)

        layout.add_widget(self.tab_box)

        # Content area for forms
        self.form_area = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.show_daily_form()
        layout.add_widget(self.form_area)

        self.content = layout

    def show_daily_form(self, *args):
        self.form_area.clear_widgets()
        self.task_name = TextInput(
            hint_text="Task Name",
            background_color=(0.95, 0.95, 0.9, 1),  # Ivory White
            foreground_color=(0.1, 0.4, 0.6, 1),  # Sapphire Blue
            cursor_color=(0.3, 0.7, 0.4, 1),  # Emerald Green
            size_hint=(1, 0.2)
        )
        self.duration = TextInput(
            hint_text="Duration (in days)",
            background_color=(0.95, 0.95, 0.9, 1),
            foreground_color=(0.1, 0.4, 0.6, 1),
            cursor_color=(0.3, 0.7, 0.4, 1),
            size_hint=(1, 0.2)
        )
        self.notes = TextInput(
            hint_text="Notes",
            background_color=(0.95, 0.95, 0.9, 1),
            foreground_color=(0.1, 0.4, 0.6, 1),
            cursor_color=(0.3, 0.7, 0.4, 1),
            size_hint=(1, 0.2)
        )

        # Buttons Layout
        buttons_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=10)
        create_task_btn = Button(
            text="Create Task",
            background_color=(0.3, 0.7, 0.4, 1),  # Emerald Green
            color=(1, 1, 1, 1),  # White text
            bold=True,
        )
        create_task_btn.bind(on_release=self.create_daily_task)

        cancel_btn = Button(
            text="Cancel",
            background_color=(0.7, 0.2, 0.2, 1),  # Ruby Red
            color=(1, 1, 1, 1),  # White text
            bold=True,
        )
        cancel_btn.bind(on_release=self.dismiss)

        buttons_box.add_widget(create_task_btn)
        buttons_box.add_widget(cancel_btn)

        self.form_area.add_widget(self.task_name)
        self.form_area.add_widget(self.duration)
        self.form_area.add_widget(self.notes)
        self.form_area.add_widget(buttons_box)

    def show_one_time_form(self, *args):
        self.form_area.clear_widgets()
        self.task_name = TextInput(
            hint_text="Task Name",
            background_color=(0.95, 0.95, 0.9, 1),  # Ivory White
            foreground_color=(0.1, 0.4, 0.6, 1),
            cursor_color=(0.3, 0.7, 0.4, 1),
            size_hint=(1, 0.2)
        )
        self.duration = TextInput(
            hint_text="Total Days",
            background_color=(0.95, 0.95, 0.9, 1),
            foreground_color=(0.1, 0.4, 0.6, 1),
            cursor_color=(0.3, 0.7, 0.4, 1),
            size_hint=(1, 0.2)
        )
        self.notes = TextInput(
            hint_text="Notes",
            background_color=(0.95, 0.95, 0.9, 1),
            foreground_color=(0.1, 0.4, 0.6, 1),
            cursor_color=(0.3, 0.7, 0.4, 1),
            size_hint=(1, 0.2)
        )

        # Buttons Layout
        buttons_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=10)
        create_task_btn = Button(
            text="Create Task",
            background_color=(0.3, 0.7, 0.4, 1),  # Emerald Green
            color=(1, 1, 1, 1),  # White text
            bold=True,
        )
        create_task_btn.bind(on_release=self.create_one_time_task)

        cancel_btn = Button(
            text="Cancel",
            background_color=(0.7, 0.2, 0.2, 1),  # Ruby Red
            color=(1, 1, 1, 1),  # White text
            bold=True,
        )
        cancel_btn.bind(on_release=self.dismiss)

        buttons_box.add_widget(create_task_btn)
        buttons_box.add_widget(cancel_btn)

        self.form_area.add_widget(self.task_name)
        self.form_area.add_widget(self.duration)
        self.form_area.add_widget(self.notes)
        self.form_area.add_widget(buttons_box)



    def create_daily_task(self, *args):
        task_name = self.task_name.text
        duration = self.duration.text
        notes = self.notes.text

        if task_name and duration.isdigit():
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.home_page.add_task(
                task_name, 
                "Daily", 
                duration=duration, 
                notes=notes,
                start_time=start_time
            )
            self.dismiss()
        else:
            self.show_error("Invalid input! \nTask name and numeric duration are required.")

    def create_one_time_task(self, *args):
        task_name = self.task_name.text
        duration = self.duration.text
        notes = self.notes.text

        if task_name and duration.isdigit():
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.home_page.add_task(
                task_name, 
                "One-Time", 
                duration=duration, 
                notes=notes,
                start_time=start_time
            )
            self.dismiss()
        else:
            self.show_error("Invalid input! Task name and numeric duration are required.")

            
    def show_error(self, message):
        error_popup = Popup(title="Error", content=Label(text=message), size_hint=(0.8, 0.4))
        error_popup.open()


class UpdateTaskPopup(Popup):
    def __init__(self, home_page, task, **kwargs):
        super().__init__(**kwargs)
        self.home_page = home_page
        self.task = task
        self.title = "Update Task"
        self.size_hint = (0.8, 0.6)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Background Color
        with layout.canvas.before:
            Color(0.15, 0.1, 0.3, 1)  # Dark blue background
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=lambda instance, value: setattr(self.rect, 'size', value))
            layout.bind(pos=lambda instance, value: setattr(self.rect, 'pos', value))

        # Task Info
        layout.add_widget(Label(text=f"Task Name: {task['name']}", color=(1, 1, 1, 1)))
        layout.add_widget(Label(text=f"Task Type: {task['type']}", color=(1, 1, 1, 1)))

        # Progress Slider with Percentage
        slider_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.3), spacing=10)
        self.progress_slider = Slider(min=0, max=100, value=task["progress"], size_hint=(0.8, 1))
        self.progress_label = Label(text=f"{int(task['progress'])}%", size_hint=(0.2, 1), color=(1, 1, 1, 1))
        self.progress_slider.bind(value=self.update_progress_label)
        slider_layout.add_widget(Label(text="Progress:", color=(1, 1, 1, 1), size_hint=(0.2, 1)))
        slider_layout.add_widget(self.progress_slider)
        slider_layout.add_widget(self.progress_label)
        layout.add_widget(slider_layout)

        # Notes Input
        self.notes_input = TextInput(
            text=task.get('notes', ''),
            hint_text="Notes",
            multiline=True,
            size_hint=(1, 0.4),
            background_color=(0.2, 0.3, 0.5, 1),
            foreground_color=(1, 1, 1, 1),
        )
        layout.add_widget(self.notes_input)

        # Buttons Layout
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=10)
        save_button = Button(
            text="Save Changes",
            background_color=(0.0, 0.5, 0.25, 1),
            size_hint=(0.5, 1),
        )
        save_button.bind(on_release=self.save_changes)

        cancel_button = Button(
            text="Cancel",
            background_color=(0.6, 0.0, 0.1, 1),
            size_hint=(0.5, 1),
        )
        cancel_button.bind(on_release=self.dismiss)

        button_layout.add_widget(save_button)
        button_layout.add_widget(cancel_button)
        layout.add_widget(button_layout)

        self.content = layout

    def update_progress_label(self, instance, value):
        """Update the percentage label when the slider is moved."""
        self.progress_label.text = f"{int(value)}%"

    def save_changes(self, instance):
        """Save changes to the task and refresh the UI."""
        self.task["progress"] = int(self.progress_slider.value)
        self.task["notes"] = self.notes_input.text
        if self.task["progress"] == 100:
            self.task["completed"] = True
        save_tasks_to_file(self.home_page.tasks)
        self.home_page.refresh_task_list()
        self.dismiss()

# Update Task Page
class UpdateTaskPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.task_name_label = Label(text="Task Name: Task 1")
        layout.add_widget(self.task_name_label)

        self.task_type_label = Label(text="Task Type: Daily")
        layout.add_widget(self.task_type_label)

        self.days_elapsed_slider = Slider(min=0, max=30, value=5)
        layout.add_widget(self.days_elapsed_slider)

        update_button = Button(text="Update Task")
        update_button.bind(on_release=self.update_task)
        layout.add_widget(update_button)

        self.add_widget(layout)

    def update_task(self, instance):
        # Implement the logic to update the task
        print("Task updated")
        
        
# History & Tracking Page
class HistoryTrackingPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.2, 0.1, 0.4, 1)  # Dark Blue Color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        layout = BoxLayout(orientation='vertical', spacing=5, padding=[10, 10, 10, 10])  # Reduced spacing and added padding
        self.tasks = load_tasks_from_file()
        # Header
        header = Label(text="History & Tracking", font_size=24, size_hint=(1, 0.1))  # Adjusted font size for smaller screen
        layout.add_widget(header)

        # Task-related buttons
        task_button_area = GridLayout(cols=3, size_hint=(1, 0.15), spacing=5)  # Use GridLayout for better alignment
        current_tasks_button = Button(text="Current Tasks", size_hint=(1, 1), background_color=(0.4, 0.7, 0.8, 1), color=(1, 1, 1, 1))  # Soft Teal
        completed_tasks_button = Button(text="Completed Tasks", size_hint=(1, 1), font_size=13, background_color=(0.7, 0.6, 0.9, 1), color=(1, 1, 1, 1))  # Lavender
        task_history_button = Button(text="Task History", size_hint=(1, 1), background_color=(0.5, 0.8, 0.5, 1), color=(1, 1, 1, 1)) 
        task_button_area.add_widget(current_tasks_button)
        task_button_area.add_widget(completed_tasks_button)
        task_button_area.add_widget(task_history_button)
        layout.add_widget(task_button_area)

        # Chart-related buttons
        # Add buttons to generate charts
        completion_ratio_chart_button = Button(text="Completion Ratio Chart", size_hint=(1, None), height=50,background_color=(0.9, 0.7, 0.5, 1), color=(1, 1, 1, 1))
        total_completion_over_time_chart_button = Button(text="Total Completion Over Time", size_hint=(1, None), height=50, background_color=(0.6, 0.9, 0.6, 1), color=(1, 1, 1, 1))  # Soft Lime
        daily_completion_trends_chart_button = Button(text="Daily Completion Trends", size_hint=(1, None), background_color=(0.6, 0.8, 0.9, 1), color=(1, 1, 1, 1))  # Sky Blue
        task_types_breakdown_chart_button = Button(text="Task Types Breakdown", size_hint=(1, None), height=50, background_color=(0.8, 0.5, 0.8, 1), color=(1, 1, 1, 1))  # Soft Purple
        cumulative_completion_history_chart_button = Button(text="Cumulative Completion History", size_hint=(1, None), height=50, background_color=(0.8, 0.7, 0.5, 1), color=(1, 1, 1, 1))  # Earthy Gold
       

        # Bind events for buttons
        current_tasks_button.bind(on_release=self.show_current_tasks)
        completed_tasks_button.bind(on_release=self.show_completed_tasks)
        task_history_button.bind(on_release=self.show_task_history)
         
        # Bind events for buttons
        completion_ratio_chart_button.bind(on_release=lambda _: self.show_chart("Completion Ratio Chart"))
        total_completion_over_time_chart_button.bind(on_release=lambda _: self.show_chartp("Total Completion Over Time"))
        daily_completion_trends_chart_button.bind(on_release=lambda _: self.show_chartz("Daily Completion Trends"))
        task_types_breakdown_chart_button.bind(on_release=lambda _: self.plot_task_types_breakdown(self.tasks))
        cumulative_completion_history_chart_button.bind(on_release=lambda _: self.plot_cumulative_completion_history())



         # Add the buttons to layout
        layout.add_widget(completion_ratio_chart_button)
        layout.add_widget(total_completion_over_time_chart_button)
        layout.add_widget(daily_completion_trends_chart_button)
        layout.add_widget(task_types_breakdown_chart_button)
        layout.add_widget(cumulative_completion_history_chart_button)
        
        # Area for tasks
        self.task_display_area = ScrollView(size_hint=(1, 0.55))  # Reduced height to fit the screen
        self.task_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.task_list.bind(minimum_height=self.task_list.setter('height'))
        self.task_display_area.add_widget(self.task_list)
        layout.add_widget(self.task_display_area)

        # Navigation Bar
        layout.add_widget(NavigationBar())

        # Add the entire layout to the screen
        self.add_widget(layout)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def show_chart(self, title):
        data = self.get_chart_data(title)
        popup = ChartPopup(title, data)
        popup.open()
    
    def show_current_tasks(self, instance):
        self.task_list.clear_widgets()
        tasks = load_tasks_from_file()
        current_tasks = [task for task in tasks if not task["completed"]]
        
        for task in current_tasks:
            task_label = Button(
                text=f"{task['name']} - Type: {task['type']} - Progress: {format(task['progress'], '.1f')}%",
                size_hint_y=None, height=40,
                background_color=(0.4, 0.7, 0.8, 1),  # Soft Teal
                color=(1, 1, 1, 1),  # White text for contrast
                on_release=lambda _, t=task: self.show_task_details(t)
            )
            self.task_list.add_widget(task_label)

    def show_completed_tasks(self, instance):
        self.task_list.clear_widgets()
        tasks = load_tasks_from_file()
        completed_tasks = [task for task in tasks if task["completed"]]
        
        for task in completed_tasks:
            completion_time = task.get("completion_time", "N/A")  # Safely get completion_time
            task_label = Button(
                text=f"{task['name']} - Type: {task['type']}\n - Completed: {completion_time}",
                size_hint_y=None, height=40,
                background_color=(0.7, 0.6, 0.9, 1),  # Lavender
                color=(1, 1, 1, 1),  # White text for contrast
                font_size=14,  # Adjusted font size
                on_release=lambda _, t=task: self.show_task_details(t)
            )
            self.task_list.add_widget(task_label)

    def show_task_history(self, instance):
        self.task_list.clear_widgets()
        tasks = load_tasks_from_file()
        
        for task in tasks:
            status = "Completed" if task["completed"] else "In Progress"
            completion_time = task.get("completion_time", "N/A")  # Safely get completion_time
            
            task_label = Button(
                text=f"{task['name']} - Type: {task['type']} - Status: {status} \n- Progress: {format(task['progress'], '.1f')}% - Completed: {completion_time}",
                size_hint_y=None, height=40,
                background_color=(0.5, 0.8, 0.5, 1),  # Mint Green
                color=(1, 1, 1, 1),  # White text for contrast
                font_size=14,  # Adjusted font size
                on_release=lambda _, t=task: self.show_task_details(t)
            )
            self.task_list.add_widget(task_label)

    
    def show_task_details(self, task):
        popup = TaskDetailsPopup(task)
        popup.open()        

    def get_chart_data(self, title):
        # Handle cases where tasks are structured data (list of dicts)
        if isinstance(self.tasks, list) and all(isinstance(task, dict) for task in self.tasks):
            if title == "Completion Ratio Chart":
                    
                completed = sum(1 for task in self.tasks if task.get("completed", False))
                incomplete = len(self.tasks) - completed
                return [completed, incomplete]
            elif title in ["Total Completion Over Time", "Daily Completion Trends"]:
                completion_dates = [task.get("completion_date") for task in self.tasks if task.get("completed", False)]
                return self.aggregate_by_date(completion_dates)
            elif title == "Task Types Breakdown":
                daily_tasks = sum(1 for task in self.tasks if task.get("type") == "Daily")
                one_time_tasks = len(self.tasks) - daily_tasks
                return [daily_tasks, one_time_tasks]
            elif title == "Cumulative Completion History":
                return [task.get("progress", 0) for task in self.tasks]
        return []
    def get_start_date(self,tasks):
    # Find the earliest start time from all tasks
        start_dates = [task.get('start_time') for task in tasks if 'start_time' in task]
        start_dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in start_dates]
        return min(start_dates) if start_dates else None
    def get_days_since_first_task(self,start_date):
        today = datetime.now()
        delta = today - start_date
        return delta.days
    def get_completed_tasks_by_date(self,tasks, start_date):
    # Collect tasks that are marked as completed and calculate their completion date
        completed_tasks = [
            task for task in tasks if task.get("completed") and "completion_time" in task
    ]
    
    # Store completion data for plotting
        task_completion_data = []
        for task in completed_tasks:
            completion_time = datetime.strptime(task["completion_time"], "%Y-%m-%d %H:%M:%S")
            days_since_start = (completion_time - start_date).days
            task_completion_data.append(days_since_start)
    
    # Sort the completion dates and return the aggregated data
        task_completion_data.sort()
        return task_completion_data
    def plot_total_completion_over_time(self, tasks):
        start_date = self.get_start_date(tasks)
        if not start_date:
            print("No tasks with start date found.")
            return

        days_since_first_task = self.get_days_since_first_task(start_date)
        completed_tasks = self.get_completed_tasks_by_date(tasks, start_date)

    # Generate the X-axis (time in days) and Y-axis (total completed tasks up to that day)
        x_data = list(range(1, days_since_first_task + 1))
        y_data = [0] * len(x_data)

        for day in completed_tasks:
            if day <= len(y_data):
                y_data[day - 1] += 1

    # Calculate cumulative completed tasks for Y-axis
        y_data_cumulative = [sum(y_data[:i + 1]) for i in range(len(y_data))]

    # Create a temporary file to save the plot
        temp_file = "total_completion_over_time.png"

    # Plot the line chart
        plt.plot(x_data, y_data_cumulative, marker='o', linestyle='-', color='b', label='Total Tasks Completed')
        plt.title("Total Completion Over Time", fontsize=16, fontweight='bold')
        plt.xlabel("Time (days)", fontsize=14)
        plt.ylabel("Total Completed Tasks", fontsize=14)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

    # Save the plot as an image
        plt.savefig(temp_file, bbox_inches='tight', dpi=300)
        plt.close()

    # Display the image in a Kivy popup
        popup = Popup(title="Total Completion Over Time",
                  size_hint=(0.9, 0.9),
                  auto_dismiss=True)

    # Create the layout
        layout = BoxLayout(orientation="vertical")

    # Add the scrollable image
        scrollview = ScrollView(size_hint=(1, 0.8))
        chart_image = Image(source=temp_file, allow_stretch=True, size_hint=(None, None))
        initial_width = chart_image.texture_size[0] * 0.2  # 70% of the original size
        initial_height = chart_image.texture_size[1] * 0.2  # 70% of the original size
        chart_image.size = (initial_width, initial_height)
        scrollview.add_widget(chart_image)

    # Zoom in and out buttons
        zoom_controls = BoxLayout(size_hint=(1, 0.1))
        zoom_in_button = Button(text="Zoom In")
        zoom_out_button = Button(text="Zoom Out")

    # Zoom functionality
        def zoom_in(instance):
            chart_image.size = (chart_image.width * 1.2, chart_image.height * 1.2)

        def zoom_out(instance):
            chart_image.size = (chart_image.width * 0.8, chart_image.height * 0.8)

        zoom_in_button.bind(on_release=zoom_in)
        zoom_out_button.bind(on_release=zoom_out)

        zoom_controls.add_widget(zoom_in_button)
        zoom_controls.add_widget(zoom_out_button)

    # Close button
        close_button = Button(text="Close", size_hint=(1, 0.1))
        close_button.bind(on_release=popup.dismiss)

    # Add components to the layout
        layout.add_widget(scrollview)
        layout.add_widget(zoom_controls)
        layout.add_widget(close_button)

        popup.content = layout
        popup.open()

    # Delete the temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

    def show_chartp(self, title):
        data = self.get_chart_data(title)  # Get the chart data
    
    # Check if the title is "Total Completion Over Time"
        if title == "Total Completion Over Time":
        # Only plot the "Total Completion Over Time" chart and not open a popup
            self.plot_total_completion_over_time(self.tasks)
        else:
        # For all other chart types, show the popup with the chart data
            popup = ChartPopup(title, data)
            popup.open()

    def aggregate_by_date(self, dates):
        """Helper method to aggregate task counts by date."""
        from collections import Counter
        date_counts = Counter(dates)
        sorted_dates = sorted(date_counts.items())  # Sort by date
        return [count for _, count in sorted_dates]
    
    def plot_daily_completion_trends_data(self,tasks):
        today = datetime.now()
        ten_days_ago = today - timedelta(days=10)

    # Collect completed tasks' completion times within the last 10 days
        completion_dates = []
        for task in tasks:
            if task.get("completed") and "completion_time" in task:
                try:
                    completion_time = datetime.strptime(task["completion_time"], "%Y-%m-%d %H:%M:%S")
                    if completion_time > ten_days_ago:
                        completion_dates.append(completion_time)
                except ValueError as e:
                    print(f"Invalid completion_time format for task: {task.get('name')}, Error: {e}")

    # Aggregate the completion dates by day
        date_counts = {}
        for date in completion_dates:
            date_str = date.strftime("%Y-%m-%d")  # Format date as string
            date_counts[date_str] = date_counts.get(date_str, 0) + 1

    # Debug: Check the aggregated counts

    # Prepare data for the bar chart
        sorted_dates = sorted(date_counts.keys())
        sorted_counts = [date_counts[date] for date in sorted_dates]

    # Plot the bar chart
        temp_file = "daily_completion_trends.png"
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(sorted_dates, sorted_counts, color='skyblue', edgecolor='black')
        ax.set_title("Daily Completion Trends", fontsize=16, fontweight='bold')
        ax.set_xlabel("Date", fontsize=14)
        ax.set_ylabel("Number of Tasks Completed", fontsize=14)
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()

    # Save the plot
        plt.savefig(temp_file, bbox_inches='tight', dpi=300)
        plt.close(fig)

        return temp_file



    def show_daily_completion_trends_popup(self, temp_file):
        """
        Create and show a popup with a scrollable chart image and zoom functionality.
        """
    # Create the popup layout
        popup = Popup(title="Daily Completion Trends",
                  size_hint=(0.9, 0.9),
                  auto_dismiss=True)

        layout = BoxLayout(orientation="vertical")

    # Create the scrollable image widget
        scrollview = ScrollView(size_hint=(1, 0.8))
        chart_image = Image(source=temp_file, allow_stretch=True, size_hint=(None, None))
        initial_width = chart_image.texture_size[0] * 0.2  # 0% of the original size
        initial_height = chart_image.texture_size[1] * 0.2  # 20% of the original size
        chart_image.size = (initial_width, initial_height)
        scrollview.add_widget(chart_image)

    # Zoom functionality (Zoom In/Out)
        zoom_controls = BoxLayout(size_hint=(1, 0.1))
        zoom_in_button = Button(text="Zoom In")
        zoom_out_button = Button(text="Zoom Out")

        def zoom_in(instance):
            chart_image.size = (chart_image.width * 1.2, chart_image.height * 1.2)

        def zoom_out(instance):
            chart_image.size = (chart_image.width * 0.8, chart_image.height * 0.8)

        zoom_in_button.bind(on_release=zoom_in)
        zoom_out_button.bind(on_release=zoom_out)
        chart_description = Label(
            text=(
                "Type: Doughnut Chart\n"
                "Details:\n"
                "- Visualizes the proportion of tasks categorized\n as daily versus one-time tasks.\n"
                "- Offers insight into the distribution\n of task types for better task management."
        ),
            font_size=12,
            size_hint_y=None,
            height=50,
            valign='middle',
            halign='center'
    )
        zoom_controls.add_widget(zoom_in_button)
        zoom_controls.add_widget(zoom_out_button)

    # Close button for the popup
        close_button = Button(text="Close", size_hint=(1, 0.1))
        close_button.bind(on_release=popup.dismiss)

    # Add all components to the layout
        layout.add_widget(scrollview)
        layout.add_widget(zoom_controls)
        layout.add_widget(close_button)
        layout.add_widget(chart_description)
        popup.content = layout
        popup.open()

    # Cleanup the temporary file after displaying
        os.remove(temp_file)
    def show_chartz(self, title):
        data = self.get_chart_data(title)  # Get the chart data

    # Check if the title is "Daily Completion Trends"
        if title == "Daily Completion Trends":
            temp_file = self.plot_daily_completion_trends_data(self.tasks)  # Generate the chart
            self.show_daily_completion_trends_popup(temp_file)  # Show the popup with the chart
        else:
        # For all other chart types, show the popup with the chart data
            popup = ChartPopup(title, data)
            popup.open()
    def plot_task_types_breakdown(self, tasks):
    # Count the number of daily and one-time tasks
        daily_tasks = sum(1 for task in tasks if task.get("type") == "Daily")
        one_time_tasks = sum(1 for task in tasks if task.get("type") == "One-Time")
    
    # Data for the chart
        data = [daily_tasks, one_time_tasks]
        labels = ["Daily Tasks", "One-Time Tasks"]
    
    # Generate the doughnut chart
        temp_file = "task_types_breakdown_doughnut_chart.png"
        fig, ax = plt.subplots(figsize=(8, 6))  # Set the size of the figure
    
    # Plot the doughnut chart
        wedges, texts, autotexts = ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.4))

    # Title and styling
        ax.set_title("Task Types Breakdown", fontsize=16, fontweight='bold')
    
    # Save the chart as an image
        plt.tight_layout()
        plt.savefig(temp_file, bbox_inches='tight', dpi=300)
        plt.close()

    # Display the chart in a Kivy Popup
        popup = Popup(title="Task Types Breakdown",
                  size_hint=(0.9, 0.9),
                  auto_dismiss=True)

    # Create layout for the Popup
        layout = BoxLayout(orientation="vertical")

    # Add the scrollable image
        scrollview = ScrollView(size_hint=(1, 0.8))
        chart_image = Image(source=temp_file, allow_stretch=True, size_hint=(None, None))
        initial_width = chart_image.texture_size[0] * 0.2  # 70% of the original size
        initial_height = chart_image.texture_size[1] * 0.2  # 70% of the original size
        chart_image.size = (initial_width, initial_height)
        scrollview.add_widget(chart_image)

    # Zoom controls
        zoom_controls = BoxLayout(size_hint=(1, 0.1))
        zoom_in_button = Button(text="Zoom In")
        zoom_out_button = Button(text="Zoom Out")

    # Zoom functionality
        def zoom_in(instance):
            chart_image.size = (chart_image.width * 1.2, chart_image.height * 1.2)

        def zoom_out(instance):
            chart_image.size = (chart_image.width * 0.8, chart_image.height * 0.8)

        zoom_in_button.bind(on_release=zoom_in)
        zoom_out_button.bind(on_release=zoom_out)
        chart_description = Label(
            text=(
                "Type: Line Chart\n"
                "Details:\n"
                "- X-axis: Time progression (e.g., days, weeks, or months)\n from the start of task tracking.\n"
                "- Y-axis: Cumulative total of tasks completed.\n"
                "- Highlights trends over time, making it\n easier to identify patterns in task completion."
        ),
            font_size=12,
            size_hint_y=None,
            height=50,
            valign='middle',
            halign='center'
    )
        zoom_controls.add_widget(zoom_in_button)
        zoom_controls.add_widget(zoom_out_button)

    # Close button
        close_button = Button(text="Close", size_hint=(1, 0.1))
        close_button.bind(on_release=popup.dismiss)

    # Add components to the layout
        layout.add_widget(scrollview)
        layout.add_widget(zoom_controls)
        layout.add_widget(close_button)
        layout.add_widget(chart_description)
        popup.content = layout
        popup.open()

    # Cleanup temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
    def load_tasks_from_json(self, file_path):
        """Load task data from the specified JSON file."""
        with open(file_path, 'r') as file:
            tasks = json.load(file)
        return tasks

    def extract_completion_data(self, tasks):
        """Extract completion data from tasks."""
        completion_data = {}

        for task in tasks:
            if task["type"] == "Daily":  # We assume Daily tasks have progress over time
                task_name = task["name"]
                completion_data[task_name] = []

                # Simulate completion data for each day (here we just mock some values, you can adjust this logic)
                days_completed = int(task["progress"] / 10)  # Assuming progress is in percentage
                progress_per_day = task["progress"] / (days_completed if days_completed else 1)

                # Fill in progress data for each day
                for i in range(days_completed):
                    completion_data[task_name].append(progress_per_day * (i + 1))
            else:
                completion_data[task["name"]] = [task["progress"]]  # For One-Time tasks, assume single progress

        return completion_data

    def plot_cumulative_completion_history(self):
        tasks = self.tasks  # Get tasks loaded from JSON
        if len(tasks) > 10:
            tasks = tasks[-10:]  # Keep only the last 10 tasks

        completion_data = self.extract_completion_data(tasks)  # Extract completion data

        task_names = list(completion_data.keys())
    # Convert values to a uniform 2D array by padding shorter sequences with zeros
        max_days = max(len(data) for data in completion_data.values())  # Find the longest sequence
        completion_percentages = np.array([data + [0] * (max_days - len(data)) for data in completion_data.values()])

    # Create stacked bar chart
        temp_file = "cumulative_completion_history_chart.png"
        fig, ax = plt.subplots(figsize=(8, 6))  # Set the size of the figure

    # Plot each task's cumulative completion as stacked bars
        ax.bar(task_names, completion_percentages[:, 0], label="Day 1")
        for i in range(1, completion_percentages.shape[1]):
            ax.bar(task_names, completion_percentages[:, i], bottom=completion_percentages[:, i - 1], label=f"Day {i + 1}")

    # Title and labels
        ax.set_title("Cumulative Completion History (Last 10 Tasks)", fontsize=16, fontweight='bold')
        ax.set_xlabel("Task Names")
        ax.set_ylabel("Completion Percentage")

    # Add legend
        ax.legend(title="Days", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save the chart as an image
        plt.tight_layout()
        plt.savefig(temp_file, bbox_inches='tight', dpi=300)
        plt.close()

    # Display the chart in a Kivy Popup
        popup = Popup(title="Cumulative Completion History",
                  size_hint=(0.9, 0.9),
                  auto_dismiss=True)

    # Create layout for the Popup
        layout = BoxLayout(orientation="vertical")

    # Add the scrollable image
        scrollview = ScrollView(size_hint=(1, 0.8))
        chart_image = Image(source=temp_file, allow_stretch=True, size_hint=(None, None))

    # Set initial zoom-out size (adjust as needed)
        initial_width = chart_image.texture_size[0] * 0.7  # 70% of the original size
        initial_height = chart_image.texture_size[1] * 0.7  # 70% of the original size
        chart_image.size = (initial_width, initial_height)

        scrollview.add_widget(chart_image)

    # Zoom controls
        zoom_controls = BoxLayout(size_hint=(1, 0.1))
        zoom_in_button = Button(text="Zoom In")
        zoom_out_button = Button(text="Zoom Out")

        # Zoom functionality
        def zoom_in(instance):
            chart_image.size = (chart_image.width * 1.2, chart_image.height * 1.2)

        def zoom_out(instance):
            chart_image.size = (chart_image.width * 0.8, chart_image.height * 0.8)

        zoom_in_button.bind(on_release=zoom_in)
        zoom_out_button.bind(on_release=zoom_out)

        # Chart description
        chart_description = Label(
            text=(
                "Type: Stacked Bar Chart\n"
                "Details:\n"
                "- X-axis: Names or categories of the last 10 tasks.\n"
                "- Y-axis: Completion percentages for each day,\n"
                "  presented as stacked bars.\n"
                "- Displays cumulative progress over time."
        ),
            font_size=12,
            size_hint_y=None,
            height=50,
            valign='middle',
            halign='center'
    )
        zoom_controls.add_widget(zoom_in_button)
        zoom_controls.add_widget(zoom_out_button)

    # Close button
        close_button = Button(text="Close", size_hint=(1, 0.1))
        close_button.bind(on_release=popup.dismiss)

    # Add components to the layout
        layout.add_widget(scrollview)
        layout.add_widget(zoom_controls)
        layout.add_widget(chart_description)
        layout.add_widget(close_button)

        popup.content = layout
        popup.open()

    # Cleanup temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
        
class ChartsAnalyticsPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Add buttons for each chart
        self.add_chart_buttons(layout)

        # Add the layout to the screen
        self.add_widget(layout)
    
    def add_chart_buttons(self, layout):
        # Add buttons to generate charts
        completion_ratio_chart_button = Button(text="Completion Ratio Chart", size_hint=(1, None), height=50)
        total_completion_over_time_chart_button = Button(text="Total Completion Over Time", size_hint=(1, None), height=50)
        daily_completion_trends_chart_button = Button(text="Daily Completion Trends", size_hint=(1, None), height=50)
        task_types_breakdown_chart_button = Button(text="Task Types Breakdown", size_hint=(1, None), height=50)
        cumulative_completion_history_chart_button = Button(text="Cumulative Completion History", size_hint=(1, None), height=50)
        
        # Bind events for buttons
        completion_ratio_chart_button.bind(on_release=lambda _: self.show_chart("Completion Ratio Chart", self.get_chart_data("Completion Ratio Chart")))
        total_completion_over_time_chart_button.bind(on_release=lambda _: self.show_chart("Total Completion Over Time", [10, 20, 30, 40, 50]))
        daily_completion_trends_chart_button.bind(on_release=lambda _: self.show_chart("Daily Completion Trends", [5, 8, 12, 15, 20]))
        task_types_breakdown_chart_button.bind(on_release=lambda _: self.show_chart("Task Types Breakdown", [60, 40]))
        cumulative_completion_history_chart_button.bind(on_release=lambda _: self.show_chart("Cumulative Completion History", [5, 10, 15, 20, 25]))
        
        # Add the buttons to layout
        layout.add_widget(completion_ratio_chart_button)
        layout.add_widget(total_completion_over_time_chart_button)
        layout.add_widget(daily_completion_trends_chart_button)
        layout.add_widget(task_types_breakdown_chart_button)
        layout.add_widget(cumulative_completion_history_chart_button)

    def calculate_completion_ratio(tasks):
        completed = sum(1 for task in tasks if task["completed"])
        incomplete = len(tasks) - completed
        return [completed, incomplete]

    def calculate_completion_over_time(tasks):
        timeline = {}
        for task in tasks:
            date = task["completion_date"]  # Ensure tasks include completion_date
            if date:
                timeline[date] = timeline.get(date, 0) + 1
        return list(timeline.values())

    
    def show_chart(self, title, data):
        popup = ChartPopup(title, data)
        popup.open()

class ChartPopup(Popup):
    def __init__(self, title, tasks, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.size_hint = (0.9, 0.9)
        self.tasks = tasks

        # Initialize zoom scale
        self.zoom_scale = 1.0

        # Create chart and description content
        content = self.create_chart_content(title)
        self.content = content

    def create_chart_content(self, title):
        temp_file = f"{title.replace(' ', '_').lower()}.png"

    # Generate chart based on the title and tasks
        fig, ax = plt.subplots(figsize=(10, 8))  # Larger figure size for better visibility
        data = self.get_chart_data(title) 

    # Validate data to prevent matplotlib errors
        if not data or all(value <= 0 for value in data):
            data = [1, 1]  # Default placeholder to avoid division by zero
            warnings.warn("Data for chart is invalid or empty; using placeholder values.")

        if title == "Completion Ratio Chart":
            completed, incomplete = data[0], data[1]

        # Calculate the total count of tasks for correct percentage calculation
            total = completed + incomplete
            if total == 0:  # Prevent division by zero
                completed_percentage = 0
                incomplete_percentage = 0
            else:
                completed_percentage = (completed / total) * 100
                incomplete_percentage = (incomplete / total) * 100

            
        # Pie chart with calculated percentages
            ax.pie([completed_percentage, incomplete_percentage], 
               labels=["Completed", "Incomplete"], 
               autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
        
        elif title == "Total Completion Over Time":
            ax.plot(data, marker='o', linestyle='-', color='b', label='Completion Over Time')
            ax.set_title("Total Tasks Completed Over Time", fontsize=16, fontweight='bold')
            ax.set_xlabel("Time (days)", fontsize=14)
            ax.set_ylabel("Total Tasks", fontsize=14)
        
        elif title == "Daily Completion Trends":
            self.plot_daily_completion_trends(self.tasks)  # Call the plot function for daily completion trends
            return

        elif title == "Task Types Breakdown":
            ax.pie(data, labels=["Daily Tasks", "One-time Tasks"], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')

        elif title == "Cumulative Completion History":
            ax.bar(range(len(data)), data, color='purple', label='Cumulative Completion')
            ax.set_title("Cumulative Completion History", fontsize=16, fontweight='bold')
            ax.set_xlabel("Task Names", fontsize=14)
            ax.set_ylabel("Completion Percentage", fontsize=14)

    # Save chart to a temporary file with high DPI for better clarity
        plt.tight_layout()
        plt.savefig(temp_file, bbox_inches='tight', dpi=300)
        plt.close(fig)

    # Create an Image widget to display the chart
        chart_image = Image(source=temp_file, allow_stretch=True, size_hint=(None, None))
        chart_image.size = (400, 800)  # Set a reasonable size for the image

    # Wrap the image in a ScrollView for scrolling
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(chart_image)
        scroll_view.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
    
    # Zoom buttons
        zoom_in_button = Button(
            text="Zoom In",
            size_hint=(None, None),
            height=50,
            width=100,
            on_release=lambda x: self.zoom_chart(chart_image, scroll_view, zoom_in=True)
    )

        zoom_out_button = Button(
            text="Zoom Out",
            size_hint=(None, None),
            height=50,
            width=100,
            on_release=lambda x: self.zoom_chart(chart_image, scroll_view, zoom_in=False)
    )

    # Chart description
        chart_description = Label(
            text=self.get_chart_description(title, data),
            font_size=12,
            size_hint_y=None,
            height=50,
            valign='middle',
            halign='center'
    )

    # Back button to close popup
        back_button = Button(
            text="Back",
            size_hint=(1, None),
            height=50,
            on_release=self.dismiss
    )

    

    # Layout for chart, buttons, and description
        layout = BoxLayout(orientation='vertical')
    
        layout.add_widget(scroll_view)  # Add scroll view for the chart
        layout.add_widget(chart_description)  # Add description
        layout.add_widget(zoom_in_button)  # Add zoom in button
        layout.add_widget(zoom_out_button)  # Add zoom out button
        layout.add_widget(back_button)  # Add back button
        # Cleanup the temp file after the display
        os.remove(temp_file)
        return layout
    
    def update_chart(self):
        """This method will update the chart when data changes."""
        # Recreate the content with the updated data
        content = self.create_chart_content(self.title)
        self.content = content
        self.update_chart()

    def zoom_chart(self, chart_image, scroll_view, zoom_in):
        """Handles zooming in and out of the chart."""
        # Adjust the zoom scale
        if zoom_in:
            self.zoom_scale *= 1.1  # Increase zoom scale by 10%
        else:
            self.zoom_scale /= 1.1  # Decrease zoom scale by 10%

        # Apply zoom scale to the image
        new_width = 400 * self.zoom_scale
        new_height = 800 * self.zoom_scale
        chart_image.size = (new_width, new_height)

        # Update the scroll_view size so it can scroll properly
        scroll_view.scroll_wheel_distance = new_height  # Adjust scroll height

        # If the image becomes too large for the window, set the max scrollable area
        scroll_view.height = new_height
        scroll_view.width = new_width


    def get_chart_data(self, title):
        print(f"Debug: Tasks data type = {type(self.tasks)}, Content = {self.tasks}")

        if isinstance(self.tasks, list):
            if all(isinstance(task, int) for task in self.tasks):
            # Handle list of integers
                if title == "Completion Ratio Chart":
                    completed = self.tasks[0] if len(self.tasks) > 0 else 0
                    incomplete = self.tasks[1] if len(self.tasks) > 1 else 0
                    
                    return [completed, incomplete]
            elif title in ["Total Completion Over Time", "Daily Completion Trends"]:
                completion_dates = [task.get("completion_date") for task in self.tasks if task.get("completed", False)]
                return self.aggregate_by_date(completion_dates)
            elif title == "Task Types Breakdown":
                daily_tasks = sum(1 for task in self.tasks if task.get("type") == "Daily")
                one_time_tasks = len(self.tasks) - daily_tasks
                return [daily_tasks, one_time_tasks]
            elif title == "Cumulative Completion History":
                return [task.get("progress", 0) for task in self.tasks]
        return []

    def aggregate_by_date(self, dates):
        """Helper method to aggregate task counts by date."""
        from collections import Counter
        date_counts = Counter(dates)
        sorted_dates = sorted(date_counts.items())  # Sort by date
        return [count for _, count in sorted_dates]

    def get_chart_description(self, title, data):
        if title == "Completion Ratio Chart":
            return (
                "Type: Pie Chart\n"
                "Details:\n"
                "- Displays the proportion of completed vs. incomplete tasks.\n"
                "- Shows percentage values for each category, providing a quick overview of task completion status."
        )
        elif title == "Total Completion Over Time":
            return (
                "Type: Line Chart\n"
                "Details:\n"
                "- X-axis: Time progression (e.g., days, weeks, or months) from the start of task tracking.\n"
                "- Y-axis: Cumulative total of tasks completed.\n"
                "- Highlights trends over time, making it easier to identify patterns in task completion."
        )
        elif title == "Daily Completion Trends":
            return (
                "Type: Bar Chart\n"
                "Details:\n"
                "- X-axis: Dates for the last 10 days.\n"
                "- Y-axis: Number of tasks completed on each specific day.\n"
                "- Useful for analyzing recent daily performance and identifying spikes or dips in productivity."
        )
        elif title == "Task Types Breakdown":
            return (
                "Type: Doughnut Chart\n"
                "Details:\n"
                "- Visualizes the proportion of tasks categorized as daily versus one-time tasks.\n"
                "- Offers insight into the distribution of task types for better task management."
        )
        elif title == "Cumulative Completion History":
            return (
                "Type: Stacked Bar Chart\n"
                "Details:\n"
                "- X-axis: Names or categories of tasks.\n"
                "- Y-axis: Completion percentages for each day, presented as stacked bars.\n"
                "- Clearly displays how progress accumulates over time, highlighting contributions toward overall completion goals."
        )
        else:
            return "No description available."
   
class NavigationBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 50

        # Create buttons
        home_button = Button(
            text="Home",
            background_color=(0.4, 0.2, 0.6, 1),  # Royal Purple
            color=(1, 1, 1, 1)  # White text for contrast
        )
        history_button = Button(
            text="History",
            background_color=(1, 0.84, 0, 1),  # Royal Gold
            color=(1, 1, 1, 1)  # White text for contrast
        )

        # Bind button actions
        home_button.bind(on_release=self.go_home)
        history_button.bind(on_release=self.go_history)

        # Add buttons to the layout
        self.add_widget(home_button)
        self.add_widget(history_button)

    def go_home(self, instance):
        # Navigate to the home screen
        App.get_running_app().root.current = 'home'

    def go_history(self, instance):
        # Navigate to the history screen
        App.get_running_app().root.current = 'history'


  

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.2, 0.6, 0.86, 1)
        self.color = (1, 1, 1, 1)
        self.font_name = 'Roboto'
        self.font_size = 18
        self.size_hint = (None, None)
        self.size = (200, 50)
        self.bind(on_enter=self.on_hover, on_leave=self.on_leave)
    
    def on_hover(self, *args):
        self.background_color = (0.3, 0.7, 0.96, 1)
    
    def on_leave(self, *args):
        self.background_color = (0.2, 0.6, 0.86, 1)

class AnimatedProgressBar(ProgressBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max = 100
        self.value = 0
        self.animate_progress()
        
    
    def animate_progress(self):
        anim = Animation(value=self.max, duration=2)
        anim.bind(on_complete=self.on_animation_complete)
        anim.start(self)
    
        
    def on_animation_complete(self, *args):
        app = App.get_running_app()
        app.root.current = 'home'    

class SemiTransparentPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background = 'path/to/semi_transparent_background.png'  

class TaskDetailsPopup(Popup):
    def __init__(self, task, **kwargs):
        super().__init__(**kwargs)
        self.title = "Task Details"
        self.size_hint = (0.8, 0.6)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=[10, 10, 10, 10])

        layout.add_widget(Label(text=f"Name: {task['name']}", size_hint=(1, 0.1)))
        layout.add_widget(Label(text=f"Type: {task['type']}", size_hint=(1, 0.1)))
        layout.add_widget(Label(text=f"Duration: {task.get('duration', 'N/A')}", size_hint=(1, 0.1)))
        layout.add_widget(Label(text=f"Progress: {format(task['progress'], '.1f')}%", size_hint=(1, 0.1)))
        layout.add_widget(Label(text=f"Start Time: {task.get('start_time', 'N/A')}", size_hint=(1, 0.1)))

        if task.get("completion_time"):
            layout.add_widget(Label(text=f"Completion Time: {task['completion_time']}", size_hint=(1, 0.1)))
        
        notes_button = Button(text="View Task Notes", size_hint=(1, 0.2))
        notes_button.bind(on_release=lambda instance: self.show_task_notes(task))
        layout.add_widget(notes_button)

        close_button = Button(text="Close", size_hint=(1, 0.2))
        close_button.bind(on_release=self.dismiss)
        layout.add_widget(close_button)

        self.content = layout

    def show_task_notes(self, task):
        notes_popup = TaskNotesPopup(task)
        notes_popup.open()

class TaskNotesPopup(Popup):
    def __init__(self, task, **kwargs):
        super().__init__(**kwargs)
        self.title = "Task Notes"
        self.size_hint = (0.8, 0.6)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=[10, 10, 10, 10])

        notes_scroll = ScrollView(size_hint=(1, 0.8), bar_width=10, bar_color=[0.2, 0.2, 0.2, 1], bar_inactive_color=[0.5, 0.5, 0.5, 1], scroll_type=['bars', 'content'])
        notes_label = Label(text=f"{task.get('notes', 'N/A')}", size_hint=(None, None), size=(400, 200), text_size=(400, None), valign='top')
        notes_scroll.add_widget(notes_label)
        layout.add_widget(notes_scroll)

        close_button = Button(text="Close", size_hint=(1, 0.2))
        close_button.bind(on_release=self.dismiss)
        layout.add_widget(close_button)

        self.content = layout
        
        
class TaskDetailsScreen(Screen):
    
    
    def __init__(self, task, home_page, **kwargs):
        super().__init__(**kwargs)
        self.task = task
        self.home_page = home_page

        layout = BoxLayout(orientation="vertical", spacing=15, padding=20)

        # Title
        title = Label(
            text="Task Details",
            font_size="24sp",
            bold=True,
            size_hint=(1, 0.1),
            halign="center",
            valign="middle",
        )
        layout.add_widget(title)

        # Task details with better alignment
        details_layout = GridLayout(cols=2, spacing=10, size_hint=(1, 0.7))
        details_layout.add_widget(Label(text="Name:", bold=True))
        details_layout.add_widget(Label(text=f"{task['name']}"))
        details_layout.add_widget(Label(text="Type:", bold=True))
        details_layout.add_widget(Label(text=f"{task['type']}"))
        details_layout.add_widget(Label(text="Duration:", bold=True))
        details_layout.add_widget(Label(text=f"{task.get('duration', 'N/A')}"))
        details_layout.add_widget(Label(text="Notes:", bold=True))
        details_layout.add_widget(Label(text=f"{task.get('notes', 'N/A')}"))
        details_layout.add_widget(Label(text="Progress:", bold=True))
        details_layout.add_widget(Label(text=f"{task['progress']}%"))
        details_layout.add_widget(Label(text="Start Time:", bold=True))
        details_layout.add_widget(Label(text=f"{task.get('start_time', 'N/A')}"))
        layout.add_widget(details_layout)

        # Buttons
        button_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        back_button = Button(text="Back", size_hint=(0.3, 1))
        back_button.bind(on_release=self.go_back)
        button_layout.add_widget(back_button)

        edit_button = Button(text="Edit Task", size_hint=(0.3, 1))
        edit_button.bind(on_release=lambda instance: self.edit_task())
        button_layout.add_widget(edit_button)

        delete_button = Button(text="Delete Task", size_hint=(0.3, 1))
        delete_button.bind(on_release=lambda instance: self.delete_task())
        button_layout.add_widget(delete_button)

        layout.add_widget(button_layout)
        self.add_widget(layout)

    

    def edit_task(self):
        popup = UpdateTaskPopup(self.home_page, self.task)
        popup.open()

    def delete_task(self):
        self.home_page.delete_task(self.task)
        self.manager.current = "home"


class AboutUsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.1, 0.1, 0.2, 1)  # Dark and moody purple-blue color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
            # Title
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Title with classy font from Google Fonts (Playfair Display)
        title = Label(
            text="About Us",
            font_size=45,
            font_name=r,  # Make sure this font is downloaded from Google Fonts
            size_hint=(1, 0.1),
            color=(0.2, 0.2, 0.2, 1)  # Dark text for contrast
        )
        layout.add_widget(title)
        scroll_view = ScrollView(size_hint=(1, 0.8))
        # About Us content
        about_text = Label(
            text="Welcome to the Task Manager App, designed to help you\n manage your tasks and boost your productivity.\n"
          "Developed by Bilal Ahmad, a 20-year-old student, \ncombining user-friendly design with robust features.\n"
          "Key Features:\n"
          "• User-Friendly Interface:\n Easy navigation for all functionalities.\n"
          "• Task Management:\n Add, categorize, and track tasks efficiently.\n"
          "• Progress Tracking: \nVisual progress bars to track completion.\n"
          "• History & Tracking: \nReview completed tasks and analyze productivity.\n"
          "• Visual Analytics: \nView trends and breakdowns with charts.\n"
          "• Suggestions & Feedback: \nProvide feedback for app improvement.\n"
          "• Daily Task Completion: \nClick a checkbox to complete one day of a daily task.\n"
          "• Manual Completion: \nOption to manually complete the total task percentage.\n\n"
          "• Task Name: On Home is also a button\n to view task details.\n"
          "Additional App Specifics:\n"
          "• The app combines a user-friendly interface,\n task management capabilities,\n"
          "   progress tracking, visual analytics,\n and a suggestion system for continuous improvement.\n\n"
          "About Bilal Ahmad\n"
          "Bilal Ahmad, a 20-year-old student passionate\n about software development, created this app.\n"
          "He aims to help users stay organized\n and improve productivity.\n\n"
          "Thank you for choosing the Task Manager App!\n We hope it helps you achieve your goals.",
            font_size=14,
            font_name=r,
            halign='center',
            valign='middle',
            size_hint=(1, None), 
            height=750
            )
        scroll_view.add_widget(about_text)
        layout.add_widget(scroll_view)

            # Back button
        back_button = Button(
            text="Back",
            size_hint=(1, 0.1),
            background_normal='',
            background_color=(0.2, 0.2, 0.3, 1),  # Moody dark blue
            color=(1, 1, 1, 1),  # White text
            font_size=16,
            bold=True
        )
        back_button.bind(on_release=lambda _: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_button)

        self.add_widget(layout)
    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    

    
# Main App
class TaskManagerApp(App):
    def build(self):
        # Ensure landscape orientation
        Window.size = (360, 800)
        sm = ScreenManager()
        sm.add_widget(LoadingScreen(name="loading"))
        sm.add_widget(HomePage(name="home"))
        sm.add_widget(HistoryTrackingPage(name="history"))
        sm.add_widget(AboutUsScreen(name="about_us"))
        return sm

 
 
    

if __name__ == "__main__":
    TaskManagerApp().run()
    
