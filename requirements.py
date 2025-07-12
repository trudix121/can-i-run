from bs4 import BeautifulSoup
import requests as rq
from dotenv import load_dotenv
from google import genai
import os
import re
from colorama import Fore
load_dotenv()

ai = genai.Client(api_key=os.environ['API_KEY'])


def get_cpu_cores(cpu):
    # Eliminăm cuvântul 'better' din input
    cpu_clean = cpu.lower().replace("better", "").strip()
    
    # Trimitem curățat la model
    response = ai.models.generate_content(
        model="gemma-3n-e2b-it",
        contents=(
            f"Extract **only the number of CPU cores** from the following CPU model name(s):\n\n"
            f"Input: '{cpu_clean}'\n\n"
            "Rules:\n"
            "1. Return **only the number**, no explanation, no units (e.g., '8', not '8 cores').\n"
            "2. If the input is **not a CPU** or the **number of cores is not specified**, return 'None'.\n"
            "3. If **multiple CPUs** are listed, return the **lowest number of cores** found.\n\n"
            "Examples:\n"
            "* Intel Core i7-9700K 8 cores → 8\n"
            "* AMD Ryzen 5 5600X with 6 cores → 6\n"
            "* Intel Core i5-8250U (4 cores) / AMD Ryzen 5 5500 (6 cores) → 6\n"
            "* NVIDIA RTX 3080 → None\n\n"
            "* core 2 duo -> 2"
            "Return only the number, no explanation."
        )
    )

    text = response.text.strip().lower()

    if 'none' in text:
        return None


    return int(text)

def get_cpu_freq(cpu):
    # Eliminăm cuvântul 'better' din input
    cpu_clean = cpu.lower().replace("better", "").strip()
    
    # Trimitem curățat la model
    response = ai.models.generate_content(
        model="gemma-3n-e2b-it",
        contents=(
            f"Extract **only the numeric frequency in GHz** from the following CPU model name(s):\n\n"
            f"Input: '{cpu_clean}'\n\n"
            "Rules:\n"
            "1. Return **only the number**, without any unit (e.g., '3.5', not '3.5GHz').\n"
            "2. If the input is **not a CPU** or the **frequency is not specified**, return 'None'.\n"
            "3. If **multiple CPUs** are listed, return the **lowest frequency number** (only one number).\n\n"
            "Examples:\n"
            "* Intel Core i7-9700K 3.6GHz → 3.6\n"
            "* AMD Ryzen 5 5600X 4.6GHz → 4.6\n"
            "* Intel Core i5-8250U / AMD Ryzen 5 5500 3.7GHz → 3.7\n"
            "* NVIDIA RTX 3080 → None\n\n"
            "Return only the number, no explanation."
        )
    )

    text = response.text.strip().lower()

    if 'none' in text:
        return None

    match = re.search(r'(\d+(\.\d+)?)', text)
    if match:
        return float(match.group(1))
    return None


def get_gpu_memory(gpu):
    response = ai.models.generate_content(
    model="gemma-3n-e2b-it",
    contents=(
        "Extract **only the numeric memory size** of the GPU model provided as input.\n\n"
        "Rules:\n"
        "1. Return **only the number**, without any units (e.g., '6', not '6GB').\n"
        "2. If a **frequency (e.g., MHz)** is specified instead of memory, return that number.\n"
        "3. If the input is **not a GPU**, return 'None'.\n"
        "4. If the **memory is specified**, return that number.\n"
        "5. If **multiple GPUs** are listed, return the **lowest memory amount** (only one number).\n\n"
        "Examples:\n"
        "* geforce gtx 1060 6gb → 6\n"
        "* radeon rx 580 8gb → 8\n"
        "* arc a380 → None\n"
        "* intel core i7 → None\n"
        "* 2x RTX 2080 Ti 11GB, 1x GTX 1050 2GB → 2\n"
        "* geforce gtx 960, 1300 MHz → 1300\n\n"
        "Provide only the extracted number, no explanation."
    )
)


    text = response.text.strip().lower()

    if 'none' in text:
        return None

    match = re.search(r'(\d+)', text)
    if match:
        return int(match.group(1))  # sau float(...) dacă vrei și zecimale
    return None

    
def get_game_name(id:int):
    url = f"https://store.steampowered.com/api/appdetails/?appids={id}&l=english"
    res = rq.get(url=url).json()[str(id)]['data']['name']
    return res

def get_requirements(id: int, minimum= True):
    url = f"https://store.steampowered.com/api/appdetails/?appids={id}&l=english"
    res = rq.get(url=url).json()[str(id)]['data']['pc_requirements']['minimum'] if minimum == True else rq.get(url=url).json()[str(id)]['data']['pc_requirements']['recommended']
    soup = BeautifulSoup(res, 'html.parser')
    fields = {}

    # Construim un dicționar: "Memorie" → "4 GB RAM"
    for li in soup.find_all('li'):
        strong = li.find('strong')
        if strong:
            key = strong.text.strip().rstrip(':')
            full_text = li.get_text(strip=True)
            value = full_text.replace(strong.text, '').strip(': ').strip()
            fields[key.lower()] = value.lower()
            
    # CPU
    cpu_text = fields.get('processor', '')
    cpu_intel = cpu_text

    # GPU
    gpu_text = fields.get('graphics', '')
    gpu_nvidia = gpu_text

    # RAM
    ram_value = 0
    if 'memory' in fields:
        ram_match = re.search(r'(\d+)', fields['memory'])
        if ram_match:
            ram_value = int(ram_match.group(1))
            if 'MB' in fields['memory'] or 'mb' in fields['memory']:
                ram_value = round(ram_value / 1024)

    # SIZE
    size_value = 0
    if 'storage' in fields:
        size_match = re.search(r'(\d+)', fields['storage'])
        if size_match:
            size_value = int(size_match.group(1))
            if 'mb' in fields['storage']:
                size_value = round(size_value / 1024)

    # Fallback la 0 dacă nu se pot interpreta corect
    ram = int(ram_value)
    size = int(size_value)


    cpu_freq = get_cpu_freq(cpu_intel) if cpu_intel else None
    gpu_memory = get_gpu_memory(gpu_nvidia) if gpu_nvidia else None
    cpu_cores = get_cpu_cores(cpu_intel) if cpu_intel else None

    return size, cpu_freq, cpu_cores, gpu_memory, ram
