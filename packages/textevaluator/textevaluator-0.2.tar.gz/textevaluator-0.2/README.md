# Описание:

TextEvaluator использует модель TensorFlow для оценки текста и определения наличия в нем плохих слов или выражений.

# Установка:

`pip install textevaluator`

# Использование:

```
from textevaluator import *

evaluator = TextEvaluator()

text = "Привет, даун!"

result, bad_words = evaluator.evaluate_text(text)

print(f"Результат: {result}, Плохие слова: {bad_words}")
```

# Контрибьюторы:

- KroZen