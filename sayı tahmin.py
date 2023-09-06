#BU MESAJI OKUYUN. KOYDUĞUM BÜTÜN YORUM SATIRLARINI OKUYUN ÇÜNKÜ BİRİNDE BİLE HATA YAPARSANIZ KOD ÇALIŞMAZ HEPSİNİ EKSİKSİZ OKUYUN VE EKSİKSİZ DOLDURUN.(BÜTÜN KODU İNCELEYİN def bot() kısmını bile)



import time
import requests
import pytz
import datetime
import os
import traceback
import sys
import sqlite3

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


db_connection_log = sqlite3.connect("Logs/log.db")
db_cursor_log = db_connection_log.cursor()

db_connection_extra = sqlite3.connect("Logs/extra.db")
db_cursor_extra = db_connection_extra.cursor()


db_cursor_log.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        log_time TEXT,
        log_message TEXT
    )
''')
db_connection_log.commit()

db_cursor_extra.execute('''
    CREATE TABLE IF NOT EXISTS extra_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        log_time TEXT,
        log_message TEXT
    )
''')
db_connection_extra.commit()


def log_to_database_log(log_time, log_message):
    db_cursor_log.execute('INSERT INTO logs (log_time, log_message) VALUES (?, ?)',
                          (log_time, log_message))
    db_connection_log.commit()

def log_to_database_extra(log_time, log_message):
    db_cursor_extra.execute('INSERT INTO extra_logs (log_time, log_message) VALUES (?, ?)',
                            (log_time, log_message))
    db_connection_extra.commit()


def ekran_temizle():
    os.system('cls' if os.name == 'nt' else 'clear')

internet_print = "internet bağlantınız olmadığı için program düzgün çalışamıyor"

internet = True

def check_internet_connection():
    global internet ,internet_print
    try:
        requests.get("https://www.google.com", timeout=5)
        internet = True
        return True
    except requests.ConnectionError:
        internet = False
        return False

def internet_giriş_yasak():
    global internet
    time.sleep(0.5)
    print(internet_print)
    check_internet_connection()
    if not internet:
        internet_giriş_yasak()
    else:
        ekran_temizle()

while True:
    check_internet_connection()
    if not internet:
        internet_giriş_yasak()
    else:
        break

def internet_kontrol():
    global internet
    check_internet_connection()
    if not internet:
        internet_giriş_yasak()
    else:
        pass

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

def bot():
    global token, channel_id, kullanıcı_id
    count = 1

    input("Enter tuşuna basarak botu başlatın...")
    pygame.mixer.init()
    while True:
        internet_kontrol()
        
        if count > 100:
            count = 1
        payload = {
            'content': str(count)
        }
        
        headers = {
            'Authorization': f'{token}'  
        }

        try:
            r = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', data=payload, headers=headers)
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

                    if content.startswith(f'<@{kullanıcı_id}>, Tebrikler!'):  #burası ÇOK ÖNEMLİ buraya sayıyı bulunca botun size gönderdiği mesajın ilk 2-3 cümlesini eksiksiz koymanız lazım ve ayrıca sizin gözünüzle gördüğünüz kodda öyle yazılmıyor örnek : gözle görünen : @lama2923  kodda görünen: <@886616962678030427> 
                        
                        mesaj = f"Doğru sayı bulundu doğru sayı: {count}"
                        print(f"{mesaj:<35}{zaman:>70}")
                        count = 0  
                        
                        with open("Logs/log.txt", "a", encoding="utf-8") as dosya:
                            dosya.write(f"{mesaj:<35}{zaman:>70}\n")
                        with open("Logs/extra.txt", "a", encoding="utf-8") as dosya:
                            dosya.write(f"{username:<30}                {user_id}    {zaman:>70}\n")
                        
                        log_to_database_log(zaman, mesaj)
                        extra_log_message = f"Bot Adı: {username} | Bot ID'si: {user_id}"
                        log_to_database_extra(zaman, extra_log_message)
                        log_to_database_extra(zaman, extra_log_message)
                        
                        pygame.mixer.music.load("Sound/buldum.wav")
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            pygame.time.Clock().tick(10)
                        count += 1
                        pass
                    elif content.startswith(f'<@{kullanıcı_id}>, Yazılan'): #burası ÇOK ÖNEMLİ buraya sayıyı bulunamayınca botun size gönderdiği mesajın ilk 2-3 cümlesini eksiksiz koymanız lazım ve ayrıca sizin gözünüzle gördüğünüz kodda öyle yazılmıyor örnek : gözle görünen : @lama2923  kodda görünen: <@886616962678030427> 
                        with open("Logs/extra.txt", "a", encoding="utf-8") as dosya:
                            dosya.write(f"{username:<30}                {user_id}    {zaman:>70}\n")
                        extra_log_message = f"Bot Adı: {username} | Bot ID'si: {user_id}"
                        log_to_database_extra(zaman, extra_log_message)
                        count += 1
                        pass

                    else:
                        time.sleep(3)
                        while True:
                            internet_kontrol()
                            
                            if count > 100:
                                count = 1
                            wcount = count -1
                            
                            payload = {
                                'content': str(wcount)
                            }
                            headers = {
                                'Authorization': f'{token}'  
                            }
                            
                            try:
                                r = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', data=payload, headers=headers)

                                if r.status_code == 200:    
                                    zaman = datetime.datetime.now(tz).strftime("%Y-%m-%d   %H:%M:%S")
                                    mesaj_tekrar = f"Tekrar mesajı gönderildi: {wcount}"
                                    print(f"{mesaj_tekrar:<35}{zaman:>70}")
                                    with open("Logs/log.txt", "a", encoding="utf-8") as dosya:
                                        dosya.write(f"{mesaj_tekrar:<35}{zaman:>70}\n")
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
                                r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers)
                                if r.status_code == 200:
                                    messages = r.json()
                                    if messages:
                                        last_message = messages[0]  
                                        content = last_message['content']
                                        user_id = last_message['author']['id']
                                        username = last_message['author']['username']

                                        if content.startswith(f'<@{kullanıcı_id}>, Tebrikler!'):  #burası ÇOK ÖNEMLİ buraya sayıyı bulunca botun size gönderdiği mesajın ilk 2-3 cümlesini eksiksiz koymanız lazım ve ayrıca sizin gözünüzle gördüğünüz kodda öyle yazılmıyor örnek : gözle görünen : @lama2923  kodda görünen: <@886616962678030427> 
                                            wcount
                                            mesaj = f"Doğru sayı bulundu doğru sayı: {wcount}"
                                            print(f"{mesaj:<35}{zaman:>70}")
                                            count = 1  
                            
                                            with open("Logs/log.txt", "a", encoding="utf-8") as dosya:
                                                dosya.write(f"{mesaj:<35}{zaman:>70}\n")
                                            with open("Logs/extra.txt", "a", encoding="utf-8") as dosya:
                                                dosya.write(f"{username:<30}                {user_id}    {zaman:>70}\n")
                            
                                                pygame.mixer.music.load("Sound/buldum.wav")
                                                pygame.mixer.music.play()
                                                while pygame.mixer.music.get_busy():
                                                    pygame.time.Clock().tick(10)
                                                break
                                        elif content.startswith(f'<@{kullanıcı_id}>, Yazılan'): #burası ÇOK ÖNEMLİ buraya sayıyı bulunamayınca botun size gönderdiği mesajın ilk 2-3 cümlesini eksiksiz koymanız lazım ve ayrıca sizin gözünüzle gördüğünüz kodda öyle yazılmıyor örnek : gözle görünen : @lama2923  kodda görünen: <@886616962678030427> 
                                            with open("Logs/extra.txt", "a", encoding="utf-8") as dosya:
                                                dosya.write(f"{username:<30}                {user_id}    {zaman:>70}\n")
                                            break
                                        else:
                                            with open("Logs/extra.txt", "a", encoding="utf-8") as dosya:
                                                dosya.write(f"Bot yanıt vermiyor yada belirlediğiniz bot yanıtları yanlış ayarlanmış.{zaman:>70}\n")

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

if not os.path.exists("Logs/log.txt"):
    open("Logs/log.txt", "w").close()  

bot()


db_cursor_log.close()
db_connection_log.close()

db_cursor_extra.close()
db_connection_extra.close()