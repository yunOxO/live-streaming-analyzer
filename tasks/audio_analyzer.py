def analyze_text(text):
    sensitive_words = ["敏感词1", "敏感词2"]
    for word in sensitive_words:
        if word in text:
            return True
    return False
