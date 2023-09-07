
#BU MESAJI OKUYUN. KOYDUĞUM BÜTÜN YORUM SATIRLARINI OKUYUN ÇÜNKÜ BİRİNDE BİLE HATA YAPARSANIZ KOD ÇALIŞMAZ HEPSİNİ EKSİKSİZ OKUYUN VE EKSİKSİZ DOLDURUN.(BÜTÜN KODU İNCELEYİN def bot() kısmını bile)

import time
import requests
import pytz
import datetime
import os
import traceback
import sqlite3
import tkinter as tk
import threading
import multiprocessing
import sys  

token = ''  # Buraya kendi kullanıcı tokeninizi koymanız gerekiyor
channel_id = ''  # Buraya sayı tahmin oynayacağınız kanalın idsini koymanız gerekiyor
kullanıcı_id = ''  # Buraya kendi kullanıcı id nizi koymanız gerekiyor

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


original_stderr = sys.stderr
sys.stderr = open("pygame_messages.txt", "w")



tz = pytz.timezone('Europe/Istanbul')

import pygame

pygame.init()
sys.stderr.close()
sys.stderr = original_stderr

tz = pytz.timezone('Europe/Istanbul')

pygame.init()

db_connection_log = sqlite3.connect("Logs/log.db")
db_cursor_log = db_connection_log.cursor()

db_connection_extra = sqlite3.connect("Logs/extra.db")
db_cursor_extra = db_connection_extra.cursor()

quit_flag = False

db_cursor_log.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        log_message TEXT,
        log_time TEXT
    )
''')
db_connection_log.commit()

db_cursor_extra.execute('''
    CREATE TABLE IF NOT EXISTS extra_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bot_name TEXT,
        bot_id TEXT,
        log_time TEXT
    )
