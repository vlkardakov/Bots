from urllib.parse import urlparse

def get_domain_tld(url):
  try:
    #print(f"url = {url}")
    parsed = urlparse(url)
    if not parsed.netloc:
      return None
    parts = parsed.netloc.split('.')
    #print(f"parts = {parts}")
    if len(parts) < 2:  # Проверка на наличие хотя бы двух частей
      return parts[0] if parts else None #Возвращаем единственный элемент если он есть
    return ".".join(parts[-2:])  # Объединяем последние две части
  except Exception as e:
    print(f"Ошибка обработки URL: {e}")
    return None


def get_domain(url):
    domains = set()
    domain_tld = get_domain_tld(url)
    if domain_tld:
      return domain_tld