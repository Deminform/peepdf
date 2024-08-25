import os
import subprocess
import pikepdf
from colorama import init, Fore, Style

# Инициализация Colorama
init(autoreset=True)



def check_pdf_with_qpdf(pdf_path):
    """
    Проверяет целостность PDF-файла с помощью QPDF.
    """
    try:
        print(Fore.CYAN + f"\nRunning QPDF check on: {pdf_path}")
        result = subprocess.run(['qpdf', '--check', pdf_path], capture_output=True, text=True)
        if result.returncode == 0:
            print(Fore.GREEN + "QPDF: PDF is structurally sound.")
        else:
            print(Fore.RED + "QPDF: Issues found in PDF structure.")
            print(Fore.RED + result.stderr)
    except FileNotFoundError:
        print(Fore.RED + "Error: QPDF is not installed or not found in system PATH.")
    except Exception as e:
        print(Fore.RED + f"An error occurred while checking with QPDF: {e}")


def analyze_metadata_with_pikepdf(pdf_path):
    """
    Анализирует метаданные PDF-файла с помощью pikepdf.
    """
    try:
        print(Fore.CYAN + f"\nAnalyzing metadata with pikepdf for: {pdf_path}")
        with pikepdf.open(pdf_path) as pdf:
            metadata = pdf.docinfo
            if metadata:
                print(Fore.YELLOW + "Metadata found:")
                for key, value in metadata.items():
                    print(Fore.YELLOW + f"{key}: {value}")
            else:
                print(Fore.RED + "No metadata found.")
    except Exception as e:
        print(Fore.RED + f"An error occurred while analyzing with pikepdf: {e}")


def process_pdf_file(pdf_path):
    """
    Выполняет полный анализ для одного PDF-файла.
    """
    print(Style.BRIGHT + Fore.MAGENTA + f"\n{'-' * 40}\nProcessing file: {pdf_path}\n{'-' * 40}")
    check_pdf_with_qpdf(pdf_path)
    analyze_metadata_with_pikepdf(pdf_path)
    print(Style.BRIGHT + Fore.MAGENTA + f"\n{'-' * 40}\nFinished processing: {pdf_path}\n{'-' * 40}\n")


def process_directory(directory_path):
    """
    Обрабатывает все PDF-файлы в указанном каталоге.
    """
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                process_pdf_file(pdf_path)


if __name__ == "__main__":
    path = input(Style.BRIGHT + Fore.CYAN + "Please enter the path to your PDF file or directory: ")

    if os.path.isfile(path) and path.lower().endswith('.pdf'):
        # Если путь указывает на PDF-файл, обрабатываем его
        process_pdf_file(path)
    elif os.path.isdir(path):
        # Если путь указывает на каталог, обрабатываем все PDF-файлы в каталоге
        process_directory(path)
    else:
        print(Fore.RED + "The provided path is not a valid PDF file or directory.")

    print(Style.BRIGHT + Fore.GREEN + "\nAnalysis complete.")
