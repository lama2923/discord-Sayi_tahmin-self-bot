#BU MESAJI OKUYUN. KOYDUĞUM BÜTÜN YORUM SATIRLARINI OKUYUN ÇÜNKÜ BİRİNDE BİLE HATA YAPARSANIZ KOD ÇALIŞMAZ HEPSİNİ EKSİKSİZ OKUYUN VE EKSİKSİZ DOLDURUN.(BÜTÜN KODU İNCELEYİN def bot() kısmını bile)



import time
import requests
import pytz
import datetime
import os
import traceback
import sys

token = 'ODg2NjE2OTYyNjc4MDMwNDI3.GuIuLd.Yzv8syn4HCLstRDSAmQYy5JSgRf9VCll2Z0cO8'  # Buraya kendi kullanıcı tokeninizi koymanız gerekiyor
channel_id = '1132261852353658921'  # Buraya sayı tahmin oynayacağınız kanalın idsini koymanız gerekiyor
kullanıcı_id = '886616962678030427'  # Buraya kendi kullanıcı id nizi koymanız gerekiyor


os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


original_stderr = sys.stderr
sys.stderr = open("pygame_messages.txt", "w")



tz = pytz.timezone('Europe/Istanbul')

import pygame

pygame.init()
sys.stderr.close()
sys.stderr = original_stderr




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
        with open("crash_reports.txt", "w", encoding="utf-8") as report_file:
            zaman = datetime.datetime.now(tz).strftime("%Y-%m-%d   %H:%M:%S")
            report_file.write(error_msg, zaman)

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
                count += 1
                
                with open("log.txt", "a", encoding="utf-8") as dosya:
                    dosya.write(f"{mesaj:<35}{zaman:>70}\n")
            else:
                zaman = datetime.datetime.now(tz).strftime("%Y-%m-%d   %H:%M:%S")
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

                    if content.startswith(f'<@{kullanıcı_id}>, Tebrikler!'):  #burası ÇOK ÖNEMLİ buraya sayıyı bulunca botun size gönderdiği mesajın ilk 2-3 cümlesini eksiksiz koymanız lazım ve ayrıca sizin gözünüzle gördüğünüz kodda öyle yazılmıyor örnek : gözle görünen : @lama2923  kodda görünen: <@886616962678030427> 
                        say_count = count - 1
                        mesaj = f"Doğru sayı bulundu doğru sayı: {say_count}"
                        print(f"{mesaj:<35}{zaman:>70}")
                        count = 1  
                        
                        with open("log.txt", "a", encoding="utf-8") as dosya:
                            dosya.write(f"{mesaj:<35}{zaman:>70}\n")
                        
                        pygame.mixer.music.load("Sound/buldum.wav")
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            pygame.time.Clock().tick(10)
                        pass
                    elif content.startswith(f'<@{kullanıcı_id}>, Yazılan'): #burası ÇOK ÖNEMLİ buraya sayıyı bulunamayınca botun size gönderdiği mesajın ilk 2-3 cümlesini eksiksiz koymanız lazım ve ayrıca sizin gözünüzle gördüğünüz kodda öyle yazılmıyor örnek : gözle görünen : @lama2923  kodda görünen: <@886616962678030427> 
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
                                    with open("log.txt", "a", encoding="utf-8") as dosya:
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

                                        if content.startswith(f'<@{kullanıcı_id}>, Tebrikler!'):  #burası ÇOK ÖNEMLİ buraya sayıyı bulunca botun size gönderdiği mesajın ilk 2-3 cümlesini eksiksiz koymanız lazım ve ayrıca sizin gözünüzle gördüğünüz kodda öyle yazılmıyor örnek : gözle görünen : @lama2923  kodda görünen: <@886616962678030427> 
                                            wcount
                                            mesaj = f"Doğru sayı bulundu doğru sayı: {wcount}"
                                            print(f"{mesaj:<35}{zaman:>70}")
                                            count = 1  
                            
                                            with open("log.txt", "a", encoding="utf-8") as dosya:
                                                dosya.write(f"{mesaj:<35}{zaman:>70}\n")
                            
                                                pygame.mixer.music.load("Sound/buldum.wav")
                                                pygame.mixer.music.play()
                                                while pygame.mixer.music.get_busy():
                                                    pygame.time.Clock().tick(10)
                                                break
                                        elif content.startswith(f'<@{kullanıcı_id}>, Yazılan'): #burası ÇOK ÖNEMLİ buraya sayıyı bulunamayınca botun size gönderdiği mesajın ilk 2-3 cümlesini eksiksiz koymanız lazım ve ayrıca sizin gözünüzle gördüğünüz kodda öyle yazılmıyor örnek : gözle görünen : @lama2923  kodda görünen: <@886616962678030427> 
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

if not os.path.exists("log.txt"):
    open("log.txt", "w").close()  

bot()