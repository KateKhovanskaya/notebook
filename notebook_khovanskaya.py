import datetime
import time
import json

notebook = 'notes_khovanskaya.json'
note_id = 1
notes = list()
monthes = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
           'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}


def load_notebook():
    try:
        global notes
        global note_id
        with open(notebook, 'r') as file:
            loaded_notes = json.load(file)
            if len(loaded_notes) > 0:
                notes = loaded_notes
                note_id = notes[len(loaded_notes)-1]['note_id'] + 1
    except FileNotFoundError:
        print('данные будут сохранены в notes_khovanskaya.json')


def notebook_read():
    global notes
    with open(notebook, 'r') as file:
        notes = json.load(file)
        for note in notes:
            print_note(note)


def note_add():
    note = {}
    global note_id
    global notes
    note['note_id'] = note_id
    note_id += 1
    in_title = input('Введите название заметки: ')
    note['title'] = in_title
    in_description = input('Введите описание заметки: ')
    note['discription'] = in_description
    note['change_time'] = time.ctime(time.time())
    notes.append(note)
    save_notebook(notes)


def note_search():
    global notes
    search_date_input = input('Введите дату для поска в формате дд.мм.гггг ')
    find_date = datetime.date(int(search_date_input[6:]),
                              int(search_date_input[3:5]),
                              int(search_date_input[:2]))
    searched_notes_indexes = list()
    flag = True
    for i in notes:
        date_of_note = datetime.date(int(i['change_time'][-4:]),
                                     int(monthes[i['change_time'][4:7]]),
                                     int(i['change_time'][8:10]))
        if date_of_note == find_date:
            searched_notes_indexes.append(notes.index(i))
            print_note(i)
            flag = False
    if flag:
        print('Ничего не найдено!')
    return searched_notes_indexes


def note_search_by_name():
    global notes
    search_text_input = input('Введите текст для поиска ')
    searched_notes_indexes = list()
    flag = True
    for i in notes:
        note_text = i['title'] + ' ' + i['discription']
        if search_text_input.upper() in note_text.upper():
            searched_notes_indexes.append(notes.index(i))
            print_note(i)
            flag = False
    if flag:
        print('Ничего не найдено!')
    return searched_notes_indexes

# Поиск индекса заметки для замены или удаления


def find_note():
    searched_notes_indexes = note_search_by_name()
    if (len(searched_notes_indexes) != 0):
        changed_index = searched_notes_indexes[0]+1
        if len(searched_notes_indexes) != 1:
            print("Укажите номер заметки из списка выше, для продолждения")
            changed_index = int(input())
    else:
        changed_index = -1
    return changed_index-1

# Редактирование заметки


def change_note():
    changed_index = find_note()
    if (changed_index >= 0):
        while True:
            print('Введите 1 для замены заголовка, 2 - описания, 3 - всё ок, '
                  'сохранить')
            mode = int(input())
            if mode == 1:
                notes[changed_index]['title'] = input('Название: ')
            elif mode == 2:
                notes[changed_index]['discription'] = input('Описание: ')
            elif mode == 3:
                break
        notes[changed_index]['change_time'] = time.ctime(time.time())
        save_notebook(notes)


# удаление заметки
def delete_note():
    deleted_index = find_note()
    if (deleted_index >= 0):
        notes.pop(deleted_index)
        save_notebook(notes)
        print('Контакт удален')

# Перезапись файла


def save_notebook(notes: list):
    with open(notebook, 'w', encoding='UTF-8') as file:
        json.dump(notes, file)


def print_note(note):
    print(f"{note['note_id']} {note['title']}. {note['discription']}. "
          f"Изменен: {note['change_time']}")


def main():
    load_notebook()
    print()
    while True:
        if (len(notes) > 0):
            print('Введите название команды для заметок \n'
                  'add - для добавления заметки\n'
                  'read - для чтения заметок\n'
                  'search by date - для поиска заметок по дате\n'
                  'search by name - для поиска по названию или описанию\n'
                  'change - для редактирования заметок\n'
                  'delete - для удаления заметок\n'
                  'stop - для завершения работы')
        else:
            print('Введите add - для добавления заметки')
        mode = input()
        if mode == 'add':
            note_add()
        elif mode == 'read':
            notebook_read()
        elif mode == 'search by date':
            note_search()
        elif mode == 'search by name':
            note_search_by_name()
        elif mode == 'change':
            change_note()
        elif mode == 'delete':
            delete_note()
        elif mode == 'stop':
            break


if __name__ == '__main__':
    main()
