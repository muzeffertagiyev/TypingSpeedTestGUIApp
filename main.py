from  tkinter import *
import tkinter.messagebox as msgb

import os
import random

from words import word_list


random_word_list = random.sample(word_list, 105)
typed_words = []


root = Tk()
root.title('Typing Speed Test')
root.geometry("800x650")

frame = Frame(root)

def close_the_app():
    if msgb.askokcancel("Quit", "Do you want to close the app?"):
        root.destroy()

def restart_test():
    if not msgb.askokcancel("Quit", "Do you want to Restart the app?"):
        return
    typed_words.clear()
    type_entry.delete(0, END)
    words_label.pack_forget()
    type_below_label.pack_forget()
    type_entry.pack_forget()
    wrong_word_label.pack_forget()
    result_label.pack_forget()
    efficiency_label.pack_forget()
    time_is_up_label.pack_forget()
    restart_button.pack_forget()
    close_app_button.pack_forget()
    start_btn.pack(pady=10)
    root.geometry("800x650")


def check_and_clear_entry(*args):
    words = type_entry.get()
    
    if words.count(' ') >= 7:
        typed_words.append(type_entry.get())
        
        type_entry.delete(0, END)


def start_timer():
    # Hide the start button
    start_btn.pack_forget()

    start_timer_label.pack()
    # Start the timer from 3 seconds
    start_countdown(3)


def write_to_file(filename,content):
    with open(filename, 'w') as file:
        file.write(content)
    

def end_countdown(time_left):
    if time_left >= 0:
        # Update the timer label
        start_timer_label.config(text=f"Time Left: {time_left}")
        time_left -= 1
        # Schedule the countdown function to run after 1 second (1000 milliseconds)
        root.after(1000, end_countdown, time_left)
    else:
        filename='data.txt'

        start_timer_label.pack_forget()
        words_label.pack_forget()
        type_below_label.pack_forget()
        type_entry.pack_forget()

        typed_words.append(type_entry.get())
        typed_string = ''.join(typed_words)
        last_typed_words = typed_string.split()

        length_typed_words = len(last_typed_words)
        set1 = set(word_list)
        set2 = set(last_typed_words)
        common_words = set1.intersection(set2)
        num_common_words = len(common_words)

        result_label.config(text=f"Number of correct words per Minute: {num_common_words}")
        wrong_word_label.config(text=f"Number of wrong words: {length_typed_words-num_common_words}")
        
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                lines = file.read()
                old_result = lines.split()[0]
                difference = num_common_words - int(old_result)
                efficiency_percentage = (difference / int(old_result)) * 100
            
            if efficiency_percentage >= 0:
                efficiency_label.config(text=f'You are now {efficiency_percentage:.2f}% quicker keep going')
            else:
                efficiency_label.config(text=f'You are now {efficiency_percentage:.2f}% slower ,do more exercises')
            efficiency_label.pack()
        write_to_file(filename,f"{num_common_words} {length_typed_words-num_common_words}")

        # Timer ends, show new buttons or labels
        time_is_up_label.pack()
        result_label.pack()
        wrong_word_label.pack()
        restart_button.pack()
        close_app_button.pack()
        root.geometry("600x200")
        typed_words.clear()
        
        
def start_countdown(time_left):
    if time_left >= 0:
        # Update the timer label
        start_timer_label.config(text=f"App starts after: {time_left}")
        time_left -= 1
        # Schedule the countdown function to run after 1 second (1000 milliseconds)
        root.after(1000, start_countdown, time_left)
    else:
        words_label.pack()
        end_countdown(60)
        type_below_label.pack()
        type_entry.pack()
        type_entry.focus_set()
        type_entry.bind("<KeyRelease>", check_and_clear_entry)
        

start_btn = Button(frame,text='Start The Test', bg='#FFCC33' ,font=('verdana',16),padx=10,pady=5, command=start_timer)
start_timer_label = Label(frame, text="", font=("Helvetica", 20))

# all_words
words_label = Label(frame,text=" ".join(random_word_list),font=("Helvetica", 25),wraplength=700, justify='left')

type_below_label = Label(frame,text='Type Below',pady=10, font=('verdana',20))
type_entry = Entry(root, width=60, font=('Helvetica',25))

# number of wrong words
wrong_word_label = Label(frame,font=("Helvetica", 20))

# number of correct words
result_label = Label(frame,font=("Helvetica", 20))

restart_button = Button(frame,text='Restart',font=('verdana',16),padx=10,pady=5,command=restart_test)
close_app_button = Button(frame,text='Close The App',font=('verdana',16),padx=10,pady=5,command=close_the_app)

time_is_up_label = Label(frame, text="Time's up! Restart again or Close the app", font=("Helvetica", 25))
efficiency_label = Label(frame,font=("Helvetica", 20))

frame.pack()
start_btn.pack(pady=10)

root.mainloop()