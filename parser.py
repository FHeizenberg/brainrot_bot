import os
import requests


def download_images(base_url, start_num, end_num, output_folder='images'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(start_num, end_num + 1):
        filename = f"itabr{i}.png"
        image_url = base_url.replace("itabr32.png", filename)

        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()

            filepath = os.path.join(output_folder, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            print(f"Успешно скачано: {filename}")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке {filename}: {e}")


base_url = "https://tiermaker.com/images/media/template_images/2024/1656085/all-italian-brainrot-animals-tiktok-meme-1656085/itabr32.png"
start_num = 1
end_num = 32

download_images(base_url, start_num, end_num)
