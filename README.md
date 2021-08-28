# ruTS-API
API для работы с библиотекой ruTS

## REST API

### `POST` `/extract/sents/`

Извлечение предложений из текста.

Пример запроса:

```json
{
  "text": "Да. Времена изменились. Дети больше не слушаются своих родителей, и каждый пишет книги.",
  "min_len": 5,
  "max_len": 0
}
```

Аргументы:

| Аргумент | Тип | Описание |
| :-: | :-: | :-: |
| `text` | str | Текст, для которого извлекаются предложения |
| `min_len` | int | Минимальная длина извлекаемого предложения |
| `max_len` | int | Максимальная длина извлекаемого предложения |

Пример ответа:

```json
[
  "Времена изменились.",
  "Дети больше не слушаются своих родителей, и каждый пишет книги."
]
```

---

### `POST` `/extract/words/`

Извлечение слов из текста.

Пример запроса:

```json
{
  "text": "Живет свободно только тот, кто находит радость в исполнении своего долга.",
  "filter_punct": true,
  "filter_nums": false,
  "use_lexemes": true,
  "stopwords": [
    "кто",
    "в",
    "тот"
  ],
  "lowercase": true,
  "ngram_range": [
    2,
    2
  ],
  "min_len": 0,
  "max_len": 0,
  "most_common": 0
}
```

Аргументы:

| Аргумент | Тип | Описание |
| :-: | :-: | :-: |
| `text` | str | Текст, для которого извлекаются слова |
| `filter_punct` | bool | Фильтровать знаки препинания |
| `filter_nums` | bool | Фильтровать числа |
| `use_lexemes` | bool | Использовать леммы слов |
| `stopwords` | list[str] | Список стоп-слов |
| `lowercase` | bool | Конвертировать слова в нижний регистр |
| `ngram_range` | tuple[int, int] | Нижняя и верхняя граница размера N-грамм |
| `min_len` | int | Минимальная длина извлекаемого слова |
| `max_len` | int | Максимальная длина извлекаемого слова |
| `most_common` | int | Количество топ-слов |

Пример ответа:

```json
[
  "жить_свободно",
  "свободно_только",
  "только_находить",
  "находить_радость",
  "радость_исполнение",
  "исполнение_свой",
  "свой_долг"
]
```

---

### `POST` `/bs/`

Вычисление основных статистик текста.

Пример запроса:

```json
{
  "text": "Живет свободно только тот, кто находит радость в исполнении своего долга.",
  "normalize": false,
  "stat": ""
}
```

Аргументы:

| Аргумент | Тип | Описание |
| :-: | :-: | :-: |
| `text` | str | Текст, для которого вычисляются статистики |
| `normalize` | bool | Вычислять нормализованные статистики |
| `stat` | str | Наименование конкретной статистики |

Пример ответа:

```json
{
  "c_letters": {
    "1": 1,
    "3": 2,
    "5": 2,
    "6": 2,
    "7": 2,
    "8": 1,
    "10": 1
  },
  "c_syllables": {
    "0": 1,
    "1": 2,
    "2": 4,
    "3": 3,
    "5": 1
  },
  "n_sents": 1,
  "n_words": 11,
  "n_unique_words": 11,
  "n_long_words": 6,
  "n_complex_words": 1,
  "n_simple_words": 9,
  "n_monosyllable_words": 2,
  "n_polysyllable_words": 8,
  "n_chars": 73,
  "n_letters": 61,
  "n_spaces": 10,
  "n_syllables": 24,
  "n_punctuations": 2
}
```

---

### `POST` `/ms/`

Вычисление морфологических статистик текста.

Пример запроса:

```json
{
  "text": "Живет свободно только тот, кто находит радость в исполнении своего долга.",
  "filter_none": true,
  "stats": [
    "pos",
    "case"
  ]
}
```

Аргументы:

| Аргумент | Тип | Описание |
| :-: | :-: | :-: |
| `text` | str | Текст, для которого вычисляются статистики |
| `filter_none` | bool | Фильтровать пустые значения |
| `stats` | list[str] | Кортеж выбранных статистик |

Пример ответа:

```json
{
  "pos": {
    "VERB": 2,
    "ADVB": 2,
    "ADJF": 2,
    "NPRO": 1,
    "NOUN": 3,
    "PREP": 1
  },
  "case": {
    "nomn": 2,
    "accs": 1,
    "loct": 1,
    "gent": 2
  }
}
```

---

### `POST` `/ms/explain/`

Разбор текста по морфологическим статистикам.

Пример запроса:

```json
{
  "text": "Живет свободно только тот, кто находит радость в исполнении своего долга.",
  "filter_none": true,
  "stats": ["pos"]
}
```

Аргументы:

| Аргумент | Тип | Описание |
| :-: | :-: | :-: |
| `text` | str | Текст, для которого вычисляются статистики |
| `filter_none` | bool | Фильтровать пустые значения |
| `stats` | list[str] | Кортеж выбранных статистик |

Пример ответа:

```json
[
  [
    "Живет",
    {"pos": "VERB"}
  ],
  [
    "свободно",
    {"pos": "ADVB"}
  ],
  [
    "только",
    {"pos": "ADVB"}
  ],
  [
    "тот",
    {"pos": "ADJF"}
  ],
  [
    "кто",
    {"pos": "NPRO"}
  ],
  [
    "находит",
    {"pos": "VERB"}
  ],
  [
    "радость",
    {"pos": "NOUN"}
  ],
  [
    "в",
    {"pos": "PREP"}
  ],
  [
    "исполнении",
    {"pos": "NOUN"}
  ],
  [
    "своего",
    {"pos": "ADJF"}
  ],
  [
    "долга",
    {"pos": "NOUN"}
  ]
]
```

---

### `POST` `/ds/`

Вычисление метрик лексического разнообразия текста.

Пример запроса:

```json
{
  "text": "Живет свободно только тот, кто находит радость в исполнении своего долга.",
  "stat": ""
}
```

Аргументы:

| Аргумент | Тип | Описание |
| :-: | :-: | :-: |
| `text` | str | Текст, для которого вычисляются метрики |
| `stat` | bool | Наименование конкретной метрики |

Пример ответа:

```json
{
  "ttr": 1,
  "rttr": 3.3166247903554,
  "cttr": 2.345207879911715,
  "httr": 1,
  "sttr": 1,
  "mttr": 0,
  "dttr": 0,
  "mattr": 1,
  "msttr": 1,
  "mtld": 0,
  "mamtld": 1,
  "hdd": -1,
  "simpson_index": 0,
  "hapax_index": 0
}
```

---

### `POST` `/rs/`

Вычисление метрик удобочитаемости текста.

Пример запроса:

```json
{
  "text": "Живет свободно только тот, кто находит радость в исполнении своего долга.",
  "stat": ""
}
```

Аргументы:

| Аргумент | Тип | Описание |
| :-: | :-: | :-: |
| `text` | str | Текст, для которого вычисляются метрики |
| `stat` | bool | Наименование конкретной метрики |

Пример ответа:

```json
{
  "flesch_kincaid_grade": 4.727272727272727,
  "flesch_reading_easy": 61.40772727272727,
  "coleman_liau_index": 6.7600454545454625,
  "smog_index": 8.891153770860452,
  "automated_readability_index": 6.7600454545454625,
  "lix": 65.54545454545455
}
```