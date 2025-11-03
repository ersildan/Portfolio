with open('file_1.txt', 'w+', encoding='UTF-8') as f:
    with open('file_2.txt', 'w+', encoding='UTF-8') as f2:
        f.write("\n".join(sorted(input().split())))  # Читаем и сортируем список - записываем в f
        f.seek(0)                                    # курсор на первую строку в первом файле
        txt_file_1 = f.read()                        # читаем текст в первом файле

        f2.write(txt_file_1)                         # Записываем текст из первого файла во второй файл
        f2.seek(0)                                   # курсор на первую строку во втором файле
        print(f2.read())                             # выводим на экран текст файла f2

# input('Матрица Скала Западня Бэтман')