import os
import sys
from typing import List
import time

# Language dictionaries
TRANSLATIONS = {
    'bg': {
        'menu_title': 'Изберете опция:',
        'encrypt': 'Криптиране на файл',
        'decrypt': 'Декриптиране на файл',
        'change_lang': 'Смяна на език',
        'exit': 'Изход',
        'choice_prompt': 'Въведете вашия избор (1-4): ',
        'goodbye': 'Довиждане!',
        'invalid_choice': 'Невалиден избор! Моля изберете отново.',
        'enter_file': 'Въведете път до файла: ',
        'file_not_exist': 'Файлът не съществува!',
        'enter_key': 'Въведете ключ за криптиране: ',
        'empty_key': 'Ключът не може да бъде празен!',
        'processing': 'Обработване на файла...',
        'done': 'Готово! Време за изпълнение: {:.2f} секунди',
        'result_saved': 'Резултатът е записан в: {}',
        'error_occurred': 'Възникна грешка при обработката на файла!',
        'press_enter': 'Натиснете Enter за да продължите...',
        'select_language': 'Изберете език / Select language / Выберите язык:\n1. Български\n2. English\n3. Русский'
    },
    'en': {
        'menu_title': 'Select an option:',
        'encrypt': 'Encrypt a file',
        'decrypt': 'Decrypt a file',
        'change_lang': 'Change language',
        'exit': 'Exit',
        'choice_prompt': 'Enter your choice (1-4): ',
        'goodbye': 'Goodbye!',
        'invalid_choice': 'Invalid choice! Please try again.',
        'enter_file': 'Enter file path: ',
        'file_not_exist': 'File does not exist!',
        'enter_key': 'Enter encryption key: ',
        'empty_key': 'Key cannot be empty!',
        'processing': 'Processing file...',
        'done': 'Done! Execution time: {:.2f} seconds',
        'result_saved': 'Result saved to: {}',
        'error_occurred': 'An error occurred while processing the file!',
        'press_enter': 'Press Enter to continue...',
        'select_language': 'Изберете език / Select language / Выберите язык:\n1. Български\n2. English\n3. Русский'
    },
    'ru': {
        'menu_title': 'Выберите опцию:',
        'encrypt': 'Зашифровать файл',
        'decrypt': 'Расшифровать файл',
        'change_lang': 'Сменить язык',
        'exit': 'Выход',
        'choice_prompt': 'Введите ваш выбор (1-4): ',
        'goodbye': 'До свидания!',
        'invalid_choice': 'Неверный выбор! Пожалуйста, попробуйте снова.',
        'enter_file': 'Введите путь к файлу: ',
        'file_not_exist': 'Файл не существует!',
        'enter_key': 'Введите ключ шифрования: ',
        'empty_key': 'Ключ не может быть пустым!',
        'processing': 'Обработка файла...',
        'done': 'Готово! Время выполнения: {:.2f} секунд',
        'result_saved': 'Результат сохранен в: {}',
        'error_occurred': 'Произошла ошибка при обработке файла!',
        'press_enter': 'Нажмите Enter для продолжения...',
        'select_language': 'Изберете език / Select language / Выберите язык:\n1. Български\n2. English\n3. Русский'
    }
}

