import csv
from datetime import datetime as dt
from typing import Dict, Any, Iterable, List, Tuple, Optional

RESULT_FILE_PATH = 'clients_info.txt'
REGION_NAME_POSITION = 0


def parse_csv(csv_path: str) -> Iterable[Dict[str, Any]]:
    print('Начали парсить исходный файл.')

    with open(csv_path, 'r', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            yield row


def transform_dict_item_to_client_info(user_data: Dict[str, Any]) -> str:
    name = user_data.get('name', None)
    device_type = user_data.get('device_type', None)
    browser = user_data.get('browser', None)
    sex = user_data.get('sex', None)
    age = user_data.get('age', None)
    bill = user_data.get('bill', None)
    region = user_data.get('region', None)

    regions_names, regions_message = get_regions_info(region=region)

    info = (
        f'Пользователь {remove_extra_whitespaces(name)} '
        f'{"женского" if sex == "female" else "мужского"} пола, '
        f'{age} лет '
        f'{"совершила" if sex == "female" else "совершил"} '
        f'покупку на {bill} у.е. '
        f'с {"мобильного" if device_type in ("mobile", "tablet") else "десктопного"} браузера {browser}. '
        f'{regions_message} {regions_names}.'
    )

    return info


def remove_extra_whitespaces(string: str) -> str:
    return " ".join([word.strip() for word in string.split()])


def get_regions_info(region: Optional[str]) -> Tuple[str, str]:
    region_names = "неизвестен"
    region_message = 'Регион, из которого совершалась покупка:'

    if region is None or region == "-":
        return region_names, region_message
    else:
        region_list = region.split(" / ")

        if len(region_list) > 1:
            region_message = 'Регионы, из которых совершались покупки:'
            region_names = ', '.join(region for region in region_list)
        else:
            region_names = region_list[REGION_NAME_POSITION]

        return region_names, region_message


def write_clients_info_to_file(clients_info: List[str]) -> None:
    with open(RESULT_FILE_PATH, 'w', encoding="utf-8") as file:
        file.writelines([client + "\n" for client in clients_info])


if __name__ == '__main__':
    file_path = 'web_clients_correct.csv'
    clients_info = []
    row_counter = 0

    start = dt.now()

    print(f'Программа начала работу. Время начала работы {start.strftime("%Y-%m-%d %H:%M:%S")}')

    for user_data in parse_csv(csv_path=file_path):
        row_counter += 1

        try:
            if row_counter % 100 == 0:
                print(f'Обработано {row_counter} строк.')

            clients_info.append(transform_dict_item_to_client_info(user_data=user_data))
        except Exception as error:
            print(
                f'Получена ошибка: {error.__class__.__name__}. '
                f'Необходимо проверить корректность данных на строке: {row_counter} в исходном файле.'
            )

    print('Записываем результат работы программы в файл: clients_info.txt.')
    write_clients_info_to_file(clients_info)
    end = dt.now() - start
    print(f'Программа завершила работу. Время выполнения составило: {round(end.total_seconds())} секунд.')
