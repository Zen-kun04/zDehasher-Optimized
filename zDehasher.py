import hashlib, time, os, shutil, re
from colorama import Fore

passwords = []

jsexp_gay = """
           /$$$$$$$            /$$                           /$$                          
          | $$__  $$          | $$                          | $$                          
 /$$$$$$$$| $$  \ $$  /$$$$$$ | $$$$$$$   /$$$$$$   /$$$$$$$| $$$$$$$   /$$$$$$   /$$$$$$ 
|____ /$$/| $$  | $$ /$$__  $$| $$__  $$ |____  $$ /$$_____/| $$__  $$ /$$__  $$ /$$__  $$
   /$$$$/ | $$  | $$| $$$$$$$$| $$  \ $$  /$$$$$$$|  $$$$$$ | $$  \ $$| $$$$$$$$| $$  \__/
  /$$__/  | $$  | $$| $$_____/| $$  | $$ /$$__  $$ \____  $$| $$  | $$| $$_____/| $$      
 /$$$$$$$$| $$$$$$$/|  $$$$$$$| $$  | $$|  $$$$$$$ /$$$$$$$/| $$  | $$|  $$$$$$$| $$      
|________/|_______/  \_______/|__/  |__/ \_______/|_______/ |__/  |__/ \_______/|__/      
                                                                               
"""

def clear_screen():
    os.system("cls || clear")

def printcenter(text):
    size = shutil.get_terminal_size().columns
    for line in text.split("\n"):
        print(' ' * (round((size/2)-len(line)/2)), line)

def bruteforce(hash_str: str, salt: str = None):
    # SHA256
    if len(hash_str) == 64:
        for password in passwords:
            if hashlib.sha256(password.encode()).hexdigest() == hash_str:
                return (hash_str, password)
            if salt is not None and (hashlib.sha256(password.encode() + salt.encode()).hexdigest() == hash_str or hashlib.sha256(hashlib.sha256(password.encode()).hexdigest().encode() + salt.encode()).hexdigest() == hash_str):
                return (hash_str, password)
    # SHA512
    elif len(hash_str) == 128:
        for password in passwords:
            if hashlib.sha512(password.encode()).hexdigest() == hash_str:
                return (hash_str, password)
            if salt is not None and (hashlib.sha512(password.encode() + salt.encode()).hexdigest() == hash_str or hashlib.sha512(hashlib.sha512(password.encode()).hexdigest().encode() + salt.encode()).hexdigest() == hash_str):
                return (hash_str, password)
    return None

def main():
    global passwords
    clear_screen()
    print()
    printcenter(f"{Fore.YELLOW}{jsexp_gay}")
    wordlist = input(f"{Fore.RED} [»] {Fore.LIGHTBLUE_EX}Nombre/Ruta de la Wordlist: {Fore.WHITE}")
    if not os.path.isfile(wordlist):
        clear_screen()
        printcenter(f"{Fore.YELLOW}{jsexp_gay}")
        printcenter(f"{Fore.LIGHTBLUE_EX}[ERROR] {Fore.WHITE}No se pudo cargar la Wordlist, intentalo nuevamente.")
        time.sleep(5)
        print()
        main()
    else:
        clear_screen()
        printcenter(f"{Fore.YELLOW}{jsexp_gay}")
        printcenter(f"{Fore.LIGHTBLUE_EX}[LOG] {Fore.WHITE}Cargando la Wordlist, espera..")
        with open(wordlist, 'r', encoding="latin-1") as f:
            passwords = [password.strip() for password in f]
            clear_screen()
            printcenter(f"{Fore.YELLOW}{jsexp_gay}")
            printcenter(f"{Fore.LIGHTBLUE_EX}             [LOG]{Fore.WHITE} Han sido cargadas {Fore.RED}{len(passwords)} {Fore.WHITE}contraseñas.")
            print()
            printcenter(f"{Fore.LIGHTBLUE_EX}[INFO] {Fore.WHITE}Introduce el Hash, luego el Salt. {Fore.YELLOW}¿No tienes Salt? {Fore.WHITE}Dejalo vacio.")
            print()
            
        while True:
            hash_str = input(f"{Fore.RED} [»] {Fore.LIGHTBLUE_EX}Introduce un hash: {Fore.WHITE}")
            if len(hash_str) < 32 or len(hash_str) > 128:
                clear_screen()
                printcenter(f"{Fore.YELLOW}{jsexp_gay}")
                printcenter(f"{Fore.LIGHTBLUE_EX}[ERROR] {Fore.WHITE}Hash invalido.")
                time.sleep(5)
                print()
                main()
            print()
            salt = input(f"{Fore.RED} [»] {Fore.LIGHTBLUE_EX}Introduce un salt: {Fore.WHITE}")
            start = time.perf_counter()
            if salt.strip() != "":
                final = bruteforce(hash_str, salt)
            else:
                final = bruteforce(hash_str)
            end = time.perf_counter()

            if final is None:
                clear_screen()
                printcenter(f"{Fore.YELLOW}{jsexp_gay}")
                printcenter(f"{Fore.LIGHTBLUE_EX}[LOG]{Fore.WHITE} Hash/Salt invalido o contraseña no encontrada.")
                time.sleep(15)
                main()
            if final[0] == hash_str:
                clear_screen()
                printcenter(f"{Fore.YELLOW}{jsexp_gay}")
                printcenter(f"{Fore.LIGHTBLUE_EX}[LOG]{Fore.WHITE} Posible contraseña encontrada -> {Fore.RED}{final[1]} {Fore.RESET}({Fore.LIGHTBLUE_EX}{end-start:.3f}s{Fore.RESET})")
                print()
                print()
                printcenter(f"{Fore.YELLOW}(1) {Fore.WHITE}Menu principal {Fore.YELLOW}(2) {Fore.WHITE}Salir")
                print()
                option = input(f"{Fore.RED} [»] {Fore.LIGHTBLUE_EX}Selecciona una opcion: {Fore.WHITE}")
                if option == "1":
                    main()
                elif option == "2":
                    clear_screen()
                    exit()
                else:
                    clear_screen()
                    printcenter(f"{Fore.YELLOW}{jsexp_gay}")
                    printcenter(f"{Fore.LIGHTBLUE_EX}[ERROR] {Fore.WHITE}¡Debes de seleccionar una opcion valida!")
                    time.sleep(5)
                    main()


def divider(content: str) -> str:
    hash_str = re.search(r"[^$SHA]\w{127}", content)
    if hash_str is None:
        hash_str = re.search(r"[^$SHA]\w{63}", content)
        if hash_str is None:
            return None
    hash_str = hash_str.group()
    salt = ''.join(item for item in content.split('$') if item != hash_str and len(item) < len(hash_str) and not item.lower().startswith('sha'))
    return f"{hash_str}:{salt}"

if __name__ == "__main__":
    print("1) Convert raw hash to hash:salt")
    print("2) Use the optimized zDehasher")
    opt = input("> ")
    if opt == "2":
        main()
    else:
        raw = input("\n\nRaw hash: ")
        divided = divider(raw)
        print("Divided:\n" + divided)