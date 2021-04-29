from django.shortcuts import render
import os.path
import nltk
import gc


def index(request):
    return render(request, 'te_app1/inptext.html')


def home(request):
    # 文章の読み込み
    #with open('ICT429w2.txt', 'r') as f:
        #data = f.read()
    data = request.POST['textdata']

    #base0 = os.path.dirname(os.path.abspath(__file__))
    #f = open(os.path.join(base0, "images/rapgod.txt"), 'r')
    #data = f.read()

    nltk.download('wordnet' and 'stopwords')
    nltk.download('punkt')

    nltk.download('averaged_perceptron_tagger')

    words_tokens = nltk.word_tokenize(data)

    p_o_s = nltk.pos_tag(words_tokens)

    # 数字、固有名詞の除去
    for hinshi in p_o_s:
        for element in hinshi:
            if element == "CD" or element == "NNP" or element == "NNPS":
                words_tokens.remove(hinshi[0])

    # 大文字を小文字にする
    komoji = []
    for wd in words_tokens:
        wd = wd.lower()
        komoji.append(wd)

    del words_tokens
    gc.collect()

    # 辞書とストップワードの辞書
    from nltk.corpus import wordnet as wn
    from nltk.corpus import stopwords as sw

    stop_words = list(sw.words('english'))

    sw_removed = [w for w in komoji if w not in stop_words]


    # 各単語を原型にする。
    original_form = []
    for wd in sw_removed:
        original = wn.morphy(wd)  # wdから原型
        original_form.append(original)
    del sw_removed
    gc.collect()

    none_removed = []
    for wd in original_form:
        if wd is not None:
            none_removed.append(wd)

    del original_form
    gc.collect()

    # 中学レベルの単語リストの読み込み
    #with open('top1000words.txt', 'r') as f:
    base1 = os.path.dirname(os.path.abspath(__file__))
    f1 = open(os.path.join(base1, "images/top1000words.txt"))
    top1000 = f1.read().splitlines()

    target = list(set(none_removed) - set(top1000))
    target.sort()

    num = len(target)


    # 単語帳の読み込み
    base2 = os.path.dirname(os.path.abspath(__file__))
    f2 = open(os.path.join(base2, "images/system_eitango.txt"))
    sample_system = f2.read().splitlines()

    base = os.path.dirname(os.path.abspath(__file__))
    f3 = open(os.path.join(base, "images/core_after.txt"))
    sample_core = f3.read().splitlines()

    base4 = os.path.dirname(os.path.abspath(__file__))
    f4 = open(os.path.join(base4, "images/sokutanafter.txt"), 'r')
    sample_soku = f4.read().splitlines()

    # 各単語帳に対象単語が含まれているか
    system_match = [wd for wd in sample_system if wd in target]
    system_num = len(system_match)
    system_unmatch = []
    system_unmatch = list(set(target) - set(system_match))
    core_match = [wd for wd in sample_core if wd in target]
    core_num = len(core_match)
    soku_match = [wd for wd in sample_soku if wd in target]
    soku_num = len(soku_match)


    # 収録率の比較
    if num == 0:
        result = "対象の単語はありませんでした。"
        return render(request, 'te_app1/result.html', {'result': result})
    else:

        if system_num >= core_num and system_num >= soku_num:
            result_book = "最適な英単語帳はシステム英単語"
            numofmatch = system_num
            url_ama = "https://www.amazon.co.jp/%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0%E8%8B%B1%E5%8D%98%E8%AA%9E-5%E" \
                      "8%A8%82%E7%89%88-%E9%9C%9C-%E5%BA%B7%E5%8F%B8/dp/4796111379/ref=sr_1_1?__mk_ja_JP=%E3%82%AB%" \
                      "E3%82%BF%E3%82%AB%E3%83%8A&crid=1RG4G2G892CDI"
        elif core_num >= system_num and core_num >= soku_num:
            result_book = "最適な英単語帳はcore1900"
            numofmatch = core_num
            url_ama = "https://www.amazon.co.jp/%E9%80%9F%E8%AA%AD%E9%80%9F%E8%81%B4%E3%83%BB%E8%8B%B1%E5%8D" \
                      "%98%E8%AA%9E-Core1900-ver-5-%E6%9D%BE%E6%9C%AC%E8%8C%82/dp/4862902413/ref=sr_1_1?__mk_ja_J" \
                      "P=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A"
        else:
            result_book = "最適な英単語帳は速読英単語"
            numofmatch = soku_num
            url_ama = "https://www.amazon.co.jp/%E9%80%9F%E8%AA%AD%E8%8B%B1%E5%8D%98%E8%AA%9E-1-%E5%BF%85%E4%BF" \
                      "%AE%E7%B7%A8-%E6%94%B9%E8%A8%82%E7%AC%AC5%E7%89%88-%E9%A2%A8%E6%97%A9/dp/4860666321/ref=sr_1" \
                      "_4?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A"

        if numofmatch == 0:
            result = "対象の単語はありませんでした。"
            return render(request, 'te_app1/result.html', {'result': result})
        else:
            result = "で、対象の文章の単語を{}個中、{:.1f}%({}語)含んでいます。".format(num, numofmatch / num * 100, numofmatch)

            return render(request,'te_app1/result.html',
                          {'result_book': result_book, 'result': result, 'url_ama': url_ama})

