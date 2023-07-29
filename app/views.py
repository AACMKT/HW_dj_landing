from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter({'original': 0, 'test': 0})
counter_click = Counter({'original': 0, 'test': 0})


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    req = request.GET.get('from-landing')
    counter_click[req] += 1

    return render(request, 'index.html')


def landing(request):
    req = request.GET.get('ab-test-arg', '')
    htmls = {'original': 'landing.html',
             'test': 'landing_alternate.html'
             }

    if req in htmls.keys():
        template_name = htmls[req]
        counter_show[req] += 1

    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    else:
        template_name = 'index.html'

    return render(request, template_name)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    if counter_show['test'] != 0:
        test_forwarded = counter_click['test'] / counter_show['test']
    else:
        test_forwarded = 0
    if counter_show['original'] != 0:
        original_forwarded = counter_click['original'] / counter_show['original']
    else:
        original_forwarded = 0

    return render(request, 'stats.html', context={
        'test_conversion': test_forwarded,
        'original_conversion': original_forwarded,
    })
