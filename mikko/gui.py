import tkinter as tk

from database import (
    add_word, word_exists, get_last_words
)


def send_message(event=None):
    message = message_entry.get()
    message_entry.delete(0, tk.END)

    if message == 'quit':
        window.quit()

    elif message == 'show last added words':
        last_words = get_last_words()
        response = f'Last words: {", ".join(last_words)}'
        text_area.insert(tk.END, response + '\n')
    
    for word in message.split():
        if word_exists(word):
            response = f'Mikko: I know that word {word}'
        else:
            response = f'Mikko: A new word ^ ^ {word}'
            add_word(word)

        text_area.insert(tk.END, response + '\n')

window = tk.Tk()
window.title("Mikko AI")

message_entry = tk.Entry(window, width=50)
message_entry.bind("<Return>", send_message)
message_entry.pack()

send_button = tk.Button(window, text='Send', command=send_message)
send_button.pack()

text_area = tk.Text(window, width=60, height=10)
text_area.pack()

window.mainloop()