class FibonacciCrypton:
    def __init__(self, key: str):
        self.key = self._generate_key_from_string(key)
        self.fib_sequence = self._generate_fibonacci(32)  # Generate first 32 Fibonacci numbers
    
    def _generate_key_from_string(self, key: str) -> List[int]:
        # Convert string key to list of integers
        return [ord(c) for c in key]
    
    def _generate_fibonacci(self, n: int) -> List[int]:
        # Generate Fibonacci sequence
        fib = [1, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return fib
    
    def encrypt_byte(self, byte: int, position: int) -> int:
        # Custom encryption using Fibonacci numbers and key
        key_byte = self.key[position % len(self.key)]
        fib_num = self.fib_sequence[position % len(self.fib_sequence)]
        encrypted = (byte + key_byte + fib_num) % 256
        return encrypted
    
    def decrypt_byte(self, byte: int, position: int) -> int:
        # Reverse the encryption process
        key_byte = self.key[position % len(self.key)]
        fib_num = self.fib_sequence[position % len(self.fib_sequence)]
        decrypted = (byte - key_byte - fib_num) % 256
        return decrypted

    def process_file(self, input_path: str, output_path: str, encrypt: bool = True) -> None:
        try:
            with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
                position = 0
                while True:
                    byte = infile.read(1)
                    if not byte:
                        break
                    
                    byte_value = int.from_bytes(byte, byteorder='big')
                    if encrypt:
                        processed_byte = self.encrypt_byte(byte_value, position)
                    else:
                        processed_byte = self.decrypt_byte(byte_value, position)
                    
                    outfile.write(bytes([processed_byte]))
                    position += 1
            return True
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            return False

def print_banner():
    banner = """                                                                                                                                                                                       
                                                                            
                                                                            
                             #%%%@@@%%%#%#**                                
                         %%@@@@@@@@@%%+++++++++                             
                      #%%%@%###%%%@@@@%%@%#****+--::::                      
                   #%%@%%**%@@@@%%#*++====+#**##*=---:::::-                 
                   *#%#+-+%@@@@%%%##*+====-=*+=++#+---::::                  
                    =%%=#@@@%%%%#####%%*===-*%-====-----:::                 
                  =#@@#%@@#+--:::::::::=*%*+#@===++=------:::::-            
                 #%@@@@@%+==--:--:::::::-=#@#@*=++++--=------::::           
                 -*%@@@@%++==---=+*#*+-:-=*%@@#+*+*+==---------:::          
           --- --:---+%%%**##*--+###**+=-=#%%@%+#++++===-------::::         
         ------:::::::-*%**#*+:--=++#*+==-*%@@#*#****=--------:::::         
       --:::::::::::::--#*++*-:-::=+==-::-+#@@%*##***===--------:::::       
         ----::::::::---++=++:::::::::::--=*%%%*#%***======---------:       
          -:-:::::::----=*+*+-===---::::---==+%*#@#**+++====-=-------:      
         --:-------------+##**+:-----------=+#%##@%#*+++++=====------       
       ------------------=+##*+++++=---------+%%#%%#*+++=====-----:::::     
      --------------------=****==--------=-::-%%#*%%#++============--::     
        ---------------=----+*=-----::-==-:::-%@@##%#+===+++====+=++=-      
         ::-------------==---=*-::--=**=-:::+%@%%@%@%+++*++++++++++++=-     
          ---:-::-:::::---------=#%#+-----+#%%%%%%%%%*******++++++++++=     
          ----:--- -::---====--=##*=-==+#%%@%%%%%%%%%@%#***+***+++++++=-:   
            --:::::--------=+#%%%%%%%%%%%%%%%%%%%%%%%%%%%#**+=+*++++++=---  
          --::::::-------=*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*+=++++++++=--  
       -----::::-----==*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@@@@%*++===+++=--  
       ------:-----=+#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@@@@%#*+++==----  
      -----------==#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@@@@%#*++=----  
      ---------===#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@@%@@%%@@@@%*+==---  
      --------===#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@@%%%@@%%%@@%*+==--- 
      -------===#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@%*+==-- 
      --:---===#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@%*+=-- 
       ---====#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@%%@%%%%%%%%%%%@@@%#+-:  
       ---=++*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@%%%%@%%%%%%%%%%%%%#=-:  
        --=++#%%%%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@%%%%%%%%%%%%%%%%%%#=-   
         --=*%%%%%%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@@%%%%%%%%%%%%+=     
         --=*#%%####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@%%%%%%%%%%#*+       
          -=*#######%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#+           
            ++*+**##%###%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#**=             
               ++***#*####%%%%%%%#%%%%######%#####%%*#**+==                 
                   +++***#######*#%%%##*#####*==+*                          
                            +*+*++++*++*++=                                 
                                                                            
    """
    print(banner)

def print_menu(lang: str):
    menu = f"""
    [1] {TRANSLATIONS[lang]['encrypt']}
    [2] {TRANSLATIONS[lang]['decrypt']}
    [3] {TRANSLATIONS[lang]['change_lang']}
    [4] {TRANSLATIONS[lang]['exit']}
    """
    print(menu)

def select_language() -> str:
    print(TRANSLATIONS['en']['select_language'])
    while True:
        choice = input("Choice/Избор/Выбор (1-3): ").strip()
        if choice == '1':
            return 'bg'
        elif choice == '2':
            return 'en'
        elif choice == '3':
            return 'ru'

def main():
    print_banner()
    current_lang = 'bg'  # Default language
    
    while True:
        print_menu(current_lang)
        choice = input(TRANSLATIONS[current_lang]['choice_prompt'])
        
        if choice == '4':
            print("\n" + TRANSLATIONS[current_lang]['goodbye'])
            break
            
        if choice == '3':
            current_lang = select_language()
            continue
            
        if choice not in ['1', '2']:
            print("\n" + TRANSLATIONS[current_lang]['invalid_choice'])
            continue
            
        input_file = input("\n" + TRANSLATIONS[current_lang]['enter_file']).strip()
        if not os.path.exists(input_file):
            print("\n" + TRANSLATIONS[current_lang]['file_not_exist'])
            continue
            
        key = input(TRANSLATIONS[current_lang]['enter_key']).strip()
        if not key:
            print("\n" + TRANSLATIONS[current_lang]['empty_key'])
            continue
            
        # Create crypton instance
        crypton = FibonacciCrypton(key)
        
        # Determine output file name
        output_file = input_file + ('.encrypted' if choice == '1' else '.decrypted')
        
        print("\n" + TRANSLATIONS[current_lang]['processing'])
        
        start_time = time.time()
        
        success = crypton.process_file(input_file, output_file, choice == '1')
        
        if success:
            end_time = time.time()
            print("\n" + TRANSLATIONS[current_lang]['done'].format(end_time - start_time))
            print(TRANSLATIONS[current_lang]['result_saved'].format(output_file))
        else:
            print("\n" + TRANSLATIONS[current_lang]['error_occurred'])
        
        input("\n" + TRANSLATIONS[current_lang]['press_enter'])

if __name__ == "__main__":
    main() 