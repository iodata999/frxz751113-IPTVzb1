import time
import os
import re
import base64
import datetime
import requests
import threading
from queue import Queue
from datetime import datetime


input_file=结果.txt
output_file=结果.m3u
echo "#EXTM3U" > "$output_file"

# Pętla odczytująca każdą linię z pliku wejściowego
while IFS= read -r line; do
    # Wyciągnięcie nazwy streamu i adresu URL
    stream_name=$(echo "$line" | cut -d$'\t' -f1)
    stream_url=$(echo "$line" | cut -d$'\t' -f2-)

    # Dodanie wpisu do pliku M3U
    echo "#EXTINF:-1,$stream_name" >> "$output_file"
    echo "$stream_url" >> "$output_file"
done < "$input_file"

echo "Plik M3U został wygenerowany: $output_file"
print(f"成功寫出M3U file")
