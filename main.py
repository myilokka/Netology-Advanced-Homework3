from HabrArticleSorter import HabrArticleSorter


if __name__ == '__main__':
    KEYWORDS = [r'алгоритм\w*', r'структур\w* данных', 'web', 'Django', r'нау\w*']
    article_sorter = HabrArticleSorter(KEYWORDS)
    article_sorter.filter_articles()
