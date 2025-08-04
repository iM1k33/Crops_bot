import pandas as pd
import ast
import tiktoken
import numpy as np
from scipy import spatial
from .config import CROPS_CSV_PATH, TOKEN_BUDGET, MAX_TOKENS_RESPONSE
from .gpt_client import get_embedding

# Функция для подсчета токенов
def count_tokens(text: str) -> int:
    """Count tokens in text string"""
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

# Загрузка данных о культурах
def load_crop_data():
    """Load crop embeddings data"""
    df = pd.read_csv(CROPS_CSV_PATH)
    df['embedding'] = df['embedding'].apply(ast.literal_eval)
    return df

# Поиск релевантных текстов
def find_related_texts(query: str, df: pd.DataFrame, top_n: int = 100):
    """Find most related texts to query"""
    query_embedding = get_embedding(query)
    
    # Преобразуем эмбеддинги в numpy array для быстрых вычислений
    embeddings = np.array(df['embedding'].tolist())
    
    # Вычисляем косинусное сходство
    similarities = 1 - spatial.distance.cdist(
        [query_embedding], 
        embeddings, 
        'cosine'
    )[0]
    
    # Сортируем по убыванию сходства
    sorted_indices = np.argsort(similarities)[::-1][:top_n]
    return df.iloc[sorted_indices]['text'].tolist(), similarities[sorted_indices]

# Построение контекстного промпта
def build_context_prompt(query: str) -> list:
    """Build context-aware prompt for GPT"""
    df = load_crop_data()
    related_texts, _ = find_related_texts(query, df)
    
    system_prompt = "You answer questions about crops in agriculture using provided Wikipedia articles."
    user_prompt = f"Question: {query}\n\nContext:\n"
    
    # Рассчитываем доступные токены для контекста
    system_tokens = count_tokens(system_prompt)
    query_tokens = count_tokens(query)
    reserved_tokens = system_tokens + query_tokens + MAX_TOKENS_RESPONSE + 100  # +100 для буфера
    available_context_tokens = TOKEN_BUDGET - reserved_tokens
    
    # Собираем контекст в пределах доступных токенов
    context_tokens = 0
    context_texts = []
    
    for text in related_texts:
        text_tokens = count_tokens(text)
        if context_tokens + text_tokens <= available_context_tokens:
            context_texts.append(text)
            context_tokens += text_tokens
        else:
            # Попробуем добавить усеченную версию текста
            truncated = truncate_text_to_tokens(text, available_context_tokens - context_tokens)
            if truncated:
                context_texts.append(truncated)
                context_tokens += count_tokens(truncated)
            break
    
    # Формируем итоговый промпт
    user_prompt += "\n---\n".join(context_texts)
    
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

# Функция для усечения текста до определенного количества токенов
def truncate_text_to_tokens(text: str, max_tokens: int) -> str:
    """Truncate text to fit within token limit"""
    if max_tokens <= 0:
        return ""
    
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    
    if len(tokens) <= max_tokens:
        return text
    
    truncated_tokens = tokens[:max_tokens]
    return encoding.decode(truncated_tokens) + " [...]"

# Основная функция запроса к GPT
def ask_gpt(query: str) -> str:
    from .gpt_client import get_gpt_response
    
    messages = build_context_prompt(query)
    return get_gpt_response(messages, max_tokens=min(MAX_TOKENS_RESPONSE, 4000 - count_tokens(str(messages))))