''')
db_connection_extra.commit()


def log_to_database_log(log_time, log_message):
    db_cursor_log.execute('INSERT INTO logs (log_message, log_time) VALUES (?, ?)',
                          (log_message, log_time))
    db_connection_log.commit()


def log_to_database_extra(bot_name, bot_id, log_time):
    db_cursor_extra.execute('INSERT INTO extra_logs (bot_name, bot_id, log_time) VALUES (?, ?, ?)',
                            (bot_name, bot_id, log_time))
    db_connection_extra.commit()


def internet_available():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False


def check_internet_connection():
    while not internet_available():
        print("Internet bağlantısı yok.")
        time.sleep(0.5)


def create_crash_report(error_msg):
    try:
        pygame.mixer.music.load("Sound/hata.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        zaman = datetime.datetime.now(tz).strftime("%Y-%m-%d   %H:%M:%S")
        with open("crash_reports.txt", "w", encoding="utf-8") as report_file:
            report_file.write(f"{error_msg}\n")
            report_file.write(f"Tarih: {zaman}\n")

        log_to_database_log(zaman, error_msg)

    except Exception as e:
        print("Crash raporu oluşturulurken bir hata oluştu:", str(e))
quit_event = multiprocessing.Event()
quit_flag = multiprocessing.Value('b', False)
quit_flag_lock = multiprocessing.Lock()



def bot_thread(quit_flag):
    global token, channel_id, kullanıcı_id
    count = 1

    pygame.init()  # Pygame'i başlat

    db_connection_log = sqlite3.connect("Logs/log.db")
    db_cursor_log = db_connection_log.cursor()

    db_connection_extra = sqlite3.connect("Logs/extra.db")
    db_cursor_extra = db_connection_extra.cursor()
    pygame.mixer.init()
    while True:
        with quit_flag_lock:
            if quit_flag.value:
                pygame.quit()
                break

        check_internet_connection()

        if count > 100:
            count = 1
        payload = {
            'content': str(count)
        }

        headers = {
            'Authorization': f'{token}'
        }

        try:
            r = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', data=payload,
                              headers=headers)
            if r.status_code == 200:
                zaman = datetime.datetime.now(tz).strftime("%Y-%m-%d   %H:%M:%S")
                mesaj = f"Mesaj gönderildi: {count}"
                print(f"{mesaj:<35}{zaman:>70}")

                with open("Logs/log.txt", "a", encoding="utf-8") as dosya:
                    dosya.write(f"{mesaj:<35}{zaman:>70}\n")

                log_to_database_log(zaman, mesaj)

            else:
                zaman = datetime.datetime.now(tz).strftime("%Y-%m-%d   %H:%M:%S")
                mesaj = f"Mesaj gönderilirken bir hata oluştu: {r.status_code}"
                print(f"{mesaj:<50}{zaman:>55}")
                pygame.mixer.music.load("Sound/hata.wav")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

        except Exception as e:
            error_msg = traceback.format_exc()
            create_crash_report(error_msg)
            print("Bir hata oluştu, crash raporu oluşturuldu.")
            break

        time.sleep(1)

        try:
            r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers)
            if r.status_code == 200:
                messages = r.json()
                if messages:
                    last_message = messages[0]
                    content = last_message['content']
                    user_id = last_message['author']['id']
                    username = last_message['author']['username']

                    if content.startswith(f'<@{kullanıcı_id}>, Tebrikler!'): #burası ÇOK ÖNEMLİ buraya sayıyı bulunca botun size gönderdiği mesajın ilk 2-3 cümlesini eksiksiz koymanız lazım ve ayrıca sizin gözünüzle gördüğünüz kodda öyle yazılmıyor örnek : gözle görünen : @lama2923  kodda görünen: <@886616962678030427> 
                        mesaj = f"Doğru sayı bulundu doğru sayı: {count}"
                        print(f"{mesaj:<35}{zaman:>70}")
                        count = 0

                        with open("Logs/log.txt", "a", encoding="utf-8") as dosya:
                            dosya.write(f"{mesaj:<35}{zaman:>70}\n")
                        with open("Logs/extra.txt", "a", encoding="utf-8") as dosya:
                            dosya.write(f"{username:<30}                {user_id}    {zaman:>70}\n")

                        log_to_database_extra(username, user_id, zaman)
                        log_to_database_log(zaman, mesaj)
                        log_to_database_extra(username, user_id, zaman)

                        pygame.mixer.music.load("Sound/buldum.wav")
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            pygame.time.Clock().tick(10)
                        count += 1
                        pass
                    elif content.startswith(f'<@{kullanıcı_id}>, Yazılan'): #burası ÇOK ÖNEMLİ buraya sayıyı bulunamayınca botun size gönderdiği mesajın ilk 2-3 cümlesini eksiksiz koymanız lazım ve ayrıca sizin gözünüzle gördüğünüz kodda öyle yazılmıyor örnek : gözle görünen : @lama2923  kodda görünen: <@886616962678030427> 
                        with open("Logs/extra.txt", "a", encoding="utf-8") as dosya:
                            dosya.write(f"{username:<30}                {user_id}    {zaman:>70}\n")

                        log_to_database_extra(username, user_id, zaman)

                        count += 1
                        pass

                    else:
                        log_to_database_extra(username, user_id, zaman)
                        time.sleep(3)
                        while True:
                            check_internet_connection()

                            if count > 100:
                                count = 1
                            wcount = count

                            payload = {
                                'content': str(wcount)
                            }
                            headers = {
                                'Authorization': f'{token}'
                            }

                            try:
                                r = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages',
                                                  data=payload, headers=headers)

                                if r.status_code == 200:
                                    zaman = datetime.datetime.now(tz).strftime("%Y-%m-%d   %H:%M:%S")
                                    mesaj_tekrar = f"Tekrar mesajı gönderildi: {wcount}"
                                    print(f"{mesaj_tekrar:<35}{zaman:>70}")
                                    with open("Logs/log.txt", "a", encoding="utf-8") as dosya:
                                        dosya.write(f"{mesaj_tekrar:<35}{zaman:>70}\n")
                                    log_to_database_log(zaman, mesaj_tekrar)

                                else:
                                    mesaj = f"Mesaj gönderilirken bir hata oluştu: {r.status_code}"
                                    print(f"{mesaj:<50}{zaman:>70}")
                                    pygame.mixer.music.load("Sound/hata.wav")
                                    pygame.mixer.music.play()
                                    while pygame.mixer.music.get_busy():
                                        pygame.time.Clock().tick(10)
                            except Exception as e:
                                error_msg = traceback.format_exc()
                                create_crash_report(error_msg)
                                print("Bir hata oluştu, crash raporu oluşturuldu.")
                                break

                            time.sleep(1)

                            try:
                                r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages',
                                                 headers=headers)
                                if r.status_code == 200:
                                    messages = r.json()
                                    if messages:
                                        last_message = messages[0]
                                        content = last_message['content']
                                        user_id = last_message['author']['id']
                                        username = last_message['author']['username']

                                        if content.startswith(f'<@{kullanıcı_id}>, Tebrikler!'): #burası ÇOK ÖNEMLİ buraya sayıyı bulunca botun size gönderdiği mesajın ilk 2-3 cümlesini eksiksiz koymanız lazım ve ayrıca sizin gözünüzle gördüğünüz kodda öyle yazılmıyor örnek : gözle görünen : @lama2923  kodda görünen: <@886616962678030427> 
                                            wcount
                                            mesaj = f"Doğru sayı bulundu doğru sayı: {wcount}"
                                            print(f"{mesaj:<35}{zaman:>70}")
                                            count = 1

                                            with open("Logs/log.txt", "a", encoding="utf-8") as dosya:
                                                dosya.write(f"{mesaj:<35}{zaman:>70}\n")

                                                log_to_database_extra(username, user_id, zaman)
                                                log_to_database_log(zaman, mesaj)
                                            with open("Logs/extra.txt", "a", encoding="utf-8") as dosya:
                                                dosya.write(f"{username:<30}                {user_id}    {zaman:>70}\n")

                                                log_to_database_extra(username, user_id, zaman)

                                                pygame.mixer.music.load("Sound/buldum.wav")
                                                pygame.mixer.music.play()
                                                while pygame.mixer.music.get_busy():
                                                    pygame.time.Clock().tick(10)
                                                break
                                        elif content.startswith(f'<@{kullanıcı_id}>, Yazılan'): #burası ÇOK ÖNEMLİ buraya sayıyı bulunamayınca botun size gönderdiği mesajın ilk 2-3 cümlesini eksiksiz koymanız lazım ve ayrıca sizin gözünüzle gördüğünüz kodda öyle yazılmıyor örnek : gözle görünen : @lama2923  kodda görünen: <@886616962678030427> 
                                            with open("Logs/extra.txt", "a", encoding="utf-8") as dosya:
                                                dosya.write(f"{username:<30}                {user_id}    {zaman:>70}\n")

                                                log_to_database_extra(username, user_id, zaman)
                                            break
                                        else:
                                            with open("Logs/extra.txt", "a", encoding="utf-8") as dosya:
                                                dosya.write(
                                                    f"Bot yanıt vermiyor yada belirlediğiniz bot yanıtları yanlış ayarlanmış.{zaman:>70}\n")
                                                username = "Null"
                                                user_id = "Null"

                                                log_to_database_extra(username, user_id, zaman)

                                    else:
                                        print("Kanalda henüz mesaj yok.")
                                else:
                                    print(f"Mesajları alırken bir hata oluştu: {r.status_code}")
                            except Exception as e:
                                error_msg = traceback.format_exc()
                                create_crash_report(error_msg)
                                print("Bir hata oluştu, crash raporu oluşturuldu.")
                                break

                            time.sleep(2.5)

                else:
                    print("Kanalda henüz mesaj yok.")
            else:
                print(f"Mesajları alırken bir hata oluştu: {r.status_code}")
        except Exception as e:
            error_msg = traceback.format_exc()
            create_crash_report(error_msg)
            print("Bir hata oluştu, crash raporu oluşturuldu.")
            break

        time.sleep(1.8)
quit_event = multiprocessing.Event()
if not os.path.exists("Logs/log.txt"):
    open("Logs/log.txt", "w").close()
quit_flag_lock = threading.Lock()
def quit_application(root, quit_flag):
    quit_flag.value = True
    root.quit()

def tkinter_loop(quit_flag):
    global quit_event  
    root = tk.Tk()
    root.title("Tkinter Penceresi Başlığı")

    quit_button = tk.Button(root, text="Çıkış", command=lambda: quit_application(root, quit_flag))
    quit_button.pack()

    while not quit_flag.value:
        try:
            root.update()  
            time.sleep(0.1)
        except tk.TclError:
            break



def create_gui():
    root = tk.Tk()
    root.title("Quit Screen")
    root.geometry("500x300")

    
    root.configure(bg="#36393F")
    root.option_add("*TButton*highlightBackground", "#7289DA")
    root.option_add("*TButton*highlightColor", "#7289DA")
    root.option_add("*TButton*background", "#7289DA")
    root.option_add("*TButton*foreground", "white")
    root.option_add("*TButton.font", ("Arial", 14))  

    
    label = tk.Label(root, text="Programı çıkış butonuna basarak kapatmanız.\nLoglarken sorun olmaması için daha sağlıklı olacaktır.", bg="#36393F", fg="white", font=("Arial", 16))
    label.pack(pady=20)

    
    button = tk.Button(root, text="Çıkış", command=lambda: quit_application(root, quit_flag), relief=tk.RAISED, width=20, height=2, font=("Arial", 14))
    button.pack()

    
    root.mainloop()
if __name__ == "__main__":
    quit_flag = multiprocessing.Value('b', False)
    bot_process = multiprocessing.Process(target=bot_thread, args=(quit_flag,))
    tkinter_thread = threading.Thread(target=create_gui)

    bot_process.start()
    tkinter_thread.start()

    bot_process.join()
    tkinter_thread.join()