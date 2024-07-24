# Описание:

TextEvaluator использует модель AI-TQA Basic для оценки текста и определения наличия в нем плохих слов или выражений.

# Установка:

`pip install ai-tqa`

# Использование:

```
from ai-tqa import *

evaluator = TextEvaluator()

text = "Привет, даун!"

result, bad_words = evaluator.evaluate_text(text)

print(f"Результат: {result}, Плохие слова: {bad_words}")
```

# Контрибьюторы:

- KroZen