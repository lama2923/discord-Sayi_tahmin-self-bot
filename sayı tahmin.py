
# BU MESAJI OKUYUN. KOYDUĞUM BÜTÜN YORUM SATIRLARINI OKUYUN ÇÜNKÜ BİRİNDE BİLE HATA YAPARSANIZ KOD ÇALIŞMAZ HEPSİNİ EKSİKSİZ OKUYUN VE EKSİKSİZ DOLDURUN.(BÜTÜN KODU MANTIĞINI ANLAMANIZ İÇİN BİR GÖZDEN GEÇİRİN)


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
import random



token = 'x' # Buraya kendi kullanıcı tokeninizi koymanız gerekiyor

channel_id = 'x' # Buraya sayı tahmin oynayacağınız kanalın idsini koymanız gerekiyor

kullanıcı_id = 'x' # Burası Önemsiz! kodu incelersiz neden koyduğumu anlarsınız diye düşünüyorum! ama sizin doldurmanıza gerek yok! (opyisonel belki sizde techno bot ile yapıcaksınz)

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


original_stderr = sys.stderr
sys.stderr = open("pygame_messages.txt", "w")


tz = pytz.timezone('Europe/Istanbul')



sys.stderr.close()
sys.stderr = original_stderr
klasor_adi = "Logs"
if not os.path.exists(klasor_adi):
    os.makedirs(klasor_adi)
tz = pytz.timezone('Europe/Istanbul')



db_connection_log = sqlite3.connect("Logs/log.db")
db_cursor_log = db_connection_log.cursor()


quit_flag = False

db_cursor_log.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        log_message TEXT,
        log_time TEXT,
        bot_name TEXT,
        bot_id iNTEGER,
        bot_reply TEXT
    )
