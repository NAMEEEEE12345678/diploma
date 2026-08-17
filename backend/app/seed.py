import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zlib import crc32

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.city import City
from app.models.country import Country
from app.models.place import Place

DESTINATIONS = [
    {
        "name": "Казахстан", "code": "KZ",
        "description": "От степей до заснеженных вершин: современный ритм и великая природа.",
        "image_url": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=900&q=80",
        "cities": [{
            "name": "Алматы", "description": "Зелёный город у подножия Тянь-Шаня — для прогулок, кофе и горных выходных.",
            "image_url": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=900&q=80",
            "places": [
                {"name": "Медеу", "description": "Высокогорный спортивный комплекс в живописной долине.", "category": "Природа", "image_url": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=900&q=80", "latitude": 43.1578, "longitude": 77.0582, "estimated_cost": 0, "recommended_duration": 120},
                {"name": "Шымбулак", "description": "Горный курорт с панорамами и маршрутами для прогулок.", "category": "Природа", "image_url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=900&q=80", "latitude": 43.1258, "longitude": 77.0765, "estimated_cost": 6500, "recommended_duration": 240},
                {"name": "Зелёный базар", "description": "Колоритный рынок со специями, фруктами и местными продуктами.", "category": "Гастрономия", "image_url": "https://images.unsplash.com/photo-1488459716781-31db52582fe9?auto=format&fit=crop&w=900&q=80", "latitude": 43.2613, "longitude": 76.9557, "estimated_cost": 3000, "recommended_duration": 90},
            ],
        }],
    },
    {
        "name": "Турция", "code": "TR",
        "description": "Море, древние города и гастрономия на стыке Европы и Азии.",
        "image_url": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=900&q=80",
        "cities": [{
            "name": "Стамбул", "description": "Два континента, Босфор и улицы, где всегда есть что открыть.",
            "image_url": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=900&q=80",
            "places": [
                {"name": "Собор Святой Софии", "description": "Легендарный памятник византийской и османской истории.", "category": "История", "image_url": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=900&q=80", "latitude": 41.0086, "longitude": 28.9802, "estimated_cost": 25, "recommended_duration": 90},
                {"name": "Галатская башня", "description": "Историческая башня с видом на Золотой Рог и Босфор.", "category": "Панорама", "image_url": "https://images.unsplash.com/photo-1530841377377-3ff06c0ca713?auto=format&fit=crop&w=900&q=80", "latitude": 41.0256, "longitude": 28.9741, "estimated_cost": 30, "recommended_duration": 75},
                {"name": "Гранд-базар", "description": "Один из крупнейших крытых рынков мира.", "category": "Шопинг", "image_url": "https://images.unsplash.com/photo-1558551649-e44c8f992010?auto=format&fit=crop&w=900&q=80", "latitude": 41.0107, "longitude": 28.9680, "estimated_cost": 0, "recommended_duration": 120},
            ],
        }],
    },
    {
        "name": "Грузия", "code": "GE",
        "description": "Тёплые дворики, винная культура и горные дороги.",
        "image_url": "https://images.unsplash.com/photo-1565008576549-57569a49371d?auto=format&fit=crop&w=900&q=80",
        "cities": [{
            "name": "Тбилиси", "description": "Атмосферный город серных бань, балконов и винных баров.",
            "image_url": "https://images.unsplash.com/photo-1565008576549-57569a49371d?auto=format&fit=crop&w=900&q=80",
            "places": [
                {"name": "Старый Тбилиси", "description": "Узкие улицы, резные балконы и исторические кварталы.", "category": "Прогулка", "image_url": "https://images.unsplash.com/photo-1565008576549-57569a49371d?auto=format&fit=crop&w=900&q=80", "latitude": 41.6912, "longitude": 44.8015, "estimated_cost": 0, "recommended_duration": 180},
                {"name": "Крепость Нарикала", "description": "Древняя крепость над старым городом с отличным видом.", "category": "История", "image_url": "https://www.orexca.com/img/georgia/tbilisi/narikala.jpg", "latitude": 41.6878, "longitude": 44.8092, "estimated_cost": 0, "recommended_duration": 90},
                {"name": "Серные бани Абанотубани", "description": "Традиционные бани в одном из самых узнаваемых районов города.", "category": "Отдых", "image_url": "https://images.unsplash.com/photo-1608501078713-8e445a709b39?auto=format&fit=crop&w=900&q=80", "latitude": 41.6897, "longitude": 44.8114, "estimated_cost": 70, "recommended_duration": 120},
            ],
        }],
    },
]

EXTRA_PLACES = {
    "Алматы": [
        ("Кок-Тобе", "Панорама", 43.2325, 76.9756, 3500, 120),
        ("Парк 28 гвардейцев-панфиловцев", "Прогулка", 43.2581, 76.9545, 0, 90),
        ("Вознесенский собор", "Культура", 43.2587, 76.9542, 0, 60),
        ("Центральный музей Казахстана", "Музей", 43.2332, 76.9554, 1500, 120),
        ("Ботанический сад Алматы", "Природа", 43.2222, 76.9102, 1000, 120),
        ("Большое Алматинское озеро", "Природа", 43.0550, 76.9850, 0, 240),
        ("Театр оперы и балета имени Абая", "Развлечения", 43.2384, 76.9457, 4000, 150),
        ("Улица Панфилова", "Гастрономия", 43.2388, 76.9452, 2500, 120),
    ],
    "Стамбул": [
        ("Голубая мечеть", "История", 41.0054, 28.9768, 0, 75),
        ("Дворец Топкапы", "Музей", 41.0115, 28.9833, 35, 180),
        ("Прогулка по Босфору", "Природа", 41.0613, 29.0565, 25, 120),
        ("Рынок специй", "Шопинг", 41.0166, 28.9700, 0, 90),
        ("Улица Истикляль", "Прогулка", 41.0369, 28.9850, 0, 120),
        ("Музей Пера", "Музей", 41.0319, 28.9769, 15, 90),
        ("Кадыкёйский рынок", "Гастрономия", 40.9907, 29.0288, 20, 120),
        ("Парк Гюльхане", "Семейный отдых", 41.0133, 28.9823, 0, 90),
    ],
    "Тбилиси": [
        ("Проспект Руставели", "Прогулка", 41.6996, 44.7955, 0, 120),
        ("Мост Мира", "Панорама", 41.6932, 44.8075, 0, 45),
        ("Национальный музей Грузии", "Музей", 41.6963, 44.7997, 15, 120),
        ("Парк Рике", "Семейный отдых", 41.6930, 44.8100, 0, 90),
        ("Фуникулёр на Мтацминду", "Развлечения", 41.6950, 44.7860, 12, 150),
        ("Блошиный рынок у Сухого моста", "Шопинг", 41.7023, 44.8027, 0, 90),
        ("Винный бар в Сололаки", "Гастрономия", 41.6905, 44.8025, 30, 90),
        ("Тбилисский ботанический сад", "Природа", 41.6860, 44.8073, 5, 150),
    ],
}
DEFAULT_PLACE_IMAGE = "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=900&q=80"
WIKIMEDIA_API = "https://ru.wikipedia.org/w/api.php"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
_wikimedia_cache: dict[str, str | None] = {}


def _image_for(subject: str) -> str:
    """A stable individual photo URL, selected deterministically for one object."""
    lock = crc32(subject.encode("utf-8")) % 100000
    return f"https://picsum.photos/seed/trip-{lock}/1200/800"


def _wikimedia_image(subject: str) -> str | None:
    """Return a direct Wikimedia thumbnail for the named real-world object."""
    if subject in _wikimedia_cache:
        return _wikimedia_cache[subject]
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": subject, "gsrnamespace": 0, "gsrlimit": 1,
        "prop": "pageimages", "piprop": "thumbnail", "pithumbsize": 1200,
    }
    image = None
    # Commons file search is both faster and more useful for cards: it returns
    # an actual photograph, not an article without a suitable thumbnail.
    for api_url, namespace in ((COMMONS_API, 6),):
        try:
            params["gsrnamespace"] = namespace
            request = Request(f"{api_url}?{urlencode(params)}", headers={"User-Agent": "TripConstructorSeed/1.0"})
            with urlopen(request, timeout=5) as response:
                pages = json.load(response).get("query", {}).get("pages", {})
            image = next(iter(pages.values()), {}).get("thumbnail", {}).get("source")
            if image:
                break
        except Exception:
            continue
    _wikimedia_cache[subject] = image
    return image


def _resolved_image(subject: str, current_url: str) -> str:
    """Replace only generated placeholder URLs; curated existing URLs stay intact."""
    if not current_url.startswith("https://picsum.photos/"):
        return current_url
    return _wikimedia_image(subject) or current_url

# Additional destinations are deliberately kept in one idempotent catalogue.  Every
# city below has five real, geocoded places, so the planner always has material to use.
EXPANDED_DESTINATIONS = [
 ("Франция","FR","Париж",48.8566,2.3522,[('Эйфелева башня','Культура',48.8584,2.2945),('Лувр','Музей',48.8606,2.3376),('Собор Парижской Богоматери','История',48.8530,2.3499),('Монмартр','Прогулка',48.8867,2.3431),('Сад Тюильри','Природа',48.8634,2.3275)]),
 ("Франция","FR","Ницца",43.7102,7.2620,[('Английская набережная','Прогулка',43.6948,7.2655),('Старый город Ниццы','История',43.6965,7.2754),('Замковый холм','Панорама',43.6960,7.2816),('Музей Матисса','Музей',43.7214,7.2787),('Рынок Кур Салея','Гастрономия',43.6965,7.2750)]),
 ("Италия","IT","Рим",41.9028,12.4964,[('Колизей','История',41.8902,12.4922),('Фонтан Треви','Культура',41.9009,12.4833),('Пантеон','История',41.8986,12.4769),('Ватиканские музеи','Музей',41.9065,12.4536),('Вилла Боргезе','Природа',41.9142,12.4923)]),
 ("Италия","IT","Венеция",45.4408,12.3155,[('Площадь Сан-Марко','История',45.4340,12.3388),('Дворец дожей','Музей',45.4337,12.3404),('Мост Риальто','Прогулка',45.4380,12.3359),('Галерея Академии','Музей',45.4319,12.3285),('Остров Бурано','Прогулка',45.4855,12.4160)]),
 ("Испания","ES","Барселона",41.3874,2.1686,[('Саграда Фамилия','Культура',41.4036,2.1744),('Парк Гуэль','Природа',41.4145,2.1527),('Дом Бальо','Культура',41.3917,2.1649),('Готический квартал','История',41.3839,2.1762),('Рынок Бокерия','Гастрономия',41.3816,2.1718)]),
 ("Испания","ES","Мадрид",40.4168,-3.7038,[('Музей Прадо','Музей',40.4138,-3.6921),('Парк Ретиро','Природа',40.4153,-3.6844),('Королевский дворец','История',40.4180,-3.7143),('Площадь Майор','Прогулка',40.4155,-3.7074),('Рынок Сан-Мигель','Гастрономия',40.4154,-3.7085)]),
 ("США","US","Нью-Йорк",40.7128,-74.0060,[('Статуя Свободы','История',40.6892,-74.0445),('Центральный парк','Природа',40.7829,-73.9654),('Метрополитен-музей','Музей',40.7794,-73.9632),('Таймс-сквер','Развлечения',40.7580,-73.9855),('Бруклинский мост','Прогулка',40.7061,-73.9969)]),
 ("США","US","Сан-Франциско",37.7749,-122.4194,[('Мост Золотые Ворота','Панорама',37.8199,-122.4783),('Алькатрас','История',37.8267,-122.4230),('Пирс 39','Развлечения',37.8087,-122.4098),('Чайнатаун Сан-Франциско','Гастрономия',37.7941,-122.4078),('Парк Золотые Ворота','Природа',37.7694,-122.4862)]),
 ("Япония","JP","Токио",35.6762,139.6503,[('Храм Сэнсо-дзи','Культура',35.7148,139.7967),('Сибуя-скрэмбл','Развлечения',35.6595,139.7005),('Токийская башня','Панорама',35.6586,139.7454),('Музей Эдо-Токио','Музей',35.6969,139.7966),('Парк Уэно','Природа',35.7148,139.7732)]),
 ("Япония","JP","Киото",35.0116,135.7681,[('Фусими Инари-тайся','Культура',34.9671,135.7727),('Кинкаку-дзи','Культура',35.0394,135.7292),('Бамбуковая роща Арасияма','Природа',35.0170,135.6713),('Рынок Нисики','Гастрономия',35.0050,135.7648),('Киёмидзу-дэра','История',34.9949,135.7850)]),
 ("Таиланд","TH","Бангкок",13.7563,100.5018,[('Большой дворец','История',13.7500,100.4913),('Ват Арун','Культура',13.7437,100.4889),('Рынок Чатучак','Шопинг',13.7999,100.5501),('Улица Каосан','Развлечения',13.7589,100.4973),('Парк Лумпхини','Природа',13.7308,100.5418)]),
 ("ОАЭ","AE","Дубай",25.2048,55.2708,[('Бурдж-Халифа','Панорама',25.1972,55.2744),('Дубай-Молл','Шопинг',25.1985,55.2796),('Старый рынок Дубая','История',25.2706,55.2962),('Пальма Джумейра','Прогулка',25.1124,55.1390),('Пустынный заповедник Дубая','Природа',24.9524,55.6000)]),
 ("Португалия","PT","Лиссабон",38.7223,-9.1393,[('Башня Белен','История',38.6916,-9.2160),('Замок Святого Георгия','История',38.7139,-9.1335),('Трамвай 28','Прогулка',38.7130,-9.1394),('Район Алфама','Культура',38.7110,-9.1307),('Рынок Тайм-Аут','Гастрономия',38.7078,-9.1459)]),
 ("Нидерланды","NL","Амстердам",52.3676,4.9041,[('Рейксмюзеум','Музей',52.3600,4.8852),('Дом Анны Франк','История',52.3752,4.8840),('Каналы Амстердама','Прогулка',52.3670,4.8950),('Музей Ван Гога','Музей',52.3584,4.8811),('Вондельпарк','Природа',52.3580,4.8680)]),
 ("Германия","DE","Берлин",52.5200,13.4050,[('Бранденбургские ворота','История',52.5163,13.3777),('Музейный остров','Музей',52.5200,13.4010),('Рейхстаг','История',52.5186,13.3762),('Восточная галерея','Культура',52.5050,13.4390),('Тиргартен','Природа',52.5145,13.3501)]),
 ("Великобритания","GB","Лондон",51.5072,-0.1276,[('Британский музей','Музей',51.5194,-0.1270),('Тауэрский мост','История',51.5055,-0.0754),('Букингемский дворец','История',51.5014,-0.1419),('Гайд-парк','Природа',51.5073,-0.1657),('Боро-маркет','Гастрономия',51.5055,-0.0910)]),
 ("Австрия","AT","Вена",48.2082,16.3738,[('Дворец Шёнбрунн','История',48.1845,16.3122),('Собор Святого Стефана','Культура',48.2085,16.3731),('Бельведер','Музей',48.1912,16.3800),('Пратер','Развлечения',48.2167,16.3958),('Нашмаркт','Гастрономия',48.1986,16.3615)]),
 ("Чехия","CZ","Прага",50.0755,14.4378,[('Карлов мост','История',50.0865,14.4114),('Пражский град','История',50.0909,14.4005),('Староместская площадь','Прогулка',50.0870,14.4208),('Еврейский музей','Музей',50.0900,14.4207),('Петршинский холм','Природа',50.0835,14.3952)]),
 ("Греция","GR","Афины",37.9838,23.7275,[('Акрополь','История',37.9715,23.7267),('Музей Акрополя','Музей',37.9685,23.7286),('Плака','Прогулка',37.9737,23.7306),('Храм Зевса Олимпийского','История',37.9694,23.7330),('Холм Ликавит','Панорама',37.9839,23.7430)]),
 ("Египет","EG","Каир",30.0444,31.2357,[('Пирамиды Гизы','История',29.9792,31.1342),('Египетский музей','Музей',30.0478,31.2336),('Хан эль-Халили','Шопинг',30.0478,31.2625),('Цитадель Саладина','История',30.0299,31.2610),('Нилометр на острове Рода','Культура',30.0050,31.2250)]),
 ("Марокко","MA","Марракеш",31.6295,-7.9811,[('Площадь Джемаа-эль-Фна','Гастрономия',31.6258,-7.9891),('Сад Мажорель','Природа',31.6416,-8.0030),('Дворец Бахия','История',31.6219,-7.9835),('Медина Марракеша','Прогулка',31.6295,-7.9811),('Медресе Бен Юсеф','Культура',31.6332,-7.9869)]),
 ("Индонезия","ID","Бали",-8.4095,115.1889,[('Храм Танах-Лот','Культура',-8.6212,115.0868),('Рисовые террасы Тегаллаланг','Природа',-8.4312,115.2792),('Лес обезьян Убуда','Семейный отдых',-8.5188,115.2580),('Водопад Тегенунган','Природа',-8.5755,115.2896),('Убудский дворец','История',-8.5069,115.2625)]),
 ("Сингапур","SG","Сингапур",1.3521,103.8198,[('Сады у залива','Природа',1.2816,103.8636),('Марина-Бей-Сэндс','Панорама',1.2834,103.8607),('Чайнатаун Сингапура','Гастрономия',1.2837,103.8440),('Национальная галерея','Музей',1.2906,103.8519),('Остров Сентоза','Развлечения',1.2494,103.8303)]),
 ("Австралия","AU","Сидней",-33.8688,151.2093,[('Сиднейский оперный театр','Культура',-33.8568,151.2153),('Харбор-Бридж','Панорама',-33.8523,151.2108),('Бонди-Бич','Природа',-33.8915,151.2767),('Королевский ботанический сад','Природа',-33.8642,151.2166),('Рокс','История',-33.8598,151.2081)]),
 ("Южная Корея","KR","Сеул",37.5665,126.9780,[('Дворец Кёнбоккун','История',37.5796,126.9770),('Деревня Букчон','Культура',37.5826,126.9830),('Телебашня N Seoul','Панорама',37.5512,126.9882),('Рынок Кванчжан','Гастрономия',37.5701,127.0005),('Ручей Чхонгечхон','Прогулка',37.5692,126.9784)]),
 ("Вьетнам","VN","Ханой",21.0278,105.8342,[('Старый квартал Ханоя','Прогулка',21.0345,105.8500),('Храм литературы','Культура',21.0281,105.8354),('Озеро Хоан Кием','Природа',21.0287,105.8525),('Мавзолей Хо Ши Мина','История',21.0368,105.8347),('Рынок Донг Суан','Шопинг',21.0387,105.8500)]),
]

def _expanded_city(country_name, country_code, city_name, city_latitude, city_longitude, places):
    return {
        "name": country_name, "code": country_code,
        "description": f"Популярное направление для путешествия в {country_name}.",
        "image_url": _image_for(country_name),
        "cities": [{"name": city_name, "description": f"{city_name} — город с культурой, прогулками и яркими впечатлениями.", "image_url": _image_for(city_name),
                    "places": [{"name": name, "description": f"{name} — реальная достопримечательность в городе {city_name}.", "category": category, "image_url": _image_for(name), "latitude": latitude, "longitude": longitude, "estimated_cost": 25 if category in {"Музей", "Развлечения"} else 0, "recommended_duration": 120} for name, category, latitude, longitude in places]}]
    }


def seed_catalog() -> None:
    with SessionLocal() as db:
        all_destinations = [*DESTINATIONS, *[_expanded_city(*destination) for destination in EXPANDED_DESTINATIONS]]
        for country_data in all_destinations:
            country_data["image_url"] = _resolved_image(country_data["name"], country_data["image_url"])
            country = db.scalar(select(Country).where(Country.code == country_data["code"]))
            if country is None:
                country = Country(
                    name=country_data["name"], code=country_data["code"],
                    description=country_data["description"], image_url=country_data["image_url"],
                )
                db.add(country)
                db.flush()
            else:
                country.name = country_data["name"]
                country.description = country_data["description"]
                country.image_url = _resolved_image(country_data["name"], country_data["image_url"])

            for city_data in country_data["cities"]:
                city_data["image_url"] = _resolved_image(city_data["name"], city_data["image_url"])
                city = db.scalar(
                    select(City).where(City.country_id == country.id, City.name == city_data["name"])
                )
                if city is None:
                    city = City(
                        country_id=country.id, name=city_data["name"],
                        description=city_data["description"], image_url=city_data["image_url"],
                    )
                    db.add(city)
                    db.flush()
                else:
                    city.description = city_data["description"]
                    city.image_url = _resolved_image(city_data["name"], city_data["image_url"])

                for place_data in city_data["places"]:
                    place_data["image_url"] = _resolved_image(place_data["name"], place_data["image_url"])
                    place = db.scalar(
                        select(Place).where(Place.city_id == city.id, Place.name == place_data["name"])
                    )
                    if place is None:
                        db.add(Place(city_id=city.id, **place_data))
                    else:
                        for field, value in place_data.items():
                            setattr(place, field, value)
                for name, category, latitude, longitude, cost, duration in EXTRA_PLACES.get(city.name, []):
                    place = db.scalar(select(Place).where(Place.city_id == city.id, Place.name == name))
                    if place is None:
                        db.add(Place(city_id=city.id, name=name, description=f"{name} — популярное место для маршрута по городу.", category=category, image_url=_image_for(name), latitude=latitude, longitude=longitude, estimated_cost=cost, recommended_duration=duration))
                    else:
                        place.image_url = _resolved_image(name, place.image_url)
        db.commit()


if __name__ == "__main__":
    seed_catalog()
    print("Каталог направлений заполнен.")