''')
db_connection_log.commit()





def log_to_database_log(log_time, log_message, bot_name, bot_id, bot_reply):
    db_cursor_log.execute('INSERT INTO logs (log_message, log_time, bot_name, bot_id, bot_reply) VALUES (?, ?, ?, ?, ?)',
                          (log_message, log_time, bot_name, bot_id, bot_reply))
    db_connection_log.commit()


def delete_last_log_from_database_log():
    try:

        db_cursor_log.execute('SELECT MAX(id) FROM logs')
        last_log_id = db_cursor_log.fetchone()[0]

        if last_log_id is not None:

            db_cursor_log.execute(
                'DELETE FROM logs WHERE id = ?', (last_log_id,))
            db_connection_log.commit()
            print(f'Son log (ID: {last_log_id}) başarıyla silindi.')
        else:
            print('ERROR!')
    except sqlite3.Error as e:
        print(f'Hata oluştu: {str(e)}')


def internet_available():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False


def check_internet_connection():
    anlamsız_sayı = 0
    while not internet_available():
        anlamsız_sayı += 1
        if anlamsız_sayı == 5:
            exit(1)
        print("Internet bağlantısı yok.")
        time.sleep(0.5)


def check_internet_connection_get():
    anlamsız_sayı = 0
    while not internet_available():
        anlamsız_sayı += 1
        if anlamsız_sayı == 1:
            delete_last_log_from_database_log()
        elif anlamsız_sayı == 5:
            exit(1)

        print("Internet bağlantısı yok.")
        time.sleep(0.5)


def create_crash_report(error_msg):
    try:

        zaman = datetime.datetime.now(tz).strftime("%Y-%m-%d   %H:%M:%S")
        with open("crash_reports.txt", "w", encoding="utf-8") as report_file:
            report_file.write(f"{error_msg}\n")
            report_file.write(f"Tarih: {zaman}\n")

        log_to_database_log(zaman)

    except Exception as e:
        print("Crash raporu oluşturulurken bir hata oluştu:", str(e))


quit_event = multiprocessing.Event()
quit_flag = multiprocessing.Value('b', False)
quit_flag_lock = multiprocessing.Lock()
Mesaj_Döngüsü_bitti = None
Correct_Number_Count = 0

def bot_thread(quit_flag):
    global token, channel_id, kullanıcı_id, Correct_Number_Count, Mesaj_Döngüsü_bitti
    count = 1
    Mesaj_gönderildi = None
    Mesaj_Döngüsü_bitti = None

    db_connection_log = sqlite3.connect("Logs/log.db")
    db_cursor_log = db_connection_log.cursor()

    okudum = []
    
    while True:
        with quit_flag_lock:
            if quit_flag.value:
                exit(1)
                break

        if count > 100:
            count = 1
        payload = {
            'content': str(count)
        }

        headers = {
            'Authorization': f'{token}'

        }

        try:
            check_internet_connection()

            # bu kısım eğer kanalın Couldown ayarı açıksa kullanabilirsiniz kendi Couldownınıza göre
            if Mesaj_gönderildi != None or Mesaj_gönderildi:
            
                while True:
                    if time.time() - Mesaj_gönderildi < 4.8:

                        pass
                    else:
                    
                        break
                    
                    time.sleep(0.1)
            else:
                time.sleep(5.75)
            # bu kısım eğer kanalın Couldown ayarı açıksa kullanabilirsiniz kendi Couldownınıza göre

            
            
            r = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', data=payload, headers=headers)
            Mesaj_gönderildi = time.time()
            zaman = datetime.datetime.now(tz).strftime("%Y-%m-%d   %H:%M:%S")
            if r.status_code == 200:
                zaman = datetime.datetime.now(
                    tz).strftime("%Y-%m-%d   %H:%M:%S")
                
                

                mesaj = f"Mesaj gönderildi: {count}"
                print(f"{mesaj:<35}{zaman:>70}")

            else:
                zaman = datetime.datetime.now(
                    tz).strftime("%Y-%m-%d   %H:%M:%S")
                Mesaj_gönderildi = False
                mesaj = f"Mesaj gönderilirken bir hata oluştu: {r.status_code}\{r}"
                print(f"{mesaj:<50}{zaman:>55}")
                count -= 1 


        except Exception as e:  
            error_msg = traceback.format_exc()
            create_crash_report(error_msg)
            print("Bir hata oluştu, crash raporu oluşturuldu.")
            pass

        time.sleep(1)

        try:
            check_internet_connection_get()
            r = requests.get(
                f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers)
            if r.status_code == 200:
                messages = r.json()
                if messages:


                    gcontent = ""
                    username = ""
                    user_id = ""
                    for INDEX, mesaj in enumerate(messages):
                        if INDEX == 10:
                            break
                        content = mesaj['content']
                        if content.startswith(f'<@{kullanıcı_id}>'):
                            if mesaj['id'] in okudum:
                                pass
                            else:
                                okudum.append(mesaj["id"])
                                user_id = mesaj['author']['id']
                                username = mesaj['author']['username']
                                gcontent = mesaj["content"]
                                break

                    # burası ÇOK ÖNEMLİ buraya sayıyı bulunca botun size gönderdiği mesajın ilk 2-3 cümlesini eksiksiz koymanız lazım ve ayrıca sizin gözünüzle gördüğünüz kodda öyle yazılmıyor örnek : gözle görünen : @lama2923  kodda görünen: <@886616962678030427>
                    if gcontent.startswith(f'<@{kullanıcı_id}>, Tebrikler!'):
                        Correct_Number_Count += 1
                        yazı = f"Doğru sayı bulundu doğru sayı: {count}, Bu {Correct_Number_Count}. Doğrumuz"
                        print(f"{yazı:<35}{zaman:>70}")
                        count = 0



                        log_to_database_log(
                            zaman, yazı, username, user_id, gcontent)


                        count += 1
                        pass
                    # burası ÇOK ÖNEMLİ buraya sayıyı bulunamayınca botun size gönderdiği mesajın ilk 2-3 cümlesini eksiksiz koymanız lazım ve ayrıca sizin gözünüzle gördüğünüz kodda öyle yazılmıyor örnek : gözle görünen : @lama2923  kodda görünen: <@886616962678030427>
                    elif gcontent.startswith(f'<@{kullanıcı_id}>, Yazılan'):
                        yazı = f"Mesaj gönderildi: {count}"

                        log_to_database_log(
                            zaman, yazı, username, user_id, gcontent)

                        count += 1
                        pass

                    else:
                        time.sleep(3)
                        random_value = random.choice(range(1, 6))
                        time.sleep(int(random_value))
                        random_value = random.choice(range(1, 6))
                        time.sleep(int(random_value))
                        while True:
                            with quit_flag_lock:
                                if quit_flag.value:
                                    exit(1)
                                    break

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
                                check_internet_connection()
                                r = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages',
                                                  data=payload, headers=headers)

                                if r.status_code == 200:
                                    zaman = datetime.datetime.now(
                                        tz).strftime("%Y-%m-%d   %H:%M:%S")
                                    Mesaj_gönderildi = time.time()
                                    mesaj_tekrar = f"Tekrar mesajı gönderildi: {wcount}"
                                    print(f"{mesaj_tekrar:<35}{zaman:>70}")


                                else:
                                    mesaj = f"Mesaj gönderilirken bir hata oluştu (1): {r.status_code}"
                                    print(f"{mesaj:<50}{zaman:>70}")

                            except Exception as e:
                                error_msg = traceback.format_exc()
                                create_crash_report(error_msg)
                                print("Bir hata oluştu, crash raporu oluşturuldu.")
                                break

                            time.sleep(1)

                            try:
                                check_internet_connection_get()
                                r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages',
                                                 headers=headers)
                                if r.status_code == 200:
                                    messages = r.json()
                                    if messages:
                                        gcontent = ""
                                        username = ""
                                        user_id = ""
                                        for INDEX, mesaj in enumerate(messages):
                                            if INDEX == 10:
                                                break
                                            content = mesaj['content']
                                            if content.startswith(f'<@{kullanıcı_id}>'):
                                                if mesaj['id'] in okudum:
                                                    pass
                                                else:
                                                    okudum.append(mesaj["id"])
                                                    user_id = mesaj['author']['id']
                                                    username = mesaj['author']['username']
                                                    gcontent = mesaj["content"]
                                                    break
                                            
                                    if messages:


                                        # burası ÇOK ÖNEMLİ buraya sayıyı bulunca botun size gönderdiği mesajın ilk 2-3 cümlesini eksiksiz koymanız lazım ve ayrıca sizin gözünüzle gördüğünüz kodda öyle yazılmıyor örnek : gözle görünen : @lama2923  kodda görünen: <@886616962678030427>
                                        if gcontent.startswith(f'<@{kullanıcı_id}>, Tebrikler!'):
                                            Correct_Number_Count += 1
                                            yazı = f"Doğru sayı bulundu doğru sayı: {wcount}, Bu {Correct_Number_Count}. Doğrumuz."
                                            print(f"{yazı:<35}{zaman:>70}")
                                            count = 1


                                            log_to_database_log(
                                                zaman, yazı, username, user_id, gcontent)





                                            break
                                        # burası ÇOK ÖNEMLİ buraya sayıyı bulunamayınca botun size gönderdiği mesajın ilk 2-3 cümlesini eksiksiz koymanız lazım ve ayrıca sizin gözünüzle gördüğünüz kodda öyle yazılmıyor örnek : gözle görünen : @lama2923  kodda görünen: <@886616962678030427>
                                        elif gcontent.startswith(f'<@{kullanıcı_id}>, Yazılan'):
                                            
                                            yazı = f"Tekrar Mesajı gönderildi: {wcount}"

                                            log_to_database_log(
                                                zaman, yazı, username, user_id, gcontent)
                                            break
                                        else:
                                            random_value = random.choice(range(1, 6))
                                            time.sleep(int(random_value))
                                            random_value = random.choice(range(1, 6))
                                            time.sleep(int(random_value))
                                            with open("Logs/extra.txt", "a", encoding="utf-8") as dosya:
                                                dosya.write(
                                                    f"Bot yanıt vermiyor yada belirlediğiniz bot yanıtları yanlış ayarlanmış.{zaman:>70}\n")
                                                username = "Null"
                                                user_id = "Null"

                                    else:
                                        print("Kanalda henüz mesaj yok.")
                                else:
                                    print(
                                        f"Mesajları alırken bir hata oluştu (1): {r.status_code}")
                            except Exception as e:
                                error_msg = traceback.format_exc()
                                create_crash_report(error_msg)
                                print("Bir hata oluştu, crash raporu oluşturuldu.")
                                break



                else:
                    print("Kanalda henüz mesaj yok.")
            else:
                print(f"Mesajları alırken bir hata oluştu: {r.status_code}")
        except Exception as e:
            error_msg = traceback.format_exc()
            create_crash_report(error_msg)
            print("Bir hata oluştu, crash raporu oluşturuldu.")
            break
        
        Mesaj_Döngüsü_bitti = time.time()


        


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

    quit_button = tk.Button(
        root, text="Çıkış", command=lambda: quit_application(root, quit_flag))
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

    label = tk.Label(root, text="Programı çıkış butonuna basarak kapatmanız.\nLoglarken sorun olmaması için daha sağlıklı olacaktır.",
                     bg="#36393F", fg="white", font=("Arial", 16))
    label.pack(pady=20)

    button = tk.Button(root, text="Çıkış", command=lambda: quit_application(
        root, quit_flag), relief=tk.RAISED, width=20, height=2, font=("Arial", 14))
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
